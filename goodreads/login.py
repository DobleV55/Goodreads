from bs4 import BeautifulSoup

def login(requests_session, email, password):
    soup, url_sign = get_html(requests_session)
    token = get_token(soup)
    n = get_n(soup)
    login_post(requests_session, email, password, token, url_sign, n)
    # check_login()
    return token

def get_html(requests_session):
    ### GET SOURCE CODE
    url_sign = 'https://www.goodreads.com/user/sign_in'
    sign_in = requests_session.get(url_sign)
    soup = BeautifulSoup(sign_in.content, 'html.parser')
    return soup, url_sign

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

def login_post(requests_session, email, password, token, url_sign, n):
    data = {
        'utf8':'',
        'authenticity_token': token,
        'user[email]': email,
        'user[password]': password,
        'remember_me': 'on',
        'next': 'Sign in',
        'n': n
    }
    log_in = requests_session.post(url_sign, data=data)

# def check_login()
#   return