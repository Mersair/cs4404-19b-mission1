# Login server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def run(server_class = HTTPServer, handler_class = BaseHTTPRequestHandler):
    server_address = ("", 7000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

class MyHandler(BaseHTTPRequestHandler):
    profiles = {"username": ("password", "audio"), "a": ("b", "c")}

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

    def verifyLogin(self, username, password, audio):
        try :
            profile = self.profiles[username]
        except:
            return 0
        return (profile[0] == password) and (profile[1] == audio)

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        print(data) # !!! cut

        username = data[data.find("username=") + 9:data.find("password=") -1]
        password = data[data.find("password=") + 9:data.find("audio=")-1]
        # !!! audio = data[data.find("audio=") + 6:]
        audio = "c"

        valid = self.verifyLogin(username, password, audio)

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
            contents = contents[:index] + "<p>Please enter a valid username, password, and audiofile.</p>" + contents [index:]
            self.wfile.write(contents)

run(handler_class=MyHandler)