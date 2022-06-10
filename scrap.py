from turtle import title
from slugify import slugify
from utils.functions import get_categories, get_books_urls, get_book_datas,get_categorie_name,get_book_image,savetocsv
from pathlib import Path 
from rich.progress import track


DATA_DIR = "data/"


def main():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    print('Récupération des catégories en cours...')
    categories_urls = get_categories('a' , 'href', 'http://books.toscrape.com/index.html','category')
    for url in categories_urls:
        print(url)
        category_name = get_categorie_name(url)
        Path(DATA_DIR + category_name).mkdir(parents=True, exist_ok=True)
        print(f'Traitement de la catégorie {category_name}')
        books_urls = get_books_urls(url)
        books_data = []
        
        for book_url,track(description= 'Processing' refresh_per_second=5) in books_urls:
            book_data = get_book_datas(book_url)
            image_url = book_data['image_url']
            book_title = slugify(book_data["title"])
            get_book_image(image_url,category_name,book_title)
            books_data.append(book_data)     
            
        savetocsv(category_name,books_data)
            
            
        
        #save_data_to_csv
    
if __name__ == '__main__':
    main()    