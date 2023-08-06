import datetime
from typing import Any, Dict, List, Type, TypeVar, cast

import cx_Oracle

from . import objects


def oracle_object_to_data(obj: cx_Oracle.Object) -> Any:
    if not isinstance(obj, cx_Oracle.Object):
        return obj
    if obj.type.iscollection:
        return [oracle_object_to_data(o) for o in obj.aslist()]
    data = {}
    for attr in obj.type.attributes:
        data[attr.name] = oracle_object_to_data(obj.__getattribute__(attr.name))
    return data


T = TypeVar('T', objects.Base, float, int, bytes, str, datetime.datetime, datetime.timedelta)


def call_function(connection: cx_Oracle.Connection, name: str, return_type: Type[T], *, args: List[Any] = None,
                  kwargs: Dict[str, Any] = None) -> T:
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []
    with connection.cursor() as cursor:
        if issubclass(return_type, objects.Base):
            r_type = connection.gettype(return_type.__type_name__)
        else:
            r_type = return_type
        args_ = [v.to_oracle_object(connection) if isinstance(v, objects.Base) else v for v in args]
        kwargs_ = {k: (v.to_oracle_object(connection) if isinstance(v, objects.Base) else v) for k, v in kwargs.items()}
        obj = cursor.callfunc(name, r_type, args_, kwargs_)
        if issubclass(return_type, objects.Base):
            return return_type.from_oracle_object(obj)
        else:
            return obj
