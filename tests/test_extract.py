import pytest
from scripts.extract import get_gender_and_category

def test_get_gender_and_category():
    """
    Test that get_gender_and_category() correctly extracts gender and category
    from a given URL.

    URL: https://www.example.co.uk/womens-clothing-jeans/?p=
    Expected gender: "womens"
    Expected category: "jeans"
    """
    url = 'https://www.example.co.uk/womens-clothing-jeans/?p='
    gender, category = get_gender_and_category(url)

    assert gender == "womens"
    assert category == "jeans"

