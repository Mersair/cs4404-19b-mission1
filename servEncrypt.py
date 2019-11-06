# Login server with encryption

# needed to install c++ compiler for python !!!
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Server HTTP request handler which encrypts messages
class MyHandler(BaseHTTPRequestHandler):
    # Set up profile and encryption
    file = open("realbase64.txt", "r").read()
    aud = file[file.find(",")+3:]
    profiles = {"name": ("pass", aud)}

    # On a GET request, return the request html file or a 404 response if file not found, encrypted
    def do_GET(self):
        try:
            if (self.path == "/"):
                path = "/index"
            path = path[1:]
            f = open(path + ".html", "r")
            contents = f.read()
            f.close()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            contents = self.encrypt(contents)
            self.wfile.write(contents)
        except:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            message = "Error 404: File not found"
            message = self.encrypt(message)
            self.wfile.write(message)

    # Check whether the login information is valid
    def verifyLogin(self, username, password, audio):
        try :
            profile = self.profiles[username]
        except:
            return 0
        return (profile[0] == password) and (profile[1] == audio)

    # Encrypt a string
    def encrypt(self, input):
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
    def decrypt(self, input):
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

    # On a POST, decrypt and parse for the login information and validate it
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        data = self.decrypt(data)
        print(data)

        username = data[data.find("username=") + 9:data.find("&password=")]
        password = data[data.find("password=") + 9:data.find("&audio=")]
        audio = data[data.find("audio=") + 6:]
        audio = urllib.unquote(audio).decode('utf8')
        audio = audio[audio.find(",")+3:]
        audio = audio.encode("ascii")

        valid = self.verifyLogin(username, password, audio)

        # Return the logged-in page if valid, otherwise return the home page with an error message, encrypted
        if valid:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("login.html", "r")
            contents = f.read()
            f.close()
            contents = self.encrypt(contents)
            self.wfile.write(contents)
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("index.html", "r")
            contents = f.read()
            f.close()
            index = contents.find("Login to your account")
            contents = contents[:index] + "<p><font color=\"red\">Error: Please enter a valid username, password, and audiofile.</p></font>" + contents [index:]
            contents = self.encrypt(contents)
            self.wfile.write(contents)

# Run the server
def run(server_class = HTTPServer, handler_class = BaseHTTPRequestHandler):
    port = int(input("Enter server port number: "))
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run(handler_class=MyHandler)
