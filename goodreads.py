import requests
from bs4 import BeautifulSoup

s = requests.Session()

url_sign = 'https://www.goodreads.com/user/sign_in'

sign_in = s.get(url_sign)
###GET AUTHENTICITY TOKEN
soup = BeautifulSoup(sign_in.content, 'html.parser')
metas_tags = soup.find_all("meta")
count = 0
for meta in metas_tags:
  count += 1
  if count == 3:
   string_meta = str(meta)
up_final_meta = string_meta[15:]
token = up_final_meta[:88]
print(token)

###GET 'N' PARAMETER TO LOGIN
soup = BeautifulSoup(sign_in.content, 'html.parser')
inputs = soup.find_all("input")
inp = str(inputs[6])
up_n = inp[37:]
n = int(up_n[:6])

print(n)
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
###LOG_IN
log_in = s.post(url_sign, data=data)

##CHECK_LOG_IN
url_check = 'https://www.goodreads.com/api/keys'
check = s.get(url_check)
print(check.text)