import csv 
import json
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from datetime import datetime

def process_sales_data(file_path):
    total_sales = 0
    sales_by_region = {}
    sales_count = 0
    sales_by_item = {}
    total_quantity = 0
    quantity_by_region = {}
    quantity_by_item = {}
    sales_by_date = {}
    quantity_by_date = {}
    customer_experience_counts = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0
    }

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                try: 
                    if row['TotalSale'] and row['Region'] and row['Quantity']:
                        amount = float(row['TotalSale'])
                        quantity = int(row['Quantity'])
                        total_sales += amount
                        total_quantity += quantity
                        sales_count += 1

                        region = row['Region']
                        if region in sales_by_region:
                            sales_by_region[region] += amount
                        else:
                            sales_by_region[region] = amount

                        if region in quantity_by_region:
                            quantity_by_region[region] += quantity 
                        else:
                            quantity_by_region[region] = quantity

                    if row['TotalSale'] and row['Product'] and row['Quantity']:
                        amount = float(row['TotalSale'])
                        quantity = int(row['Quantity'])

                        item = row['Product']
                        if item in sales_by_item:
                            sales_by_item[item] += amount
                        else:
                            sales_by_item[item] = amount

                        if item in quantity_by_item:
                            quantity_by_item[item] += quantity
                        else:
                            quantity_by_item[item] = quantity

                    if row['TotalSale'] and row['Quantity'] and row['Date']:
                        amount = float(row['TotalSale'])
                        quantity = int(row['Quantity'])

                        date = row['Date']
                        date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
                        if date in sales_by_date:
                            sales_by_date[date] += amount
                        else:
                            sales_by_date[date] = amount
                        
                        if date in quantity_by_date:
                            quantity_by_date[date] += quantity
                        else:
                            quantity_by_date[date] = quantity
                            
                    if row['CustomerExperience']:
                        try:
                            score = float(row['CustomerExperience'])
                            score_range = "1"
                            if score < 2:
                                score_range = "1"
                            elif score < 3:
                                score_range = "2"
                            elif score < 4:
                                score_range = "3"
                            elif score < 5:
                                score_range = "4"
                            else: 
                                score_range = "5"

                            customer_experience_counts[score_range] += 1
                        except ValueError:
                            pass

                except ValueError as e:
                    print(f"Error processing row {row} : {e}")

        avg_sales = total_sales / sales_count if sales_count > 0 else 0 

        summary = {
                "total_sales": round(total_sales, 2),
                "total_quantity": total_quantity,
                "average_sales": round(avg_sales, 2),
                "sales_by_region": {region: round(value, 2) for region, value in sorted(sales_by_region.items(), key=lambda item: item[1], reverse=True)},
                "sales_by_item": {item: round(value, 2) for item, value in sorted(sales_by_item.items(), key=lambda item: item[1], reverse=True)},
                "quantity_by_region": dict(sorted(quantity_by_region.items(), key=lambda item: item[1], reverse=True)),
                "quantity_by_item": dict(sorted(quantity_by_item.items(), key=lambda item: item[1], reverse=True)),
                "sales_by_date": {date: round(value, 2) for date, value in sorted(sales_by_date.items())},
                "quantity_by_date": dict(sorted(quantity_by_date.items())),
                "customer_experience_counts": customer_experience_counts
        }

        return summary

    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def save_json_report(data, output_file):
    try:
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON report saved to {output_file}")
        return True
    except Exception as e: 
        print(f"Error saving JSON report: {e}")
        return False

def create_visualizations(data, output_folder):
    data_dir = output_folder
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # aggregate sales by regions 
    regions = list(data['sales_by_region'].keys())
    sales = list(data['sales_by_region'].values())

    sort_indices = np.argsort(sales)
    
    sorted_regions = [regions[i] for i in sort_indices]
    sorted_sales = [sales[i] for i in sort_indices]

    # bar chart
    plt.figure(figsize=(10,6))
    plt.bar(sorted_regions, sorted_sales)
    plt.title('Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Sales Amount')
    plt.savefig(f"{output_folder}/sales_by_region_bar.png")

    # quantity by items sort
    items = list(data['quantity_by_item'].keys())
    quantity = list(data['quantity_by_item'].values())

    sort_indices = np.argsort(quantity)
    
    sorted_items = [items[i] for i in sort_indices]
    sorted_quantity = [quantity[i] for i in sort_indices]

    # bar chart
    plt.figure(figsize=(10,8))
    plt.barh(sorted_items, sorted_quantity)
    plt.title('Quantity by Item')
    plt.ylabel('Item')
    plt.xlabel('Quantity')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/quantity_by_item_bar.png")

    # customer experience bar
    scores = list(data['customer_experience_counts'].keys())
    counts = list(data['customer_experience_counts'].values())

    plt.figure(figsize=(8,6))
    plt.bar(scores, counts, color = 'skyblue')
    plt.title('Transaaction Count by Customer Experience Score')
    plt.xlabel('Customer Experience Score')
    plt.ylabel('Number of Transactions')
    plt.xticks(scores)

    for i, count in enumerate(counts):
        plt.text(scores[i], count + 0.1, str(count), ha='center')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f"{output_folder}/customer_experience_bar.png")


    # donut chart
    top_n = 5
    plt.figure(figsize=(8,8))
    plt.pie(sorted_quantity[-top_n:],
            labels=sorted_items[-top_n:], 
            autopct='%.1f%%',
            wedgeprops=dict(width=0.5))
    plt.title('Quantity Distribution by Top 5 Items')
    plt.savefig(f"{output_folder}/quantity_by_item_pie.png")

    print(f"Visualizations saved to {output_folder}")

    # line chart
    date = list(data['sales_by_date'].keys())
    sales = list(data['sales_by_date'].values())
    
    plt.figure(figsize=(10,6))
    plt.plot(date, sales, marker = 'o', linewidth = 2)

    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Sales by Date')

    plt.xticks(rotation=45)

    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()

    plt.savefig(f"{output_folder}/sales_by_date_line.png")

def main():
    input_file = "sales_data.csv"
    output_file = "sales_report.json"
    output_folder = "visualizations"

    sales_data = process_sales_data(input_file)
    if sales_data:
        save_json_report(sales_data, output_file)

        create_visualizations(sales_data, output_folder)
    else:
        print("failed to process sales data")
if __name__ == "__main__":
    main()
