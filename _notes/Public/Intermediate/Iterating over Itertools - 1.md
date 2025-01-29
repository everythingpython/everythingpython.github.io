---
title: Iterating over Itertools - 1
feed: show
date: 2024-10-31
---
#### 31st Oct 2024


I had the opportunity to work with some of the functions in the `itertools` package in Python over the month and I thought before the month ends in a few minutes, I’ll write about a few of them -

**a) The Count function -**

This is useful when you want to iterate from a starting number , say ‘n’ up to an indeterminate number that you do not know at the point of starting the iterator. The example below assumes the end limit to be 10 numbers from the point of starting the counter. The second argument to the ‘count’ function is a “step” parameter.

i.e. Starting at 1, and counting ahead in steps of 3 - giving us 1,4,7,10… etc

**b) Cycle Function**

The `cycle` function is useful when you need to repeatedly iterate over a sequence without knowing how many times it will be needed. It’s perfect for scenarios where you have a pattern that needs to repeat until a condition is met. For instance, in the example below, we loop through `"EverythingPython"` till we hit a counter of 20 characters.

**c) Filterfalse Function**

Sometimes, you need to filter out certain items based on a condition, rather than include them. This is where `filterfalse` comes in. In the example below, we use `filterfalse` to exclude the words in `cities` from `full_string`.

```python

import itertools

# Count function
for i in itertools.count(1, 3):
    if i > 10:
        break
    print(i)

counter = 0
# Cycle function
for i in itertools.cycle("EverythingPython"):
    if counter < 20:
        print(i, end="")
    else:
        break

    counter = counter + 1

print("\n")

full_string = "The weather in Chennai is very hot."
cities = ["Chennai", "Bangalore"]
# Filterfalse function
for i in itertools.filterfalse(lambda x: x in cities, full_string.split()):
    print(i, end=" ")
```

This post only talks about 3 of the itertools functions. But more will come soon!