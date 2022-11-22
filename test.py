import rsa

usermsg = "hello my name is prem"
publicKey,privateKey = rsa.newkeys(1024)
usermsg = rsa.encrypt(usermsg.encode(),publicKey)
clean = rsa.decrypt(usermsg,privateKey).decode()
print(clean)