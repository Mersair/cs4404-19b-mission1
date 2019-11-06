import requests

print ("#############################")
print ("# Send a login POST request #")
print ("# Type 'valid' or 'invalid' #")
print ("#############################")

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

print(PARAMS)
r = requests.Response
invalid = 0
try:
    r = requests.post(url = URL, data = PARAMS)
except:
    print("Error sending to " + URL)
    invalid = 1

if not invalid:
    print ("### BEGIN DECRYPTED RESPONSE ###")
    print(r.text)
    print ("### END RESPONSE ###")
