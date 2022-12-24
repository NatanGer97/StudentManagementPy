# import logging
#
# from sqlalchemy import text
#
# from app.main import database
#
# db = database.get_db()
#
#
# def get_json_value(x):
#     if 'data' in str(type(x)):
#         return str(x)
#     elif 'Decimal' in str(type(x)):
#         return float(x)
#     return x
#
#
# def get_paginated(fields, from_str, where_str, orderby_field, orderby_direction, page, page_size, params):
#     select_str = "SELECT" + ",".join(map(lambda x: x[0] + " " + x[1],
#                                          fields)) + ' ' + from_str
#     ob = list(filter(lambda x: x[1] == orderby_field,
#                      fields))
#     orderby_str = " ORDER BY " + ob[0][0] + " " + orderby_direction + " "
#
#     if page and page_size:
#         orderby_str = orderby_str + " LIMIT " + str(page_size)
#         orderby_str = orderby_str + " OFFSET " + str((page - 1) * page_size)
#
#     sql = select_str + where_str + orderby_str
#     print("running sql: " + sql)
#     fetchAll = db.execute(text(sql),
#                           params).fetchall()
#     rowcount = db.execute(text("SELECT COUNT(*) cnt FROM (" + select_str + where_str + ") as a"),
#                           params).fetcall()
#
#     res = {}
#     total = rowcount[0]["cnt"]
#     res['count'] = total
#     if page_size > total:
#         count = total
#     if page and page_size:
#         res['page'] = page
#         last_page = 1
#         if total % page_size == 0:
#             last_page = 0
#         res['of_page'] = (total / page_size) + last_page
#         res['data'] = [dict(zip(row._fields,
#                                 map(lambda x: get_json_value(x),
#                                     row._data))) for row in fetchAll]
#     return res


from sqlalchemy import text

from app.main import database

def get_json_value(x):
    if 'date' in  str(type(x)):
        return str(x)
    elif 'Decimal' in  str(type(x)):
        return float(x)
    return x

def get_paginated(fields, from_str, where_str, orderby_field, orderby_direction, page, count, params ):
    select_str = 'select ' + ','.join(map(lambda x: x[0] + " " + x[1] ,fields)) + ' ' + from_str + ' '
    ob = list(filter(lambda x: x[1] == orderby_field, fields))
    orderby_str = ""
    if (len(ob) > 0):
        orderby_str = " order by " + ob[0][0] + " " + orderby_direction + " "

    if page and  count:
        orderby_str = orderby_str + " limit " +str(count)
        orderby_str = orderby_str + " offset " + str((page - 1) * count)

    sql = select_str + where_str + orderby_str
    print("running:" + sql)
    fetchall = database.engine.execute(text(sql), params).fetchall()
    rowcount = database.engine.execute(text("select count(*) cnt from (" + select_str + where_str + ") as a"), params).fetchall()

    res = {}
    total = rowcount[0]["cnt"]
    res['count'] = total
    if count > total:
        count = total
    if page and count:
        res['page'] = page
        last = 1
        if total % count == 0:
            last = 0
        res['of_page'] = (total / count) + last
    res['data'] =  [dict(zip(row._fields, map(lambda x: get_json_value(x), row._data))) for row in fetchall]
    return res
