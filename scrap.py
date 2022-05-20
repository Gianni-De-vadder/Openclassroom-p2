from utils.functions import get_categories, get_books_urls, get_book_datas


def main():
    
    categories_urls = get_categories('a' , 'href', 'http://books.toscrape.com/index.html','category')

    for url in categories_urls:
        books_urls = get_books_urls(url)
    
        books_data = []
        for book_url in books_urls:
            book_data = get_book_datas(book_url)
            books_data.append(book_data)
    
    print(books_data)
if __name__ == '__main__':
    main()