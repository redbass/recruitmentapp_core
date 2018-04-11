from pymongo.cursor import Cursor


def get_pagination_from_cursor(cursor: Cursor,
                               start: int,
                               limit: int):
    total = cursor.count()

    results = cursor.skip(start).limit(limit)
    has_next = total > (start + limit)

    pagination = {
        "start": start,
        "limit": limit,
        "total": total,
        "hasNext": has_next,
        "results": list(results)
    }

    return pagination
