from slugify import slugify
from utils.functions import get_categories, get_books_urls, get_book_datas,get_categorie_name,get_book_image
from pathlib import Path 


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
        
        for book_url in books_urls:
            book_data = get_book_datas(book_url)
            get_book_image(book_data["image_url"],category_name,slugify(book_data["title"]))
            books_data.append(book_data)            
            
        
        #save_data_to_csv
    
if __name__ == '__main__':
    main()    