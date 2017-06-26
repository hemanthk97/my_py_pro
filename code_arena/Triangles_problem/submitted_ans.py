try:
   N = int(input())
   if N <= 0 and N >= 10**5:
       raise valueError(0)
   lis = []
   for _ in range(N):
       lis.append(sum(list(map(int,input().split()))))
   unique = 0
   for i in lis:
       if lis.count(i) == 1:
          unique = unique + 1
   print(unique)
except:
    print(0)
