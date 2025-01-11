---
title: import re
feed: show
date: 2025-01-11
---
### 11th Jan 2025

I was writing some tests for work today and I accidentally ended up using the re.match() function instead of re.search() function and I thought I'd write that as today's mini-TIL.

In a nutshell, 
> re.match() checks for a match only at the beginning of the string, 

whereas 

> re.search() checks for a match anywhere in the string.

Here's a quick example to illustrate the difference:

```python
import re

string = "Was it a car or a cat I saw?"
string2 = "Severus was impressed at Harry's Occlumency skills but he did not show it."
# re.match() will return None
print(re.match("cat", string))

# re.search() will return a match object
print(re.search("cat", string))

# re.match() will return a match object
print(re.match("Severus", string2))

# re.search() will return a match object
print(re.search("Severus", string2))
```

Output - 

```bash
None
<re.Match object; span=(18, 21), match='cat'>
<re.Match object; span=(0, 7), match='Severus'>
<re.Match object; span=(0, 7), match='Severus'>
```

---

Other regex functions that are worth reading about are -
- `re.findall()` : for finding all matches
- `re.finditer()` : for iteration
- `re.sub()`  :  for substituting one string with another in a string
- `re.split()` : for splitting a string based on a regex pattern

Here's an example using them all - 

```python

import re

string = "Was it a car or a cat I saw?"
string2 = "Hello, World!"
# re.match() will return None because the pattern does not match the beginning of the string
print(re.match("cat", string))

# re.match() will return a match object with the first match - checking in string 2
print(re.match("Hello", string2))


# re.search() will return a match object with the first match
print(re.search("cat", string))

# re.findall() will return a list of all matches as strings
print(re.findall("cat", string))

# re.finditer() will return an iterator of all matches as match objects
for match in re.finditer("cat", string):
    print(match)

# re.fullmatch() will return None because the pattern does not match the entire string
print(re.fullmatch("cat", string))

# re.split() will return a list of strings split by the pattern provided
print(re.split(" ", string))

# re.sub() will return a string with the substitution made
print(re.sub("cat", "dog", string))

```

Output - 

```bash
None
<re.Match object; span=(0, 5), match='Hello'>
<re.Match object; span=(18, 21), match='cat'>
['cat']
<re.Match object; span=(18, 21), match='cat'>
None
['Was', 'it', 'a', 'car', 'or', 'a', 'cat', 'I', 'saw?']
Was it a car or a dog I saw?
```