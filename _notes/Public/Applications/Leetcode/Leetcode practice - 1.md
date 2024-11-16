---
title: LC Num 21
date: 15-04-2024
feed: show
tags:
  - leetcode
  - easy
---
### 15-04-2024

[21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

First I didn't understand the problem I think. In the sense that I accepted the inputs as two lists and returned a list - Python list. 
Then I read it and realized they want the operation in Linked lists. 

i took some time to recall how to move along a list and finally figured it out. 

The other thing that gave me a minor ankle break was when the test case was two empty lists. 

Handled that as well eventually. 

Here's the cumulative code - 


```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        c = []
        a =[]
        b=[]

        i = list1
        j = list2
        while i:
            a.append(i.val)
            i = i.next
        while j:
            b.append(j.val)
            j = j.next
        i, j = 0 , 0
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                c.append(a[i])
                i = i + 1
            else:
                c.append(b[j])
                j = j+1
        if j < len(b):
            c.extend(b[j:])
        elif i < len(a):
            c.extend(a[i:])
        if len(c) > 0:
            listNode3 = ListNode(c[0],None)
            head = listNode3
            for i in c[1:]:
                temp_node = ListNode(i,None)
                listNode3.next = temp_node
                listNode3 = listNode3.next
        else:
            head = None
        
        return head
```

And boom!

![Alt Text](/assets/img/lc/lc21/lc21_1.png)

---
By minorly changing the above code to not create lists out of ListNodes initially, a speedup of 2 seconds can be achieved - 

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        c = []
        a =[]
        b=[]

        i = list1
        j = list2
        while i and j:
            if i.val < j.val:
                c.append(i.val)
                i = i.next
            else:
                c.append(j.val)
                j = j.next
        if j:
            while j:
                c.append(j.val)
                j = j.next
            
        elif i:
            while i :
                c.append(i.val)
                i = i.next
        if len(c) > 0:
            listNode3 = ListNode(c[0],None)
            head = listNode3
            for i in c[1:]:
                temp_node = ListNode(i,None)
                listNode3.next = temp_node
                listNode3 = listNode3.next
        else:
            head = None
        
        return head
```


![Alt Text](/assets/img/lc/lc21/lc21_2.png)