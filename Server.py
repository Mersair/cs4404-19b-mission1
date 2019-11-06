# Login server
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Server HTTP request handler
class MyHandler(BaseHTTPRequestHandler):
    # Set up valid profile and audio file
    file = open("realbase64.txt", "r").read()
    aud = file[file.find(",")+3:]
    profiles = {"name": ("pass", aud)}

    # On a GET request, return the request html file or a 404 response if file not found
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
            self.wfile.write(contents)
        except:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Error 404: File not found")

    # Check whether the login information is valid
    def verifyLogin(self, username, password, audio):
        try :
            profile = self.profiles[username]
        except:
            return 0
        return (profile[0] == password) and (profile[1] == audio)

    # On a POST, parse for the login information and validate it
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        print(data)

        username = data[data.find("username=") + 9:data.find("&password=")]
        password = data[data.find("password=") + 9:data.find("&audio=")]
        audio = data[data.find("audio=") + 6:]
        audio = urllib.unquote(audio).decode('utf8')
        audio = audio[audio.find(",")+3:]
        audio = audio.encode("ascii")

        valid = self.verifyLogin(username, password, audio)

        # Return the logged-in page if valid, otherwise return the home page with an error message
        if valid:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("login.html", "r")
            contents = f.read()
            f.close()
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
            self.wfile.write(contents)

# Run the server
def run(server_class = HTTPServer, handler_class = BaseHTTPRequestHandler):
    port = int(input("Enter server port number: "))
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run(handler_class=MyHandler)