#!/usr/bin/env python3

import socketserver
import http.server
import threading
import logging
import cgi
import signal
import sys, os, ast
import json
import configparser
from urllib.parse import unquote
from os.path import expanduser
from pygments import highlight, lexers, formatters

from pyawscp.pymxgraph.HttpServerServicesMock import HttpServerServicesMock
from pyawscp.pymxgraph.HttpServerServices import HttpServerServices

sys.path.append('..')
from pyawscp.Utils import Utils
from pyawscp.Emoticons import Emoticons

signal.signal(signal.SIGINT, signal.SIG_DFL)

PORT = 5679
LIST_VPC            = "listVpc"
LIST_SUBNET         = "listSubnet"
LIST_EC2            = "listEc2"
LIST_SECURITY_GROUP = "listSecurityGroup"

class HttpServerHandler(http.server.SimpleHTTPRequestHandler):

    VERBOSE     = False
    HTTP_SERVER = None

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_str = self.listVpc()
        self.wfile.write(json_str.encode(encoding='utf_8'))

    def do_OPTIONS(self):           
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        path        = self.path
        contentType = self.headers['Content-Type']

        if "/export" == path:
            self.exportImage(contentType)
        else:
            self.servicesCall(contentType)

    def exportImage(self, contentType):
        if "application/x-www-form-urlencoded" == contentType:
           contentLength = self.headers['Content-Length']
           request_bytes = self.rfile.read(int(contentLength))
           request_str   = request_bytes.decode('utf-8')
           request_str   = unquote(request_str)

           self.send_response(200)
           self.send_header('Access-Control-Allow-Origin', '*')
           self.send_header('Access-Control-Allow-Methods', 'POST')
           self.send_header("Content-Type", "image/png")
           self.end_headers()

           self.wfile.write(request_bytes)         

    def servicesCall(self, contentType):
        if "application/json" == contentType:
            contentLength = self.headers['Content-Length']
            request_bytes = self.rfile.read(int(contentLength))
            request_str   = request_bytes.decode('utf-8')
            request_json  = json.loads(request_str)

            if HttpServerHandler.VERBOSE:
               print(">>--->\033[93m REQUEST =================================================================\033[0m")
               print(highlight(Utils.dictToJson(request_json), lexers.JsonLexer(), formatters.TerminalFormatter()))
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST')
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_json = self.processRequest(request_json)

            if HttpServerHandler.VERBOSE:
               print(">>--->\033[93m RESPONSE =================================================================\033[0m")
               print(highlight(response_json, lexers.JsonLexer(), formatters.TerminalFormatter()))
            
            self.wfile.write(response_json.encode(encoding='utf_8'))         
        else:
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST')
            self.send_header("Content-Type", "application/json")
            self.end_headers()

    def showAction(self,action):
        if HttpServerHandler.VERBOSE:
           print(">>--->\033[93m ACTION   =========   \033[32m{}\033[93m".format(action))

    def processRequest(self, request_json):
        response_json = ""
        if  LIST_VPC == request_json["action"]:
            self.showAction("List VPCs")
            response_json = self.listVpc()
        elif LIST_SUBNET == request_json["action"]:
            self.showAction("List Subnets")
            response_json = self.listSubnet(request_json)
        elif LIST_EC2 == request_json["action"]:
            self.showAction("List EC2s")
            response_json = self.listEc2(request_json)
        elif LIST_SECURITY_GROUP == request_json["action"]:
            self.showAction("List Security Groups")
            response_json = self.listSecurityGroup(request_json)    
        else:
            response = {}
            response["aws"] = {}
            response["aws"]["status"] = "Action " + request_json["action"] + " not recognized!"
            response_json = json.dumps(response)
        return response_json      
                

    def listVpc(self):
        httpServices  = HttpServerServices()
        #httpServicesMock = HttpServerServicesMock()
        return httpServices.listVpc()

    def listEc2(self, request_json):
        httpServices = HttpServerServices()
        return httpServices.listEc2(request_json)

    def listSubnet(self, request_json):
        httpServices = HttpServerServices()
        #httpServicesMock = HttpServerServicesMock()
        return httpServices.listSubnet(request_json)

    def listSecurityGroup(self, request_json):
        httpServices = HttpServerServices()
        return httpServices.listSecurityGroup(request_json)    

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

shutdown_evt = threading.Event()

class HttpServer:
    def __init__(self, verbose):
        self.httpd   = None
        self.verbose = verbose
        HttpServerHandler.VERBOSE = self.verbose
    def run(self):
        self.httpd = ThreadedTCPServer(('127.0.0.1', PORT), HttpServerHandler)
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(Emoticons.ok() + " \033[93mAWS Navigator serving\033[0m")
        print(Emoticons.ok() + " Press \033[93mENTER\033[0m to shutdown...")
        input("")
        shutdown_evt.set()
        self.httpd.shutdown()
        self.httpd.server_close()

if __name__ == '__main__':
   httpServer = HttpServer(True)
   httpServer.run()