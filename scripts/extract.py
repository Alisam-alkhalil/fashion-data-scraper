import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_gender_and_category(url: str) -> tuple[str, str | None]:
    """
    Extract gender and category information from the provided URL.

    Args:
        url (str): The URL of the page to extract gender and category information from.

    Returns:
        tuple[str, str | None]: A tuple containing the gender and category if found,
                                 or (None, None) if an error occurs or the information is not found.
    """
    split_url = url.split('/')
    split_end = split_url[-2].split('-')

    try:
        split_end.remove('clothing')
    except ValueError:
        pass

    if 'womens' in split_end or 'women' in split_end:
        try:
            split_end.remove('womens')
        except ValueError:
            split_end.remove('women')
        gender = 'womens'
        category = ''.join(split_end)

    elif 'mens' in split_end or 'men' in split_end:
        try:
            split_end.remove('mens')
        except ValueError:
            split_end.remove('men')
        gender = 'mens'
        category = ''.join(split_end)
        
    else:
        print(f"Error: Gender not found in URL: {url}")
        return None, None

    return gender, category

def extract(list_of_urls: list[str]) -> None:
    """
    Extract data from each URL in the list and save it to CSV files.

    Args:
        list_of_urls (list[str]): A list of URLs to scrape data from.

    Returns:
        None
    """
    for url in list_of_urls:
        page_number = 1
        gender, category = get_gender_and_category(url)

        if not gender or not category:
            continue 

        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--user-agent=Mozilla/5.0") 
        driver = webdriver.Chrome(options=options)

        with open(f"csv_files/raw_data_{gender}_{category}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)

            
            try:
                for x in range(1):
                    url_with_page = f"{url}{page_number}"
                    driver.get(url_with_page)

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    time.sleep(1)

                    all_text = driver.find_element("tag name", "body").text

                    if f'Page {page_number} of ' in all_text:
                        writer.writerow([all_text])
                        print(f"Page {page_number} data saved to 'raw_data_{gender}_{category}.csv'")
                        page_number += 1
                    else:
                        print(f"End of {gender} {category} pages.")
                        break



            except Exception as e:
                print(f"An error occurred while processing {url_with_page}: {e}")
                break

            finally:
                driver.quit()
