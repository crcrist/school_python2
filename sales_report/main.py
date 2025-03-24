import csv
import random
from datetime import datetime, timedelta


REGIONS = ['North', 'South', 'East', 'West', 'Central']

PRODUCT_PRICES = {
        'Headphones': 19.99, 
        'Keyboard': 40.00, 
        'Mouse': 15.99, 
        'Monitor': 119.99,
        'Laptop': 499.99,
        'Monster': 3.99,
        'Charger': 9.99,
        'Marker': 2.99,
        'CPU': 399.99,
        'GPU': 1499.99,
        'Motherboard': 299.99,
        'RAM': 129.99,
        'Harddrive': 49.99,
        'SSD': 39.99
    }

SALES_PEOPLE = ('John Smith', 'Jane Doh', 'Robert Johnson', 'Lisa Chen', 'Miguel Rodriguez')

CUSTOMER_EXPERIENCE_RATING = ['Bad', 'Under Expectations', 'Satisfactory', 'Exceeded Expectations', 'Excellent']


def generate_sales_data(row_count, start_date, end_date, output_file):
    
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)    

        header = ['Date', 'Product', 'Price', 'Quantity', 'Region', 'Salesperson',  'TotalSale']
        csv_writer.writerow(header)

        for _ in range(row_count):
            # generate random start and end date
            days_range = (end_date - start_date).days
            random_days = random.randint(0, days_range)
            sale_date = start_date + timedelta(days = random_days)

            # select random product and get its price
            product = random.choice(list(PRODUCT_PRICES.keys()))
            price = PRODUCT_PRICES[product]

            # generate random quantity
            quantity = random.randint(1,10)

            # select random region and sales person
            region = random.choice(REGIONS)
            salesperson = random.choice(SALES_PEOPLE)
            
            # calculate total sale
            total_sale = price * quantity 

            # format date as a stirng (YYYY-MM-DD)
            date_str = sale_date.strftime('%Y-%m-%d')
        
            # write record to CSV 
            csv_writer.writerow([date_str, product, price, quantity, region, salesperson, total_sale])


    print(f"Generated {row_count} sales records in {output_file}")


if __name__ == "__main__":
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    generate_sales_data(
        row_count = 1000,
        start_date = start_date,
        end_date = end_date,
        output_file = "sales_data.csv"
    )


