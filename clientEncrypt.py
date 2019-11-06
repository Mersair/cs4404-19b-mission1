import requests

print ("#############################")
print ("# Send a login POST request #")
print ("# Type 'valid' or 'invalid' #")
print ("#############################")

# Encrypt message
def encrypt(input):
    arr = []
    for c in input:
        arr.append(ord(c))
    for x in range(len(arr)):
        arr[x] = arr[x] << 1
    ret = ""
    for x in arr:
        add = str(x)
        rem = 3 - len(add)
        for x in range(rem):
            add = "0" + add
        ret += add
    return ret

# Decrypt sent messages
def decrypt(input):
    arr = []
    for c in range(len(input) // 3):
        curr = input[c * 3: c * 3 + 3]
        arr.append(int(curr))
    for x in range(len(arr)):
        arr[x] = arr[x] >> 1
    ret = ""
    for x in arr:
        ret += chr(x)
    return ret

if raw_input() == "valid":
    filepath = "real.txt"
    print ("Sending login POST data with a valid audio file...")
else:
    filepath = "imposter.txt"
    print ("Sending login POST data with a invalid audio file...")

with open(filepath, 'r') as file:
   recording = file.read()

URL = "http://" + raw_input("Enter the server URL and port (in format x.x.x.x:port): ")
PARAMS = "username=name&password=pass&audio=" + recording

ENCRYPTED = encrypt(PARAMS)

print(ENCRYPTED)
r = requests.Response
invalid = 0
try:
    r = requests.post(url = URL, data = ENCRYPTED)
except:
    print("Error sending to " + URL)
    invalid = 1

if not invalid:
    print ("### BEGIN DECRYPTED RESPONSE ###")
    output = r.text
    output2 = decrypt(output)
    print(output2)
    print ("### END RESPONSE ###")
