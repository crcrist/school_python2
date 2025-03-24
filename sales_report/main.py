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
            # initializing values
            sale_date = None
            product = None
            price = None
            quantity = None
            region = None
            salesperson = None
            total_sale = None 

            if random.random() >= 0.03:
                days_range = (end_date - start_date).days
                random_days = random.randint(0, days_range)
                sale_date = start_date + timedelta(days=random_days)

            if random.random() >= 0.03:
                product = random.choice(list(PRODUCT_PRICES.keys()))
                price = PRODUCT_PRICES[product]

            if random.random() >= 0.03:
                quantity = random.randint(1,10)

            if random.random() >= 0.03:
                region = random.choice(REGIONS)

            if random.random() >= 0.03:
                salesperson = random.choice(SALES_PEOPLE)
            
            if price is not None and quantity is not None:
                total_sale = price * quantity 

            # format date as a stirng (YYYY-MM-DD)
            date_str = '' if sale_date is None else sale_date.strftime('%Y-%m-%d')
            product_str = '' if product is None else product
            price_str = '' if price is None else price
            quantity_str = '' if quantity is None else quantity
            region_str = '' if region is None else region
            salesperson_str = '' if salesperson is None else salesperson
            total_sale_str = '' if total_sale is None else total_sale

            # write record to CSV 
            csv_writer.writerow([date_str, product_str, price_str, quantity_str, region_str, salesperson_str, total_sale_str])


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


