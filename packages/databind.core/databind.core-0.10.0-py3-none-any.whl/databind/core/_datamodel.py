
"""
Extends the functionality of the #dataclass module to provide additional metadata for
(de-) serializing data classes.
"""

import types
import textwrap
from typing import (Any, Callable, Dict, Iterable, List, Optional, Union, Tuple, Type, TypeVar,
  cast, get_type_hints)

from dataclasses import dataclass as _dataclass, field as _field, Field as _Field, _MISSING_TYPE

from ._union import (UnionResolver, ClassUnionResolver, InterfaceUnionResolver,
  StaticUnionResolver, from_resolver_spec)
from .utils import type_repr, expect

T = TypeVar('T')
T_BaseMetadata = TypeVar('T_BaseMetadata', bound='BaseMetadata')
TypeHint = Any  # Supposed to represent the type of a Python type hint.
uninitialized = object()  # Placeholder object to inidicate that a field does not actually have a default.

__all__ = [
  'datamodel',
  'enumerate_fields',
  'FieldMetadata',
  'field',
  'implementation',
  'interface',
  'is_datamodel',
  'is_uniontype',
  'ModelMetadata',
  'uniontype',
  'TypeHint',
  'UnionMetadata',
]


def _extract_dataclass_from_kwargs(dataclass: Type[T], kwargs: Dict[str, Any]) -> T:
  """
  Internal. Extracts all keyword arguments matching the fields in *dataclass* from the
  dictionary *kwargs* and returns an instance of *dataclass*.
  """

  return dataclass(**{  # type: ignore
    field.name: kwargs.pop(field.name)
    for field in dataclass.__dataclass_fields__.values()  # type: ignore
    if field.name in kwargs
  })


def _field_has_default(field: _Field) -> bool:
  return any(not isinstance(x, _MISSING_TYPE) for x in (field.default, field.default_factory))  # type: ignore


def _field_get_default(field: _Field) -> Any:
  if not isinstance(field.default, _MISSING_TYPE):  # type: ignore
    return field.default
  if not isinstance(field.default_factory, _MISSING_TYPE):  # type: ignore
    return field.default_factory()  # type: ignore
  raise RuntimeError('{!r} has no default'.format(field))


@_dataclass
class BaseMetadata:
  #: Use strict deserialization mode where that is not already the default.
  strict: bool = _field(default=False)

  #: Use relaxed deserialization mode where that is not already the default.
  relaxed: bool = _field(default=False)

  ATTRIBUTE = '__databind_metadata__'

  @classmethod
  def for_type(cls: Type[T_BaseMetadata], type_: Type) -> Optional[T_BaseMetadata]:
    try:
      result = vars(type_).get(cast(BaseMetadata, cls).ATTRIBUTE)
    except TypeError:
      return None
    if result is not None and not isinstance(result, cls):
      result = None
    return result


@_dataclass
class ModelMetadata(BaseMetadata):
  #: Allow only keyword arguments when constructing an instance of the model.
  kwonly: bool = _field(default=False)

  #: A type definition which overrides the type for deserializing/serializing the datamodel.
  serialize_as: Union[Callable[[], TypeHint], TypeHint, None] = None

  @classmethod
  def for_type(cls, type_: Type) -> Optional['ModelMetadata']:
    result = super().for_type(type_)
    if result is None and hasattr(type_, '__dataclass_fields__'):
      result = cls()
    return result


