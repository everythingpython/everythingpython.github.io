from typing import List
from timer import timer_decorator


class Solution:

    @timer_decorator
    def hasDuplicate(self, nums: List[int]) -> bool:
        if len(set(nums)) < len(nums):
            return True
        return False


class Solution2:
    @timer_decorator
    def containsDuplicate(self, nums: List[int]) -> bool:
        nums2 = (set(nums))
        if len(nums2) != len(nums):
            return True
        return False


class Solution3:
    @timer_decorator
    def sort_check_duplicate(self, nums):
        nums.sort()
        set_ = set()
        for i in nums:
            if i in set_:
                return False
            set_.add(i)
        return True


test_cases = [
    [1, 2, 3, 3],
    [1, 2, 3, 4]
]
soln = Solution()
soln2 = Solution2()
soln3 = Solution3()
for i in test_cases:
    print(soln.hasDuplicate(i))
    print(soln2.containsDuplicate(i))
    print(soln3.sort_check_duplicate(i))
