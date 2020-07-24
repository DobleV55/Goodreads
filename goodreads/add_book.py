import requests

def add_book_to_shelf(requests_session,token, book_id):
    
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
    
    url = 'https://www.goodreads.com/shelf/add_to_shelf.json'

    add_book = requests_session.post(url, headers=headers, data=data)

    print("https://www.goodreads.com/book/show/"+book_id)