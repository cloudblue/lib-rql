import json
from pprint import pprint

from py_rql.constants import FilterTypes
from py_rql.filter_cls import FilterClass


DATA = json.load(open('./books.json'))['books']


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


def main():
    total = len(DATA)
    filters = BookFilter()

    query = 'eq(title,Practical Modern JavaScript)'
    results = list(filters.filter(query, DATA))

    print(f'\nquery: {query} -> matches {len(results)}/{total}\n')
    pprint(results)
    print('*' * 70)

    query = 'or(eq(pages,472),lt(pages,400))'
    results = list(filters.filter(query, DATA))

    print(f'\nquery: {query} -> matches {len(results)}/{total}\n')
    pprint(results)
    print('*' * 70)

    query = 'and(eq(featured,true),in(status,(published,draft)))'
    results = list(filters.filter(query, DATA))

    print(f'\nquery: {query} -> matches {len(results)}/{total}\n')
    pprint(results)
    print('*' * 70)

    query = 'eq(status,null())'
    results = list(filters.filter(query, DATA))

    print(f'\nquery: {query} -> matches {len(results)}/{total}\n')
    pprint(results)
    print('*' * 70)

    query = 'like(title,*JavaScript*)'
    results = list(filters.filter(query, DATA))

    print(f'\nquery: {query} -> matches {len(results)}/{total}\n')
    pprint(results)
    print('*' * 70)

    query = 'ilike(title,*JavaScript*)'
    results = list(filters.filter(query, DATA))

    print(f'\nquery: {query} -> matches {len(results)}/{total}\n')
    pprint(results)
    print('*' * 70)


if __name__ == '__main__':
    main()
