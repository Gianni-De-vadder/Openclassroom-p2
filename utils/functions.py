import requests
import bs4
from bs4 import BeautifulSoup
#from slugify import slugify
import csv


MAIN_URL = 'http://books.toscrape.com/'
#-------------------------------------------------------------------------------------------------------------
#								Récupération des catégories
def get_categories(area, what, url, search=None):
	"""Return list of categories urls"""
	mycategory = []
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")
	where = soup.find_all(area)
	for i in where:
			if area=='a' or area=="img":
				temp = MAIN_URL + (i[what])
				if search is None:
					mycategory.append(temp)	
				else:	
						resultat = temp.__contains__(search)	
						if resultat:
							mycategory.append(temp)			
			else:
				links = what
	mycategory.pop(0)			
	return(mycategory)

#-------------------------------------------------------------------------------------------------------------
#								Récupération des Livres de la catégorie
def get_books(resultlinks):
	books_urls = []
	for url in resultlinks:
		print(url)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		h3_elements = soup.find_all('h3')
		for h3 in h3_elements:
			book_url = MAIN_URL + 'catalogue/' + (h3.a["href"][9:])
			print(book_url)

		# print(area)
		# where = soup.find_all(area)
		# b = len(area)
		# y = 0
		# for y in range(b):
		# 	mybooks.append(area['title'])
		# 	y += 1

		# x += 1
		#print(mybooks)
		#return(mybooks)
		
if __name__ == '__main__':
	print('Execution du module fonction')
	resultlinks = get_categories('a' , 'href', 'http://books.toscrape.com/index.html','category')
	print(resultlinks)
		
		

		

						
#def Navigation(link):
#	for i in link:
#		test = Get_Links('a', 'title', i, '')
