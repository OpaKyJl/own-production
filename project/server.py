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
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM {db_name};'
        )
        print(cursor.fetchall())
        # selected_data = cursor.fetchall()
        # for row in selected_data:
        #     print("Id = ", row[0], )
        #     print("product = ", row[1])
        #     print("price  = ", row[2], "\n")


def insert_into_table(connection, db_name):
    try:
        with connection.cursor() as cursor:
            insert_script = f'INSERT INTO {db_name}(product, price_per_1000gr) VALUES (%s, %s);'
            insert_value = ('Овощ', 33.00)
            cursor.execute(insert_script, insert_value)

            print("[INFO] Data was successfully inserted")
    except Exception as ex:
        print("[INFO] Ошибка добавления:", ex)


def update_row(connection, db_products):
    # sql = """ UPDATE vendors
    #                 SET vendor_name = %s
    #                 WHERE vendor_id = %s"""
    try:
        with connection.cursor() as cursor:
            update_script = f'UPDATE {db_products} SET price_per_1000gr = %s WHERE id = %s;'
            update_value = (4444, 14)
            cursor.execute(update_script, update_value)

            print("[INFO] Data was successfully updated")
    except Exception as ex:
        print("[INFO] Ошибка обновления", ex)

def delete_row(connection, db_products):
    try:
        with connection.cursor() as cursor:
            delete_script = f'DELETE FROM {db_products} WHERE id = {15}'
            cursor.execute(delete_script)

            print("[INFO] Data was successfully deleted")
    except Exception as ex:
        print("[INFO] Ошибка удаления:", ex)

db_products = "products"
db_products_accounting = "products_accounting"
db_recipe = "recipe"
db_recipe_cost = "recipe_cost"
db_sales_accounting = "sales_accounting"


connection = None
connection = set_connection(connection)
connection.autocommit = True
check_connection(connection)

# select_from_table(connection, db_products)
# insert_into_table(connection, db_products)
# update_row(connection, db_products)
delete_row(connection, db_products)

close_connection(connection)
check_connection(connection)


# a = {
#     'a': 3,
#     'b': "это б"
# }
# print(a['a'])