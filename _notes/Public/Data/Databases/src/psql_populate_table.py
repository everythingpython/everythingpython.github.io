import psycopg2
from faker import Faker
import random
from datetime import datetime

# Database connection settings
conn = psycopg2.connect(
    dbname="everythingpy",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432",
)
cur = conn.cursor()

fake = Faker()


def create_sales_table(end_goal, rows_to_insert):
    cur.execute("SELECT COUNT(*) FROM sales")
    count = cur.fetchone()[0]
    print(f"Total rows in sales table: {count}")
    count_begin = count
    while count <= end_goal:
        for _ in range(rows_to_insert):
            product_name = fake.word().capitalize()
            date_sold = fake.date_between(
                start_date="-1y", end_date="today"
            )  # Random date in the last 365 days
            cost_price = round(random.uniform(10, 1000), 2)
            markup = random.uniform(1.05, 1.5)
            selling_price = round(cost_price * markup, 2)
            profit = round(selling_price - cost_price, 2)
            sale_location = random.choice(
                ["Hyderabad", "Bangalore", "Chennai", "Mumbai", "Delhi"]
            )

            columns = "product_name, date_sold, cost_price, selling_price, profit, sale_location"

            cur.execute(f"""INSERT INTO sales ({columns}) VALUES ({product_name}, 
            {date_sold}, 
            {cost_price}, 
            {selling_price}, 
            {profit}, 
            {sale_location})""")

            conn.commit()
        cur.execute("SELECT COUNT(*) FROM sales")
        count = cur.fetchone()[0]
        print(f"Total rows in sales table: {count}")

        start_time = datetime.now()
        cur.execute("SELECT COUNT(*) FROM sales WHERE sale_location = 'Hyderabad'")
        hyderabad_sales_count = cur.fetchone()[0]
        print(f"Total sales in Hyderabad: {hyderabad_sales_count}")

        end_time = datetime.now()
        duration = end_time - start_time
        print(
            f"Time taken for query when count = {count}: {duration.total_seconds()} seconds"
        )
        cur.execute("""
            CREATE TABLE IF NOT EXISTS query_times (
                id SERIAL PRIMARY KEY,
                count INT,
                time_taken FLOAT
            )
        """)
        cur.execute(
            """
            INSERT INTO query_times (count, time_taken)
            VALUES (%s, %s)
        """,
            (count, duration.total_seconds()),
        )
    print(f"Inserted {count - count_begin} random rows into the sales table.")

    cur.close()
    conn.close()


rows_to_insert = 10000
end_goal = 1000001
create_sales_table(end_goal, rows_to_insert)
