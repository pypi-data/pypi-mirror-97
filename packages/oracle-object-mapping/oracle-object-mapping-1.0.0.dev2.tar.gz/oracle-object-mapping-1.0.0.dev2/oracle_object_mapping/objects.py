from __future__ import annotations

import abc
import sys
import typing

import cx_Oracle


class DbType:
    def from_data(self, var_name: str) -> str:
        return f'{var_name}'

    def to_data(self, var_name: str) -> str:
        return f'{var_name}'

    def from_oracle_object(self, var_name: str) -> str:
        return f'{var_name}'

    def to_oracle_object(self, var_name: str) -> str:
        return f'{var_name}'


class _OBJECT(DbType):
    def __init__(self, name: str):
        self.name = name

    def from_data(self, var_name: str) -> str:
        return f'{self.name}.from_data({var_name})'

    def to_data(self, var_name: str) -> str:
        return f'{var_name}.to_data()'

    def from_oracle_object(self, var_name: str) -> str:
        return f'{self.name}.from_oracle_object({var_name})'

    def to_oracle_object(self, var_name: str) -> str:
        return f'{var_name}.to_oracle_object(connection)'


def _is_direct_subclass_of_base_type_instance(class_bases: typing.List[type], base_type: type) -> bool:
    """
    Return True if class (defined by the class_bases) is in the level 3.

    [1]          MetaObject(type)                MetaCollection(type)
                       |                                 |
    [2]    Object(metaclass=MetaObject)  Collection(metaclass=MetaCollection)
                       |                                 |
                 -------------                     -------------
                 |           |                     |           |
    [3]      A(Object)   B(Object)         C(Collection)   D(Collection)
                 |           |                     |           |
    [4]        Xa(A)       Xb(B)                 Ya(A)       Yb(B)

    """
    found = False
    for b in class_bases:
        if isinstance(b, base_type):
            found = True
            for bb in b.__bases__:
                if isinstance(bb, base_type):
                    return False
    return found


def __is_none_type(type_: type) -> bool:
    return type_ == type(None)  # noqa


def __is_optional_type(type_: typing.Any) -> bool:
    if type_ is typing.Union or isinstance(type_, typing._GenericAlias) and (type_.__origin__ is typing.Union):
        return any(__is_none_type(t) for t in type_.__args__)
    else:
        return False


def _get_database_type(python_type: typing.Any = None, database_type: DbType = None) -> DbType:
    if isinstance(python_type, type) and issubclass(python_type, Base):
        return _OBJECT(python_type.__qualname__)
    elif isinstance(python_type, typing.ForwardRef):
        return _OBJECT(python_type.__forward_arg__)
    elif database_type is not None:
        if not isinstance(database_type, DbType):
            raise Exception('Database type must be an instance of DbType.')
        return database_type
    else:
        return DbType()


_TypeAttributes = typing.Dict[str, typing.Tuple[DbType, type]]


def _get_object_attributes(class_attributes: typing.Dict[str, typing.Any]) -> _TypeAttributes:
    dumb_type = type('t', (), {'__annotations__': class_attributes['__annotations__']})
    global_ns = sys.modules[class_attributes['__module__']].__dict__
    local_ns = {class_attributes['__qualname__']: class_attributes['__qualname__']}
    type_hints = typing.get_type_hints(dumb_type, global_ns, local_ns)
    attrs: _TypeAttributes = {}
    for attr, type_ in type_hints.items():
        if not __is_optional_type(type_):
            raise Exception(f'Found non optional attribute: {attr}. All attributes must be optional.')
        hints = [t for t in type_.__args__ if not __is_none_type(t)]
        db_type = class_attributes.get(attr, None)
        attrs[attr] = _get_database_type(hints[0], db_type), hints[0]
    return attrs


def _create_object_init(attributes: _TypeAttributes) -> str:
    # add each attribute as an init argument, all attributes are optional
    args = ', '.join((f'{attr}=None' for attr in attributes))
    # assign attributes to instance variables
    attributions = '\n '.join((f'self.{attr} = {attr}' for attr in attributes))
    # create __init__ def
    func_def = f'def __init__(self, {args}):\n {attributions}'
    return func_def


def _create_object_from_data(attributes: _TypeAttributes) -> str:
    # get all attributes from dict, None if not found
    attributions = '\n '.join(f"{attr} = data.get('{attr}', None)" for attr in attributes)
    # create cls arguments
    args_l = []
    for attr, (type_, _) in attributes.items():
        if type_.from_data(attr) == attr:
            args_l.append(f'{attr}={attr}')
        else:
            args_l.append(f'{attr}={type_.from_data(attr)} if {attr} is not None else None')
    args = ',\n            '.join(args_l)
    # create from_data def
    func_def = f'@classmethod\ndef from_data(cls, data):\n {attributions}\n return cls({args})'
    return func_def


