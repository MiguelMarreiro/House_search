from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import lxml  # use if html.parser doesn't work
import requests
import time

zillow_url = 'https://www.zillow.com/san-francisco-ca/rent-houses-1-bedrooms/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417331103516%2C%22east%22%3A-122.23248568896484%2C%22south%22%3A37.66992586293845%2C%22north%22%3A37.8805080917795%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3A1%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A600394%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22usersSearchTerm%22%3A%22San%20Francisco%20CA%22%7D'
# zillow_url = "https://appbrewery.github.io/Zillow-Clone/"
form_link = "https://forms.gle/JjHEcvFAFowWUMxS7"

######################### with beaufiful soup scrap the listings info
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(zillow_url, headers=header)
# Check if the request was successful
if response.status_code == 200:
    # Process the content (for example, print it or parse it with BeautifulSoup)
    content = response.text
    # print(content)
else:
    print(f"Failed to retrieve the URL: {response.status_code}")

soup = BeautifulSoup(content, "html.parser")
print(soup.prettify())

all_listings = soup.find_all(class_="StyledPropertyCardDataWrapper-c11n-8-102-0__sc-hfbvv9-0 cXubMK property-card-data")

links = []
addresses = []
costs = []

for listing in all_listings:
    # print(listing.div)
    links.append(listing.a['href'])
    addresses.append(listing.a.address.text.strip().replace("|", "").replace("  ", " "))
    unformatted_cost = listing.find(class_="StyledPropertyCardDataArea-c11n-8-102-0__sc-10i1r6-0 gHLzem").div.span.text
    costs.append("$"+unformatted_cost.strip("$+/mo").split("+")[0])


print(links)
print(addresses)
print(costs)


################################### with selenium fill the Google forms
# Keep Chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


# bridge between selenium and chrome
driver = webdriver.Chrome(options=chrome_options)
driver.get(form_link)

for index in range(len(links)):
    time.sleep(2)
    # Fill form
    address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    cost_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address_input.send_keys(addresses[index])
    cost_input.send_keys(costs[index])
    link_input.send_keys(links[index])

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Enviar')]"))).click()

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Enviar outra resposta"))).click()

# //*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span