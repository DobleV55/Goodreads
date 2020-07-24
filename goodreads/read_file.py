import click
import os
def read_file():
    read_file = open('../books.txt', 'r')
    books_titles = []
    for title in read_file:
        title = title.strip()
        if not title:
            break
        books_titles.append(title)
    return books_titles