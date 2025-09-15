from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


product = input("Enter card name: ").replace(" ", "+")
grade = input("Enter card grade (e.g., 10): ")

url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={product}&_sop=12&LH_BIN=1&LH_Auction=0&Grade={grade}&Language=English&LH_FS=1"
item_list = []
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

print(f"Navigating to eBay search for '{product}'...")
driver.get(url)

try:    
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "srp-river-results")))
    
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    item_list = soup.find_all("li", class_="s-card s-card--vertical")
    print(f"Found {len(item_list)} items.")

    if not item_list:
        print("No items found")
    else:
        for item in item_list:
            title = item.find("div", class_="s-card__title").text
            price = item.find("span", class_="su-styled-text primary bold large-1 s-card__price").text
            #link = item.find("a", class_="su-link").get("href")

            item_data = {
                "title": title,
                "price": price,
                #"link": link
            }

            item_list.append(item_data)
            print(item_data)

except Exception as e:
    print(f"Failed to load the page or find the results container. Error: {e}")
finally:
    driver.quit()
