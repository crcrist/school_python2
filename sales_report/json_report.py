import csv 
import json
import matplotlib.pyplot as plt
import os
import numpy as np

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
                        if date in sales_by_date:
                            sales_by_date[date] += amount
                        else:
                            sales_by_date[date] = amount
                        
                        if date in quantity_by_date:
                            quantity_by_date[date] += quantity
                        else:
                            quantity_by_date[date] = quantity
                            
                

                except ValueError as e:
                    print(f"Error processing row {row} : {e}")

        avg_sales = total_sales / sales_count if sales_count > 0 else 0 

        summary = {
                "total_sales": total_sales,
                "total_quantity": total_quantity,
                "average_sales": avg_sales,
                "sales_by_region": sales_by_region,
                "sales_by_item": sales_by_item,
                "quantity_by_region": quantity_by_region,
                "quantity_by_item": quantity_by_item,
                "sales_by_date": sales_by_date,
                "quantity_by_date": quantity_by_date
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


    regions = list(data['sales_by_region'].keys())
    sales = list(data['sales_by_region'].values())

    sort_indices = np.argsort(sales)
    
    sorted_regions = [regions[i] for i in sort_indices]
    sorted_sales = [sales[i] for i in sort_indices]

    plt.figure(figsize=(10,6))
    plt.bar(sorted_regions, sorted_sales)
    plt.title('Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Sales Amount')
    plt.savefig(f"{output_folder}/sales_by_region_bar.png")

    plt.figure(figsize=(8,8))
    plt.pie(sales, labels=regions, autopct='%1.1f%%')
    plt.title('Sales Distribution by Region')
    plt.savefig(f"{output_folder}/sales_by_region_pie.png")

    print(f"Visualizations saved to {output_folder}")

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
