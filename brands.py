import psycopg2
from config import load_config
from faker import Faker
import random
import json
from math import floor

config = load_config()
fake = Faker()

class Brand:
    def __init__(self):
        self.brand_name = fake.name()
        self.country = fake.country()
        self.create_at = fake.date_time_between(start_date='-30d', end_date='now')

    def gen_brands(self):
        gen_sql = '''
        INSERT INTO brands(brand_name, country, create_at) values(
        %s, %s, %s);
        '''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(gen_sql, (self.brand_name, self.country, self.create_at))
                conn.commit()
        except psycopg2.Error as e:
            print(e)

class Categories:
    def __init__(self):
        self.category_name = None
        self.parent_category_id = None
        self.level=0
        self.create_at = fake.date_time_this_year()
    def gen_level(self):
        with open('category_name.json', 'r') as category:
            text = json.load(category)
        relate = []
        for category in text:
            relate.append(category['letter'])
            relate.extend(category['names'])
        if self.level%16 == 0:
            self.level =1
            self.parent_category_id = None
        else:
            self.level = 2
            self.parent_category_id = floor(self.level/16)
    def gen_categories(self):
        self.gen_level()
        gen_sql = '''
        INSERT INTO categories(category_name, country, create_at) values(
        %s, %s, %s);
        '''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(gen_sql, (self.brand_name, self.country, self.create_at))
                conn.commit()
        except psycopg2.Error as e:
            print(e)



if __name__ == '__main__':
    pass

