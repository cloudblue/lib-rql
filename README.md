Python RQL
==========
![pyversions](https://img.shields.io/pypi/pyversions/lib-rql.svg)
[![PyPi Status](https://img.shields.io/pypi/v/lib-rql.svg)](https://pypi.org/project/lib-rql/)
[![codecov](https://codecov.io/gh/cloudblue/lib-rql/branch/master/graph/badge.svg)](https://codecov.io/gh/cloudblue/lib-rql)
[![PyPI status](https://img.shields.io/pypi/status/lib-rql.svg)](https://pypi.python.org/pypi/lib-rql/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lib-rql&metric=alert_status)](https://sonarcloud.io/dashboard?id=lib-rql)

RQL
---

RQL (Resource query language) is designed for modern application development. It is built for the web, ready for NoSQL, and highly extensible with simple syntax.
This is a query language fast and convenient database interaction. RQL was designed for use in URLs to request object-style data structures.

[RQL Reference](https://connect.cloudblue.com/community/api/rql/)

Notes
-----

Parsing is done with [Lark](https://github.com/lark-parser/lark) ([cheatsheet](https://lark-parser.readthedocs.io/en/latest/lark_cheatsheet.pdf)).
The current parsing algorithm is [LALR(1)](https://www.wikiwand.com/en/LALR_parser) with standard lexer.

Supported operators
=============================
1. Comparison (eq, ne, gt, ge, lt, le, like, ilike, search)
2. List (in, out)
3. Logical (and, or, not)
4. Constants (null(), empty())
5. Ordering (ordering)
6. Select (select)
7. Tuple (t)


Example
=======
```python
from py_rql import parse
from py_rql.exceptions import RQLFilterError

try:
    tree = parse('eq(key,value)')
except RQLFilterError:
    pass
```

Notes
=====
0. Values with whitespaces or special characters, like ',' need to have "" or ''
1. Supported date format is ISO8601: 2019-02-12
2. Supported datetime format is ISO8601: 2019-02-12T10:02:00 / 2019-02-12T10:02Z / 2019-02-12T10:02:00+03:00


Development
===========

1. Python 3.6+
0. Install dependencies `requirements/dev.txt`

Testing
=======

1. Python 3.6+
0. Install dependencies `requirements/test.txt`

Check code style: `flake8`
Run tests: `pytest`

Tests reports are generated in `tests/reports`.
* `out.xml` - JUnit test results
* `coverage.xml` - Coverage xml results

To generate HTML coverage reports use:
`--cov-report html:tests/reports/cov_html`

