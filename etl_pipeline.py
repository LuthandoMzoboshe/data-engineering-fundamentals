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



#TRANSFORMATION

# Mapping for standardising descriptions
DESCRIPTION_MAP = {
    "checkers - groceries": "Checkers - Groceries",
    "checkers - bread and milk": "Checkers - Groceries",
    "checkers groceries": "Checkers - Groceries",
    "checkers hyper": "Checkers",
    "uber trip": "Uber",
    "uber to sandton": "Uber",
    "uber eats": "Uber Eats",
    "netflix": "Netflix",
    "netflix subscription": "Netflix",
    "engen petrol": "Engen",
    "engen garage": "Engen",
    "takealot - headphones": "Takealot",
    "takealot - phone charger": "Takealot",
    "takealot - book": "Takealot",
    "takealot - mouse": "Takealot",
    "woolworths lunch": "Woolworths",
    "woolworths - dinner": "Woolworths",
    "capitec bank charges": "Capitec Bank Charges",
    "capitec interest": "Capitec Interest",
    "salary": "Salary",
    "salary bonus": "Salary Bonus",
    "spar - bread and snacks": "Spar",
    "virgin active membership": "Virgin Active",
    "nandos lunch": "Nandos",
    "shell petrol": "Shell",
    "pick n pay groceries": "Pick n Pay",
    "vodacom airtime": "Vodacom Airtime",
    "spotify subscription": "Spotify",
    "mcdonalds drive thru": "McDonalds",
    "total garage": "Total",
    "dis-chem vitamins": "Dis-Chem",
}

# Mapping for standardising categories based on keywords in descriptions
CATEGORY_RULES = {
    "checkers": "Groceries",
    "spar": "Groceries",
    "pick n pay": "Groceries",
    "woolworths": "Groceries",
    "uber": "Transport",
    "shell": "Transport",
    "engen": "Transport",
    "total": "Transport",
    "netflix": "Entertainment",
    "spotify": "Entertainment",
    "takealot": "Shopping",
    "nandos": "Food",
    "mcdonalds": "Food",
    "capitec": "Banking",
    "salary": "Income",
    "vodacom": "Utilities",
    "virgin active": "Health & Fitness",
    "dis-chem": "Health",
}

def standardise_description(description):
    """Standardise a description to a canonical form."""
    description_lower = description.strip().lower()
    return DESCRIPTION_MAP.get(description_lower, description.strip())

def infer_category(description, existing_category):
    """Infer a category fromthe description if one is not provided."""
    if existing_category and existing_category.strip():
        return existing_category.strip().title()
    
    description_lower = description.lower()
    for keyword, category in CATEGORY_RULES.items():
        if keyword in description_lower:
            return category

    return "Uncategorized"

def transform(transactions):
    """Cleans and Standardises the raw transaction data.
    Returns a list of cleaned dictionaries."""

    clean_data = []
    seen = set()
    duplicates_removed = 0
    missing_filled = 0

    for row in transactions:
        #Parse amount to flooat
        amount = float(row.get("amount"))

        #Determine transaction type
        transaction_type = "Income" if amount > 0 else "Expense"

        #Standardise description
        clean_description = standardise_description(row["description"])

        #Infer or standardise category
        original_category = row.get("category", "")
        clean_category = infer_category(clean_description, original_category)
        if not original_category.strip():
            missing_filled += 1


        clean_row = {
            "date": row["date"],
            "description": clean_description,
            "amount": amount,
            "category": clean_category,
            "transaction_type": transaction_type,
        
        }

        #Check for duplicates
        row_key = (clean_row["date"], clean_row["description"], clean_row["amount"])
        if row_key in seen:
            duplicates_removed += 1
            continue
        seen.add(row_key)

        clean_data.append(clean_row)


    print(f"[TRANSFORM] Missing categories filled: {missing_filled}")
    print(f"[TRANSFORM] Duplicates removed: {duplicates_removed}")
    print(f"[TRANSFORM] Clean rows remaining: {len(clean_data)}")

    return clean_data

























































                #MAIN

if __name__ == "__main__":
    print("=" * 50)
    print("Starting ETL pipeline...")
    print("=" * 50) 

                #Extract
    raw_data = extract(RAW_DATA_PATH)

    #Quick check to see if data was extracted correctly
    if raw_data:
        clean_data = transform(raw_data)
        print(f"\n Sample clean rows:")
        for row in clean_data[:3]:
            print(f" {row}")
    else: 
        print("[PIPELINE] No data to transform. Exiting.")

    
