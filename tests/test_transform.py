import os
import pytest
from scripts.transform import transform
import csv

def mock_csv():
    """Creates a mock CSV file with product data for testing purposes.

    The CSV file contains eight products with various prices and attributes.
    The file is created in the 'tests' directory and the full path is returned.

    Returns:
        str: Full path to the created CSV file.
    """
    csv_data = '''
    Oxmo
    OXELLA - Jumper dress - black
    From
    £24.99
    £51.99
    up to -19%
    heart_outlined
    Sponsored
    Oxmo
    OXELLA - Jumper dress - grey mel
    From
    £41.99
    £51.99
    heart_outlined
    Sponsored
    Oxmo
    OXOMILA - Day dress - insignia blue
    £56.99
    New
    heart_outlined
    WAL G.
    JULIA TULIP HIGH NECK MAXI - Cocktail dress / Party dress - forest green
    £54.99
    Long-distance delivery
    New
    heart_outlined
    Zign Studio
    Denim dress - dark blue denim
    £35.99
    '''

    with open('tests/test.csv', 'w', encoding='utf-8', newline='') as f:	
        f.write(csv_data)

    return os.path.abspath('tests/test.csv')

def test_transform():
    """
    Test the transform function for correctly parsing and transforming CSV data.

    This test verifies that the transform function accurately processes a mock CSV file 
    containing product details, extracting the price, brand, category, and gender 
    information into a structured list of dictionaries. The test checks that the 
    transformation aligns with expected output for the given input data.

    Steps:
    1. Create a mock CSV file with product data.
    2. Use the transform function to process the CSV file.
    3. Assert that the transformed data matches the expected output.
    4. Remove the mock CSV file after the test is complete.
    """

    csv_file = mock_csv()
    transformed = transform(csv_file, 'dresses', 'womens')


    assert transformed == [{'price':'51.99','brand':'Oxmo','category':'dresses','gender':'womens'},
    {'price':'51.99','brand':'Oxmo','category':'dresses','gender':'womens'},
    {'price':'56.99','brand':'Oxmo','category':'dresses','gender':'womens'},
    {'price':'54.99','brand':'WAL G.','category':'dresses','gender':'womens'},
    {'price':'35.99','brand':'Zign Studio','category':'dresses','gender':'womens'}]

    os.remove(csv_file)

