import os
from scripts.transform import transform
from scripts.extract import extract
from scripts.load import load
from config.urls import list_of_urls

RAW_DATA_FOLDER = "csv_files/"

def main() -> None:
    """
    Main function that orchestrates the process of extracting data from URLs,
    transforming it, and loading it into a database.
    
    Iterates through CSV files in the RAW_DATA_FOLDER, parses their filenames,
    applies transformation, and loads the resulting data.
    """
    extract(list_of_urls)

    for file in os.listdir(RAW_DATA_FOLDER):
        file_path = os.path.join(RAW_DATA_FOLDER, file)
        
        if file.endswith('.csv'):

            gender, category = parse_filename(file)

            transformed_data = transform(file_path, category, gender)

            load(transformed_data)

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
