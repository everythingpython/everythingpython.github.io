---
title: Reading DDIA - Part 1
feed: show
date: 23-09-2024
---
#ddia

*(Here's the [preface]([[Reading DDIA - Preface]]) in case you missed it)*
# Chapter 1 - Thoughts 

This chapter's goal is to effectively give us a high level overview of what this book is fundamentally about - 

Thinking about data systems along the axes of : 
- Reliability
- Scalability
- Maintainability


# What is a reliable system?

### My thoughts before reading the section : 
- A system that is available to return results/outputs that are expected of it when it is employed. 
- If I'm accessing an API, if the API is available 99 out of 100 times, then its reliability is 99%
- If a server is available for 23 hrs 45 minutes per day then its availability is 23.75/24 = 98.9% 
- But is availability == reliability? Let's see. 
- A reliable human is someone who does something that he says he will do or is expected to do every time. Similarly a reliable system is one that returns the expected results every time that they are used. 
- An ATM is reliable if I can withdraw money from it in the denominations that I want, when I want it. For example, the ATM in Puttenahalli , JP Nagar is perpetually unavailable. Everytime I go there, the system is under maintenance. It is 0% reliable.

Let's read the chapter. 

### Thoughts after reading the section : 
While my thoughts were rather scattered and scrambling to think about the topic, the section was extremely well divided - into - 
- Faults
	- A fault is a part/a specific component failing . A failure is the entire system not being available. The way to aid this is by counter intuitively introducing faults to stress test the system and exercise and test different scenarios proactively. Also important to address this in the aspect of security. E.g. [Netflix's Chaos Monkey](https://github.com/Netflix/chaosmonkey)
- Hardware Failures
	- If there's a hard disk failure, what do you do?
	- Redundancy helps.
- Software Failures
	- Examples - 
		- Time based issues such as leap days not being handled properly
		- Or cascading failures
	- No real solutions but thorough testing and process isolation can help.
- Human errors
	- There are programmers, and users. It's possible for things to go wrong across multiple interfaces.
	- Decoupling environments - non-prod sandbox
	- Test thoroughly. 
	- Monitoring

---
Also I've started listening to the [San Diego Machine Learning](https://www.youtube.com/watch?v=JqDAEH_2t6M&t=1653s) group's reading of this book alongside after my reading of the book. 
- Version control was asked about. Of course that helps with reliability, backups etc
- Steven mentioned that there would be redundant computers in computations for space tech that didn't align with DDIA's version of redundancy. I read up a little more about [this](https://www.nasa.gov/history/sts1/pages/computer.html#:~:text=On%20the%20Shuttle%2C%20four%20identical,data%20buses%2C%20in%20precise%20synchronization).
- There was a book called # Toward Zero Defect Programming that was mentioned by Dr. Stavely (Cleanroom technique)

Had a lot of fun doing this :)

*Note to self - Let's keep this up!*