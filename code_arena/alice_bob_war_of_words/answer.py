N = int(input())
for i in range(N):
    alice = ''.join(input().split())
    bob = ''.join(input().split())
    alice_set = set(alice).difference(set(bob))
    bob_set = set(bob).difference(set(alice))
    if len(bob_set) == 0:
        print('You win some.')
    elif len(alice_set) == 0:
        print('You lose some.')
    elif len(alice_set) > 0 and len(bob_set) > 0 :
        print('You draw some.')
