try:
   N = int(input())
   if N <= 0 and N >= 10:
       raise valueError(0)
   for _ in range(N):
      A1 = list(map(int,input().split()))
      A2 = list(map(str,input().split()))
      for i in range(A1[0],len(A2)):
          if A2[i] in set(A2[:i]):
             print('YES')
          else:
             print('NO')
except:
    print(0)
