import psycopg2
from dateutil.relativedelta import relativedelta
from faker import Faker
from config import load_config
import random
from datetime import datetime

fake = Faker()
config = load_config()

campaign_name = ['Flash Sale', 'Sitewide Discount Sale', 'First Order Special Discount', 'Buy One Get One Offer ', 'Conditional Free Shipping Offer ', 'Newsletter Signup Discount' , 'Holiday Special Sale', 'Digital Coupons','Free Sample Offer','Social Media Contest ','Loyalty Program Rewards', 'End-of-Season Sale' ]
promotion_type = ['advertising', 'digital selling', 'sales promotion','public relations']



class Promotions:
    def __init__(self):
        self.promotion_name = random.choice(campaign_name)
        self.promotion_type = random.choice(promotion_type)
        self.discount_type = random.choice(['PERCENT', 'FIXED', 'NONE'])
        if self.discount_type == 'PERCENT':
            self.discount_value = random.randint(5, 30)  # 5% - 30%
        elif self.discount_type == 'FIXED':
            self.discount_value = random.randint(10000, 500000)  # 10k - 500k VNĐ
        else:
            self.discount_value = 0
        self.start_date = fake.date_between(start_date='-1y', end_date='today')
        self.end_date = self.start_date + relativedelta(days=random.randint(1, 30))
        self.data = [self.promotion_name,self.promotion_type,self.discount_type,self.discount_value,self.start_date,self.end_date]
    def insert_promotion(self):
        sql = '''
              INSERT INTO promotions(promotion_name,promotion_type,discount_type,discount_value,start_date,end_date)
              values (%s, %s, %s, %s, %s, %s)'''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, self.data)
                conn.commit()

        except psycopg2.Error as e:
            print(e)

if __name__ == "__main__":
    for _ in range(10):
        promotions = Promotions()
        promotions.insert_promotion()
        
