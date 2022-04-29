import re
from webbrowser import get
from utils.functions import Get_Category
from utils.functions import Get_Books


resultlinks = Get_Category('a' , 'href', 'http://books.toscrape.com/index.html','category')

Get_Books(resultlinks)