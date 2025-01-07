---
title: FrozenLists
feed: show
date: 2025-01-07
---
### 7th Jan 2025

I happened to see this package - **FrozenList** - get installed when i was installing a set of requirements for an environment for work. I've not yet dived deep into which package frozenlist was a dependency for. 

But I still wanted to see what it was and Googled it. 

Turns out it's a package created to create a new data structure which is, well, a list that can be *frozen*.

What does it mean to freeze a list? Is  a FrozenList frozen by default?
No.

First when we use the data structure after installing it as a package - `pip install frozenlist`

```python
from frozenlist import FrozenList
list_ = FrozenList([1,3,4]
```

This list `list_` is at this point, a list that can be frozen. Till such time as it Is frozen, it is for all intents and purposes, a normal list. 

```python
list_.append(5)
```

results in `FrozenList([1,3,4,5])`. 

The real fun begins when you execute - 

```python
list_.freeze()
```

At this point, at least 2 special features emerge - 
a) The FrozenList `list_` is now immutable and any addition of further elements results in a Runtime exception.
b) The FrozenList `list_` is now hashable; meaning it can be used as a key for a dictionary, among other implications.

---
# So what?

As of now, I can't think of a reason to use this in my usecases in production. But since I found it as a dependency package, I'm sure one of the main packages I use must be using it. I will find out at some point.

In the meantime, here's a quick (useless) example I could think of where making the key a transparent hashed FrozenList atleast is indicative of what the value of the dictionary is w.r.t the key. 
Here, the values are the next element in the Arithmetic Progression that is the hashed key.

```python
from frozenlist import FrozenList

def find_the_next_term(*args):
    arg0 = args[0]
    n = len(arg0) + 1
    _next = arg0[0] + (n - 1) * (arg0[1] - arg0[0])
    return _next
```

```python
from frozenlist import FrozenList

d = {}  # Initialize the dictionary to store results

for i in range(3, 10):
    nums = FrozenList(range(1, i))
    nums.freeze()  # Freeze the FrozenList so it can be hashed
    print(nums)
    d[nums] = find_the_next_term(nums)

# Optional: Print the dictionary to see the results
print(d)
```

**Output -** 
```shell
<FrozenList(frozen=True, [1, 2])>
<FrozenList(frozen=True, [1, 2, 3])>
<FrozenList(frozen=True, [1, 2, 3, 4])>
<FrozenList(frozen=True, [1, 2, 3, 4, 5])>
<FrozenList(frozen=True, [1, 2, 3, 4, 5, 6])>
<FrozenList(frozen=True, [1, 2, 3, 4, 5, 6, 7])>
<FrozenList(frozen=True, [1, 2, 3, 4, 5, 6, 7, 8])>
```
