---
title: Reading DDIA - Part 2
feed: show
date: 25-09-2024
tags:
  - ddia
  - books
  - reading
---
## Chapter 1 - Thoughts - Cont.d 

In [[Reading DDIA - Part 1]] , I read about Reliability. The next section is Scalability . 
First let me talk about the assumptions I made about the term Scalability, what I understand from it prior to reading Martin Kleppman's thoughts on the topic - 

# What is a scalable system?


### My own thoughts prior to reading the section - 

Scale refers to how does a system grow. Growth can be needed for multiple reasons - 
- The amount of data to be processed can increase
- The number of users using the system over time can increase
- The number of users using the system at a single moment in time or certain periods of time can drastically increase. 
All of these contribute to the overall load on the system and it needs to be addressed. 
I've studied/worked with scaling of a system in two ways - horizontal scaling and vertical scaling. 
What is the difference? Horizontal scaling is adding more machines - physical or virtual to a cluster with a config that mimics the existing machines or maybe enhanced.
Vertical scaling is increasing the resources available on a single machine. 
The former is mostly used when there is a need for more parallelization whereas the latter is used when there is a need for a workload to use more resources (compute, memory etc.)

---

Now let's read the section .
*Reading section*

---

>❓  *What is the throughput of a system that receives and handled 3 requests per minute, each request of size 2 GB?*

### Thoughts after reading the section

Some of what I've mentioned from my learnings is echoed in the book as well - 
a)  Scale cannot be thought about without talking about the load on the system. 
- To describe it, a few *load parameters* are considered. 
	- The parameters themselves depend on the architecture of the system. Some examples include : requests per second to a web server, ratio of reads to writes in a database, the number of simultaneous users in a chat room, hit rate on a cache etc.
- The example of Twitter is given. Makes sense since it's a high load, high concurrency system processing tens of thousands of tweets across the world per second. 
b) The second thing mentioned in relation to scale is the performance of the system itself. 
- The metrics of interest here are **throughput**  in a batch processing system and **response time** in an online system.
	- Throughput is the number of requests that can be processed per second or the total amount of time that a job takes to process a dataset of a certain size. 
	- Response time is the amount of time for a system between when the request is made by a client and when it receives a response
	- Response times are best thought of in terms of percentile - typically the 95th, the 99th and 99.9th percentiles, abbreviated p95, p99 and p999.
	For example, if the 95th percentile response time is 1.5 seconds, it means that 95 out of 100 requests take less than 1.5 seconds. Used in SLOs and SLAs
		
> 💻 I didn't completely understand this right away, so I decided to write a small program to see how this would be computed - 


```python
import numpy as np

# List of response times (in milliseconds)
response_times = [150, 200, 250, 300, 180, 220, 210, 190, 500, 800, 1000]

# Calculate percentiles
p95 = np.percentile(response_times, 95)
p99 = np.percentile(response_times, 99)
p999 = np.percentile(response_times, 99.9)

print(f'p95: {p95} ms')
print(f'p99: {p99} ms')
print(f'p999: {p999} ms')
```

> Response - 


```bash
(py312) abhiram@everythingpython everythingpython.github.io % python percentile.py
The response times are : [150, 200, 250, 300, 180, 220, 210, 190, 500, 800, 1000]
p95: 900.0 ms
p99: 980.0000000000001 ms
p999: 998.0000000000005 ms
```

Basically if you computed for what value is 95% of the response times lesser than that value. Here the p95 = 900.ms

Finally what is discussed in this section is the way to cope with said load i.e. via horizontal or  vertical scaling.
But what is practically followed is a hybrid approach since there is no one-size-fits-all. Also some systems are elastic in nature - wherein the usage determines the resources allocated. 

>📝 This actually reminds me of my [M.Tech thesis paper](https://ieeexplore.ieee.org/abstract/document/7015482) - Workload Fingerprinting using Adaboost, where based on the study of 4 workloads taxing compute, memory and I/O , we tried to predict what a future workload might consume along these axes. 

One nice example he gives in the section (which is what the question earlier is based on) is that a system that is designed to handle 3 requests per minute where each request has a 2 GB payload looks very different from a system that is designed to handle 100000 requests per second of 1 kB per request payload - even though their payloads are identical. 

The ideal architecture that handles scale is built around which operations are assumed to be more frequent and which operations are assumed to be rare. 

I'm looking forward to reading more about how this book addresses the problems and solutions around Scale. 

*Note to self - Let's keep this up!*