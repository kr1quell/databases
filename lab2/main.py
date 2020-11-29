from view import View
from model import Model
from controller import Controller
import psycopg2


def input_value(controller, type_name, fk_table=None):
    value = None
    if fk_table is not None:
        controller.show_items(fk_table)
        print("Виберіть ключ зі списку")
        value = int(input())
    elif type_name == 'integer':
        print("Тип поля число")
        value = int(input())
    elif type_name == 'date':
        print("Тип поля дата")
        value = input()
    elif type_name == 'character varying':
        print("Тип поля текст")
        value = input()
    elif type_name == 'text':
        print("Тип поля текст")
        value = input()
    return value


def generate_values(controller, type_name, num, size):
    if type_name == 'integer':
        print("Введіть максимальне число")
        value = int(input())
        return controller.model.generate_numbers(num, value)
    elif type_name == 'date':
        print("Введіть кількість днів в діапазоні")
        value = int(input())
        return controller.model.generate_date(num, value, 0)
    elif type_name == 'character varying':
        print("Введіть довжину рядка")
        value = int(input())
        return controller.model.generate_str(num, value)
    elif type_name == 'text':
        print("Введіть довжину рядка")
        value = int(input())
        return controller.model.generate_str(num, value)
    else:
        return controller.model.generate_numbers(num, 100)


# Завдення1. CRUD (Create, Read, Update, Delete)
def option1(controller):
    controller.show_table_list()
    table_num = -1
    try:
        table_num = int(input())
        tbl_name = controller.get_table_name(table_num - 1)
    except ValueError as e:
        print('Помилка введення даних!')
        return

    op = 0
    while op != 5:
        controller.show_operation_list()
        op = int(input())
        if op == 1:
            tbl_columns = controller.get_columns(tbl_name)
            tbl_column_types = controller.get_column_types(tbl_name)
            item = []
            try:
                for i, column in enumerate(tbl_columns):
                    parent_tbl = controller.get_parent_table(tbl_name, column)
                    print('Введіть значення поля {}'.format(column))
                    val = input_value(controller, tbl_column_types[i], parent_tbl)
                    item.append(val)
                controller.insert_item(tbl_name, tbl_columns, item)
            except ValueError as e:
                print('Помилка введення даних!')
                return
        elif op == 2:
            tbl_columns = controller.get_columns(tbl_name)
            tbl_column_types = controller.get_column_types(tbl_name)
            item = []
            try:
                for i, column in enumerate(tbl_columns):
                    parent_tbl = controller.get_parent_table(tbl_name, column)
                    print('Введіть значення поля {}'.format(column))
                    val = input_value(controller, tbl_column_types[i], parent_tbl)
                    item.append(val)
                controller.update_item(tbl_name, tbl_columns, item)
            except ValueError as e:
                print('Помилка введення даних!')
                return
        elif op == 3:
            controller.show_items(tbl_name)
        elif op == 4:
            try:
                print("Введіть ключ для запису який необхідно видалити")
                item_id = int(input())
                controller.delete_item(tbl_name, item_id)
            except ValueError as e:
                print('Помилка введення даних')
                return
        input("Для продовження натисніть Enter...")


# Завдання 2
def option2(controller):
    controller.show_table_list()
    table_num = int(input())
    tbl_name = controller.get_table_name(table_num - 1)
    op = 0
    print("Обрано таблицю {}".format(tbl_name))
    print("Скільки записів потрібно згенерувати?")
    num = int(input())
    tbl_columns = controller.get_columns(tbl_name)
    tbl_column_types = controller.get_column_types(tbl_name)
    elements = []
    for i, column in enumerate(tbl_columns):
        print('Введіть дані для поля {}'.format(column))
        val = generate_values(controller, tbl_column_types[i], num, 5)
        elements.append(val)
    for j in range(num):
        item = []
        for k in range(len(tbl_columns)):
            item.append(elements[k][j])
        try:
            controller.model.create_item(tbl_name, tbl_columns, item)
        except(Exception, psycopg2.DatabaseError) as error:
            controller.model.roll_back()


# Завдання 3
def option3(controller):
    print('1. Фільми, що будуть показувати після дати у кінотеатрі')
    print('Виберіть одну з дій...')
    op = int(input())
    if op == 1:
        print('Введіть назву кінотеатру')
        cinema = input()
        print('Введіть дату після якої будуть показувати фільми (дд/мм/рр)')
        date = input()
        columns, items = controller.model.search_query(date, cinema)
        print(columns)
        controller.view.show_number_point_list('Films', items)

    input("Для продовження натисніть Enter...")


if __name__ == '__main__':
    model = Model()
    model.add_tables(["Films", "Cinemas", "Schedule", "Sessions"])
    key1 = {'fk_table': 'Sessions', 'fk_column': 'id_f', 'ref_table': 'Films', 'ref_column': 'if_f'}
    model.add_foreign_key(key1)
    key2 = {'fk_table': 'Schedule', 'fk_column': 'id_s', 'ref_table': 'Sessions', 'ref_column': 'id_s'}
    model.add_foreign_key(key2)
    key3 = {'fk_table': 'Schedule', 'fk_column': 'id_c', 'ref_table': 'Cinemas', 'ref_column': 'id_c'}
    model.add_foreign_key(key3)

    controller = Controller(model, View())
    while True:
        controller.show_menu()
        option = int(input())
        if option == 1:
            option1(controller)
        elif option == 2:
            option2(controller)
        elif option == 3:
            option3(controller)
        elif option == 4:
            break
