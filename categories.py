import psycopg2
from faker import Faker
import random
from config import load_config


fake = Faker()

config = load_config()


class Category:
    def __init__(self, category_name, parent_category_id=None, level=1):
        self.category_name = category_name
        self.parent_category_id = parent_category_id
        self.level = level
        self.created_at = fake.date_time_this_year()

    def insert_category(self):
        """Insert một category vào database"""
        gen_sql = '''
                  INSERT INTO categories(category_name, parent_category_id, level, created_at)
                  VALUES (%s, %s, %s, %s) RETURNING category_id; \
                  '''
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(gen_sql, (
                        self.category_name,
                        self.parent_category_id,
                        self.level,
                        self.created_at
                    ))
                    category_id = cur.fetchone()[0]
                conn.commit()
                print(f"Inserted: {self.category_name} (ID: {category_id}, Level: {self.level})")
                return category_id
        except psycopg2.Error as e:
            print(f"Error inserting {self.category_name}: {e}")
            return None


class CategoryGenerator:
    def __init__(self):
        # Danh sách categories chính (level 1)
        self.main_categories = [
            "Electronics",
            "Fashion",
            "Home & Garden",
            "Sports & Outdoors",
            "Books",
            "Toys & Games",
            "Health & Beauty",
            "Automotive",
            "Food & Beverages",
            "Office Supplies"
        ]

        # Danh sách sub-categories (level 2)
        self.sub_categories = {
            "Electronics": ["Smartphones", "Laptops", "Tablets", "Cameras", "Audio"],
            "Fashion": ["Men's Clothing", "Women's Clothing", "Shoes", "Accessories", "Jewelry"],
            "Home & Garden": ["Furniture", "Kitchen", "Bedding", "Garden Tools", "Decor"],
            "Sports & Outdoors": ["Fitness Equipment", "Camping", "Cycling", "Team Sports", "Water Sports"],
            "Books": ["Fiction", "Non-Fiction", "Comics", "Educational", "Children's Books"],
            "Toys & Games": ["Action Figures", "Board Games", "Puzzles", "Educational Toys", "Video Games"],
            "Health & Beauty": ["Skincare", "Makeup", "Hair Care", "Vitamins", "Personal Care"],
            "Automotive": ["Car Parts", "Accessories", "Tools", "Oils & Fluids", "Tires"],
            "Food & Beverages": ["Snacks", "Beverages", "Fresh Produce", "Canned Goods", "Frozen Foods"],
            "Office Supplies": ["Paper Products", "Writing Tools", "Office Equipment", "Storage", "Desk Accessories"]
        }

        self.parent_ids = {}
        self.level2_ids = []


    def gen_main_categories(self):
        """Tạo các categories chính (level 1)"""
        print("\n=== Generating Main Categories (Level 1) ===")
        for cat_name in self.main_categories:
            category = Category(cat_name, parent_category_id=None, level=1)
            cat_id = category.insert_category()
            if cat_id:
                self.parent_ids[cat_name] = cat_id

    def gen_sub_categories(self):
        """Tạo các sub-categories (level 2)"""
        print("\n=== Generating Sub Categories (Level 2) ===")
        for parent_name, subs in self.sub_categories.items():
            parent_id = self.parent_ids.get(parent_name)
            if parent_id:
                for sub_name in subs:
                    category = Category(sub_name, parent_category_id=parent_id, level=2)
                    cat_id = category.insert_category()
                    if cat_id:
                        self.level2_ids.append((cat_id, sub_name))

    def run(self):
        """Chạy toàn bộ quá trình"""
        print("Starting category generation...")

        # Sửa bảng (nếu cần)
        # self.alter_table()

        # Tạo categories theo từng level
        self.gen_main_categories()
        self.gen_sub_categories()

        print("\nDone!")


# Chạy chương trình
if __name__ == "__main__":
    generator = CategoryGenerator()
    generator.run()