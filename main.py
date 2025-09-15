from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


product = input("Enter card name: ").replace(" ", "+")
grade = input("Enter card grade (e.g., 10): ")

eBay_url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={product}&_sop=12&LH_BIN=1&LH_Auction=0&Grade={grade}&Language=English&LH_FS=1"
tcg_url = f"https://www.tcgplayer.com/search/all/product?q={product}&view=grid"
eBay_item_list = []
tcg_item_list = []

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def scrape_eBay(driver, url):
    print(f"Navigating to eBay search for '{product}'...")
    driver.get(url)

    try:    
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "srp-river-results")))
        
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        eBay_item_list = soup.find_all("li", class_="s-card s-card--vertical")
        print(f"Found {len(eBay_item_list)} items.")

        if not eBay_item_list:
            print("No items found")
        else:
            for item in eBay_item_list:
                title = item.find("div", class_="s-card__title").text
                price = item.find("span", class_="su-styled-text primary bold large-1 s-card__price").text
                #link = item.find("a", class_="su-link").get("href")

                item_data = {
                    "title": title,
                    "price": price,
                    #"link": link
                }

                eBay_item_list.append(item_data)
                print(item_data)

    except Exception as e:
        print(f"Failed to load the page or find the results container. Error: {e}")

def scrape_tcg(driver, url):
    print(f"Navigating to TCGPlayer search for '{product}'...")
    driver.get(url)

    try:    
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card__product")))

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        tcg_item_list = soup.find_all("section", class_="product-card__product product-card__product-variant-a")
        print(f"Found {len(tcg_item_list)} items.")

        if not tcg_item_list:
            print("No items found")
        else:
            for item in tcg_item_list:
                title = item.find("span", class_="product-card__title truncate").text.strip()
                price = item.find("span", class_="inventory__price-with-shipping").text.strip()

                item_data = {
                    "title": title,
                    "price": price,
                }

                tcg_item_list.append(item_data)
                print(item_data)

    except Exception as e:
        print(f"Failed to load the page or find the results container. Error: {e}")
    finally:
        driver.quit()

scrape_eBay(driver, eBay_url)
scrape_tcg(driver, tcg_url)


