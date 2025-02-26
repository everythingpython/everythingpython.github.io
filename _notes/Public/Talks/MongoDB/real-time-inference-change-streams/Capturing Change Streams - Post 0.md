---
title: Capturing Change Streams - Post 0
feed: show
date: 2025-02-24
---
#talks  #mongodb
## Motivation and Plan

This is about understanding what I'm doing to talk about and what info it will cover. 

So effectively there are two nodes and an edge traversing from A to B . 

Point A - Oxygen Monitor
Point B - Mongo Change Streams
Point Mid - LLMs

So how do we traverse from A to B via Mid and keep it relevant?

For this, I need to understand some things about Change Streams - 
- What do Change Streams do?
- Are they even necessary? 
- What problem do they solve?
- When was it introduced? Which version of Mongo?
- Why was it introduced?

---

A change stream is a real-time stream, flowing from your MongoDB database to your application, of all database changes. [Src](https://www.mongodb.com/resources/products/capabilities/change-streams#:~:text=A%20change%20stream%20is%20a%20real%2Dtime%20stream%2C%20flowing%20from%20your%20MongoDB%20database%20to%20your%20application%2C%20of%20all%20database%20changes.)

It effectively converts MongoDB into a Realtime Database. 

[[Starting MongoDB as a Replica Set]]

[Meeting invite](https://www.mongodb.com/community/events/form/t/311109?rsvpStatus=false&ref=forums)

[Installation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
