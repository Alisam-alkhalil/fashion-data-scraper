import os
from scripts.transform import transform
from scripts.extract import extract
from scripts.load import load, overwrite_csv
from scripts.dbt_models import run_dbt_models
from config.urls import list_of_urls
import csv

RAW_DATA_FOLDER = "csv_files/"

def main() -> None:
    """
    Main function that orchestrates the process of extracting data from URLs,
    transforming it, and loading it into a database.
    
    Iterates through CSV files in the RAW_DATA_FOLDER, parses their filenames,
    applies transformation, loads the resulting data and deletes the CSV file. It then runs dbt models
    to create the final_prices table which gives the final price of each product to sell in-store.
    """
    extract(list_of_urls)

    for file in os.listdir(RAW_DATA_FOLDER):
        file_path = os.path.join(RAW_DATA_FOLDER, file)
        
        if file.endswith('.csv'):

            gender, category = parse_filename(file)

            transformed_data = transform(file_path, category, gender)

            overwrite_csv(file_path, transformed_data)

            load(file_path)

            os.remove(file_path)

    run_dbt_models()
def parse_filename(filename: str) -> tuple[str, str]:
    """
    Parse a filename of the form "raw_data_<gender>_<category>.csv" into
    its constituent parts.

    Args:
        filename (str): Filename to parse

    Returns:
        tuple[str, str]: A tuple containing gender and category if successful,
                         or (None, None) if an error occurs.
    """
    try:
        parts = filename.split('_')
        gender = parts[-2]
        category = parts[-1].replace('.csv', '')  
        return gender, category
    except Exception as e:
        print(f"Error parsing filename {filename}: {e}")
        return None, None

if __name__ == "__main__":
    main()
