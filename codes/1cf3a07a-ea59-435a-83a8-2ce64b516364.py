n = int(input())
nums = list(map(int, input().split()))
target = int(input())

mp = {}
for i, num in enumerate(nums):
    diff = target - num
    if diff in mp:
        print(mp[diff], i)
        break
    mp[num] = i