import psycopg2


def connect_to_db():
    conn = psycopg2.connect(database='postgres', user='postgres', password='admin', host='localhost')
    return conn


def disconnect_from_db(conn):
    if conn is not None:
        conn.close()


def get_columns(conn, table_name):
    query = 'SELECT * FROM "' + table_name + '" LIMIT 0'
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    return columns


def create_item(conn, table_name, columns, item):
    query = 'INSERT INTO ' + '"' + table_name + '" ('
    query += '"' + columns[0] + '"'

    for column in range(1, len(columns)):
        query += ', "' + str(columns[column]) + '"'

    query += ') VALUES('

    query += "'" + str(item[0]) + "'"
    for field in range(1, len(item)):
        query += ", '" + str(item[field]) + "'"

    query += ")"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def create_items(conn, tbl_name, columns, items):
    for item in items:
        create_item(conn, tbl_name, columns, item)


def read_item(conn, tbl_name, columns=None, item_id=None):
    query = 'SELECT * FROM "' + tbl_name + '"'
    if columns is None:
        columns = get_columns(conn, tbl_name)
    else:
        pass
    if item_id is not None:
        query += ' WHERE "' + columns[0] + '" = ' + str(item_id)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()


def read_items(conn, tbl_name, columns=None):
    query = 'SELECT * FROM "' + tbl_name + '"'
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def update_item(conn, tbl_name, columns, item, item_id):
    query = 'UPDATE "' + tbl_name + '" SET '
    query += '"' + columns[0] + '" = ' + "'" + str(item[0]) + "'"

    for field in range(1, len(columns)):
        query += ', "' + columns[field] + '" = ' + "'" + str(item[field]) + "'"

    query += ' WHERE "' + columns[0] + '" = ' + str(item_id)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def delete_item(conn, tbl_name, columns, item_id):
    query = 'DELETE FROM "' + tbl_name + '" WHERE '
    query += '"' + columns[0] + '" = ' + str(item_id)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
