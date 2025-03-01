---
title: Streaming Real-Time AI Inference Results into MongoDB
feed: show
date: 2025-02-28
tags:
  - talks
  - mongodb
---



I'm going to be presenting a talk at a Mongo DB User group meetup later today and I thought I'd write about it so that it would - 
- serve as reading material for folks wanting to go through the content of my talk later
- let everyone else know what this is all about. 

Let me pre-emptively say, I don't know why I chose this to be the "TITLE" of the talk. 
It is extremely dry. But the topic is actually a lot of fun!

Effectively, there is this concept called Change Streams in Mongo DB and this talk is an attempt to understand and illustrate its usage. 

## So first off, what is Mongo DB and where is it used? 

MongoDB is a database that follows a document model to store data. 
This means that, in comparison to normal relational databases where data is stored using fixed schemas in rows and columns, Mongo DB and its other Document DB brethren store data in a more flexible format - in JSON-like documents. 

Example of a dataset that can be stored in Mongo : 
```json
{
  "_id" : ObjectId(),
  "title" : "Anna Karenina",
  "author" : "Leo Tolstoy",
  "content" : "It's a classic of world literature, exploring themes of love, loyalty, family, and social class in 19th-century Russia.",
  "tags" : [ "Russian" , "Serious" ],
  "publishedDate" : ISODate()
},
{
  "_id" : ObjectId(),
  "title" : "War and Peace",
  "author" : "Leo Tolstoy",
  "content" : "Set during the Napoleonic Wars and focusing on several aristocratic families in Russia.",
  "tags" : [ "Russian", "Serious" ],
  "publishedDate" : ISODate()
}
```

MongoDB can be used where the data to be stored doesn't particularly benefit from being modelled into strict tables. It can be used when the data schema needs to be more flexible.

For example, the same data above could have potentially been stored in a Relational DB. But as the number of fields increases and as there end up being more and more complicated JOINS, the Relational DB model might suffer from slowdown. 

---
## What is this post about?

[**Change Streams**](https://www.mongodb.com/resources/products/capabilities/change-streams#:~:text=A%20change%20stream%20is%20a%20real%2Dtime%20stream%2C%20flowing%20from%20your%20MongoDB%20database%20to%20your%20application%2C%20of%20all%20database%20changes.)! 

This is a feature that has been around for a long time now. We're currently on Mongo DB 8.0.4 as of December 2024 but this feature was introduced in **MongoDB 3.6** in 2017.

> **It is used to let applications access real-time data changes in Mongo DB. Without having to keep polling for it.** 

Now other DBs also have this in some shape or form but they all vary in difficulty levels of configuration -

- Postgres has support for a Debezium connector that can be used for Change Data Capture
- Amazon's DocumentDB also has Change Streams but it might need additional configuration compared to Mongo DB
- Relational DBs can be configured to use Triggers or [Log based CDC](https://medium.com/mercedes-benz-techinnovation-blog/change-data-capture-lessons-learnt-7976391cf78d) but it can impact performance or needs some non-trivial know-how.

In that aspect Change Streams are very easy to configure. 

**How do Change Streams work?**

- This whole mechanism hinges on the fact that Mongo DB relies on "op-log" or operations-log based replication. 
- What this means is that if Mongo DB is configured to use a replica set, any changes that are made to the DB are written to the op-log by the primary node. Secondary nodes read /tail  the oplog and apply changes in the same order.
- Change Streams can be used by using a "watch" method on  a collection, a database or a whole cluster. 
- So now, whenever there's a certain operation-based change on the "system" under watch, the change stream captures it from the corresponding oplog entry.
- The operations supported are  : insert, update, delete, replace , invalidate

---

## How can I enable Change Streams?

> This post assumes you have a working MongoDb setup - I'll write a separate post for this.

- Go to the Mongo Shell and execute ``rs.status()``

If there's a replica set configuration like so - 
![Alt Text](/assets/img/talks/replica-set-conf.png)

you're all good. If not, you need to do the following : 

- Stop the mongo service - Either from Task Manager if you're on Windows. Or using ``sudo systemctl stop mongod`` if on Linux. 
- Find the mongod.cfg (Windows) or mongod.conf (Linux) file and add the following line - 

```
replication:
	  replSetName: "<Whatever name you want>"
```

So it looks like - 

![Alt Text](/assets/img/talks/replica-set-vs-code.png)

- Restart the Mongo service. 

- Reopen the Mongo shell and run ``rs.initiate()``

Boom! Change Streams are now enabled!

---

## Great. Now how do I use them?

I thought about this a lot as well. My initial thought was to mimic the functioning of an oxymeter in a hospital that keeps reporting the oxygen level of a patient. 

But I thought I'd keep it a little lighter. 

So, my simulated use case is one of segregating News Items into 1 of 4 categories as they keep getting pulled from News Sources. 

**Here's a broad architecture diagram -**

![Alt Text](/assets/img/talks/mongo-app-arch.png)

Let's consider this piece by piece : 

### News Generator : 

- Here we have 5 "news sources", producing news items every, say 10 seconds.
- The item , which here is a string is sent to an Azure OpenAI LLM instance with a prompt designed to return the "Category" of News it belongs to. We have a preset expectation of news items to fall under 5 categories : "Sports", "Politics", "Entertainment", "Tech", "Misc".
- I'm using gpt-4o for this example but it's such a trivial activity that most older or any Small Local Model should also suffice for this task.
- What is not shown in the diagram is that I'm using Opik (launched locally) to track my LLM calls. 
- Now as soon as this categorization is obtained, the data is pushed into a collection called "articles" under a DB called "newsDB".

![Alt Text](/assets/img/talks/mongo-entries.png)

### The Flask App

- This doesn't necessarily have to be a Flask app. Pick your web server of choice - FastAPI, Django, Bottle, whatever you want. But yes, in this example, it is a flask app. 
- Here, I do a few things : 
	a) Make sure the Mongo DB is connected to on port 27017 (default) and that the UI reflects the number of pre-existing records  for each category in the DB. For a fresh start, that number is 0 for all categories.
	b) Set up a `collection.watch()` on the `articles` collection so that the change stream can be captured.
	c) Start the flask server  using websockets (via flask-socketio) so that a steady, bidirectional connection is established between server and client. This way, the browser is always watching for any changes that the DB is ready to communicate back without needing a refresh of the screen.

### The Client/ UI/ Browser 

- If the server is started on say, port 5002, I navigate to http://localhost:5002

![Alt Text](/assets/img/talks/final-gif.gif.gif)

This changes automatically every 20 seconds. 

Hopefully this gave you an idea of how Change Streams can be used!

---

### Codebase - 

All the code for this project can be found [here](https://github.com/everythingpython/everythingpython.github.io/tree/main/_notes/Public/Talks/MongoDB/real-time-inference-change-streams/src/NewsMon).