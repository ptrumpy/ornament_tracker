from connection_pool import pool
import psycopg2
from psycopg2 import sql

def initial_data():
    con = pool.getconn()
    cur = con.cursor()
    query = sql.SQL("select * from {table} order by {field}").format(table=sql.Identifier('ornaments'),
    field = sql.Identifier('year'))
    cur.execute(query)
    rows = cur.fetchall()
    pool.putconn(con)
    return rows

def populate_series_dropdown():
    con = pool.getconn()
    cur = con.cursor()
    query = sql.SQL("select distinct {field1} from {table} order by {field2}").format(
        field1 = sql.Identifier('series'),table= sql.Identifier('ornaments'),
        field2 = sql.Identifier('series')
    )
    cur.execute(query)
    series_list = cur.fetchall()
    pool.putconn(con)
    return series_list

def add_record(upc, series, year, description, quantity, notes):
    con = pool.getconn()
    cur = con.cursor()
    cur.execute(
        sql.SQL("insert into {} VALUES (%s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('ornaments')),
        [upc,series,year,description, quantity, notes])
    con.commit()
    pool.putconn(con)

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
    #print(query.as_string(con))
    cur.execute(query,upd)
    con.commit()
    pool.putconn(con)

def search_records(search, search_like):
    con = pool.getconn()
    cur = con.cursor()
    query = sql.SQL("Select * from {table} where {data} ").format(
        table=sql.Identifier('ornaments'),
        data= sql.SQL(' and ').join(
            sql.Composed([sql.Identifier(k),sql.SQL(' = '), sql.Placeholder(k)]) for k in search.keys())
        )
    query = (cur.mogrify(query,search).decode('utf-8'))
    if len(search_like)==2:
        query2 = sql.SQL("and lower({data2}").format(
            data2 = sql.SQL(' and lower(' ).join(
            sql.Composed([(sql.Identifier(j)),sql.SQL(') like '), sql.Placeholder(j)]) for j in search_like.keys())
            )
    elif len(search_like)==1:
        query2 = sql.SQL("and lower({data2}").format(
            data2 = sql.SQL(' and ' ).join(
            sql.Composed([(sql.Identifier(j)),sql.SQL(') like '), sql.Placeholder(j)]) for j in search_like.keys())
            )
    query2 = cur.mogrify(query2,search_like).decode('utf-8')
    cur.execute(query + query2)
    rows = cur.fetchall()
    pool.putconn(con)
    return rows
