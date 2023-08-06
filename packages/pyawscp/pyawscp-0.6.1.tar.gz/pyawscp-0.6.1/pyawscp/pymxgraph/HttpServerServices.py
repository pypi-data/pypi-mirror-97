#!/usr/bin/env python3

import socketserver
import http.server
import logging
import cgi
import signal
import sys, os, ast
import json
import configparser
import datetime
from os.path import expanduser

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from pyawscp.Config import Config
from pyawscp.Utils import Utils


LIST_VPC            = "listVpc"
LIST_SUBNET         = "listSubnet"
LIST_EC2            = "listEc2"
LIST_SECURITY_GROUP = "listSecurityGroup"

class HttpServerServices:

    def __init__(self):
        FILE_INI = expanduser("~") + "/.pyawscp/" + "pyawscp.ini"
        self.config = Config()
        if os.path.exists(FILE_INI):
           configFileIni = configparser.ConfigParser()
           configFileIni.read(FILE_INI)
           self.config.awsProfile         = configFileIni["PREFERENCES"]["aws-profile"]
           self.config.awsRegion          = configFileIni["PREFERENCES"]["aws-region"]
           self.config.awsTags            = ast.literal_eval(configFileIni["PREFERENCES"]["aws-tags"])
           self.config.printResults       = configFileIni["PREFERENCES"]["print-results"] in ['True','true']
           self.config.tableLineSeparator = configFileIni["PREFERENCES"]["table-line-separator"] in ['True','true']
           if "assume-role" in configFileIni["PREFERENCES"]:
              self.config.assumeRole      = configFileIni["PREFERENCES"]["assume-role"]
           else:
              self.config.assumeRole      = ""
           if "mfa-serial" in configFileIni["PREFERENCES"]:
              self.config.mfaSerial       = configFileIni["PREFERENCES"]["mfa-serial"]
           else:
              self.config.mfaSerial       = ""

    def listVpc(self):
        ec2Client              = self.botoSession().client('ec2')
        vpcs                   = ec2Client.describe_vpcs()
        response               = self.buildAwsResponse(LIST_VPC)
        response["aws"]["vpc"] = []
        for vpc in vpcs["Vpcs"]:

            tags = []
            if "Tags" in vpc:
               for tag in vpc["Tags"]:
                   tags.append({"key":tag["Key"],"value":tag["Value"]})

            response["aws"]["vpc"].append(
                {
                    "vpcId":vpc["VpcId"],
                    "cidrBlock":vpc["CidrBlock"],
                    "tags": tags
                }
            )
        json_str = json.dumps(response)
        return json_str
    
    def listSubnet(self, request_json):
        ec2Client = self.botoSession().client('ec2')
        params    = self.buildParams(request_json)
        filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    params["vpcId"]
                ]
            }
        ]
        subnets  = ec2Client.describe_subnets( Filters=filters )
        response = self.buildAwsResponse(LIST_SUBNET)
        response["aws"]["vpc"]            = {}
        response["aws"]["vpc"]["vpcId"]   = params["vpcId"]
        response["aws"]["vpc"]["subnets"] = []

        for subnet in subnets["Subnets"]:
            tags = []
            if "Tags" in subnet:
               for tag in subnet["Tags"]:
                   tags.append({"key":tag["Key"],"value":tag["Value"]})

            isPublic = self._checkSubnetIsPublic(ec2Client, subnet["SubnetId"])    
            public   = "public" if isPublic else "private"

            subnetJson = {
                "subnetId":subnet["SubnetId"],
                "vpcId":subnet["VpcId"],
                "scope":public,
                "availabilitZone":subnet["AvailabilityZone"],
                "availabilitZoneId":subnet["AvailabilityZoneId"] if "AvailabilityZoneId" in subnet else "",
                "availableIpAddressCount":subnet["AvailableIpAddressCount"],
                "cidrBlock":subnet["CidrBlock"],
                "defaultForAz":subnet["DefaultForAz"],
                "state":subnet["State"],
                "subnetArn":subnet["SubnetArn"] if "SubnetArn" in subnet else "",
                "tags": tags
            }
            
            response["aws"]["vpc"]["subnets"].append(subnetJson)
        json_str = json.dumps(response)
        return json_str

    def _checkSubnetIsPublic(self, ec2Client, subnetId):
        filters=[{'Name': 'association.subnet-id','Values': [subnetId]}, 
                 {'Name': 'route.destination-cidr-block','Values': ['0.0.0.0/0']},
                 {'Name': 'route.gateway-id','Values': ['igw-*']}
        ]
        route_tables = ec2Client.describe_route_tables(Filters=filters)
        routeTableIgw = route_tables['RouteTables']
        if len(routeTableIgw) >= 1:
            return True
        else:
            return False

    def listEc2(self, request_json):
        ec2Client = self.botoSession().client('ec2')
        params    = self.buildParams(request_json)
        filters=[
            {
                'Name': 'subnet-id',
                'Values': [
                    params["subnetId"]
                ]
            }
        ]
        ec2s  = ec2Client.describe_instances( Filters=filters )
        response = self.buildAwsResponse(LIST_EC2)
        response["aws"]["ec2"] = {}
        response["aws"]["ec2"]["vpcId"]     = params["vpcId"]
        response["aws"]["ec2"]["subnetId"]  = params["subnetId"]
        response["aws"]["ec2"]["instances"] = []

        for reservations in ec2s["Reservations"]:
           for instance in reservations["Instances"]:
               tags = []
               for tag in instance["Tags"]:
                   tags.append({"key":tag["Key"],"value":tag["Value"]})
   
               securityGroups = []
               for sg in instance["SecurityGroups"]:
                   securityGroups.append({"groupId":sg["GroupId"],"groupName":sg["GroupName"]})
   
               blockDeviceMappings = []
               for bdm in instance["BlockDeviceMappings"]:
                   blockDeviceMappings.append({
                                "deviceName":bdm["DeviceName"],
                                "ebs":{
                                    "attachTime":bdm["Ebs"]["AttachTime"],
                                    "deleteOnTermination":bdm["Ebs"]["DeleteOnTermination"],
                                    "status":bdm["Ebs"]["Status"],
                                    "volumeId":bdm["Ebs"]["VolumeId"],
                                }
                              })        
   
               publicIpAddress = ""
               if "PublicIpAddress" in instance:
                   publicIpAddress = instance["PublicIpAddress"]

               cpuValue = {}
               if "CpuOptions" in instance:
                   cpuValue["coreCount"]      = instance["CpuOptions"]["CoreCount"]
                   cpuValue["threadsPerCore"] = instance["CpuOptions"]["ThreadsPerCore"]

               instanceJson = {
                   "subnetId":instance["SubnetId"],
                   "vpcId":instance["VpcId"],
                   "instanceId":instance["InstanceId"],
                   "imageId":instance["ImageId"],
                   "instanceType":instance["InstanceType"],
                   "launchTime":instance["LaunchTime"],
                   "privateDnsName":instance["PrivateDnsName"],
                   "privateIpAddress":instance["PrivateIpAddress"],
                   "publicIpAddress":publicIpAddress,
                   "publicDnsName":instance["PublicDnsName"],
                   "state":{"code":instance["State"]["Code"],"name":instance["State"]["Name"]},
                   "ebsOptimized":instance["EbsOptimized"],
                   "rootDeviceName":instance["RootDeviceName"],
                   "rootDeviceType":instance["RootDeviceType"],
                   "securityGroups":securityGroups,
                   "cpu":cpuValue,
                   "blockDeviceMappings":blockDeviceMappings,
                   "tags": tags
               }
               
               response["aws"]["ec2"]["instances"].append(instanceJson)

        json_str = json.dumps(response, default = self.myConverter)
        return json_str

    def listSecurityGroup(self, request_json):
        ec2Client = self.botoSession().client('ec2')
        params    = self.buildParams(request_json)
        filters=[
            {
                'Name': 'group-id',
                'Values': [
                    params["groupId"]
                ]
            }
        ]
        securityGroups  = ec2Client.describe_security_groups( Filters=filters )
        response = self.buildAwsResponse(LIST_SECURITY_GROUP)
        response["aws"]["ec2"] = {}
        response["aws"]["ec2"]["securityGroup"] = []

        for securityGroup in securityGroups["SecurityGroups"]:

            tags = []
            for tag in securityGroup["Tags"]:
                tags.append({"key":tag["Key"],"value":tag["Value"]})


            ingresses = []
            for ingress in securityGroup["IpPermissions"]:
                ipRanges = []
                for ipRange in ingress["IpRanges"]:
                    ipRanges.append({
                        "cidrIp":ipRange["CidrIp"],
                        "description":ipRange["Description"],
                    })

                ingresses.append({
                    "fromPort":ingress["FromPort"],
                    "ipProtocol":ingress["IpProtocol"],
                    "ipRanges": ipRanges,
                    "toPort":ingress["ToPort"]
                })

            egresses = []
            for egress in securityGroup["IpPermissionsEgress"]:
                ipRanges = []
                for ipRange in egress["IpRanges"]:
                    ipRanges.append({
                        "cidrIp":ipRange["CidrIp"],
                        "description":ipRange["Description"],
                    })

                egresses.append({
                    "ipProtocol":egress["IpProtocol"],
                    "ipRanges": ipRanges
                })        


            sgJson = {
                   "groupId":securityGroup["GroupId"],
                   "description":securityGroup["Description"],
                   "vpcId":securityGroup["VpcId"],
                   "ingress": ingresses,
                   "egress": egresses,
                   "tags": tags
            }
               
            response["aws"]["ec2"]["securityGroup"].append(sgJson) 

        json_str = json.dumps(response, default = self.myConverter)
        return json_str          

        """ 
        for reservations in ec2s["Reservations"]:
           for instance in reservations["Instances"]:
               tags = []
               for tag in instance["Tags"]:
                   tags.append({"key":tag["Key"],"value":tag["Value"]})
   
               securityGroups = []
               for sg in instance["SecurityGroups"]:
                   securityGroups.append({"groupId":sg["GroupId"],"groupName":sg["GroupName"]})
   
               blockDeviceMappings = []
               for bdm in instance["BlockDeviceMappings"]:
                   blockDeviceMappings.append({
                                "deviceName":bdm["DeviceName"],
                                "ebs":{
                                    "attachTime":bdm["Ebs"]["AttachTime"],
                                    "deleteOnTermination":bdm["Ebs"]["DeleteOnTermination"],
                                    "status":bdm["Ebs"]["Status"],
                                    "volumeId":bdm["Ebs"]["VolumeId"],
                                }
                              })        
   
               publicIpAddress = ""
               if "PublicIpAddress" in instance:
                   publicIpAddress = instance["PublicIpAddress"]

               instanceJson = {
                   "subnetId":instance["SubnetId"],
                   "vpcId":instance["VpcId"],
                   "instanceId":instance["InstanceId"],
                   "imageId":instance["ImageId"],
                   "instanceType":instance["InstanceType"],
                   "launchTime":instance["LaunchTime"],
                   "privateDnsName":instance["PrivateDnsName"],
                   "privateIpAddress":instance["PrivateIpAddress"],
                   "publicIpAddress":publicIpAddress,
                   "publicDnsName":instance["PublicDnsName"],
                   "state":{"code":instance["State"]["Code"],"name":instance["State"]["Name"]},
                   "ebsOptimized":instance["EbsOptimized"],
                   "rootDeviceName":instance["RootDeviceName"],
                   "rootDeviceType":instance["RootDeviceType"],
                   "securityGroups":securityGroups,
                   "cpu":{"coreCount":instance["CpuOptions"]["CoreCount"],"threadsPerCore":instance["CpuOptions"]["ThreadsPerCore"]},
                   "blockDeviceMappings":blockDeviceMappings,
                   "tags": tags
               }
               
               response["aws"]["ec2"]["instances"].append(instanceJson)

        json_str = json.dumps(response, default = self.myConverter)
        return json_str  """  

    def myConverter(self,o):
        if isinstance(o, datetime.datetime):
           #return o.__str__()    
           return o.strftime('%d-%m-%Y %H:%M:%S')

    def botoSession(self):
        return self.config.botoSession()

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

    def getParamValue(self, request_json, paraName): 
        for params in request_json["parameters"]:
            if params["name"] == paraName:
               return params["value"]
        return None    

if __name__ == '__main__':
   httpServices = HttpServerServices()
   #print(httpServices.listVpc())
   #print(httpServices.listSubnet({'action': 'listSubnet', 'parameters': [{'name': 'vpcId', 'value': 'vpc-090a0f7286ab4281c'}]}))
   #print(httpServices.listEc2({'action': 'listEc2', 'parameters': [{'name': 'vpcId', 'value': 'vpc-01c6810fb391d215b'}, {'name': 'subnetId', 'value': 'subnet-0313b32f6f116c352'}]}))
   print(httpServices.listSecurityGroup({'action': 'listSecurityGroup', 'parameters': [{'name': 'groupId', 'value': 'sg-07dcfaec3ee966a3d'}]}))

      
