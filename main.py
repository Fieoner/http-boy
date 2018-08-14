#!/usr/bin/env python

import emulator
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

pyboy = emulator.init_emulator()

class GBHTTPRequestHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        try:
            if self.path.endswith('start'):
                emulator.gamestart(pyboy)
                self.send_response(200)
                self.send_header('Content-type', 'text-json')
                self.end_headers()
                self.wfile.write('ok')
            if self.path.endswith('up'):
                print('up')

        except IOError:
            self.send_error(404, 'not actually 404 but haha')

def main():
    print('starting...')



    server_address = ('127.0.0.1', 8123)
    httpd = HTTPServer(server_address, GBHTTPRequestHandler)
    print('server running...')
    httpd.serve_forever()





if __name__ == '__main__':
    main()
