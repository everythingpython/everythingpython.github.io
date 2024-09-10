def download_book(title):
    from time import sleep
    from googlesearch import search

    title_dict = {}
    print(f"Processing {title}")
    counter = 0
    for i in search(title+ " goodreads", num_results=5):
        if counter == 0:
            first_result = i
        if "goodreads.com/book/show" in i:
            title_dict[title] = i
            break
    if len(title_dict) == 0:
        title_dict[title] = first_result
    sleep(5)
    return title_dict

from concurrent import futures
import pandas as pd
import time

time_start = time.time()
df = pd.read_csv('data/books_5.csv')
MAX_WORKERS = 5 
books_list = df["title"].tolist()
num_books = len(books_list)
from time import sleep
workers = min(MAX_WORKERS, num_books) 
with futures.ThreadPoolExecutor(workers) as executor:
    res = list(executor.map(download_book, sorted(books_list)))
book_list = {"Title":[], "Link":[]}
for i in res:
    for k, v in i.items():
        book_list["Title"].append(k)
        book_list["Link"].append(v)

df = pd.DataFrame(book_list)
df.to_csv("data/book_links_5.csv", index=False)

time_end = time.time()
time_taken = time_end - time_start

print(f"Downloaded {num_books} books in {time_taken:.2f} seconds")
