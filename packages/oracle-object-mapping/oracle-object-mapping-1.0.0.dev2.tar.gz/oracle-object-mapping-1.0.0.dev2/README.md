# Oracle Object Mapping

# Requirements
- Python 3.7+

# Install
```
pip install oracle-object-mapping
```

## Example

### Types definition
```python
import datetime
from typing import Optional

from oracle_object_mapping import objects, fields


class TABLE_VARCHARS(objects.Collection[str]):
    pass


class TABLE_CLOBS(objects.Collection[str]):
    package = 'LIBRARY'
    database_type = fields.CLOB()


class BOOK(objects.Object):
    package = 'LIBRARY'
    ID: Optional[int]
    TITLE: Optional[str]
    AUTHORS: Optional[TABLE_VARCHARS]
    DEDICATION: Optional[str] = fields.CLOB()
    PAGES: Optional[TABLE_CLOBS]
    PUBLISH_DATE: Optional[datetime.datetime]
```

### Manipulate objects
```python
data = ["a" * x for x in range(10)]

table_a = TABLE_VARCHARS()
for x in data:
    table_a.append(x)

table_b = TABLE_VARCHARS.from_data(data)

# table_a == table_b
```

```python
book_a = BOOK()
book_a.TITLE = 'Hello'
book_a.AUTHORS = TABLE_VARCHARS.from_data(['Alberto', 'José'])

# ba.to_data() == {'TITLE': 'HELLO', 'AUTHORS': ['Alberto', 'José']}

data = {'TITLE': 'HELLO', 'AUTHORS': ['Alberto', 'José']}
book_b = BOOK.from_data(data)

# book_a == book_b
```

### Call function
```python
from oracle_object_mapping import utils

connection: cx_Oracle.connection
name = 'LIBRARY.CREATE_BOOK'
return_type = BOOK
new_book = utils.call_function(connection, name, return_type, args=[book_a])
print(new_book.ID)
```
