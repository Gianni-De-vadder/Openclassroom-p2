from os import mkdir
from sys import exit
import requests
import bs4
from bs4 import BeautifulSoup
from slugify import slugify
import csv
from pathlib import Path
from rich.console import Console
from rich.table import Table

MAIN_URL = 'http://books.toscrape.com/'
DATA_DIR = "data/"


def get_soup(url):
	"""
	It takes a url as an argument, makes a request to that url, and returns a BeautifulSoup object
	
	:param url: The URL of the page you want to scrape
	:return: A soup object
	"""
	response = requests.get(url)
	if not response.ok:
		print(f"Un problème est survenu durant la requete avec l'url : {url}")
		exit()

	soup = BeautifulSoup(response.content, "html.parser")
	return soup	


#								Récupération des catégories
def get_categories(area, what, url, search=None):
	"""
	It takes a url, and returns a list of all the links on that page
	
	:param area: the area where the links are located
	:param what: the attribute of the tag you want to get
	:param url: the url of the page you want to scrape
	:param search: is the search term you want to use to filter the results
	:return: A list of categories
	"""
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
	return categories

def get_categorie_name(url: str) -> str:
    # Extract the last part of the url containing the category name beginning at 51
    categorie_name = url[51:]
    # Find the position of the "_" char
    under_position = categorie_name.index("_")
    categorie_name = categorie_name[:under_position]

    return categorie_name


#								Récupération des Livres de la catégorie
def get_books_urls(url_category):
	"""
	It takes a url as an argument, and returns a list of urls for each book in that category
	
	:param url_category: the url of the category page
	:return: A list of urls for each book in the category.
	"""
	books_urls = []
	is_nextpage = True
	next_url = url_category

	while is_nextpage:	
		#for url in url_category:
		page = get_soup(next_url)
		h3_elements = page.find_all('h3')
		for h3 in h3_elements:
			book_url = MAIN_URL + 'catalogue/' + (h3.a["href"][9:])
			books_urls.append(book_url)	
		
		btn_next = page.find("li", {"class": "next"})
		if btn_next:
			url_btn_next = btn_next.a['href']
			next_url = url_category.replace('index.html', url_btn_next)
			
		else:
			is_nextpage = False	

	return books_urls


def get_book_datas(book_url):
	"""
	It takes a URL, scrapes the page, and returns a dictionary of the data
	
	:param book_url: The URL of the book page
	:return: A dictionary with the data of the book.
	"""

	soup = get_soup(book_url)
 
	tds = soup.find_all("td")
 
	title = soup.find('h1').text
	
	product_gallery = soup.find("div", {"id": "product_gallery"})
	image_url = "http://books.toscrape.com/" + \
	product_gallery.find('img')["src"].replace('../../', '')

# Récupérer category (breadcrumbs : dernier li avant class active)
	breadcrumb = soup.find('ul', {"class": "breadcrumb"})
	links = breadcrumb.select('li:not(.active)')
	category_name = links[len(links) - 1].text.strip()

# Récupérer description (id product_description +  p)
	description = soup.find('div', {"id": 'product_description'})

	if description:
		description = description.findNext('p').text
	else:
		print(f" Livre sans description : {book_url}")
		description = "Ce livre n'a pas de description"

# Récupérer review_rating (class star-rating + class indiquant le nombre d'étoile)
	review_rating = soup.find('p', {"class": "star-rating"})
	review_rating = review_rating["class"][1]
	review_rating = transform_rating(review_rating)

# Récupérer number_available (instock outofstock en dessous du prix du produit)
	availability = tds[5].text[10:]
	availability = availability.replace(' available)', '')
	availability = int(availability)
 
	category_name = slugify(category_name)
	image_file =  f"{DATA_DIR}{category_name}/images/{slugify(title)}.jpg"
 
	product_informations = {}
	product_informations['title'] = title
	product_informations["product_page_url"] =  book_url
	product_informations["category"] = category_name
	product_informations["product_description"] = description.strip()
	product_informations["image_url"] = image_url
	product_informations['image_file'] = image_file
	product_informations["universal_product_code"] = tds[0].text
	product_informations["price_excluding_tax"] = tds[2].text
	product_informations["price_including_tax"] = tds[3].text
	product_informations['review_rating'] = review_rating
	product_informations["number_available"] = availability
 
	return product_informations


def transform_rating(rating_text):
	"""
	Get as parameter the rating as letters and return in a digit
	
	:param rating_text: The text of the rating
	:return: The rating of the book as digit
	"""
	rating = 0
	if rating_text == "One":
		rating = 1
	elif rating_text == "Two":
		rating = 2
	elif rating_text == 'Three':
		rating = 3
	elif rating_text == "Four":
		rating = 4
	elif rating_text == "Five":
		rating = 5
    
	return rating


def get_book_image(image_url,category_name,image_name):
	"""
	It takes an image url, a category name and an image name as parameters, and downloads the image to
	the specified directory
	
	:param image_url: The URL of the image we want to download
	:param category_name: The name of the category of the book
	:param image_name: The name of the image file
	"""
	reponse = requests.get(image_url)
	if not reponse.ok:
		print("Il y a eu un problème lors de la récupération de l'image, passage à l'image suivante...")

	else:
		Path(DATA_DIR + category_name + "/images/").mkdir(parents=True, exist_ok=True)
		with open(f"{DATA_DIR}{category_name}/images/{image_name}.jpg", "wb") as f:
			f.write(reponse.content)

    
def savetocsv(category_name,books_data):
	"""
	It takes a category name and a list of dictionaries as input, and writes the list of dictionaries to
	a csv file
	
	:param category_name: The name of the category you want to save the data to
	:param books_data: a list of dictionaries, each dictionary is a book's data
	"""
	field_names = books_data[0].keys()
	category_path = DATA_DIR + category_name + "/" 
	csv_name = category_name +  ".csv"
	with open(category_path + csv_name , 'w', newline='', encoding='utf-8-sig') as csvfile:
		w = csv.DictWriter(csvfile, fieldnames=field_names)
		w.writeheader()
		w.writerows(books_data)
  
#if __name__ == "__main__":