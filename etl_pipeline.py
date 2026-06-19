import csv
import os

#CONFIGURATION

RAW_DATA_PATH = os.path.join("data", "raw_transactions.csv")


#EXTRACTION

def extract(file_path):

    transactions = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
        print(f"[EXTRACT] Successfully read  {len(transactions)} rows from{file_path}")

    except FileNotFoundError:
        print(f"[EXTRACT] Error: File not found: {file_path}")
    except Exception as e:
        print(f"[EXTRACT] An error occurred: {e}")

    return transactions

                #MAIN

if __name__ == "__main__":
    print("=" * 50)
    print("Starting ETL pipeline...")
    print("=" * 50) 

                #Extract
    raw_data = extract(RAW_DATA_PATH)

    #Quick check to see if data was extracted correctly
    if raw_data:
        print(f"\nFirst row: {raw_data[0]}")
        print(f"Last row: {raw_data[-1]}")

    
