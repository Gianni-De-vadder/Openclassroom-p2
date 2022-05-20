from asyncore import write
from sys import exit
import requests
import bs4
from bs4 import BeautifulSoup
#from slugify import slugify
import csv
import urllib.request


MAIN_URL = 'http://books.toscrape.com/'

def get_soup(url):
	response = requests.get(url)
	if not response.ok:
		print(f"Un problème est survenu durant la requete avec l'url : {url}")
		exit()

	soup = BeautifulSoup(response.text, "html.parser")
	return soup	
	
#-------------------------------------------------------------------------------------------------------------
#								Récupération des catégories
def get_categories(area, what, url, search=None):
	"""Return list of categories urls"""
	categories = []
	soup = get_soup(url)
	where = soup.find_all(area)
	for i in where:
		if area=='a' or area=="img":
			temp = MAIN_URL + (i[what])
			if search is None:
				categories.append(temp)	
			else:	
				resultat = temp.__contains__(search)	
				if resultat:
					categories.append(temp)			
		else:
			links = what
	categories.pop(0)			
	return(categories)

#-------------------------------------------------------------------------------------------------------------
#								Récupération des Livres de la catégorie
def get_books_urls(url_category):
	books_urls = []
	is_nextpage = True
	next_url = url_category

	while is_nextpage:	
		#for url in url_category:
		print(url_category)
		page = get_soup(next_url)
		h3_elements = page.find_all('h3')
		for h3 in h3_elements:
			book_url = MAIN_URL + 'catalogue/' + (h3.a["href"][9:])
			books_urls.append(book_url)	
		
		btn_next = page.find("li", {"class": "next"})
		if btn_next:
			url_btn_next = btn_next.a['href']
			next_url = url_category.replace('index.html', url_btn_next)
			print(next_url)
		else:
			is_nextpage = False	

	return books_urls

	

def get_book_datas(book_url):
	"""Return a dict with data book """
	url = book_url

	product_informations = { "product_page_url": url }

	response = requests.get(product_informations["product_page_url"])

	soup = BeautifulSoup(response.text, 'html.parser')

	# Récupérer universal_product_code / price_excluding_taxe / price_including_tax
	
	informations = soup.findAll("tr")

	for information in informations:
		information_label = information.find('th').text
		information_value = information.find('td').text

		target_dict = False

		if (information_label == "UPC"):
			target_dict = "universal_product_code"
		elif (information_label == "Price (excl. tax)"):
			target_dict = "price_excluding_tax"
		elif (information_label == "Price (incl. tax)"):
			target_dict = "price_including_tax"

		if target_dict:
			if "Â" in information_value:
				information_value = information_value.replace("Â", "")

			product_informations[target_dict] = information_value

		# Récupérer image_url (id product_gallery)
		product_gallery = soup.find("div", {"id": "product_gallery"})
		product_informations["image_url"] = "http://books.toscrape.com/" + \
			product_gallery.find('img')["src"].replace('../../', '')

# Récupérer category (breadcrumbs : dernier li avant class active)
		breadcrumb = soup.find('ul', {"class": "breadcrumb"})
		links = breadcrumb.select('li:not(.active)')
		product_informations["category"] = links[len(links) - 1].text.strip()

# Récupérer title (titre H1)
		product_informations['title'] = soup.find('h1').text

# Récupérer description (id product_description +  p)
		description = soup.find('div', {"id": 'product_description'})

		if description:
			product_informations["product_description"] = description.findNext('p').text

# Récupérer review_rating (class star-rating + class indiquant le nombre d'étoile)
		review_rating = soup.find('p', {"class": "star-rating"})
		if review_rating.has_attr('class'):
			review_rating = review_rating["class"][1]

		if review_rating == "One":
			review_rating = 1
		elif review_rating == "Two":
			review_rating = 2
		elif review_rating == "Three":
			review_rating = 3
		elif review_rating == "Four":
			review_rating = 4
		elif review_rating == "Five":
			review_rating = 5
		else:
			review_rating = 0
	
	else:
		review_rating = 0

	product_informations['review_rating'] = review_rating

# Récupérer number_available (instock outofstock en dessous du prix du produit)
	availability = soup.select('p.availability.instock')

	if availability:
		availability = availability[0].text
		availability = availability.replace('In stock (', '')
		availability = availability.replace(' available)', '')
		availability = int(availability)

		product_informations["number_available"] = availability
	else:
		product_informations["number_available"] = 0

	return product_informations



#if __name__ == "__main__":
#csv.DictWriter


# with open(monfichier.jpg, wb) as f:
# 		write(datas)
