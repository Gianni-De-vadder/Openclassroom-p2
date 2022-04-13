import requests
import bs4
from bs4 import BeautifulSoup
url = 'http://books.toscrape.com'
page = requests.get(url)
links = []
  

def lien(area,what):
		soup = BeautifulSoup(page.text, "html.parser")
		where = soup.find_all(area)
		for i in where:
				links = 'http://books.toscrape.com/' + (i[what])
				print(links)
