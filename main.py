from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import lxml  # use if html.parser doesn't work
import requests

zillow_url = "https://appbrewery.github.io/Zillow-Clone/"


# Create Form
form_link = "https://docs.google.com/forms/d/e/1FAIpQLSdtyLUY1Iy78eboHiEYTI98LhBiMxMFklkDXBKBFLk8mJwUtQ/viewform?usp=sf_link"


# with beaufiful soup scrap the listings info

response = requests.get(zillow_url)
# Check if the request was successful
if response.status_code == 200:
    # Process the content (for example, print it or parse it with BeautifulSoup)
    content = response.text
    # print(content)
else:
    print(f"Failed to retrieve the URL: {response.status_code}")

soup = BeautifulSoup(content, "html.parser")
# print(soup.prettify())

all_listings = soup.find_all(class_="StyledPropertyCardDataWrapper")

links = []
addresses = []
costs = []

for listing in all_listings:
    # print(listing.div)
    links.append(listing.a['href'])
    addresses.append(listing.a.address.text.strip().replace("|", "").replace("  ", " "))
    unformatted_cost = listing.find(class_="StyledPropertyCardDataArea-fDSTNn").div.span.text
    costs.append("$"+unformatted_cost.strip("$+/mo"))


print(links)
print(addresses)
print(costs)
    # print(listing.div.div.article.div.div)

# # with selenium fill the Google forms
# # Keep Chrome open
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)
#
# # bridge between selenium and chrome
# driver = webdriver.Chrome(options=chrome_options)
#
# # driver.get(zillow_url)
