---
title: Neetcode For Fun - 1
feed: show
date: 2025-02-19
---
Solving https://neetcode.io/problems/is-anagram . Started at 1:29 AM.


![](/assets/img/lc/nc-1/nc-1-1.png)

---

Let's think about this for a minute. 

A word 'w1' is an anagram of a word 'w2' if all the characters in w1 belong in w2. Duplicates included.

So the simplest solution would be to go through every letter in w1 and then check if it is there in w2. 
That's a O(n^2) complexity because to check against the second string, each letter would have to be compared against. 
**Let's code it up :** 

```python
class Solution:
	def isAnagram(self, s: str, t: str) -> bool:
		anagram = True
		for i in s: 
			if i not in t:
				anagram = False
				break
		return anagram
			
```

### Analysis level 2 : 

The problem with this solution while it works in theory is that it checks for "membership" i.e. belonging-to-a-string but it doesn't check if the number of times a character belongs in w1 is the same as in w2. 

Therefore it would fail for 

```markdown
s="xx"
t="x"
```

Accounting for frequency of characters : 

```python
class Solution:
	def isAnagram(self, s: str, t: str) -> bool:
		letter_counter_s = {i:s.count(i) for i in s}
		letter_counter_t = {i:t.count(i) for i in t}
		anagram = True
		for k, v in letter_counter_s.items():
			if k in letter_counter_t:
				if letter_counter_t[k] != v:
					anagram = False
					break
			else:
				anagram = False
				break
		return anagram
```

### Analysis level 3 :

Again, this Looks like it works but it fails when the first string is shorter than the second string. (Can you see why?)

![](/assets/img/lc/nc-1/nc-1-2.png)

Therefore, straight away rejecting the possibility of an anagram if the lengths of the strings don't match - 

```python
class Solution:
	def isAnagram(self, s: str, t: str) -> bool:
		if len(s) != len(t):
			return False
		letter_counter_s = {i:s.count(i) for i in s}
		letter_counter_t = {i:t.count(i) for i in t}
		anagram = True
		for k, v in letter_counter_s.items():
			if k in letter_counter_t:
				if letter_counter_t[k] != v:
					anagram = False
					break
			else:
				anagram = False
				break
		return anagram
```

And that yielded the complete case - 

![](/assets/img/lc/nc-1/nc-1-3.png)

Atleast functionally....
Let's see on Leetcode how slow our solution is. 

![](/assets/img/lc/nc-1/nc-1-4.png)

As expected, from a time complexity perspective, we're trailing towards the end, beating only 5% of all solutions. So let's examine this a little more. 

What if instead of an array look-up , I used a get method? Would that help?
```python
class Solution:
	def isAnagram(self, s: str, t: str) -> bool:
		if len(s) != len(t):
			return False
		letter_counter_s = {i:s.count(i) for i in s}
		letter_counter_t = {i:t.count(i) for i in t}
		anagram = True
		for k, v in letter_counter_s.items():
			if letter_counter_t.get(k) != v:
				anagram = False
				break
		return anagram
```

It did not. 

```python
class Solution:
	def isAnagram(self, s: str, t: str) -> bool:
		if len(s) != len(t):
			return False
		tl = list(t)
		for i in s:
			if i in tl:
				tl.remove(i)
			else:
				return False
		return True
```

This got a little better (down from 5800 ms to 900 ms). But still poor.

![](nc-1-5.png)

2.15 AM I will continue this in the morning. 