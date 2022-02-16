User guide
==========


Getting started
---------------


Install
^^^^^^^

*Python RQL* is a small python package that can be installed
from the `pypi.org <https://pypi.org/project/lib-rql/>`_ repository.


.. code-block:: sh

    $ pip install lib-rql



First steps with Python RQL
---------------------------

Python RQL allows you to filter a list of python dictionary using RQL.

First of all you have define your filters. To do so you have to create a class that
inherits from :class:`~py_rql.filter_cls.FilterClass` and declare your filters like in the following example:

.. code-block:: python

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



Then you can use your BookFilter like in the following example:

.. code-block:: python

    filters = BookFilter()

    query = 'eq(title,Practical Modern JavaScript)'
    results = list(filters.filter(query, DATA))

    print(results)

    query = 'or(eq(pages,472),lt(pages,400))'
    results = list(filters.filter(query, DATA))

    print(results)


See the examples folder in the project root for a demo program.


Customize filter lookups
------------------------

You can explicitly declare the lookups you want to support for a specific filter.
For example if you want to just support the `eq` and `ne` lookup for a string filter you can do
that like in the following example:


.. code-block:: python

    from py_rql.constants import FilterLookups, FilterTypes
    from py_rql.filter_cls import FilterClass


    class BookFilter(FilterClass):
        FILTERS = [
            {
                'filter': 'title',
                'lookups': {FilterLookups.EQ, FilterLookups.NE}
            },
        ]

