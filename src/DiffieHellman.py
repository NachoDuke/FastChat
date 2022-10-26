from cgi import print_arguments
from src.MillerRabin import *
from src.generatePrime import *

LOWER_LIMIT=1000
UPPER_LIMIT=10000

def DHKey():
    #Generates a random prime for the diffie-hellman protocol
    p=getPrime(LOWER_LIMIT,UPPER_LIMIT)
    
    #Obtains a random generator for the prime generated above
    while(True):
        g=random.randint(1,p)
        if(generator(g,p)):
            break
    
    #Printing out the prime and the generator (temporary)
    print("Prime: ",p)
    print("Generator: ",g)

    #Randomly generates numbers for each party's secret number (the exponent)
    a=random.randint(2,50)
    b=random.randint(2,50)

    atob=modPower(g,a,p)
    btoa=modPower(g,b,p)

    #Printing the new data shared publicly
    print("The first party has publicly shared ",atob)
    print("The second party has publicly shared ",btoa)

    #Calculation of secret key by the first party
    key1=modPower(btoa,a,p)
    #Calculation of secret key by the second party
    key2=modPower(atob,b,p)

    if(key1==key2):
        #Success
        print("The keys are equal")
    else:
        #Failed
        print("The keys are not equal")

    return (key1,p)

def encryptMessage(message,prime,key):
    return (message+key)%prime

def decryptMessage(message,prime,key):
    return (message-key)%prime
    
