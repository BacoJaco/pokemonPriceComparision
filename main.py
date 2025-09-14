from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#baseUrl = "https://www.ebay.com/sch/i.html"
url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=Zekrom&_sop=15&LH_BIN=1&LH_Auction=0&Grade=10&Language=English&LH_FS=1"

product = "Zekrom"


parameters = {
    "_from": "R40",
    "_nkw": product,
    "_sop": "15",  # Sort by price low -> high
    "LH_BIN": "1",
    "LH_Auction": "0",
    "Grade": "10",
    "Language": "English",
    "LH_FS": "1"
}



item_list = []
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

print(f"Navigating to eBay search for '{product}'...")
driver.get(url)

try:    
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "srp-river-results")))
    
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    # nextPage = soup.find("a", class_="pagination__next icon-link", type="next")

    # if not nextPage:
    #     print("nvcnvonvornv")

    # if nextPage and nextPage.get("aria-disabled"):
    #     print("No more pages")
    # else:
    #     item_list = soup.find_all("li", class_="s-card s-card--vertical")

    #     if not item_list:
    #         print("No items found")
    #     for item in item_list:
    #         title = item.find("div", class_="s-card__title").text
    #         price = item.find("span", class_="su-styled-text primary bold large-1 s-card__price").text
    #         #link = item.find("a", class_="su-link").get("href")

    #         item_data = {
    #             "title": title,
    #             "price": price,
    #             #"link": link
    #         }

    #         item_list.append(item_data)
    #         print(item_data)
except Exception as e:
    print(f"Failed to load the page or find the results container. Error: {e}")
finally:
    driver.quit()

