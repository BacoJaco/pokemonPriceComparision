from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=Mozilla/5.0...')


def scrape_eBay(driver, url):
    results = []

    print(f"Navigating to eBay search for '{product}'...")
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "srp-river-results")))
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        item_elements = soup.find_all("div", class_="su-card-container su-card-container--vertical")
        print(f"Found {len(item_elements)} items on eBay.")

        if not item_elements:
            print("No items found on eBay")
        else:
            for item in item_elements:
                title = item.find("span", class_="su-styled-text primary default")
                price = item.find("span", class_="su-styled-text primary bold large-1 s-card__price")
                
                if title and price:
                    title = title.text
                    price = price.text
                    
                    item_data = {
                        "title": title,
                        "price": price
                    }
                    results.append(item_data)

        return results
    except Exception as e:
        print(f"Failed to scrape eBay. Error: {e}")
        return []

def scrape_tcg(driver, url):
    results = []
    
    print(f"Navigating to TCGPlayer search for '{product}'...")
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        item_elements = soup.find_all("section", class_="product-card__product product-card__product-variant-a")
        print(f"Found {len(item_elements)} items on TCGPlayer.")

        if not item_elements:
            print("No items found on TCGPlayer")
        else:
            for item in item_elements:
                title = item.find("span", class_="product-card__title truncate")
                price = item.find("span", class_="inventory__price-with-shipping")

                if title and price:
                    title = title.text
                    price = price.text
                    
                    item_data = {
                        "title": title,
                        "price": price
                    }
                    results.append(item_data)

        return results
    except Exception as e:
        print(f"Failed to scrape TCGPlayer. Error: {e}")
        return []

product = input("Enter card name: ").replace(" ", "+")
grade = input("Enter card grade (put '00' for raw): ")

eBay_url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={product}&_sop=12&LH_BIN=1&LH_Auction=0&Grade={grade}&Language=English&LH_FS=1"
tcg_url = f"https://www.tcgplayer.com/search/all/product?q={product}&view=grid"

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

try:
    eBay_list = scrape_eBay(driver, eBay_url)
    tcg_list = scrape_tcg(driver, tcg_url)

    print("\neBay Items:")
    if eBay_list:
        for item in eBay_list[:10]:
            print(item.get("title"), "-", item.get("price"))
    else:
        print("Could not retrieve eBay listings.")

    print("\nTCGPlayer Items:")
    if tcg_list:
        for item in tcg_list[:10]:
            print(item.get("title"), "-", item.get("price"))
    else:
        print("Could not retrieve TCGPlayer listings.")

finally:
    driver.quit()