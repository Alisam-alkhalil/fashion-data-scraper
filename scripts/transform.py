from typing import List, Dict

def transform(file: str, category: str, gender: str) -> List[Dict[str, str]]:
    """
    Transform the raw data from a CSV file into a structured format for processing.

    Args:
        file (str): The path to the CSV file to be transformed.
        category (str): The category of the products.
        gender (str): The gender for the products.

    Returns:
        List[Dict[str, str]]: A list of dictionaries where each dictionary contains product details (price, brand, category, gender).
    """
    data = []

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in range(1, len(lines)):

        item_details = {}

        if '£' in lines[line] and "£" not in lines[line+1] and "£" not in lines[line-1]:

            if 'From' not in lines[line-1]:
                item_details['price'] = lines[line].strip()
                item_details['brand'] = lines[line-2].strip()
                item_details['category'] = category
                item_details['gender'] = gender

            else:
                item_details['price'] = lines[line].strip()
                item_details['brand'] = lines[line-3].strip()
                item_details['category'] = category
                item_details['gender'] = gender
                    
        elif '£' in lines[line] and "£" in lines[line+1]:

            if 'From' not in lines[line-1]:
                item_details['price'] = lines[line+1].strip()
                item_details['brand'] = lines[line-2].strip()
                item_details['category'] = category
                item_details['gender'] = gender

            else:
                item_details['price'] = lines[line+1].strip()
                item_details['brand'] = lines[line-3].strip()
                item_details['category'] = category
                item_details['gender'] = gender
        
        if item_details:
            data.append(item_details)

    return data
