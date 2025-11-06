import psycopg2
from faker import Faker
from config import load_config
import random
from datetime import datetime
from products import manipulate_product
fake = Faker()
config = load_config()


class Order:
    def __init__(self, sellers_id):
        self.order_date = datetime.now()
        self.seller_id = random.choice(sellers_id)
        self.status = random.choice(['PAID', 'CANCELED', 'RETURNED'])
        self.total_amount = 0
        self.create_at = datetime.now()
        self.order_id = None
        self.order = []

    def insert_order(self):
        sql = '''
              INSERT INTO orders(order_date, seller_id, status, total_amount, created_at)
              VALUES (%s, %s, %s, %s, %s) RETURNING order_id'''  # Quan trọng: RETURNING để lấy order_id

        data = [self.order_date, self.seller_id, self.status, self.total_amount, self.create_at]

        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, data)
                    self.order_id = cur.fetchone()[0]  # Lấy order_id vừa insert
                conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error inserting order: {e}")
            return False

    def check_product(self, item_name, quantity):
        sql = '''SELECT product_id, product_name, price, stock_qty
                 FROM products \
                 WHERE product_name = %s'''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, [item_name])
                    data = cur.fetchone()

            if not data:
                print(f"Sản phẩm '{item_name}' không có trong kho")
                return None

            if quantity > data[-1]:
                print(f"Không đủ số lượng. Còn lại: {data[-1]}, yêu cầu: {quantity}")
                return None
            return data

        except psycopg2.Error as e:
            print(f"Error checking product: {e}")
            return None

    def insert_order_item(self, item_name, quantity):
        data = self.check_product(item_name, quantity)
        if not data:
            return False

        product_id = data[0]
        unit_price = float(data[2])
        subtotal = quantity * unit_price
        self.total_amount += subtotal

        oi_sql = '''INSERT INTO order_items(order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)'''
        oi_data = [self.order_id, product_id, quantity, unit_price, subtotal]

        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(oi_sql, oi_data)
                conn.commit()
            return True
        except psycopg2.Error as e:
            print(e)
            return False

    def update_total_amount(self):
        sql = '''UPDATE orders \
                 SET total_amount = %s \
                 WHERE order_id = %s'''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, [self.total_amount, self.order_id])
                conn.commit()
            return True
        except psycopg2.Error as e:
            print(e)
            return False

    def run(self):
        if not self.insert_order():
            print("Không thể tạo order")
            return

        print(f"Da tao order_id: {self.order_id}")
        prod_name = input("Nhap ten hang muon lay: ")
        quantity = int(input("Nhap so luong: "))
        manipulate_product('lay', prod_name, quantity)
        self.insert_order_item(prod_name, quantity)

        self.update_total_amount()
        print(f"total: {self.total_amount}")


def take_seller():
    sql = '''SELECT seller_id \
             FROM sellers'''
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                seller_raw = cur.fetchall()
                sellers = [x[0] for x in seller_raw]
        return sellers
    except psycopg2.Error as e:
        print(e)
        return []


if __name__ == "__main__":
    sellers = take_seller()
    if sellers:
        order = Order(sellers)
        num_prod = int(input("Nhap loai hang can lay: "))
        for i in range(num_prod):
            order.run()
    else:
        print("Khong co sellers trong database")