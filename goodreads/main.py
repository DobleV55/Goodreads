from main_menu import *
from get_book_id import *
from login import *
from add_book import *
from read_file import *

import click
import requests

@click.command()
@click.option('--email',  help='Goodreads email account')
@click.option('--password', help='Goodreads password account')
@click.option('--book', help="Book Title (can contain spaces ' ')")
def main(email, password, book):
    requests_session = requests.Session()
    choose = main_menu()
    if email is None:
        email = click.prompt('Goodreads email ')
    if password is None:
        password = click.prompt('Goodreads password ',hide_input=True)
    token = login(requests_session, email, password)
    # def check_credentials()
    if choose == 'Enter a Book Name':
        book_id = get_book_id(book)
        add_book_to_shelf(requests_session, token, book_id)
    elif choose == 'Upload a file with Book Names':
        books_titles = read_file()
        for title in books_titles:
            book_id = get_book_id(title)
            add_book_to_shelf(requests_session,token, book_id)

if __name__ == "__main__":
    main()