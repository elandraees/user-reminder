def threeSum(nums: list[int]) -> list[list[int]]:
    result = []

    for i in range(len(nums) - 2):
        j = i + 1
        while j < len(nums) - 1:
            k = j + 1
            while k < len(nums):
                if nums[i] + nums[j] + nums[k] == 0:
                    arr = [nums[i], nums[j], nums[k]]
                    arr.sort()
                    if arr not in result:
                        result.append(arr)
                k = k + 1
            j = j + 1

    return result


print(threeSum([-1, 0, 1, 2, -1, -4]))