def _create_object_to_data(attributes: _TypeAttributes) -> str:
    code = 'def to_data(self):\n data = {}\n'
    for attr, (type_, _) in attributes.items():
        code += f' if self.{attr} is not None:\n'
        code += f"  data['{attr}'] = {type_.to_data('self.' + attr)}\n"
    code += ' return data'
    return code


def _create_object_from_oracle_object(attributes: _TypeAttributes) -> str:
    # create cls arguments
    args_l = []
    for attr, (type_, _) in attributes.items():
        if type_.from_oracle_object(attr) == attr:
            args_l.append(f'{attr}=obj.{attr}')
        else:
            args_l.append(f'{attr}={type_.from_oracle_object("obj." + attr)} if obj.{attr} is not None else None')
    args = ',\n            '.join(args_l)
    # create from_data def
    func_def = f'@classmethod\ndef from_oracle_object(cls, obj):\n return cls({args})'
    return func_def


def _create_object_to_oracle_object(attributes: _TypeAttributes, object_type_name: str) -> str:
    code = 'def to_oracle_object(self, connection):\n'
    code += f" obj = connection.gettype('{object_type_name}').newobject()\n"
    for attr, (type_, _) in attributes.items():
        if type_.to_data(attr) == attr:
            code += f' obj.{attr} = self.{attr}\n'
        else:
            code += f' obj.{attr} = {type_.to_oracle_object("self." + attr)} if self.{attr} is not None else None\n'
    code += ' return obj'
    return code


class ObjectMeta(type):
    """Metaclass for all object types."""

    def __new__(mcs, name, bases, attrs, **kwargs):
        # Ensure initialization is only performed for direct subclasses of Object
        if not _is_direct_subclass_of_base_type_instance(bases, ObjectMeta):
            return super().__new__(mcs, name, bases, attrs)

        # class attributes are only the ones in the class annotations
        if '__annotations__' not in attrs or len(attrs['__annotations__']) == 0:
            raise Exception('Object must have attributes.')
        attributes: _TypeAttributes = _get_object_attributes(attrs)

        # set class attributes
        new_attrs = {
            '__module__': attrs['__module__'],
            '__qualname__': attrs['__qualname__'],
            '__annotations__': attrs['__annotations__'],
            '__slots__': tuple(attributes.keys()),  # add attributes to __slots__
            '__type_name__': f'{attrs["package"]}.{name}' if 'package' in attrs else name,
        }

        globals_ = sys.modules[attrs['__module__']].__dict__
        locals_: typing.Dict[str, typing.Any] = {}
        methods_code = []

        # add __init__
        code = _create_object_init(attributes)
        exec(code, globals_, locals_)
        new_attrs['__init__'] = locals_['__init__']
        methods_code.append(code)

        # add from_data
        code = _create_object_from_data(attributes)
        exec(code, globals_, locals_)
        new_attrs['from_data'] = locals_['from_data']
        methods_code.append(code)

        # add to_data
        code = _create_object_to_data(attributes)
        exec(code, globals_, locals_)
        new_attrs['to_data'] = locals_['to_data']
        methods_code.append(code)

        # add from_data
        code = _create_object_from_oracle_object(attributes)
        exec(code, globals_, locals_)
        new_attrs['from_oracle_object'] = locals_['from_oracle_object']
        methods_code.append(code)

        # add to_data
        code = _create_object_to_oracle_object(attributes, new_attrs['__type_name__'])
        exec(code, globals_, locals_)
        new_attrs['to_oracle_object'] = locals_['to_oracle_object']
        methods_code.append(code)

        def ident(text: str, length: int = 1) -> str:
            return '\n'.join(' ' * length + ln for ln in text.split('\n'))

        # store generated code in __class_code__
        new_attrs['__class_code__'] = f'class {name}(Base):\n'
        new_attrs['__class_code__'] += ' __slots__ = (' + ', '.join(
            map(lambda x: f"'{x}'", new_attrs['__slots__'])) + ')\n'
        new_attrs['__class_code__'] += '\n'.join(f' {n}: {t}' for n, t in attrs['__annotations__'].items())
        new_attrs['__class_code__'] += '\n\n'
        new_attrs['__class_code__'] += '\n\n'.join(ident(code) for code in methods_code)

        return super().__new__(mcs, name, bases, new_attrs)


def _create_collection_from_data(database_type: DbType) -> str:
    code = '@classmethod\ndef from_data(cls, items):\n'
    code += ' self = cls()\n'
    code += ' for item in items:\n'
    code += f'  self.append({database_type.from_data("item")})\n'
    code += ' return self'
    return code


