from slugify import slugify
from utils.functions import get_categories, get_books_urls, get_book_datas,get_categorie_name,get_book_image,savetocsv
from pathlib import Path 
from rich.progress import track
from rich import print
import shutil
import os

DATA_DIR = "data/"


def main():
    """
    It creates a directory called data, then creates a directory for each category,
    downloads the book cover image for each book in each category.
    """
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    print('Récupération des catégories en cours...')
    categories_urls = get_categories('a' , 'href', 'http://books.toscrape.com/index.html','category')
    for url in categories_urls:
        print(url)
        category_name = get_categorie_name(url)
        Path(DATA_DIR + category_name).mkdir(parents=True, exist_ok=True)
        print(f'Traitement de la catégorie [bold red]{category_name}[/bold red]')
        books_urls = get_books_urls(url)
        books_data = []
        
        # A for loop that iterates through the books_urls list and for each url it gets the book data
        # And then it downloads the image and saves it in the data folder.
        for book_url in track(books_urls, description='Processing', refresh_per_second=5):
            book_data = get_book_datas(book_url)
            image_url = book_data['image_url']
            book_title = slugify(book_data["title"])
            get_book_image(image_url,category_name,book_title)
            books_data.append(book_data)     
            
        # Saving the data to a csv file.
        savetocsv(category_name,books_data)
        
    #Zipping the folder "data" and saving it as "data.zip"
    print('Creating Archive...')
    shutil.make_archive("./data", 'zip', "data")    
    
    if os.path.isfile('./data.zip'):
        print('Archive data.zip successfully created')
        print('Removing /data directory')
        shutil.rmtree('./data', ignore_errors=True)
        
        
    
    
    print('End of script.')
            
    
if __name__ == '__main__':
    main()    