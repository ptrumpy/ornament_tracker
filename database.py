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
def update_records(series, year, desc, qty, notes):
    con = pool.getconn()
    cur = con.cursor()
    query = sql.SQL("update {table} set {field1} = %s, {field2} = %s,{field3} = %s"
    ",{field4}= %s,{field5}=%s where {field6} = %s").format(table=sql.Identifier('ornaments'),
    field1=sql.Identifier('series'),field2=sql.Identifier('year'))
    con.commit()
    pool.putconn(con)
