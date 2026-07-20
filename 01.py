n = int(input("请输入一个整数："))
sum = 0
n0 = n
deg = len(str(n))
while n > 0:
    i = n % 10
    sum += i **deg
n = n // 10

if sum == n0:
    print(f"{n0} 是水仙花数")
else:
    print(f"{n0} 不是水仙花数")