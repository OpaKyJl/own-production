from datetime import datetime
import pytz
import time

import psycopg2
from config import host, user, password, db_name

# connection = None
cursor = None


def set_connection(connection):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        return connection


def close_connection(connection):
    if connection is not None:
        connection.close()
        print("[INFO] PostgreSQL connection closed")


def check_connection(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f"Server version: {cursor.fetchone()}")
    except Exception as ex:
        print("[INFO] Соединение закрыто:", ex)


def select_from_table(connection, db_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT * FROM {db_name};'
            )
            # print(cursor.fetchall())
            selected_data = cursor.fetchall()

            match db_name:
                case "products":
                    # for row in selected_data:
                    #     print("Id = ", row[0], )
                    #     print("product = ", row[1])
                    #     print("price (100 gr)  = ", row[2], "\n")
                    return selected_data

                case "products_accounting":
                    # for row in selected_data:
                    #     print("Id = ", row[0], )
                    #     print("production = ", row[1])
                    #     print("product = ", row[2])
                    #     print("date = ", row[3])
                    #     print("product_used = ", row[4])
                    #     print("cost (использованного продукта)  = ", row[5], "\n")
                    return selected_data

                case "recipe":
                    # for row in selected_data:
                    #     print("Id = ", row[0], )
                    #     print("production = ", row[1])
                    #     print("product = ", row[2])
                    #     print("gram = ", row[3])
                    #     print("cost (аторасчёт)  = ", row[4], "\n")
                    return selected_data

                case "recipe_cost":
                    # for row in selected_data:
                    #     print("Id = ", row[0], )
                    #     print("product = ", row[1])
                    #     print("cost (100 gr)  = ", row[2], "\n")
                    return selected_data

                case "sales_accounting":
                    # for row in selected_data:
                    #     print("Id = ", row[0], )
                    #     print("production = ", row[1])
                    #     print("date = ", row[2])
                    #     print("продано в граммах = ", row[3])
                    #     print("стоимость проданного  = ", row[4], "\n")
                    return selected_data

    except Exception as ex:
        print(f'[INFO] Ошибка получения из таблицы {db_name}:', ex)

def insert_into_table(connection, db_name):
    try:
        with connection.cursor() as cursor:

            match db_name:
                case "products":
                    insert_script = f'INSERT INTO {db_name}(product, price_per_1000gr) VALUES (%s, %s);'
                    insert_value = ('Овощ1', 33.00)
                    cursor.execute(insert_script, insert_value)

                case "products_accounting":
                    insert_script = ("INSERT INTO products_accounting "
                                     "(production_id, product_id, date_accounting, product_used, product_used_cost) "
                                     "VALUES (%s, %s, %s, %s, %s)")
                    insert_value = (1, 4, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 333, 4444)
                    cursor.execute(insert_script, insert_value)

                case "recipe":
                    print("recipe 3")

                case "recipe_cost":
                    print("recipe_cost 4")

                case "sales_accounting":
                    insert_script = ("INSERT INTO sales_accounting "
                                     "(production_id, date_accounting, production_sale_grs, price) "
                                     "VALUES (%s, %s, %s, %s)")
                    insert_value = (1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 333, 4444)
                    cursor.execute(insert_script, insert_value)

            print(f'[INFO] Данные успешно добавлены в таблицу {db_name}')
    except Exception as ex:
        print(f'[INFO] Ошибка добавления в таблицу {db_name}:', ex)


def update_row(connection, db_name):
    # sql = """ UPDATE vendors
    #                 SET vendor_name = %s
    #                 WHERE vendor_id = %s"""
    try:
        with connection.cursor() as cursor:
            update_script = f'UPDATE {db_name} SET price_per_1000gr = %s WHERE id = %s;'
            update_value = (4444, 14)
            cursor.execute(update_script, update_value)

            match db_name:
                case "products":
                    print("db_name 1")

                case "products_accounting":
                    print("products_accounting 2")

                case "recipe":
                    print("recipe 3")

                case "recipe_cost":
                    print("recipe_cost 4")

                case "sales_accounting":
                    print("sales_accounting 5")

            print(f'[INFO] Данные были успешно изменены в таблице {db_name}')
    except Exception as ex:
        print(f'[INFO] Ошибка обновления строки в таблице {db_name}', ex)

def delete_row(connection, db_name):
    try:
        with connection.cursor() as cursor:
            delete_script = f'DELETE FROM {db_name} WHERE id = {15}'
            cursor.execute(delete_script)

            match db_name:
                case "products":
                    print("db_name 1")

                case "products_accounting":
                    print("products_accounting 2")

                case "recipe":
                    print("recipe 3")

                case "recipe_cost":
                    print("recipe_cost 4")

                case "sales_accounting":
                    print("sales_accounting 5")

            print(f'[INFO] Данные были успешно удалены из таблицы {db_name}')
    except Exception as ex:
        print(f'[INFO] Ошибка удаления строки из таблицы{db_name}:', ex)

# db_products = "products"
# db_products_accounting = "products_accounting"
# db_recipe = "recipe"
# db_recipe_cost = "recipe_cost"
# db_sales_accounting = "sales_accounting"
#
#
# connection = None
# connection = set_connection(connection)
# connection.autocommit = True
# check_connection(connection)
#
# # select_from_table(connection, db_products_accounting)
# insert_into_table(connection, db_sales_accounting)
# # update_row(connection, db_products)
# # delete_row(connection, db_products)
#
# close_connection(connection)
# check_connection(connection)


# a = {
#     'a': 3,
#     'b': "это б"
# }
# print(a['a'])