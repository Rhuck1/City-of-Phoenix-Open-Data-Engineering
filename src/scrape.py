from bs4 import BeautifulSoup
import requests
from helper_functions import url_scraper


# URL for City of Phoenix city checkbook
url = 'https://www.phoenixopendata.com/dataset/city-checkbook'

# establishing API connection
response = requests.get(url)

# checking connection status
if response.status_code == 200:
    print('Connection established')
else:
    print('There is a problem with the connection')
    
# Scraping with BeautifulSoup    
page_html = response.text

page_soup = BeautifulSoup(page_html, 'html.parser')

web_scrapings = url_scraper(page_soup)

print(web_scrapings)