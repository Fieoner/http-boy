#!/usr/bin/env python

import emulator
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from urlparse import urlparse, parse_qs

pyboy = emulator.init_emulator()

class GBHTTPRequestHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)
        path = parsed_url.path
        print(query)
        keys = ["up", "down", "left", "right", "b", "a", "start", "select"]
        try:
            if path == '/start':
                emulator.gamestart(pyboy)
                self.send_response(200)
                self.send_header('Content-type', 'text-json')
                self.end_headers()
                self.wfile.write('ok')
                return

            if path == '/execute':
                key = query["key"][0]
                if key not in keys:
                    return
                emulator.presskey(pyboy, key)

                screenshot = pyboy.window.getScreenBuffer()

                self.send_response(200)
                self.send_header('Content-type', 'text-json')
                self.end_headers()

                n_1 = len(screenshot[0])
                n_2 = len(screenshot)

                print("n_1")
                print(n_1)
                print("n_2")
                print(n_2)

                to_string_pixels = list(map(lambda x: list(map(lambda y: str(y), x)), screenshot))
                to_string_rows = list(map(lambda x: ','.join(x), to_string_pixels))
                to_string_all = '&'.join(to_string_rows)

                data = {}
                data['result'] = {
                    "type": 'simple',
                    "screenshot": to_string_all
                }

                data['options'] = {
                    "type": 'controller'
                }
                json_data = json.dumps(data, separators=(',',':'))

                # for line in screenshot:
                #     line = ",".join(str(line))
                # screenshot = "&".join(str(screenshot))
                # for line in to_string:
                #    self.wfile.write(line)
                #    self.wfile.write("\n")
                self.wfile.write(json_data)

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
