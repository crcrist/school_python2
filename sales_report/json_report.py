import csv 
import json
import matplotlib.pyplot as plt
import os 

def process_sales_data(file_path):
    total_sales = 0
    sales_by_region = {}
    sales_count = 0

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                try: 
                    if not row['TotalSale'] or not row['Region']:
                        print(f"Warning: missing data in row {row}")
                        continue

                    amount = float(row['TotalSale'])
                    total_sales += amount
                    sales_count += 1

                    region = row['Region']
                    if region in sales_by_region:
                        sales_by_region[region] += amount
                    else:
                        sales_by_region[region] = amount

                except ValueError as e:
                    print(f"Error processing row {row} : {e}")

        avg_sales = total_sales / sales_count if sales_count > 0 else 0 

        summary = {
                "total_sales": total_sales,
                "average_sales": avg_sales,
                "sales_by_region": sales_by_region
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

    plt.figure(figsize=(10,6))
    plt.bar(regions, sales)
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
