from connection_pool import pool
import psycopg2
from psycopg2 import sql

def add_record(upc, series, year, description, quantity, notes):
    con = pool.getconn()
    cur = con.cursor()

    cur.execute(
        sql.SQL("insert into {} VALUES (%s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('ornaments')),
        [upc,series,year,description, quantity, notes])

    con.commit()
    pool.putconn(con)

def initial_data():
    con = pool.getconn()
    cur = con.cursor()
    query = sql.SQL("select * from {table} order by {field}").format(table=sql.Identifier('ornaments'),
    field = sql.Identifier('year'))
    cur.execute(query)
    rows = cur.fetchall()
    return rows

#delete records
def delete_records(upc):
    con = pool.getconn()
    cur = con.cursor()
    query = sql.SQL ("delete from {table} where {field} = %s").format(table=sql.Identifier('ornaments'),
    field=sql.Identifier('upc_code'))
    cur.execute(query,(upc,))
    con.commit()
    pool.putconn(con)

#update records
def update_records(upc,upd):
    con = pool.getconn()
    cur = con.cursor()
    query = sql.SQL("update {table} set {data} where upc_code = {upc_code}").format(
        table=sql.Identifier('ornaments'),
        data= sql.SQL(',').join(
            sql.Composed([sql.Identifier(k),sql.SQL(" = "), sql.Placeholder(k)]) for k in upd.keys()
            ),
        upc_code=sql.Placeholder('upc_code')
        )
    upd.update(upc_code=upc)
    print(query.as_string(con))
    cur.execute(query,upd)
    con.commit()
    pool.putconn(con)
