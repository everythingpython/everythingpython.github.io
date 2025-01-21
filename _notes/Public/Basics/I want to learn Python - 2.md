---
title: I want to learn Python -2 
feed: show
date: 2025-01-14
---
### 14th Jan 2025


### I've installed Python. Now what?

If you can open CMD and when you execute `python --version`, you see 
`Python 3.13.1` , it means your installation is successful. 

There are a Lot of syntaxes and operations to cover in Python and in programming in general. 

But I will consider some common operations in the real world and we will see what the programming construct for it is and what the corresponding Python commands are for it. 

If I was a novice to the programming world and someone told me that Python could be used to solve a real-world problem , how would I go learning the language?

# Scenario 1 :  File Renaming

Let's take a very simple case where coding can be handy - I have a bunch of files named DCIM_001.jpeg, DCIM_002.jpeg etc. 

If I know that those pics were taken in October of 2024, then a more (albeit not the most) meaningful way to rename them would be something associating the files with that month and year and probably even the occasion on which that photo was clicked. 

If it was 1 or 2 or even 10 photos, then I could have done the job manually. But what if there were a 100 photos taken on a particular day? I remember taking a huge amount of photos on my father's 60th birthday on a digital camera and the filenames were exactly in this fashion. 

Now, we can write a simple `script` in Python to solve this problem. 

If you'd like to follow along you will need two things - 
a) A folder full of files with names like this or in some format like this. 
b) The Python script to enable the renaming

For the purposes of this exercise, I've created a hundred dummy images with names like IMG_001.jpg, IMG_002.jpg, IMG_003.jpg etc. I'm going to assume that I want to rename them to Family_Func_Oct24_001.jpg, Family_Func_Oct24_002.jpg, Family_Func_Oct24_003.jpg etc
 
The goal is to understand the following steps : 
- Access the folder with these 100 images using code
- Rename them and save them either in the same folder or in a different folder. 
- **CASE 1** - Some of us might want to save them in the same folder so that we don't create duplicates of the files 
- **CASE 2** - Others might want to save them in a different folder so as to preserve the originals 

Here's how the code for this looks like for **CASE 1** - 

```python
import os

folder_path = "./photos"  # Replace with your folder path
new_prefix = "Family_Func_Oct24"

files = os.listdir(folder_path)
for i, filename in enumerate(files):
    if filename.endswith(".jpg"):
        new_name = f"{new_prefix}_{i + 1:03}.jpg"
        os.rename(
            os.path.join(folder_path, filename),
            os.path.join(folder_path, new_name)
        )
print("Files renamed successfully!")
```

We'll go through it line by line :

1. `import os`

This is called **importing a package** . Think of it as picking up a particular box of tools to do one or more number of tasks . For example, if you wanted to write something, and you anticipate that you might need to draw a line or erase a mistake, you might end up buying a pencil box that contains a pen/pencil, a scale and an eraser. Here `import` is the equivalent of the action of purchasing something . And `os` is the equivalent of a pencil box - *a set of tools*. In Python, anything that is imported is a **package**. 

Once you've imported a package, you can use the **methods** inside the package to perform different actions. A **method** for the purposes of this post, is one of the aforementioned tools.

2. `folder_path = "./photos"`