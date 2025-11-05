from config import load_config
import psycopg2

def create_tables():
    sql = ('''
    CREATE TABLE brands(
        brand_id SERIAL PRIMARY KEY,
        brand_name VARCHAR(100),
        country VARCHAR(50),
        create_at TIMESTAMP)
    ''',
           '''
           CREATE TABLE  categories(
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(100),
                parent_category_id int,
                level smallint,
               create_at TIMESTAMP)
           ''',
           '''
           CREATE TABLE sellers(
                seller_id	SERIAL PRIMARY KEY,
                seller_name	VARCHAR(150),
                join_date	DATE,
                seller_type	VARCHAR(50),
                rating	DECIMAL(2,1),
                country	VARCHAR(50))
           ''',
           '''
           CREATE TABLE products(
               product_id	SERIAL PRIMARY KEY,
                product_name	VARCHAR(200),
                category_id	INT REFERENCES categories(category_id),
                brand_id	INT REFERENCES brands(brand_id),
                seller_id	INT REFERENCES sellers(seller_id),
                price	DECIMAL(12,2),
                discount_price	DECIMAL(12,2),
                stock_qty	INT,
                rating	FLOAT,
                created_at	TIMESTAMP,
                is_active  BOOLEAN)
           ''',
           '''
           CREATE TABLE orders(
                order_id	SERIAL PRIMARY KEY,
                order_date	TIMESTAMP,
                seller_id	INT REFERENCES sellers(seller_id),
                status	VARCHAR(20),
                total_amount	DECIMAL(12,2),
                created_at	TIMESTAMP)
           ''',
           '''
           CREATE TABLE order_items(
                order_item_id	SERIAL PRIMARY KEY,
                order_id	INT REFERENCES orders(order_id),
                product_id	INT REFERENCES products(product_id),
                quantity	INT,
                unit_price	DECIMAL(12,2),
                subtotal	DECIMAL(12,2))
           ''',
           '''
           CREATE TABLE promotions(
                promotion_id	SERIAL PRIMARY KEY,
                promotion_name	VARCHAR(100),
                promotion_type	VARCHAR(50),
                discount_type 	VARCHAR(20),
                discount_value	NUMERIC(10,2),
                start_date	DATE,
                end_date	DATE)
           ''',
           '''
           CREATE TABLE promotion_products(
               promo_product_id	SERIAL PRIMARY KEY,
                promotion_id	INT REFERENCES promotions(promotion_id),
                product_id	INT REFERENCES products(product_id),
                created_at	TIMESTAMP)
           '''
           )
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in sql:
                    cur.execute(command)
        print('tao database thanh cong')
    except psycopg2.Error as e:
        print(e)

if __name__ == '__main__':
    create_tables()
