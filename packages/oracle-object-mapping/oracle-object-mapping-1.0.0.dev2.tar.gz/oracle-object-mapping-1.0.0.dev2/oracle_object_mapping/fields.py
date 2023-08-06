from . import objects

"""
Database fields types mapping.
"""

"""
BFILE: cx_Oracle.LOB
BINARY_DOUBLE: float
BINARY_FLOAT: float
BLOB: bytes
CHAR: str
CLOB: str
CURSOR: cx_Oracle.Cursor
DATE: datetime.datetime
INTERVAL_DAY_TO_SECOND: datetime.timedelta
LONG: str
LONG_RAW: bytes
NCHAR: str
NCLOB: cx_Oracle.LOB
NUMBER: typing.Union[float, int]
NVARCHAR2: str
OBJECT: TypeVar('T1', bound=TypeVar('T0', bound=Base))
RAW: bytes
ROWID: str
TIMESTAMP: datetime.datetime
TIMESTAMP_WITH_LOCAL_TIME_ZONE': datetime.datetime
TIMESTAMP_WITH_TIME_ZONE': datetime.datetime
UROWID: str
VARCHAR2: str
"""


# the non DbType superclasses are set to allow attributions in class definition without MyPy complain
class CLOB(str, objects.DbType):
    def from_oracle_object(self, var_name: str) -> str:
        return f'{var_name}.read()'
