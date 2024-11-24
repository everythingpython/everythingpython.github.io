---
title: The Apache Airflow piece
feed: show
date: 2024-11-23
---
### 23rd Nov 2024

Yesterday I learnt how to get Google News articles using Python - [[Read GoogleNews using Python]]

The next piece I need for my planned workflow is running Airflow - locally - at first.

Airflow is a platform for scheduling and executing workflows. 
To give an example, suppose I run a restaurant. If it's not doing very well, you don't really need a workflow, so one way to reduce work is to be unsuccessful 😀👀
But if I run it successfully and get a lot of orders on a daily basis, I would like to have a mechanism to process everything. Let's say I have the following steps to be done - 
- Export the order receipts to a folder
- Extract key metrics out of them - say, date, orders, sales, discounts, gross profits, net profits
- Put these metrics into another sink - CSV/database etc.
- Generate a report out of the metrics and publish it or store it.

To do this, I can have a bunch of scripts, sure. But these are fairly disjoint yet dependent steps. And any of these can have points of failure in them. 
So Airflow is **one** way to ensure that we can execute each of these steps one by one and monitor each of them for success or failure thereby monitoring the entire **pipeline** for success or failure. 

In a more realistic sense, I'm trying to build a pipeline here as well. But for that I need to first Install Airflow - the Python library to use it, rather. 

So when I tried to install it in a `uv` virtual environment, this happened - 

![Alt Text](/assets/img/applications/airflow/airflow-err.png)

So after looking up a few [Github issues](https://github.com/google/re2/issues/437) , I thought I had the solution. Just install `abseil` and `re` on brew separately and then build `google-re2` 

![Alt Text](/assets/img/applications/airflow/install-abseil-re.png)

Hurray! 
Right?

![Alt Text](/assets/img/applications/airflow/no-dice.png)

NOPE :-/

Alright . Let's try this later.