from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint

from bs4 import BeautifulSoup
import click
import requests


def main_menu():
  style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
  })

  option1 = 'Enter a Book Name'
  option2 = 'Upload a file with Book Names'

  questions = [
      {
          'type': 'list',
          'message': '',
          'name': 'option',
          'choices':  [
            Separator('How do you want to add your book/s to Goodread?'),
                        {
                          'name': option1
                        },
                        {
                          'name': option2
                        },
                      ],
          'validate': lambda answer: 'You must choose at least one.' \
              if len(answer) == 0 else True
      }
  ]

  answers = prompt(questions, style=style)
  if answers['option'] == option1:
    input_option()    
  elif answers['option'] == option2:
    file_option()

def input_option():
  ### IF USER CHOOSE OPTION 1 : Enter a Book Name 
  soup, url_sign, s = get_html()
  token = get_token(soup)
  n = get_n(soup)
  login(token, url_sign, n, s)
  book_id_from_input = get_book_id_from_input()
  add_book_from_input(s, token, book_id_from_input)

def file_option():
  ### IF USER CHOOSE OPTION 2 : Upload a file with Book Names 
  soup, url_sign, s = get_html()
  token = get_token(soup)
  n = get_n(soup)
  login(token, url_sign, n, s)
  books_ids = get_book_id_from_file()
  add_books_from_file(s, token, books_ids)

def get_html():
  ### GET SOURCE CODE
  s = requests.Session()
  url_sign = 'https://www.goodreads.com/user/sign_in'
  sign_in = s.get(url_sign)
  soup = BeautifulSoup(sign_in.content, 'html.parser')
  return soup, url_sign, s

def get_token(soup):
  ### GET TOKEN NEED TO LOGIN
  metas_tags = soup.find_all("meta")
  count = 0
  for meta in metas_tags:
    count += 1
    if count == 3:
     string_meta = str(meta)
  up_final_meta = string_meta[15:]
  token = up_final_meta[:88]
  return token
  
  
def get_n(soup):
  ### GET 'N' PARAMETER NEED TO LOGIN
  inputs = soup.find_all("input")
  inp = str(inputs[6])
  up_n = inp[37:]
  n = int(up_n[:6])
  return n

def login(token, url_sign, n, s):
  email = click.prompt('Goodreads Email', type=str)
  password = click.prompt('Goodreads Password', hide_input=True, type=str)
  data = {
    'utf8':'',
    'authenticity_token': token,
    'user[email]': email,
    'user[password]': password,
    'remember_me': 'on',
    'next': 'Sign in',
    'n': n
  }
  log_in = s.post(url_sign, data=data)
  
def get_book_id_from_input():
  ### GET YOUR BOOK NAME INPUT AND CONVERT IT TO GOODREADS BOOK ID
  search = click.prompt("Book Title (can contain spaces ' ')")
  search = search.replace(' ', '+')
  url = 'https://www.goodreads.com/search?q='+search
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')
  match = (soup.find('a', class_='bookTitle'))
  matcha = match.attrs['href']
  book = str(matcha)
  numbers = ['1','2','3','4','5','6','7','8','9','0']
  book_id = ''
  for digit in book:
      if digit in numbers:
          book_id+=digit
      elif digit == '-':
          break
      elif digit == '.':
          break
      elif digit == '_':
          break
  print("See your book added to your 'Want to Read' shelf: https://www.goodreads.com/book/show/"+book_id)
  return book_id

def get_book_id_from_file():
  ### READ LINES FROM FILE AND CONVERT THEM TO GOODREADS BOOK ID'S
  click.prompt('File name')
  book_file = open('books.txt', 'r')
  books_ids = []
  for line in book_file:
    search = line
    search = search.replace(' ', '+')
    url = 'https://www.goodreads.com/search?q='+search
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    match = (soup.find('a', class_='bookTitle'))
    matcha = match.attrs['href']
    book = str(matcha)
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    book_id = ''
    for digit in book:
        if digit in numbers:
            book_id+=digit
        elif digit == '-':
            break
        elif digit == '.':
            break
        elif digit == '_':
            break
    books_ids.append(book_id)
    print("See your book added to your 'Want to Read' shelf: https://www.goodreads.com/book/show/"+book_id)
  return books_ids
  

def add_book_from_input(s,token, book_id):
  ### ADD BOOK TO YOUR 'WANT_TO_READ' SHELF
  headers = {
      'X-CSRF-Token': token,
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  }

  data = {
    'book_id': book_id,
    'name': 'to-read',
    'v': '2'
  }
  add_book = s.post('https://www.goodreads.com/shelf/add_to_shelf.json', headers=headers, data=data)

def add_books_from_file(s,token, books_ids):
  ### ADD BOOK TO YOUR 'WANT_TO_READ' SHELF
  for book in books_ids:
    print(book)
    headers = {
        'X-CSRF-Token': token,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    data = {
      'book_id': book,
      'name': 'to-read',
      'v': '2'
    }
    add_book = s.post('https://www.goodreads.com/shelf/add_to_shelf.json', headers=headers, data=data)

if __name__ == "__main__":
  main_menu()
