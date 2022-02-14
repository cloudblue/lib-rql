# Python RQL


[![pyversions](https://img.shields.io/pypi/pyversions/lib-rql.svg)](https://pypi.org/project/lib-rql/)
[![PyPi Status](https://img.shields.io/pypi/v/lib-rql.svg)](https://pypi.org/project/lib-rql/)
[![PyPI status](https://img.shields.io/pypi/status/lib-rql.svg)](https://pypi.org/project/lib-rql/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/lib-rql)](https://pypi.org/project/lib-rql/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lib-rql&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=lib-rql)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=lib-rql&metric=coverage)](https://sonarcloud.io/summary/new_code?id=lib-rql)



## Introduction

RQL (Resource query language) is designed for modern application development. It is built for the web, ready for NoSQL, and highly extensible with simple syntax.
This is a query language fast and convenient database interaction. RQL was designed for use in URLs to request object-style data structures.

[RQL Reference](https://connect.cloudblue.com/community/api/rql/)

## Install

`Python RQL` can be installed from [pypi.org](https://pypi.org/project/lib-rql/) using pip:

```
$ pip install lib-rql
```

## Documentation

[`Python RQL` documentation](https://lib-rql.readthedocs.io/en/latest/) is hosted on the _Read the Docs_ service.


## Projects using Python RQL

`Django RQL` is the Django app, that adds RQL filtering to your application.

Visit the [Django RQL](https://github.com/cloudblue/django-rql) project repository for more informations.


## Notes

Parsing is done with [Lark](https://github.com/lark-parser/lark) ([cheatsheet](https://lark-parser.readthedocs.io/en/latest/lark_cheatsheet.pdf)).
The current parsing algorithm is [LALR(1)](https://www.wikiwand.com/en/LALR_parser) with standard lexer.

0. Values with whitespaces or special characters, like ',' need to have "" or ''
1. Supported date format is ISO8601: 2019-02-12
2. Supported datetime format is ISO8601: 2019-02-12T10:02:00 / 2019-02-12T10:02Z / 2019-02-12T10:02:00+03:00


## Supported operators

1. Comparison (eq, ne, gt, ge, lt, le, like, ilike, search)
2. List (in, out)
3. Logical (and, or, not)
4. Constants (null(), empty())
5. Ordering (ordering)
6. Select (select)
7. Tuple (t)


## Examples

### Parsing a RQL query


```python
from py_rql import parse
from py_rql.exceptions import RQLFilterError

try:
    tree = parse('eq(key,value)')
except RQLFilterError:
    pass
```


### Filter a list of dictionaries

```python
from py_rql.constants import FilterTypes
from py_rql.filter_cls import FilterClass


class BookFilter(FilterClass):
    FILTERS = [
        {
            'filter': 'title',
        },
        {
            'filter': 'author.name',
        },
        {
            'filter': 'status',
        },
        {
            'filter': 'pages',
            'type': FilterTypes.INT,
        },
        {
            'filter': 'featured',
            'type': FilterTypes.BOOLEAN,
        },
        {
            'filter': 'publish_date',
            'type': FilterTypes.DATETIME,
        },
    ]

filters = BookFilter()

query = 'eq(title,Practical Modern JavaScript)'
results = list(filters.filter(query, DATA))

print(results)

query = 'or(eq(pages,472),lt(pages,400))'
results = list(filters.filter(query, DATA))

print(results)
```


## Development


1. Python 3.6+
0. Install dependencies `pip install poetry && poetry install`

## Testing

1. Python 3.6+
0. Install dependencies `pip install poetry && poetry install`

Check code style: `poetry run flake8`
Run tests: `poetry run pytest`

Tests reports are generated in `tests/reports`.
* `out.xml` - JUnit test results
* `coverage.xml` - Coverage xml results

To generate HTML coverage reports use:
`--cov-report html:tests/reports/cov_html`

## License

`Python RQL` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
