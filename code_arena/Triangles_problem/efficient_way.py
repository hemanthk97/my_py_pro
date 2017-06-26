from collections import Counter

print(Counter([" ".join(sorted(raw_input().rstrip().split(" "))) for i in range(input())]).values().count(1))
