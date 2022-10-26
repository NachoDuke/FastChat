from src.DiffieHellman import *

if __name__=="__main__":
    key,prime=DHKey()
    print("Key: ",key)

    msg=int(input("Enter a numeric message"))
    encryptedMsg=encryptMessage(msg,prime,key)
    print("Encrypted Message: ",encryptedMsg)
    decryptedMsg=decryptMessage(encryptedMsg,prime,key)
    print("Decrypted Message: ",decryptedMsg)