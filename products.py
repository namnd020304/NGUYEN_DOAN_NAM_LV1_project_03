import psycopg2
from faker import Faker
from config import load_config
import random

fake = Faker()
config = load_config()

def get_id():
    cat_sql = '''
    select category_id from categories'''
    brand_sql ='''
    select brand_id from brands'''
    sellers_sql = '''
    select seller_id from sellers'''
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cursor1:
            cursor1.execute(cat_sql)
            # while cursor.fetchone() != None:
            cat_id=[x[0] for x in cursor1.fetchall()]
        with conn.cursor() as cursor2:
            cursor2.execute(brand_sql)
            # while cursor.fetchone() != None:
            brand_id=[x[0] for x in cursor2.fetchall()]
        with conn.cursor() as cursor3:
            cursor3.execute(sellers_sql)
            # while cursor.fetchone() != None:
            sellers_id=[x[0] for x in cursor3.fetchall()]
    return cat_id, brand_id, sellers_id




class Product:
    def __init__(self, categories_id, brands_id, sellers_id):
        self.product_name =fake.catch_phrase()
        self.category_id = random.choice(categories_id)
        self.brand_id = random.choice(brands_id)
        self.seller_id = random.choice(sellers_id)
        self.price = round(random.uniform(100000,50000000), 2)
        self.discount_price = self.price * random.uniform(0.7,1.0)
        self.stock_qty = random.randint(0,500)
        self.rating = round(random.uniform(3,5),1)
        self.created_at = fake.date_time_between(start_date='-3y')
        if self.stock_qty == 0:
            self.is_active = False
        else:
            self.is_active = True
        self.data = [self.product_name, self.category_id, self.brand_id,self.seller_id,self.price,self.discount_price,self.stock_qty,self.rating,self.created_at]

    def insert_seller(self):
        sql = '''
              INSERT INTO products(product_name, category_id, brand_id,seller_id,price,discount_price,stock_qty,rating,created_at)
              values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, self.data)
                conn.commit()

        except psycopg2.Error as e:
            print(e)


def manipulate_product():
    while True:
        print('=======THEM/LAY/THOAT hang=======')
        chose = input("Lua chon Them/Lay")
        prod_name = input("Nhap ten hang can lay: ")
        prod_name = prod_name.strip()
        quantity = int(input("So luong: "))
        sql = '''
              select stock_qty \
              from products \
              where product_name = %s'''
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [prod_name,])
                stock_qty = cur.fetchone()[0]
                print(f'So luong san pham {prod_name} Ban dau {stock_qty}')
        if chose == 'Them':
            stock_qty += int(quantity)
        elif chose == 'Lay':
            if stock_qty > int(quantity):
                stock_qty -= int(quantity)
            else:
                print("Khong du so luong muon lay")
        elif chose == 'THOAT':
            break
        else:
            print('Loi cu phap')
        sql = '''
        UPDATE products SET stock_qty = %s WHERE product_name = %s'''
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, [stock_qty, prod_name,])
        print(f'So san pham {prod_name} hien co {stock_qty}')



if __name__ == '__main__':
    manipulate_product()


