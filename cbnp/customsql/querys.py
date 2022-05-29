import sqlite3

QUERYS = {
    "read_all": "SELECT * FROM %s",
    "read_by_id": "SELECT * FROM %s WHERE id = %s",
    "create_one": 'INSERT INTO %s(%s) VALUES (%s)',
    "update_one": 'UPDATE %s SET %s WHERE "id"=%s',
    "delete_one": 'DELETE FROM %s WHERE "id"=%s',
    "join_tables": 'SELECT * FROM %s INNER JOIN %s WHERE %s'
}


def read_clients(id=None, **kwargs):
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        table = 'clients'
        if id:
            cursor.execute(QUERYS['read_by_id'] % (table, id))
        else:
            cursor.execute(QUERYS["read_all"] % table)
        return cursor.fetchall()


def create_clients(**kwargs):
    params_q = ''
    values_q = ''
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        table = 'clients'
        for key, value in kwargs.items():
            params_q += f'"{key}",'
            if isinstance(value, str):
                values_q += f'"{value}",'
            else:
                values_q += f'{value},'
        params_q = params_q[:-1]
        values_q = values_q[:-1]
        cursor.execute(
            QUERYS['create_one'] % (table, params_q, values_q)
        )
        return cursor.lastrowid


def update_clients(**kwargs):
    params_q = ''
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        table = 'clients'
        for key, value in kwargs.items():
            if 'id' in key:
                continue
            params_q += f'"{key}"="{value}",'
        params_q = params_q[:-1]
        cursor.execute(
            QUERYS['update_one'] % (table, params_q, kwargs['id'])
        )
        return cursor.lastrowid


def delete_clients(**kwargs):
    search = read_clients(kwargs['id'])
    if not search:
        return False
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        table = 'clients'
        cursor.execute(
            QUERYS['delete_one'] % (table, kwargs['id'])
        )
        return cursor.lastrowid


def join_tables(params: dict, id=None, **kwargs):
    where = ''
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()

        for k, v in params.items():
            where += f"{k}.{v}="
        where = where[:-1]
        table_1, table_2 = params.keys()
        if id:
            where += f" AND {table_1}.id={id}"

        cursor.execute(
            QUERYS['join_tables'] % (table_1, table_2, where)
        )
        return cursor.fetchall()
