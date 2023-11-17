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


def select_from_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM products;"""
        )
        # print(cursor.fetchall())
        selected_data = cursor.fetchall()
        for row in selected_data:
            print("Id = ", row[0], )
            print("product = ", row[1])
            print("price  = ", row[2], "\n")


def insert_into_table(connection):
    try:
        with connection.cursor() as cursor:
            insert_script = 'INSERT INTO products(product, price_per_1000gr) VALUES (%s, %s);'
            insert_value = ('Овощ', 33.00)
            cursor.execute(insert_script, insert_value)

            print("[INFO] Data was successfully inserted")
    except Exception as ex:
        print("[INFO] Ошибка добавления:", ex)


def update_row(connection):
    # sql = """ UPDATE vendors
    #                 SET vendor_name = %s
    #                 WHERE vendor_id = %s"""
    try:
        with connection.cursor() as cursor:
            update_script = 'UPDATE products SET price_per_1000gr = %s WHERE id = %s;'
            update_value = (9999, 13)
            cursor.execute(update_script, update_value)

            print("[INFO] Data was successfully updated")
    except Exception as ex:
        print("[INFO] Ошибка обновления", ex)

def delete_row(connection):
    try:
        with connection.cursor() as cursor:
            delete_script = f'DELETE FROM products WHERE id = {11}'
            cursor.execute(delete_script)

            print("[INFO] Data was successfully deleted")
    except Exception as ex:
        print("[INFO] Ошибка удаления:", ex)

connection = None
connection = set_connection(connection)
connection.autocommit = True
check_connection(connection)

# select_from_table(connection)
# insert_into_table(connection)
# update_row(connection)
# delete_row(connection)

close_connection(connection)
check_connection(connection)


# a = {
#     'a': 3,
#     'b': "это б"
# }
# print(a['a'])