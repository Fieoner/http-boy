#!/usr/bin/env python

from emulator import Emulator
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from urlparse import urlparse, parse_qs
import base64
import cStringIO
import traceback


emulator = Emulator()

def htmlguarro(texto):
    return "<title>test</title><h3>"+texto+"</h3>"

class GBHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)
        path = parsed_url.path
        print(query)
        keys = ["up", "down", "left", "right", "b", "a", "start", "select"]
        try:
            if path == '/resume' or path == '/start':
                emulator.resumegame()
                self.send_response(200)
                self.send_header('Content-type', 'text-json')
                self.end_headers()
                ss_image = emulator.getScreenshot()
                buf = cStringIO.StringIO()
                ss_image.save(buf, format="PNG")
                ss_image.save('test.png')
                base64string = base64.b64encode(buf.getvalue())

                data = {}
                data['result'] = {
                    "type": 'simple',
                    "screenshot": base64string
                }

                data['options'] = {
                    "type": 'controller'
                }
                json_data = json.dumps(data, separators=(',',':'))
                self.wfile.write(json_data)
                return

            if path == '/execute':
                key = query["key"][0]
                if key not in keys:
                    return
                emulator.presskey(key)

                self.send_response(200)
                self.send_header('Content-type', 'text-json')
                self.end_headers()

                ss_image = emulator.getScreenshot()
                buf = cStringIO.StringIO()
                ss_image.save(buf, format="PNG")
                ss_image.save('test.png')
                base64string = base64.b64encode(buf.getvalue())

                data = {}
                data['result'] = {
                    "type": 'simple',
                    "screenshot": base64string
                }

                data['options'] = {
                    "type": 'controller'
                }
                json_data = json.dumps(data, separators=(',',':'))
                self.wfile.write(json_data)

            if path == '/read':
                try:
                    print("query: "+query["addr"][0])
                    address = int(query["addr"][0], 16)
                except:
                    print("it broke")
                    address = 0x0000
                value = emulator.read(address)
                cleantext = '0x'+hex(address).upper()[2:]+": "+'0x'+hex(value).upper()[2:]
                print(cleantext)

                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.end_headers()

                self.wfile.write(htmlguarro(cleantext))

        except Exception as e:
            self.send_error(404, 'not actually 404 but haha')
            print (e)
            traceback.print_exc()

def main():
    print('starting...')



    server_address = ('127.0.0.1', 8123)
    httpd = HTTPServer(server_address, GBHTTPRequestHandler)
    print('server running...')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
