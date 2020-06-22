###
# AGREGAR ADD BOOK TO SHELF
# AGREGAR BUSQUEDA DE BOOK_ID POR NOMBRE
###

import requests
from bs4 import BeautifulSoup
import click

def __main__():
  soup, url_sign, s = get_html()
  token = get_token(soup)
  n = get_n(soup)
  login(token, url_sign, n, s)
  get_book_id()
  add_book(s)

def get_html():
  s = requests.Session()
  url_sign = 'https://www.goodreads.com/user/sign_in'
  sign_in = s.get(url_sign)
  soup = BeautifulSoup(sign_in.content, 'html.parser')
  return soup, url_sign, s

def get_token(soup):
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
  ###GET 'N' PARAMETER TO LOGIN
  inputs = soup.find_all("input")
  inp = str(inputs[6])
  up_n = inp[37:]
  n = int(up_n[:6])
  return n

def login(token, url_sign, n, s):
  email = click.prompt('Email', type=str)
  password = click.prompt('Password', hide_input=True, type=str)
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
  
def get_book_id():
  search = click.prompt('enter book title')
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
  print(search)
  print('https://www.goodreads.com/book/show/'+book_id)

def add_book(s):
  # CREATE FUNC TO ADD BOOK TO WANT_TO_READ
  return

if __name__ == "__main__":
  __main__()
