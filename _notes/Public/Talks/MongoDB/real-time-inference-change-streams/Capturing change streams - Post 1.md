---
title: Capturing change streams - Post 1
feed: show
date: 2025-02-23
---
This is the first in a series of posts in my run up to my talk on Saturday about how Change Streams can be used to capture realtime data from LLMs . 

**What all I did :** 

- Installed mongo-community using : 
	```sh
	brew tap mongodb/brew
	brew update
	brew install mongodb-community@8.0
```

- Created a virtual environment for this project. 
	```sh
	uv venv
	source .venv/bin/activate
```

- Installed `pymongo` to interact with Mongo DB
```sh
uv pip install pymongo
```


---

