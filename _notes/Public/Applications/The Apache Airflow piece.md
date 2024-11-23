---
title: The Apache Airflow piece
feed: show
date: 2024-11-23
---
### 23rd Nov 2024

Yesterday I learnt how to get Google News articles using Python - [[Read GoogleNews using Python]]

The next piece I need for my planned workflow is running Airflow - locally - at first.

So when I tried to install it in a `uv` virtual environment, this happened - 

![Alt Text](/assets/img/Applications/airflow/airflow-err.png)

So after looking up a few [Github issues](https://github.com/google/re2/issues/437) , I thought I had the solution. Just install `abseil` and `re` on brew separately and then build `google-re2` 

![Alt Text](/assets/img/Applications/airflow/install-abseil-re.png)

Hurray! 
Right?

![Alt Text](/assets/img/Applications/airflow/no-dice.png)

NOPE :-/

Alright . Let's try this later.