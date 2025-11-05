import psycopg2
from faker import Faker
from config import load_config
import random

config = load_config()
fake = Faker()

class Seller:
    def __init__(self):
        self.seller_name = fake.company()
        self.join_date = fake.date_time_this_year()
        self.seller_type = random.choice(['Official' ,'Preferred', 'Overseas', 'Marketplace'])
        self.rating = round(random.uniform(0, 5),1)
        self.country = 'Vietnam'
    def insert_seller(self):
        sql = '''
        INSERT INTO sellers (seller_name, join_date, seller_type, rating, country) values 
              (%s, %s, %s, %s, %s)'''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, [self.seller_name, self.join_date, self.seller_type, self.rating, self.country,])
                conn.commit()

        except psycopg2.Error as e:
            print(e)

if __name__ == '__main__':
    for i in range(25):
        seller = Seller()
        seller.insert_seller()