@_dataclass
class FieldMetadata(BaseMetadata):
  #: Alternative name of the field used during the (de-) serialization. This may be
  #: set to change the name of a field to a value that is not valid Python syntax
  #: (for example "field-name").
  altname: Optional[str] = _field(default=None)

  #: Set to `True` to indicate that the field is required during deserialization.
  #: This does not indicate that the field is required when constructing the object
  #: in memory, in which case the field's default value is always used.
  required: bool = _field(default=False)

  #: Set to `True` if the field is populated with derived data and should be ignored
  #: during (de-) serialization.
  derived: bool = _field(default=False)

  #: Set to `True` if the type of the field should be flattened into the parent
  #: object when (de-) serializing. There can be only one flattened field on a data
  #: model and it works with other data models as well as dictionaries.
  flatten: bool = _field(default=False)

  #: Indicate that the field should be assigned the raw data from the deserialization.
  #: Setting this to `True` sets #derived to `True` as well.
  raw: bool = _field(default=False)

  #: A list of format specifiers that the (de-) serializer should respect, if applicable
  #: to the field type. Examples of format specifiers would be date format templates for
  #: date types or #decimal.Context for #decimal.Decimal fields.
  formats: List[Any] = _field(default_factory=list)

  #: The original #_Field that this #FieldMetadata is associated with. This may not be set
  #: if the #FieldMetadata is instantiated at the top level. NOTE: We should use a weak
  #: reference here, but the #_Field class is not compatible with weakrefs.
  _owning_field: 'Optional[_Field]' = _field(default=None)

  #: Metadata that supplements the original #_Field's metadata. When a #FieldMetadata is
  #: instantiated for a field in a #datamodel, the metadata will be set to the metadata
  #: of the #_Field.
  metadata: Dict[str, Any] = _field(default_factory=dict)

  KEYSPACE = 'databind.core'

  def __post_init__(self):
    if self.raw:
      self.derived = True

  @classmethod
  def for_field(cls, field: _Field) -> 'FieldMetadata':
    return field.metadata.get(cls.KEYSPACE) or cls(_owning_field=field)


def datamodel(*args, **kwargs):
  """
  This function wraps the #dataclasses.dataclass() decorator. Applicable keyword arguments are
  redirected to the #ModelMetadata which is then set in the `__databind_metadata__` attribute.
  """

  metadata = _extract_dataclass_from_kwargs(ModelMetadata, kwargs)
  no_default_fields = []

  def _before_dataclass(cls):
    # Allow non-default arguments to follow default-arguments.
    existing_fields = getattr(cls, '__dataclass_fields__', {})
    annotations = getattr(cls, '__annotations__', {})
    if '__annotations__' not in cls.__dict__:
      cls.__annotations__ = annotations
    for key in annotations.keys():
      if not hasattr(cls, key):
        f = existing_fields.get(key, field())
        setattr(cls, key, f)
      else:
        f = getattr(cls, key)
        if not isinstance(f, _Field):
          continue
      if not _field_has_default(f):
        # This prevents a SyntaxError if non-default arguments follow default arguments.
        f.default = uninitialized
        no_default_fields.append(key)

    # Override the `__post_init__` method that is called by the dataclass `__init__`.
    old_postinit = getattr(cls, '__post_init__', None)
    def __post_init__(self):
      # Ensure that no field has a "uninitialized" value.
      for key in self.__dataclass_fields__.keys():
        if getattr(self, key) == uninitialized:
          raise TypeError(f'missing required argument {key!r}')
      if old_postinit:
        old_postinit(self)
    cls.__post_init__ = __post_init__

    return cls

  def _after_dataclass(cls):
    setattr(cls, ModelMetadata.ATTRIBUTE, metadata)

    if metadata.kwonly:
      old_init = cls.__init__
      def __init__(self, **kwargs):
        old_init(self, **kwargs)
      cls.__init__ = __init__

    for key in no_default_fields:
      if getattr(cls, key, None) is uninitialized:
        delattr(cls, key)

    return cls

  if args:
    _before_dataclass(args[0])

  result = _dataclass(*args, **kwargs)

  if not args:
    def wrapper(cls):
      return _after_dataclass(result(_before_dataclass(cls)))
    return wrapper

  return _after_dataclass(result)


def field(*args, **kwargs) -> _Field:
  """
  This function wraps the #dataclasses.field() function, equipping the field with additional
  #FieldMetadata.
  """

  metadata = kwargs.pop('metadata', {})
  field_metadata = _extract_dataclass_from_kwargs(FieldMetadata, kwargs)
  metadata[FieldMetadata.KEYSPACE] = field_metadata
  kwargs['metadata'] = metadata
  field = _field(*args, **kwargs)
  field_metadata._owning_field = field
  field_metadata.metadata = field.metadata
  return field


