from unicodedata import category
import requests
import bs4
from bs4 import BeautifulSoup
import csv
main_url = 'http://books.toscrape.com/'
links = []
url = '0'


def Get_Links(area, what, url, search):
		mycategory = []
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		where = soup.find_all(area)
		for i in where:
				print(where)
				if area=='a' or area=="img":
					temp = main_url + (i[what])
					if not search:
						resultat = temp.__contains__(search)
						if resultat:
							mycategory.append(temp)	
					else:
						mycategory.append(temp)						
				else:
					links = what
		return(mycategory)
						
def Navigation(link):
	for i in link:
		test = Get_Links('a', 'title', i, '')