def _create_collection_to_data(database_type: DbType) -> str:
    code = 'def to_data(self):\n'
    code += f' return [{database_type.to_data("item")} for item in self]'
    return code


def _create_collection_from_oracle_object(database_type: DbType) -> str:
    code = '@classmethod\ndef from_oracle_object(cls, obj):\n'
    code += ' self = cls()\n'
    code += ' for item in obj.aslist():\n'
    code += f'  self.append({database_type.from_oracle_object("item")})\n'
    code += ' return self'
    return code


def _create_collection_to_oracle_object(database_type: DbType, object_type_name: str) -> str:
    code = 'def to_oracle_object(self, connection):\n'
    code += f" obj = connection.gettype('{object_type_name}').newobject()\n"
    code += ' for item in self:\n'
    code += f'  obj.append({database_type.to_oracle_object("item")})\n'
    code += ' return obj'
    return code


class CollectionMeta(type):
    """Metaclass for all collection types."""

    def __new__(mcs, name, bases, attrs, **kwargs):
        # Ensure initialization is only performed for direct subclasses of Collection
        if not _is_direct_subclass_of_base_type_instance(bases, CollectionMeta):
            return super().__new__(mcs, name, bases, attrs)

        # set class attributes
        new_attrs = {
            '__module__': attrs['__module__'],
            '__qualname__': attrs['__qualname__'],
            '__type_name__': f'{attrs["package"]}.{name}' if 'package' in attrs else name,
        }

        globals_ = sys.modules[attrs['__module__']].__dict__
        locals_: typing.Dict[str, typing.Any] = {}
        methods_code = []
        db_type = _get_database_type(attrs['__orig_bases__'][0].__args__[0], attrs.get('database_type', None))

        # add from_data
        code = _create_collection_from_data(db_type)
        exec(code, globals_, locals_)
        new_attrs['from_data'] = locals_['from_data']
        methods_code.append(code)

        # add to_data
        code = _create_collection_to_data(db_type)
        exec(code, globals_, locals_)
        new_attrs['to_data'] = locals_['to_data']
        methods_code.append(code)

        # add from_oracle_object
        code = _create_collection_from_oracle_object(db_type)
        exec(code, globals_, locals_)
        new_attrs['from_oracle_object'] = locals_['from_oracle_object']
        methods_code.append(code)

        # add to_oracle_object
        code = _create_collection_to_oracle_object(db_type, new_attrs['__type_name__'])
        exec(code, globals_, locals_)
        new_attrs['to_oracle_object'] = locals_['to_oracle_object']
        methods_code.append(code)

        def ident(text: str, length: int = 1) -> str:
            return '\n'.join(' ' * length + ln for ln in text.split('\n'))

        # store generated code in __class_code__
        new_attrs['__class_code__'] = f'class {name}(list, Base):\n'
        new_attrs['__class_code__'] += '\n\n'.join(ident(code) for code in methods_code)

        return super().__new__(mcs, name, bases, new_attrs)


T = typing.TypeVar('T')


class Base:
    __type_name__: str
    package: typing.ClassVar[str]

    @classmethod
    @abc.abstractmethod
    def from_data(cls: typing.Type[T], data: typing.Any) -> T:
        ...

    @abc.abstractmethod
    def to_data(self) -> typing.Union[typing.Dict[str, typing.Any], typing.List[typing.Any]]:
        ...

    @classmethod
    @abc.abstractmethod
    def from_oracle_object(cls: typing.Type[T], obj: cx_Oracle.Object) -> T:
        ...

    @abc.abstractmethod
    def to_oracle_object(self, connection: cx_Oracle.Connection) -> cx_Oracle.Object:
        ...


class Object(Base, metaclass=ObjectMeta):
    @classmethod
    def from_data(cls: typing.Type[T], data: typing.Dict[str, typing.Any]) -> T:
        ...

    def to_data(self) -> typing.Dict[str, typing.Any]:
        ...

    @classmethod
    def from_oracle_object(cls: typing.Type[T], obj: cx_Oracle.Object) -> T:
        ...

    def to_oracle_object(self, connection: cx_Oracle.Connection) -> cx_Oracle.Object:
        ...


class Collection(typing.List[T], Base, metaclass=CollectionMeta):
    database_type: typing.ClassVar[DbType]

    @classmethod
    def from_data(cls: typing.Type[Collection[T]], data: typing.List[typing.Any]) -> Collection[T]:
        ...

    def to_data(self) -> typing.List[typing.Any]:
        ...

    @classmethod
    def from_oracle_object(cls: typing.Type[Collection[T]], obj: cx_Oracle.Object) -> Collection[T]:
        ...

    def to_oracle_object(self, connection: cx_Oracle.Connection) -> cx_Oracle.Object:
        ...
