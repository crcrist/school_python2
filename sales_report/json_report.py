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
                            
                

                except ValueError as e:
                    print(f"Error processing row {row} : {e}")

        avg_sales = total_sales / sales_count if sales_count > 0 else 0 

        summary = {
                "total_sales": total_sales,
                "total_quantity": total_quantity,
                "average_sales": avg_sales,
                "sales_by_region": dict(sorted(sales_by_region.items(), key=lambda item: item[1], reverse=True)),
                "sales_by_item": dict(sorted(sales_by_item.items(), key=lambda item: item[1], reverse=True)),
                "quantity_by_region": dict(sorted(quantity_by_region.items(), key=lambda item: item[1], reverse=True)),
                "quantity_by_item": dict(sorted(quantity_by_item.items(), key=lambda item: item[1], reverse=True)),
                "sales_by_date": dict(sorted(sales_by_date.items())),
                "quantity_by_date": dict(sorted(quantity_by_date.items()))
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

    # pie chart
    plt.figure(figsize=(8,8))
    plt.pie(sales, labels=regions, autopct='%1.1f%%')
    plt.title('Sales Distribution by Region')
    plt.savefig(f"{output_folder}/sales_by_region_pie.png")


    # quantity by items visual 
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

    # scatter plot
    df = pd.read_csv("sales_data.csv")
    
    regions = df['Region'].tolist()
    sales = df['Quantity'].tolist()
    customer_exp = df['CustomerExperience'].tolist() 
    
    plt.figure(figsize=(10,6))
    
    unique_regions = list(df['Region'].unique())
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_regions)))
    color_dict = dict(zip(unique_regions, colors))

    # create emptly handles and lables for the legend
    handles = []
    labels = []
    
    # plot each region with the appropriate color
    for region in unique_regions:
        # filter data for the region
        region_data = df[df['Region'] == region]

        # create scatterplot for the region
        scatter = plt.scatter(
            region_data['Quantity'],
            region_data['CustomerExperience'],
            color=color_dict[region],
            label=region,
            alpha=0.7,
            s=100
        )

        handles.append(scatter)
        labels.append(region) 

    plt.xlabel('Quantity')
    plt.ylabel('Customer Experience Rating')
    plt.title('Sales vs Customer Experience by Region')

    plt.legend(handles, labels)

    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(f"{output_folder}/sales_vs_experience_scatter.png")


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
