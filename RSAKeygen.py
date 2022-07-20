from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import os

hostname = os.uname().nodename
bitsize = 4096

def genKeys():
    folder = os.path.exists("keys")
    if(folder == True):
        os.mkdir("keys")
        
    print(f"==> Generating {bitsize}-bit RSA Keys",end="",flush=True)
    keyPair = RSA.generate(bitsize)
    pubKey = keyPair.publickey()
    print(" > [DONE]")

    print("==> Exporting Public Key",end="",flush=True)
    f = open(f'keys/{hostname}_pubkey.pem', 'wb')
    f.write(pubKey.exportKey('PEM'))
    f.close()
    print(" > [DONE]")

    print("==> Exporting Private Key",end="",flush=True)
    f = open(f'keys/{hostname}_privkey.pem', 'wb')
    f.write(keyPair.exportKey('PEM'))
    f.close()
    print(" > [DONE]")

def verifyKeys():
    pubkeypem = os.path.exists(f"keys/{hostname}_pubkey.pem")
    privkeypem = os.path.exists(f"keys/{hostname}_privkey.pem")
    if(pubkeypem == True and privkeypem == True):
        return True
    else:
        return False

 ## -- Read Keys -- ##
def getKeysAddr():
    # - Read Private Key - ##
    with open(f'keys/{hostname}_privkey.pem', 'rb') as privkeyfile:
        privkeypem = privkeyfile.read()
    privkey = RSA.importKey(privkeypem)
    # - Read Public Key - ##
    with open(f'keys/{hostname}_pubkey.pem', 'rb') as pubkeyfile:
        pubkeypem = pubkeyfile.read()
    pubkey = RSA.importKey(pubkeypem)
    # - Get Keys Addresses - $
    pubKeyAddr = str.split(str(pubkey),"at ")[1]
    privKeyAddr = str.split(str(privkey),"at ")[1]
    return privKeyAddr,pubKeyAddr

def main():
    global hostname,bitsize
    if(verifyKeys() == False):
        genKeys()
    privAddr,pubAddr = getKeysAddr()
    print(privAddr,pubAddr)
    
if __name__ == '__main__':
    main()
