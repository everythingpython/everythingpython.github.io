from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        c = []
        a = []
        b = []

        i = list1
        j = list2
        while i:
            a.append(i.val)
            i = i.next
        while j:
            b.append(j.val)
            j = j.next
        i, j = 0, 0
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                c.append(a[i])
                i = i + 1
            else:
                c.append(b[j])
                j = j + 1
        if j < len(b):
            c.extend(b[j:])
        elif i < len(a):
            c.extend(a[i:])
        if len(c) > 0:
            listNode3 = ListNode(c[0], None)
            head = listNode3
            for i in c[1:]:
                temp_node = ListNode(i, None)
                listNode3.next = temp_node
                listNode3 = listNode3.next
        else:
            head = None

        return head
