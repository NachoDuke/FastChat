import rsa

usermsg = "hello my name is prem"
publicKey,privateKey = rsa.newkeys(1024)
with open("private.pem","wb") as f:
    f.write(privateKey.save_pkcs1("PEM"))
with open("public.pem","wb") as f:
    f.write(publicKey.save_pkcs1("PEM"))

with open("public.pem","rb") as f:
    publicKey = rsa.PublicKey.load_pkcs1(f.read())
with open("private.pem","rb") as f:
    privateKey = rsa.PrivateKey.load_pkcs1(f.read())
usermsg = rsa.encrypt(usermsg.encode(),publicKey)
clean = rsa.decrypt(usermsg,privateKey).decode()
print(clean)