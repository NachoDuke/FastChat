import math
import random


def gcd(a,b):
    #This function returns the gcd of the two numbers entered as parameters
    while True:
        temp=a%b
        if(temp==0):
            break
        else:
            a=b
            b=temp
    return b

def sieve(n):
    #Implements the sieve of Eratosthenes to obtain a list of primes less than n
    if(n<2):
        return []
    else:
        length=n-1
        sqr=int(math.sqrt(n))
        prime=[]
        for i in range(length):
            prime.append(True)
        for i in range(2,sqr+1):
            if(not prime[i-2]):
                continue
            else:
                multiple=2*i
                while(multiple<=n):
                    prime[multiple-2]=False
                    multiple+=i
        
        primes=[]
        for i in range(length):
            if(prime[i]):
                primes.append(i+2)
        return primes

def getPrimes(lower,upper):
    #Gets a list of primes between the lower and upper bounds (parameters)
    if(lower>upper):
        return []
    if(upper<2):
        return []
    primeList=sieve(int(math.sqrt(upper)))
    if(lower<2):
        lower=2
    length=upper-lower+1
    prime=[]
    for i in range(length):
        prime.append(True)
    for p in primeList:
        factor=math.floor(lower/p)
        multiple=p*factor
        while(multiple<=upper):
            if(multiple>=lower):
                prime[multiple-lower]=False
            multiple+=p
    
    primes=[]
    for i in range(length):
        if(prime[i]):
            primes.append(i+lower)
    return primes

def getPrime(lower,upper):
    #Returns a random prime number in the given interval
    primes=getPrimes(lower,upper)
    index=random.randint(0,len(primes)-1)
    return primes[index]


def generator(g,p):
    #checks if g is a generator of p
    if(g>=p):
        return False
    l=[]
    for i in range(0,p-1):
        if(pow(g,i)%p in l):
            return False
        else:
            l.append(pow(g,i)%p)
    return True

def modPower(g,a,p):
    #a function to obtain (g^a) mod p
    res=1
    for i in range(a):
        res=res*g
        res=res%p
    return res
