# main_db.py
import sqlite3
from db import queries


db = sqlite3.connect('db/shop.sqlite3')
cursor = db.cursor()


async def DataBase_create():
    if db:
        print('База данных подключена!')
    cursor.execute(queries.CREATE_TABLE_shop)
    cursor.execute(queries.CREATE_TABLE_product_details)
    cursor.execute(queries.CREATE_TABLE_collection_products)



async def sql_insert_shop(name_product, product_size, price, photo, productid):
    cursor.execute(queries.INSERT_shop_QUERY, (
        name_product, product_size, price, photo, productid
    ))
    db.commit()

async def sql_insert_product_details(productid, category, infoproduct):
    cursor.execute(queries.INSERT_product_details_QUERY, (
        productid, category, infoproduct
    ))
    db.commit()

async def sql_insert_collection_products(productid, collection):
    cursor.execute(queries.INSERT_collection_products_QUERY, (
        productid, collection
    ))
    db.commit()

# CRUD - Read
# =====================================================

# Основное подключение к базе (Для CRUD)
def get_db_connection():
    conn = sqlite3.connect('db/shop.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * from shop s
    INNER JOIN product_details pd 
    ON s.productid = pd.productid
    INNER JOIN collection_products cp 
    ON s.productid = cp.productid
    """).fetchall()
    conn.close()
    return products




# CRUD - Delete
# =====================================================

def delete_product(productid):
    conn = get_db_connection()

    conn.execute('DELETE FROM shop WHERE productid = ?', (productid,))

    conn.commit()
    conn.close()



# CRUD - Update
# =====================================================
def update_product_field(productid, field_name, new_value):
    store_table = ["name_product", "product_size", "price", "photo"]
    store_detail_table = ["infoproduct", "category"]
    collection_table = ["collection"]
    conn = get_db_connection()
    try:
        if field_name in store_table:
            query = f'UPDATE shop SET {field_name} = ? WHERE productid = ?'
        elif field_name in store_detail_table:
            query = f'UPDATE product_details SET {field_name} = ? WHERE productid = ?'
        elif field_name in collection_table:
            query = f'UPDATE collection_products SET {field_name} = ? WHERE productid = ?'
        else:
            raise ValueError(f'Нет такого поля {field_name}')

        conn.execute(query, (new_value, productid))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'Ошибка - {e}')
    finally:
        conn.close()