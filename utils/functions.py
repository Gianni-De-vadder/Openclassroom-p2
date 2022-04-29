from operator import le
from re import M
import re
from unicodedata import category
import requests
import bs4
from bs4 import BeautifulSoup
import csv
main_url = 'http://books.toscrape.com/'
links = []
url = '0'
#-------------------------------------------------------------------------------------------------------------
#								Récupération des catégories
def Get_Category(area, what, url, search):
		mycategory = []
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		where = soup.find_all(area)
		for i in where:
				if area=='a' or area=="img":
					temp = main_url + (i[what])
					if not search:
						mycategory.append(temp)	
					else:	
							resultat = temp.__contains__(search)	
							if resultat:
								mycategory.append(temp)			
				else:
					links = what
		return(mycategory)

#-------------------------------------------------------------------------------------------------------------
#								Récupération des Livres de la catégorie
def Get_Books(resultlinks):
	mybooks = []
	i = len(resultlinks)
	x = 0
	for x in range(i):
		url = resultlinks[3]
		print(url)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		area = soup.find_all('a')
		print(area)
		where = soup.find_all(area)
		b = len(area)
		y = 0
		for y in range(b):
			mybooks.append(area['title'])
			y += 1

		x += 1
		print(mybooks)
		print(mybooks)
		return(mybooks)
		
		
		
		

		

						
#def Navigation(link):
#	for i in link:
#		test = Get_Links('a', 'title', i, '')