@_dataclass
class _EnumeratedField:
  field: _Field = _field(repr=False)
  name: str
  type: Type
  metadata: FieldMetadata = _field(repr=False)

  def has_default(self) -> bool:
    return _field_has_default(self.field)

  def get_default(self) -> Any:
    return _field_get_default(self.field)


def enumerate_fields(data_model: Union[T, Type[T]]) -> Iterable[_EnumeratedField]:
  """
  Enumerate the fields of a datamodel. The items yielded by this generator are tuples of
  the field name, the resolved type hint and the #FieldMetadata.
  """

  if not isinstance(data_model, type):
    data_model = type(data_model)

  type_hints = get_type_hints(data_model)
  for field in data_model.__dataclass_fields__.values():  # type: ignore
    yield _EnumeratedField(field, field.name, type_hints[field.name], FieldMetadata.for_field(field))


def is_datamodel(obj: Any) -> bool:
  return isinstance(BaseMetadata.for_type(obj), ModelMetadata)


@datamodel
class UnionMetadata(BaseMetadata):
  #: The resolver that is used to map type names to a datatype. If no resolver is set,
  #: the union type acts as a container for exactly one of it's dataclass fields.
  resolver: UnionResolver

  #: Indicates whether the union type is a container for its members.
  container: bool = _field(default=False)

  #: The type field of the union container.
  type_field: Optional[str] = _field(default=None)

  #: The key in the data structure that identifies the union type. Defaults to "type".
  type_key: str = _field(default='type')

  #: Whether union members should be converted from Python to flat data structures. This option
  #: must be set to `False` in order to de-serialize union members that cannot be deserialized
  #: from mappings (like plain types). The default is `True`.
  flat: bool = _field(default=True)


def uniontype(
  resolver: Union[UnionResolver, Dict[str, Type], Type, str, None] = None,
  container: bool = False,
  type_field: str = None,
  **kwargs
):
  """
  Decorator for classes to define them as union types, and are to be (de-) serialized as such.
  Union types can either act as placeholders or as containers for their members.

  If a *resolver* is specified or *container* is `False`, the union type will act as a placeholder
  and will be converted directly into one the union member types. If no *resolver* is specified,
  the members will be determined from the type hints.

  If *container* is #True, the union type will be equipped as a container for its members
  based on the type hints. The *type_field* will be used to store the type name in the
  container.
  """

  if isinstance(resolver, str):
    resolver = from_resolver_spec(resolver)

  cls = None
  if isinstance(resolver, type):
    resolver, cls = None, resolver

  if container:
    if not type_field:
      type_field = kwargs.get('type_key', 'type')
    kwargs.setdefault('type_key', type_field)

  if resolver is not None:
    if container:
      raise TypeError('"container" argument cannot be combined with "resolver" argument')
    if type_field is not None:
      raise TypeError('"type_field" argument cannot be combined with "resolver" argument')
    if isinstance(resolver, dict):
      resolver = StaticUnionResolver(resolver)

  def _init_as_container(cls, type_hints):
    """
    Initializes *cls* as a container for the union type members.
    """

    # TODO(NiklasRosenstein): Parse with ast() module and set filename/lineno of the below code
    #   to the location of where the @uniontype() decorator was used.
    scope = {}
    exec(textwrap.dedent(f"""
      def __init__(self, **kwarg):
        if len(kwarg) != 1:
          raise TypeError("{{}}.__init__() expected exactly one keyword argument".format(type(self).__name__))
        self._type, self._value = next(iter(kwarg.items()))
      @property
      def {type_field}(self):
        return self._type
      def __repr__(self) -> str:
        return '{{}}({type_field}={{!r}})'.format(type(self).__name__, self._value)
      def __eq__(self, other) -> bool:
        if isinstance(self, type(other)) or isinstance(other, type(self)):
          return self._type == other._type and self._value == other._value
        return False
      def __ne__(self, other) -> bool:
        if not isinstance(self, type(other)) and not isinstance(other, type(self)):
          return False
        return self._type != other._type or self._value != other._value
    """), {}, scope)

    for key, value in scope.items():
      if key not in vars(cls):
        setattr(cls, key, value)

    def _make_property(type_name: str, annotation: Any) -> property:

      def getter(self) -> annotation:  # type: ignore
        assert type_field is not None
        if self._type != type_name:
          raise TypeError(f'{type(self).__name__}.{type_name} cannot be accessed when type is .{self._type}')
        return self._value

      def setter(self, value: annotation) -> None:  # type: ignore
        assert type_field is not None
        self._type = type_name
        self._value = value
      return property(getter, setter)

    for key, annotation in type_hints.items():
      setattr(cls, key, _make_property(key, annotation))

    return cls

  def _prevent_init(cls):
    def __init__(self, *args, **kwargs):
      raise TypeError(f'non-container @uniontype {type_repr(cls)} cannot be constructed directly')
    if '__init__' not in vars(cls):
      cls.__init__ = __init__

  def decorator(cls):
    nonlocal resolver
    if not resolver:
      resolver = ClassUnionResolver(cls)
    if container:
      _init_as_container(cls, get_type_hints(cls))
    else:
      _prevent_init(cls)

    kwargs['resolver'] = resolver
    kwargs['container'] = container
    kwargs['type_field'] = type_field
    setattr(cls, UnionMetadata.ATTRIBUTE, UnionMetadata(**kwargs))

    return cls

  if cls:
    return decorator(cls)

  return decorator


