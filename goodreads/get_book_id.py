### IF USER CHOOSE OPTION 1 : Enter a Book Name 
import click
import requests
from bs4 import BeautifulSoup


def get_book_id(book):
    ### GET YOUR BOOK NAME INPUT AND CONVERT IT TO GOODREADS BOOK ID
    if book is None:
        book = click.prompt('Book ', type=str)
    search = book.replace(' ', '+')
    url = 'https://www.goodreads.com/search?q='+search
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    match = (soup.find('a', class_='bookTitle'))
    matcha = match.attrs['href']
    ### ADD BOOK NOT FOUND
    book_search = str(matcha)
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    book_id = ''
    for digit in book_search:
        if digit in numbers:
            book_id+=digit
        elif digit == '-':
            break
        elif digit == '.':
            break
        elif digit == '_':
            break
    print("See the book "+book+" added to your 'Want to Read' shelf:")
    return book_id