---
title: Concurrency in Python
feed: show
date: 21-04-2024
---
## 21-04-2024

These next set of posts are going to be about Concurrency and Async in Python. 
So, one non-tech thing about me is that I run a bookclub that meets once a month. In this bookclub, we discuss books we've read that month and at the end of the meet, we have a nice list of books that each person has mentioned and/or discussed. 
After I get back home, I typically try and get the Goodreads link for each book discussed and create a little more comprehensive list for people to refer to later on. 

I used to do this manually initially and once the process got tedious, I decided to take a  programmatic approach. 

I wrote a small program to look up the book's name along with the string "Goodreads" and do a best-effort retrieval of the book's link on Goodreads. 
Now, today I can probably do that using OpenAI APIs but that's a post for a different day. 

Coming back to the programmatic retrieval, I used to do this sequentially for a long time. And because I didn't want to seem like a DOS attack was taking place, I introduced a sleep function in between each download. 

Here's a function that given the name of a book, will look for the name of the book along with "Goodreads" and pick the link that is likely to be the link for a book - 

```python
def download_book(title):
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
```



While I was thinking of a way to introduce concurrent processing using Python, this felt like an excellent usecase to try and automate, so here we go - 

- Let's assume we have a list of 5 books for which we need the Goodreads links. 
- It is possible that we do not obtain the Goodreads link for a particular book. This is okay. 
- The goal is to try and obtain the Goodreads links for as many books in our list as possible in the shortest amount of time.

This is how the sequential retrieval of the book link list looked like - 

```python
import pandas as pd
import time
time_start = time.time()
df = pd.read_csv('data/books_5.csv')
books_list = df["title"].tolist()
num_books = len(books_list)
res = []
for book in books_list:
    res.append(download_book(book))

book_list = {"Title":[], "Link":[]}
for i in res:
    for k, v in i.items():
        book_list["Title"].append(k)
        book_list["Link"].append(v)

df = pd.DataFrame(book_list)
df.to_csv("data/book_links_5_seq.csv", index=False)

time_end = time.time()
time_taken = time_end - time_start

print(f"Downloaded {num_books} books in {time_taken:.2f} seconds")
```

This did the job but it took quite some time - 
```bash
Processing The Talented Mr Ripley
Processing Ripley's game
Processing Invisible Women
Processing Beyond Interpretation
Processing Men without women

Downloaded 5 books in 28.96 seconds
```

Now let's try the same program using `futures`

```python
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
```

And unsurprisingly - 
```bash
Processing Beyond Interpretation
Processing Invisible Women
Processing Men without women
Processing Ripley's game
Processing The Talented Mr Ripley

Downloaded 5 books in 6.70 seconds
```

So it's understood that in this case, where a network call was involved, the concurrent processing was much faster than the sequential processing. This is because the network call is the bottleneck here and the CPU is mostly idle while waiting for the network call to return. Also it's important to note that the network calls were disjoint and hence could be parallelized.

The same reasoning and method can be applied to I/O bound tasks as well.

If you want to try this out, you can find the code and the data [here](https://github.com/everythingpython/posts/tree/main/2024_07_10_concurrency)