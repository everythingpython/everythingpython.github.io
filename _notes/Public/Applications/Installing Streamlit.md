---
title: Installing Streamlit
feed: show
date: 2024-10-30
---
#### 30th Oct 2024


This is a rather simplistic topic but one of my good friends has been trying to setup Streamlit and has been unsuccessful at it. So he asked if I could help him out.  If this helps him atleast, I will have done my job. 

Hence this topic for today's mini essay.

Going forward, pretty much every local package I install will use `uv`. 
(How to install uv? https://everythingpython.substack.com/p/uv-python-packager-written-in-rust)
Operating system under use - Windows (but this will work on Ubuntu as well)
So let's create a folder for our Streamlit apps - 

```shell
D:> mkdir streamlit_apps
D:> cd streamlit_apps
```

Creating a virtual environment in this folder , activating it and installing streamlit - 
```shell
D:\streamlit_apps> uv venv
D:\streamlit_apps> .venv\Scripts\activate
(streamlit_apps)D:\streamlit_apps> uv pip install streamlit
```

And voila!

---

Now let's create a quick app and run it. 

Here's the code to create a simple app, that accepts a user input, does a quick Github search to find the top 3 repos corresponding to that term and outputs it. Assume the filename is `streamlit_app.py`


```python

import streamlit as st
import requests

# Function to fetch top 3 repositories from GitHub based on user query
def fetch_top_repositories(query):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json().get("items", [])[:3]
        return [
            {"name": repo["name"], "stars": repo["stargazers_count"], "url": repo["html_url"]}
            for repo in repos
        ]
    else:
        st.error("Failed to fetch data from GitHub.")
        return []

# Streamlit app UI
st.title("GitHub Repository Finder")
st.write("Enter a search term to find the top 3 repositories on GitHub.")

# Input field for user query
query = st.text_input("Search GitHub Repositories", "")

# Button to trigger the search
if st.button("Search") and query:
    with st.spinner("Fetching top repositories..."):
        results = fetch_top_repositories(query)
        
        if results:
            st.write("### Top 3 Repositories:")
            for repo in results:
                st.write(f"**{repo['name']}**")
                st.write(f"⭐ Stars: {repo['stars']}")
                st.write(f"[Repository Link]({repo['url']})")
        else:
            st.write("No repositories found.")
```


So once we've activated our environment like above, the way to run it is - 


```
(streamlit_apps)D:\streamlit_apps> streamlit run streamlit_app.py
```


This results in the browser being launched and a window opening up like so - 

![Alt Text](/assets/img/install-streamlit/1.png)


And any search results in the top repos by stars as expected - 

![Alt Text](/assets/img/install-streamlit/2.png)


Hope this gives you the push to create your own fun little apps!
Let me know what you create!