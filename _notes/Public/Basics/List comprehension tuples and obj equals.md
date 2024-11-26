---
title: List comprehension tuples and obj equals
feed: show
date: 2024-11-21
---
### 21st Nov 2024

2 Quick TILs today - 

1) You cannot use a tuple in a list comprehension without params - 
![Alt Text](/assets/img/basics/lc_tuples/lc_tuples_1.png)

The correct syntax is 
`[(i,j) for i in a for j in b`


2) The usage of obj= within a formatted string during printing results in both the object's name as well its value separated by an "=" being printed - 

In the imge below, `a` is a list as used earlier. Therefore - 

![Alt Text](/assets/img/basics/lc_tuples/lc_tuples_2.png)

3) WIP