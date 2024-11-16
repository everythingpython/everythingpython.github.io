---
title: 
feed: show
date: 2024-11-15
tags:
  - leetcode
  - easy
---
### 15th Nov 2024

I think I'm going to be more regular in trying out Leetcode problems going forward - or grinding Leetcode, as the kids call it these days. 
I'm doing this mainly so my logical skills will stay sharp and I hope to find some nice Python concepts along the way that can then fuel my blog.

Today I solved one of the easy problems - Finding if there's a duplicate element in a list of numbers. This is [Leetcode problem # 217](https://leetcode.com/problems/contains-duplicate/) in the 'easy' category.


Now mind you, I did not actually have to find which numbers were duplicate. So that was one layer of complexity avoided.

Just to make things clearer (and they probably have been for a while now) , a list of numbers is given - say `[1,2,3,4,4]` . If there are any duplicates, I'm supposed to return `True` , else `False`. In this array's case, since the element `4` is repeated, I should return `True`.

The immediate solution I thought of was predicated on the idea that a `set` datatype/ datastructure. Since a set does not allow duplicates, the idea was that converting the list provided to a set would convert it into a collection of unique elements. 
Now if the number of elements in the converted data structure is the same as in the original list provided, then we can conclude that there were no duplicates to begin with. 

That leads us to the implementation as follows : 

```python
def check_duplicates(array):
	if len(set(nums)) < len(nums):  
	    return True  
return False

```

Fairly straightforward. 
Since the creation of a set takes a full traversal of the list, the time complexity of this solution is `O(n)`.

---

I was looking up other solutions of this on Leetcode and one of them involved sorting the array prior to finding the duplicate. 

That would have resulted in an `O(nlog(n))` time complexity. 
For an array that's very large in size, this would probably be a better approach since the latter grows logarithmically and `O(n)` grows linearly. 

The implementation for that would be - 

```python
def sort_check_duplicate(self, nums):  
    nums.sort()  
    set_ = set()  
    for i in nums:  
        if i in set_:  
            return False  
        set_.add(i)  
    return True
```