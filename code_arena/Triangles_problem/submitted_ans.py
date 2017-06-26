try:
   N = 5
   a = [[7, 6, 5],[5, 7, 6],[8, 2, 9],[2, 3, 4],[2, 4, 3]]
   if N <= 0 and N >= 10**5:
       raise valueError(0)
   lis = []
   for i in range(N):
       lis.append(sum(a[i]))
   unique = 0
   for i in lis:
       if lis.count(i) == 1:
          unique = unique + 1
   print(unique)
except:
    print(0)
