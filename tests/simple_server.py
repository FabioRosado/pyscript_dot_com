import contextlib
import json
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle a GET request by returning the JSON data"""
        if self.path == "/exception":
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.send_header("Connection", "close")  # Optionally close the connection
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

        elif self.path == "/test-cookies":
            # Get cookies from the request
            cookies = self.headers.get("Cookie")
            if cookies:
                # Convert cookies to a dictionary
                cookies = dict(c.split("=") for c in cookies.split("; "))
            else:
                cookies = {}

            self._send_headers()
            json_data = json.dumps(cookies)
            self.wfile.write(json_data.encode("utf-8"))

        elif self.path == "/test-headers":
            # Get headers from the request
            headers = dict(self.headers.items())

            self._send_headers()
            json_data = json.dumps(headers)
            self.wfile.write(json_data.encode("utf-8"))

        elif self.path == "/my/api-proxies/test":
            self._send_headers()
            json_data = json.dumps(
                {"message": "You called the 'test' proxy with a 'GET' method!"}
            )
            self.wfile.write(json_data.encode("utf-8"))
        else:
            self._send_headers()

            # Create a dictionary to represent your JSON data
            data = {"message": "Hello, this is the server response!"}

            # Convert the dictionary to JSON string
            json_data = json.dumps(data)

            # Write the JSON string to the response body
            self.wfile.write(json_data.encode("utf-8"))

    def do_POST(self):
        """Handle a POST request by returning the same data"""
        # Get the content length of the request body so we
        # can read it
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        self._send_headers()

        # Now let's just send the same data back
        self.wfile.write(post_data)

    def _send_headers(self, content_type="application/json"):
        """Send the headers for the response"""  # Return a 200 response
        self.send_response(200)
        # Set the right headers
        self.send_header("Content-type", content_type)
        self.end_headers()


def start_server():
    port = get_free_port()
    server_address = (
        "127.0.0.1",
        port,
    )
    httpd = TCPServer(server_address, MyHandler)
    httpd.allow_reuse_address = True
    httpd.allow_reuse_port = True

    # Run the server in a separate thread
    server_thread = Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Store server information (address, etc.) in a data structure
    server_info = {
        "address": f"http://{server_address[0]}:{server_address[1]}",
        "httpd": httpd,
        "thread": server_thread,
    }

    return server_info


def stop_server(server_info):
    server_info["httpd"].close_connection = True

    # Shut down the server
    server_info["httpd"].shutdown()

    # Close the socket to release the port
    with contextlib.suppress(Exception):
        server_info["httpd"].socket.close()

    # Wait for the server thread to finish
    server_info["thread"].join()


def get_free_port():
    """Get free port to run server on.

    We can't just use port 0 upstream because it seems to block,
    plust we need to try to bind to the port first to confirm that
    is available.

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    port = s.getsockname()[1]
    s.close()
    return port
