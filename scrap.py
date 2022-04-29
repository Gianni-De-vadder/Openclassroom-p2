from utils.functions import get_categories
from utils.functions import get_books


def main():
    
    resultlinks = get_categories('a' , 'href', 'http://books.toscrape.com/index.html','category')

    #print(resultlinks)
    #print(len(resultlinks))
    get_books(resultlinks)

if __name__ == '__main__':
    main()