class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            if i < target:
                for j in range(i + 1, len(nums)):
                    if nums[i] + nums[j] == target:
                        return [i, j]


r = Solution()
r.twoSum(nums=[0, 4, 3, 0], target=0)
825029135
