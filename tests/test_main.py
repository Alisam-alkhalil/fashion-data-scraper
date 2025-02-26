from main import parse_filename

def test_parse_filename():
    """
    Test the parse_filename function to ensure it correctly parses the gender and category
    from a given filename.

    The test uses a sample filename 'raw_data_women_dresses.csv' and verifies that the
    function returns the tuple ('women', 'dresses') as expected.
    """

    file_name = 'raw_data_women_dresses.csv'
    assert parse_filename(file_name) == ('women', 'dresses')