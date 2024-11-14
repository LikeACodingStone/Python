import os
from cryptography.fernet import Fernet
def write_key():
    newKey = Fernet.generate_key()
    curDir = os.getcwd()
    keyDir = os.path.dirname(curDir) + os.sep + "GenKey"
    if not os.path.exists(keyDir):
        os.makedirs(keyDir)
    existKeyCount = 0
    for key in os.listdir(keyDir):
        if not key.endswith(".key"):
            continue
        existKeyCount = existKeyCount + 1
    trKeyName = keyDir + os.sep + "key" + str(existKeyCount) + ".key"
    with open(trKeyName, "wb") as key_file:
        key_file.write(newKey)
        
write_key()
