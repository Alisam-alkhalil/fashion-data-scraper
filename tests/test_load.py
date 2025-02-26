import pytest
from unittest.mock import patch, MagicMock
import os
import csv
from scripts.load import load  

@pytest.fixture
def mock_snowflake_connection():

    """
    Mock a Snowflake connection for testing.

    This fixture uses the `patch` context manager from `unittest.mock` to replace
    the `connect` method of the `snowflake.connector` module. It returns a
    `MagicMock` object that stands in for the connection object, and another
    `MagicMock` that stands in for the cursor object.

    This allows us to test the `load` function without actually connecting to
    Snowflake.

    Yields:
        tuple: A tuple of two `MagicMock` objects, the first of which is the
            connection object and the second of which is the cursor object.
    """

    with patch('snowflake.connector.connect') as mock_connect:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        yield mock_connection, mock_cursor

def mock_csv_file():
    """
    Creates a mock CSV file for testing the load function.

    The CSV file contains five products with various prices and attributes.
    The file is created in the 'tests' directory and the full path is returned.

    Returns:
        str: Full path to the created CSV file.
    """

    csv_data = [
        {'price':'51.99','brand':'Oxmo','category':'dresses','gender':'womens'},
        {'price':'51.99','brand':'Oxmo','category':'dresses','gender':'womens'},
        {'price':'56.99','brand':'Oxmo','category':'dresses','gender':'womens'},
        {'price':'54.99','brand':'WAL G.','category':'dresses','gender':'womens'},
        {'price':'35.99','brand':'Zign Studio','category':'dresses','gender':'womens'}
    ]

    with open('tests/test_data.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)

    return 'tests/test_data.csv'

def normalize_query(query):
    """Normalize a SQL query by removing extra whitespace for comparison."""
    return ' '.join(query.lower().split())

def test_load(mock_snowflake_connection):
    """
    Test the load function by mocking a Snowflake connection and checking the SQL queries
    that are executed. The load function should create a table and a stage, copy the file into
    the stage, and then copy the data from the stage into the table.

    The test uses the `normalize_query` function to remove extra whitespace from the queries
    for comparison.
    """

    mock_connection, mock_cursor = mock_snowflake_connection

    test_file = mock_csv_file()

    with patch('os.path.basename', return_value='test_data.csv'):
        
        load(test_file)
        
        calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        
        assert any('create table if not exists products' in normalize_query(call) for call in calls), \
            "Table creation query not found"
        
        assert any('create stage if not exists products' in normalize_query(call) for call in calls), \
            "Stage creation query not found"
            
        assert any(f"put file://{test_file.lower()} @products" in normalize_query(call) for call in calls), \
            "PUT command not found"
            
        assert any("copy into products" in normalize_query(call) and "test_data.csv" in normalize_query(call) for call in calls), \
            "COPY INTO command not found"
        
        mock_connection.commit.assert_called_once()
        
        mock_connection.close.assert_called_once()

        os.remove(test_file)