def is_uniontype(obj: Any) -> bool:
  return isinstance(BaseMetadata.for_type(obj), UnionMetadata)


def interface(resolver: Union[UnionResolver, Type, str, None] = None, **kwargs):
  """
  This decorator is a specialized form of the #@uniontype() decorator that sets an abstract
  base class up for extension by subclasses. Type hints of the base class are deserialized
  as unions of all of it's registered subclasses.

  Subclasses are registered based on the specified *resolver*. It defaults to an
  #InterfaceUnionResolver, which recognizes only subclasses decorated with the #@implementation()
  decorator.

  Another common use case is to use the #Import
  """

  def _decorator(type_: Type):
    nonlocal resolver
    if resolver is None:
      resolver = InterfaceUnionResolver()
    return uniontype(resolver, container=False, **kwargs)(type_)

  if isinstance(resolver, type):
    # @interface
    type_ = resolver
    resolver = None
    return _decorator(type_)
  else:
    # @interface()
    # @interface(resolver)
    return _decorator


def implementation(name: str, for_: Optional[Type] = None):
  """
  This decorator must be used on a subclass of a class decorated with #@interface() if the
  default #InterfaceUnionResolver() is used. It will register the subclass as a member of
  the interface union.
  """

  def _decorator(type_: Type):
    if for_:
      resolver = expect(UnionMetadata.for_type(for_)).resolver
      if not isinstance(resolver, InterfaceUnionResolver):
        raise RuntimeError(f'@implementation(for_={type_repr(for_)}) can only be used if the '
          'for_ argument is a class decorated with @interface() and uses an InterfaceUnionResolver')
      targets = [resolver]
    else:
      # Find the base-class(es) to register the implementation for.
      targets = []
      for cls in type_.__bases__:
        metadata = UnionMetadata.for_type(cls)
        if metadata and isinstance(metadata.resolver, InterfaceUnionResolver):
          targets.append(metadata.resolver)
      if not targets:
        raise RuntimeError('@imlpementation() can only be used if at least one base is '
          'decorated with @interface() and uses an InterfaceUnionResolver')

    # The parent class' metadata will be a UnionMetadata, which is inherted by `type_`.
    # We override the metadata of `type_` to None if it's not already set explicitly
    # to reduce the confusion when an error occurs because no metadata is provided by
    # this class.
    if BaseMetadata.ATTRIBUTE not in vars(type_):
      setattr(type_, BaseMetadata.ATTRIBUTE, None)

    for resolver in targets:
      resolver.register_implementation(name, type_)

    return type_

  return _decorator
