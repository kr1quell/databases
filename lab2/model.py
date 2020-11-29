import psycopg2
import bd_func as bd
from timer import timer


class Model(object):
    def __init__(self):
        self.conn = bd.connect_to_db()
        self.tables = []
        self.foreign_keys = []

    def add_tables(self, tables):
        self.tables = tables

    @property
    def tables_property(self):
        return self.tables

    def add_foreign_key(self, key_parameters):
        if len(key_parameters) != 4:
            return
        if (key_parameters.get('fk_table') is not None
                and key_parameters.get('fk_column') is not None
                and key_parameters.get('ref_table') is not None
                and key_parameters.get('ref_column')):
            self.foreign_keys.append(key_parameters)

    @property
    def foreign_keys_property(self):
        return self.foreign_keys

    def get_columns(self, table_name):
        return bd.get_columns(self.conn, table_name)

    def get_column_type(self, table, column_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns "
                       "WHERE table_name = '{}'".format(table))
        for col in cursor.fetchall():
            if column_name in col:
                return col[1]

    def get_column_types(self, table):
        cursor = self.conn.cursor()
        cursor.execute("SELECT data_type FROM information_schema.columns "
                       "WHERE table_name = '{}'".format(table))
        columns_types = [col_type[0] for col_type in cursor.fetchall()]
        return columns_types

    def generate_numbers(self, quantity, max_value):
        query = 'SELECT trunc(random()*{0})::int from generate_series({1},{2})'.format(max_value, 1, quantity)
        cursor = self.conn.cursor()
        cursor.execute(query)
        numbers = [num[0] for num in cursor.fetchall()]
        return numbers

    def generate_str(self, quantity, str_len):
        if str_len <= 0:
            return ''
        op = 'chr(trunc(65 + random()*25)::int)'
        parameters = op
        for i in range(1, str_len):
            parameters += ' || ' + op
        query = 'SELECT {0} from generate_series({1},{2})'.format(parameters, 1, quantity)
        cursor = self.conn.cursor()
        cursor.execute(query)
        str_res = [str0[0] for str0 in cursor.fetchall()]
        return str_res

    def generate_date(self, quantity, days=90, shift=0, start_date=None):
        if start_date is None:
            start_date = "NOW()"
        query = "select to_char(NOW() + (random() * (NOW() + '{0} days' - NOW())) + '{1} days', 'DD/MM/YYYY') " \
                "from generate_series({2},{3})" \
            .format(days, shift, 1, quantity)
        cursor = self.conn.cursor()
        cursor.execute(query)
        dates = [date0[0] for date0 in cursor.fetchall()]
        return dates

    # Фільми, що будуть показувати після дати у кінотеатрі
    @timer
    def search_query(self, after_date, cinema):
        query = 'SELECT name_f, genre_f, start_date, hall_name ' \
                'FROM "Films", "Sessions", "Schedule", "Cinemas" ' \
                'WHERE "Films"."id_f" = "Sessions"."id_f"' \
                'AND "Sessions"."id_s" = "Schedule"."id_s"' \
                'AND "Schedule"."id_c" = "Cinemas"."id_c"' \
                'AND "Cinemas".name_c = \'{}\' AND "Sessions".start_date > \'{}\'' \
            .format(cinema, after_date)
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return [desc[0] for desc in cursor.description], cursor.fetchall()

    def roll_back(self):
        self.conn.rollback()

    def create_item(self, table_name, columns, item):
        bd.create_item(self.conn, table_name, columns, item)

    def create_items(self, table_name, columns, items):
        bd.create_items(self.conn, table_name, columns, items)

    def read_item(self, table_name, columns, item_id):
        return bd.read_item(self.conn, table_name, columns, item_id)

    def read_items(self, table_name, columns):
        return bd.read_items(self.conn, table_name, columns)

    def update_item(self, table_name, columns, item, item_id):
        bd.update_item(self.conn, table_name, columns, item, item_id)

    def delete_item(self, table_name, item_id):
        columns = self.get_columns(table_name)
        bd.delete_item(self.conn, table_name, columns, item_id)

    def __del__(self):
        bd.disconnect_from_db(self.conn)
