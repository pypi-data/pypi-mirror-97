#!/usr/bin/env python3

import socketserver
import http.server
import logging
import cgi
import signal
import sys, os, ast
import json
import configparser
from os.path import expanduser

LIST_VPC    = "listVpc"
LIST_SUBNET = "listSubnet"
LIST_EC2    = "listEc2"

class HttpServerServicesMock:

    def listVpc(self):
        response = self.buildAwsResponse(LIST_VPC)
        response["aws"]["vpc"] = []
        response["aws"]["vpc"].append({"vpcId":"vpc-123456789"})
        response["aws"]["vpc"].append({"vpcId":"vpc-01457"})
        response["aws"]["vpc"].append({"vpcId":"vpc-789456"})
        json_str = json.dumps(response)
        return json_str

    def listEc2(self, request_json):
        response = self.buildAwsResponse(LIST_EC2)
        params   = self.buildParams(request_json)
        response["aws"]["ec2"] = {}
        response["aws"]["ec2"]["vpcId"]     = params["vpcId"]
        response["aws"]["ec2"]["subnetId"]  = params["subnetId"]
        response["aws"]["ec2"]["instances"] = []
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-123456789","privateIp":"10.0.22.2","sg":"123"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-000100010","privateIp":"10.230.233.1","sg":"456"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5ewq25552jhg","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5q5525552ads1","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5w25552221","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5qwe5fds55ew2221","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5ew525552ew221","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5fds255522ewq21","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-55525552w21","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5fdsytryt25552f1","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5fdsa5552we21","privateIp":"10.1.22.2","sg":"789"})
        response["aws"]["ec2"]["instances"].append({"instanceId":"i-5ewq5525gfdgf21","privateIp":"10.1.22.2","sg":"789"})
        json_str = json.dumps(response)
        return json_str    

    def listSubnet(self, request_json):
        response = self.buildAwsResponse(LIST_SUBNET)
        params   = self.buildParams(request_json)
        response["aws"]["vpc"] = {}
        response["aws"]["vpc"]["vpcId"] = params["vpcId"]
        response["aws"]["vpc"]["subnets"] = []
        if params["vpcId"] == "vpc-01457":
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-AAAA","scope":"public"})
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-BBBB","scope":"private"})
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-CCCC","scope":"public"})
        elif params["vpcId"] == "vpc-789456": 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-D1","scope":"public"})
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-D2","scope":"public"})
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-D3","scope":"public"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-D4","scope":"private"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-D5","scope":"private"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-D6","scope":"public"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-D7","scope":"private"})
        elif params["vpcId"] == "vpc-123456789":
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-1", "scope":"public"})
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-2", "scope":"public"})
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-3", "scope":"public"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-4", "scope":"public"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-5", "scope":"private"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-6", "scope":"private"}) 
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-7", "scope":"private"})    
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-8", "scope":"private"})    
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-9", "scope":"public"})    
           response["aws"]["vpc"]["subnets"].append({"subnetId":"subnetId-x1x-10","scope":"public"})    
        json_str = json.dumps(response)
        return json_str

    def buildAwsResponse(self, action):
        response = {}
        response["aws"] = {}
        response["aws"]["status"] = "OK"
        response["aws"]["action"] = action
        return response
    def buildParams(self, json):
        params = {}
        for param in json["parameters"]:
           params[param["name"]] = {}
           params[param["name"]] = param["value"]
        return params   
