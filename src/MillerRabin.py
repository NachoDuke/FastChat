from src.generatePrime import *

def isPrime(n):
    #returns true if n is prime and false if n is composite
    #handling corner cases
    if(n<=1 or n==4):
        return False
    elif(n<=3):
        return True
    if(n%2==0):
        return False
    
    #obtaining d
    d=n-1
    s=0
    while(d%2==0):
        s+=1
        d=d//2
    #choose number of iterations
    k=10
    for i in range(k):
        if(not millerRabinTest(n,d,s)):
            return False
    return True


def millerRabinTest(n,d,s):
    #Each iteration of the test
    a=random.randint(2,n-2)
    x=modPower(a,d,n)
    if(x==1 or x==n-1):
        return True
    else:
        for j in range(s-1):
            x=(x*x)%n
            if(x==n-1):
                return True
        return False

