---
title: Making your first blog with mkdocs
feed: show
date: 16-11-2024
tags:
  - blogs
  - application
---
Now, why do this? 
What's wrong with medium.com and substack.com and wordpress.com and blogger.com and all the tens of websites out there?
Nothing. You could totally just create a blog there and publish. That's why Content Management Systems exist - so you could focus on the *content* and not on the *management* .

But if you're like me and want some more control over how you publish your blogs, customize them etc. , you will find this and the other upcoming articles in this category interesting. 

Recently I found out about this great project documentation library implemented in Python called "mkdocs" , more specifically - "Matieral for MkDocs" . It's used by a lot of companies to maintain their documentation and open source offerings if any. 

Now, while this library is marketed as one for documentation - even the name says "docs" - there is no reason we can't host our blog using it! It may not end up being the most flashiest looking site, but for someone who wants to blog regularly - technical or non-technical - and likes the markdown format, which is one of the most versatile formats out there, mkdocs is a great way to hit the ground running. 

This particular blog itself is published using Obsidian and Jekyll (Ruby). But my personal website - "https://abhiramr.com" was recently ported from a mixture of Jekyll and Wordpress to pure mkdocs. 

This is how I went about it. And this is how you go about it - 

-  As always, create a virtual environment first. If you need help, I've done this in a few of my earlier [articles]([https://everythingpython.substack.com/p/virtual-environments-using-uv]) .
- After you've activated the virtual environment - let's call it `blog_env`, install the package `mkdocs-material` inside it - 

```python
uv pip install mkdocs-material
```

- Once you've installed the package, create a new blog skeleton using - 

```python
mkdocs new .
```

- This will create a structure like so -

![Alt Text](/assets/img/blog/mkdocs/mkdocs-1.png)


The `mkdocs.yml` file is the life-blood of this site. It has information related to the URL that  your site should redirect to, the plugins that you want to support, the theme your site should use, the overall structure your site should have etc. 

This is what my site's mkdocs.yml looks like - 

![Alt Text](/assets/img/blog/mkdocs/mkdocs-2.png)

Basically, the theme I'm using is the default theme mkdocs-material supports, which is "material". 
My site has two navigation options - Tech and Non-Tech - under which I've segregated my posts. 
I also have a few plugins which will end up being elaborated in a future post. For this post, we will restrict our discussion to the "blog" plugin. 

---

**The very first thing we will do is set up our Home page.** 
This is accomplished by creating an `index.md` file under the **docs** directory.
The contents of this `index.md` file can be embedded HTML or markdown. E.g. - 

```markdown
# Hi. I'm Abhiram

<p>

I'm a Machine Learning Engineer at O9 Solutions, a supply chain based company in Bangalore. I like coding in Python and R, <b><a href="https://abhiramr.com/books/" style="color: rgba(19, 116, 161, 0.596);">reading fiction/non-fiction</b></a> and <b><a href="https://abhiwrites.com" style="color: rgba(19, 116, 161, 0.596);">writing short stories</a></b>. I co-created and run <b><a href="https://brokebibliophilesbangalore.com/about/" style="color: rgba(19, 116, 161, 0.596);">Broke Bibliophiles Bangalore</a></b>, one of the largest bookclubs in Bangalore (2017 - present).</p>

```

---

**Next we will set up our blog posts -** 

When you specify the usage of the "blog" plugin, you're telling mkdocs to consider your site as a blog. This is aided by the placement of your posts, which are expected to be markdown files. 

These files are to be placed in the "posts" directory with the following structure - `docs > blog > posts` .

Under "blog", all you need to have is one `index.md` file with the heading you want your main blog's subsection to have. 

This should be the net structure - 

![Alt Text](/assets/img/blog/mkdocs/mkdocs-3.png)

---

Now let's see the result of our work. 

Run - `mkdocs serve` and you should be able to launch your budding blog at `localhost:8000`

![Alt Text](/assets/img/blog/mkdocs/mkdocs-4.png)

The next article in this category will cover the publishing of the blog!


---
**References -**

The official pages are excellent - 

- https://github.com/squidfunk/mkdocs-material#trusted-by-
- https://squidfunk.github.io/mkdocs-material/
- https://www.mkdocs.org/



