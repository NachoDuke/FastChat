from src.MillerRabin import *
from src.generatePrime import *


def DHKey():
    #Takes in the prime number used as the modulus
    while(True):
        p=int(input("Enter a publicly known value for a prime modulus"))
        if(isPrime(p)):
            break
        else:
            print("Please enter a PRIME")
    
    #Takes in a generator for the previously inputted prime
    while(True):
        g=int(input("Enter a publicly known generator"))
        if(generator(g,p)):
            break
        else:
            print("Please enter a valid generator")
    
    #Takes in inputs for each party's secret number (the exponent)
    a=int(input("Enter the secret number chosen by the first party."))
    b=int(input("Enter the secret number chosen by the second party."))

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
