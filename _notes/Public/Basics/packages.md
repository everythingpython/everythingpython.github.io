---
title: Packages -1 
date: 10-09-2024
feed: show
---
## 10-09-2024

#### What is a package in Python?

Hold up, isn't this one of those terms we use synonymously with other terms like `library`, `module` etc?

Well no. Let's learn what the differences are - 

---
### Module 
A `module` can be any file with a `.py` extension. For example - 

#### **`hero.py`**
```python  
def hero():
    return f"Anyone"

print(hero())
```

This module when executed using `python hero.py` returns the string "Anyone". 
_Because a hero can be [Anyone](https://www.youtube.com/watch?v=iGx5a1ifSDs)._ 

---

### Package 

A package is typically a collection or a group of related modules. 
The indication of a package is via an empty __init__.py file alongside the rest of the package's modules. 

E.g. 
```
top_level_folder
|- cloud_functions
    |- __init__.py
    |- gcp.py
    |- aws.py
    |- azure.py
|- main.py
```
Now if `__init.py__` is empty and `gcp.py` looks something like this - 

```python
from google.cloud import storage
from googleapiclient import discovery
from google.oauth2 import service_account


class GCPClient:
    def __init__(self, credentials_file):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_file)
        # More instance variables

    # GCS: Upload file to Google Cloud Storage
    def upload_file_to_gcs(self, bucket_name, source_file_name, destination_blob_name):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name}.")

# ... Other functions 
```

Then in `main.py`, the functions in `gcp.py` can be accessed as - 

```python
from cloud_functions.gcp import *

upload_file_to_gcs(...)
```

Here `cloud_functions` is a package - a package of related cloud functionalities.

---

### Library

A library in common parlance is a building where books are housed. A library in Python similarly is a (usually installable) collection of packages and modules. 

For example, the popular data manipulation tool `pandas` is a library. 

Like the way to make a package is by way of an empty `__init.py__` file, the way to make a Python library is by providing a way to package the set of packages and modules using something called a `setup.py` file. 
Here's a sample Python library's structure - 

```
superheroes/
├── dc/
│   ├── __init__.py  # This makes it a package
│   └── batman.py    # Python file in dc package
└── setup.py         # Setup script for distribution
└── README.md        # Most packages have a README to provide context about it
```

A typical setup file looks like - 
```python
# setup.py

from setuptools import setup, find_packages

setup(
    name="superheroes",  # The name of our library
    version="0.1",  # Release version
    author="EverythingPython",
    author_email="everythingpython0@gmail.com",
    description="A package to chronicle all Superheroes",
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[],  # List dependencies here if any
)
```

A package is installed using a package installer like pip. 