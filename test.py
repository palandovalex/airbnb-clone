from random import random

print("Hello world")

num_experts = 15
exeprt_fail_chance = 0.40
num_right_experts = 0

for i in range(10000):
    num_right = 0
    for j in range(num_experts):
        if random() > exeprt_fail_chance:
            num_right += 1
    if num_right > num_experts//2:
        num_right_experts += 1

print(num_right_experts/10000.0)


s = "I love Python"
n = s.find("t")
print(s[:n])

s_temp = s
n = s_temp.find(" ")
while n >= 0:
    s_temp = s_temp[:n]+s_temp[n+1:]
    n = s_temp.find(" ")
print(s_temp)

nums = ['22', '68', '110', '89', '31', '12']
nums_int = [int(i) for i in nums]
print(nums_int)

print(map(lambda i: i**2, nums_int))

del nums_int[-1]
print(nums_int)
a0 = dict([("1", 2)])
print("1" in a0)
