from random import randrange
for i in range(1,100000):
    n = randrange(2000)
    if n < 100:
        n = 1
    elif n < 150:
        n = 2
    elif n < 175:
        n = 3
    print repr(n)+" "+repr(randrange(100))
