---
title: Making your first blog with mkdocs
feed: show
date: 16-11-2024
tags:
  - blogs
  - application
---
### 16th Nov 2024

![Alt Text](/assets/img/blog/mkdocs/mkdocs-banner.webp)

Now, why do this? 

What's wrong with [Medium](medium.com) and [Substack](https://substack.com) and [Blogger](blogger.com)  and [Wordpress](wordpress.com) and all the tens of websites out there?
Nothing. You could totally just create a blog there and publish. That's why Content Management Systems exist - so you could focus on the *content* and not on the *management* .

But if you're like me and want some more control over how you publish your blogs, customize them etc. , you will find this and the other upcoming articles in this category interesting. 

---

<div style="background-color:#1b2738; border: 0.5px solid #5078f0; padding: 6px; border-radius: 5px; color:white"> <p></p><p> <b>
✏️ Note
</b> </p>  <p>❓ <em>
This article assumes that you are using Windows for your development. But the same steps can be used on any flavor of Linux as well.
</em></p> <p></p><p></p></div>
 ---

Now, while mkdocs is marketed as a tool for documentation - even the name says "docs" - there is no reason we can't host our blog using it! It may not end up being the most flashiest looking site, but for someone who wants to blog regularly - technical or non-technical - and likes the markdown format, which is one of the most versatile formats out there, mkdocs is a great way to hit the ground running. 

This particular blog itself is published using Obsidian and Jekyll (Ruby) - More on this later. But my [personal website](https://abhiramr.com) was recently ported from a mixture of Jekyll and Wordpress to pure mkdocs. 

This is how I went about it. And this is how you go about it - 

- First, let's create a folder for our blog setup. Call it `blog_setup`  and navigate to it.

```batch
D:> mkdir blog_setup
D:> cd blog_setup
D:\blog_setup>
```
- As always, create a virtual environment first. If you need help installing the package manager `uv`, I've done this in a few of my earlier [articles]([https://everythingpython.substack.com/p/virtual-environments-using-uv]) . I now almost completely use `uv` for all my virtual environments.
- After you've activated the virtual environment - let's call it `blog_env`, install the package `mkdocs-material` inside it - 

```batch
D:\blog_setup> uv pip install mkdocs-material
```

- Once you've installed the package, create a new blog skeleton using - 
```batch
D:\blog_setup>mkdocs new .
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

### Setting up our home page

The first thing you see on any blog is the home page - where you introduce yourself and set the stage for your audience to understand a little bit about what you like to write. 

This is accomplished by creating an `index.md` file under the **docs** directory.
The contents of this `index.md` file can be embedded HTML or markdown. E.g. - 


```markdown

# Hi. I'm Abhiram

I'm a Machine Learning Engineer and stay in Bangalore, India. 
I like coding in Python and of-late Ruby, reading fiction/non-fiction and writing short stories. 
I also write technical blogs at [Everything Python](https://everythingpython.github.io)
I co-created and run [Broke Bibliophiles Bangalore](https://brokebibliophilesbangalore.com/about/), one of the largest bookclubs in Bangalore (2017 - present).
```

This markdown file will get rendered into HTML when it comes time to build and publish  the blog.

---

### Setting up our Blog posts

When you specify the usage of the "blog" plugin, you're telling mkdocs to consider your site as a blog. This is aided by the placement of your posts, which are expected to be markdown files. 

These files are to be placed in the "posts" directory with the following structure - `docs > blog > posts` .

Under "blog", all you need to have is one `index.md` file with the heading you want your main blog's subsection to have. 

This should be the net structure - 

![Alt Text](/assets/img/blog/mkdocs/mkdocs-3.png)

---

### Testing 

Now let's see the result of our work.  Execute the following in the CMD window - 

```batch
(blog_setup) D:\blog_setup>mkdocs serve
``` 

and you should be able to launch your budding blog at `http://localhost:8000`

![Alt Text](/assets/img/blog/mkdocs/mkdocs-4.png)

The next article in this category will cover the publishing of the blog!


---
**References -**

The official pages are excellent - 

- https://github.com/squidfunk/mkdocs-material#trusted-by-
- https://squidfunk.github.io/mkdocs-material/
- https://www.mkdocs.org/



