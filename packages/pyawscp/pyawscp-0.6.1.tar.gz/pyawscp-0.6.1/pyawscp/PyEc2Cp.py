#!/usr/bin/env python3

import boto3
import logging
import sys
import json
import os, re
import random
from botocore.exceptions import ClientError
from datetime import datetime
from pyawscp.Functions import Functions
from pyawscp.Utils import Utils, Style
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.CsvDrawIo import CsvDrawIo
from pyawscp.CsvDrawIoNetworking import CsvDrawIoNetworking
from pyawscp.TableArgs import TableArgs
from pygments import highlight, lexers, formatters

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

class PyEc2CP:

    def __init__(self, config):
        self.config = config
        self.tempCredentials = None

    # A main function called from user
    # Check if a specific subnetId is Public looking up its Route Table for a IGW-* 0.0.0.0/0
    # arguments:
    #      subnetId: mandatory
    def subnetIsPublic(self):
        ec2      = self.botoSession().client('ec2')
        subnetId = self.config.commandArguments

        if not subnetId:
           resultTxt = "Where is the SubnetId? You didn't tell me which one " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.SUBNET_IS_PUBLIC,resultTxt, self.config, "", True)

        filters=[{'Name': 'association.subnet-id','Values': [subnetId]}, 
                 {'Name': 'route.destination-cidr-block','Values': ['0.0.0.0/0']},
                 {'Name': 'route.gateway-id','Values': ['igw-*']}]
        if self.config.awsTagsToFilter():
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               ) 
        route_tables = ec2.describe_route_tables(Filters=filters)

        jsonResult = ""
        if self.config.printResults: 
           jsonResult = Utils.dictToJson(route_tables)

        routeTableIgw = route_tables['RouteTables']
        if len(routeTableIgw) >= 1:
           resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RESET + " is " + Style.GREEN + "PUBLIC" +  Style.RESET + "\n"

           printSeparator = False
           for route in routeTableIgw[0]["Routes"]:
               if route["DestinationCidrBlock"] == '0.0.0.0/0':
                  if route["State"]:
                     if not printSeparator:
                        resultTxt = resultTxt + Utils.separator()
                        printSeparator = True
                     resultTxt = resultTxt + "\n"
                     resultTxt = resultTxt + ' '.ljust(2,' ') + "- State...........: " + Style.GREEN + route['State'] + Style.RESET 
                  if route["GatewayId"]:
                     if not printSeparator:
                        resultTxt = resultTxt + Utils.separator()
                        printSeparator = True
                     resultTxt = resultTxt + "\n"
                     resultTxt = resultTxt + ' '.ljust(2,' ') + "- GatewayId.......: " + Style.GREEN + route['GatewayId'] + Style.RESET    
                  if routeTableIgw[0]["VpcId"]:
                     if not printSeparator:
                        resultTxt = resultTxt + Utils.separator()
                        printSeparator = True
                     resultTxt = resultTxt + "\n"
                     resultTxt = resultTxt + ' '.ljust(2,' ') + "- Vpc Id..........: " + Style.GREEN + routeTableIgw[0]['VpcId'] + Style.RESET   
           return Utils.formatResult(Functions.FUNCTIONS[Functions.SUBNET_IS_PUBLIC]["name"],resultTxt, self.config, jsonResult, True, None)
        else:
           resultTxt = ""
           subnet = ec2.describe_subnets(Filters=[{'Name':'subnet-id','Values':[subnetId]}])
           if len(subnet['Subnets']) == 0:
               resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RED + " not found! " + Emoticons.ops() +  Style.RESET
           else:   
               if self.config.awsTagsToFilter():
                  resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RESET + " is NOT " + Style.GREEN + "PUBLIC" +  Style.RESET + ", or either did not pass the Filters Tag! " + + Emoticons.thumbsUp()
               else:   
                  resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RESET + " is NOT " + Style.GREEN + "PUBLIC" +  Style.RESET + " " + Emoticons.thumbsUp() 
           return Utils.formatResult(Functions.FUNCTIONS[Functions.SUBNET_IS_PUBLIC]["name"],resultTxt, self.config, "", True, None)     
    
    # Reusable Function, used by: 
    # -lisSubtnetsVpc
    def _checkSubnetIsPublic(self, subnetId, extraFilters):
        ec2 = self.botoSession().client('ec2')
        filters=[{'Name': 'association.subnet-id','Values': [subnetId]}, 
                 {'Name': 'route.destination-cidr-block','Values': ['0.0.0.0/0']},
                 {'Name': 'route.gateway-id','Values': ['igw-*']}
        ]
        route_tables = ec2.describe_route_tables(Filters=filters)
        routeTableIgw = route_tables['RouteTables']
        if len(routeTableIgw) >= 1:
            return True
        else:
            return False    

    # List all Subnets from a VPC
    def listSubnetsVpc(self):
        ec2   = self.botoSession().client('ec2')

        vpcId     = ""
        isPublic  = False
        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        if "," in self.config.commandArguments:
           vpcId = self.config.commandArguments.split(",")[0]
           tableArgs.setArguments(self.config.commandArguments)
           if "ispublic" in self.config.commandArguments:
               isPublic = True
        else:
           vpcId = tableArgs.cleanPipelineArguments()

        if not vpcId:
           resultTxt = "Where is the VpcId? You didn't tell me which VPC " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.LIST_SUBNETS_VPC,resultTxt, self.config, "", True, tableArgs)

        filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcId
                ]
            }
        ]
        if self.config.awsTagsToFilter():
           # Environment Tags set
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )

        subnets = ec2.describe_subnets( Filters=filters )

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(subnets)

        resultTxt = ""
        if len(subnets["Subnets"]) >= 1:
            resultTxt = "The VPC " + Style.GREEN + vpcId + Style.RESET + " has " + Style.GREEN + str(len(subnets["Subnets"])) + Style.RESET + " Subnets\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"

            idx_lin=0
            header      = ["#","Subnet Id", "Availability Zone", "CIDR Block", "Available IP Address Count"]
            if isPublic:
                header.append("Is Public?")
            if tableArgs.showTags:
                header.append("Tags")    
            prettyTable = PrettyTable(header)
            
            for subnet in subnets["Subnets"]:
                idx_lin += 1

                columns = [ str(idx_lin), subnet['SubnetId'], subnet['AvailabilityZone'],  subnet['CidrBlock'], subnet['AvailableIpAddressCount'] ]

                if isPublic:
                   resultIsPublic = self._checkSubnetIsPublic(subnet['SubnetId'], None)
                   result = "--- "
                   if resultIsPublic:
                      result = "PUBLIC"
                   columns.append(result)
                if tableArgs.showTags:
                   tags = Utils.formatPrintTags(subnet['Tags'])
                   columns.append(tags)

                prettyTable.addRow(columns)

            if (int(tableArgs.sortCol) - 1) > len(columns):
                tableArgs.sortCol = "1"
            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.ascendingOrder(not tableArgs.desc)
            result = "VPC...: " + Style.GREEN + vpcId + Style.RESET + "\n\n" + prettyTable.printMe("listSubnetsVpc",self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_SUBNETS_VPC]["name"], result, self.config, jsonResult, True, tableArgs)
        else:
           resultTxt = ""
           try: 
             vpc = ec2.describe_vpcs(VpcIds=[vpcId])
             if not self.config.awsTagsToFilter():
                resultTxt = "VPC was found, but there's no Subnet associated. " + Emoticons.ops()
             else:   
                resultTxt = "VPC was found, but there's no Subnet associated or either did not pass the Filters Tag! " + Emoticons.ops()
           except ClientError as e:
             if "InvalidVpcID.NotFound" == e.response['Error']['Code']:
                resultTxt = "VPC with the Id " + Style.GREEN + vpcId + Style.RESET + " was not found! " + Emoticons.ops() +  Style.RESET
             else:    
                resultTxt = "Exception! ❌💣 " + Style.GREEN + e.response['Error']['Code'] + Style.RESET
           except:
             resultTxt = sys.exc_info + " ❌💣 "
           return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_SUBNETS_VPC]["name"], resultTxt, self.config, "", True, tableArgs)

    # List all VPCs
    def listVpc(self):
        ec2 = self.botoSession().client('ec2')

        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        listSubnets    = False
        subnetIsPublic = False

        if "subnets" in self.config.commandArguments:
           listSubnets    = True
        if "ispublic" in self.config.commandArguments:
           subnetIsPublic = True   

        filters = []
        if self.config.awsTagsToFilter():
           # Tags from Environment
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )
        vpcs = ec2.describe_vpcs(Filters=filters)

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
           jsonResult = Utils.dictToJson(vpcs)

        data         = {}
        data["vpcs"] = []
        resultTxt = ""
        if len(vpcs["Vpcs"]) >= 1:
            resultTxt = "List of VPCs, total of " + Style.GREEN + str(len(vpcs["Vpcs"])) + Style.RESET + "\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"

            idx_lin=0
            header = ["#","VPC Id", "CIDR Block", "Default"]
            if listSubnets:
               header = ["#","VPC Id", "CIDR Block", "Default", "Subnet Id", "Subnet CIDR Block", "AZ", "Available IP Count"] 
               if subnetIsPublic:
                  header.append("Is Public?")
            if tableArgs.showTags:
               header.append("VPC Tags")       

            prettyTable = PrettyTable(header)
            for vpc in vpcs["Vpcs"]:
                idx_lin += 1

                vpcId       = vpc['VpcId']
                cidrBlock   = vpc['CidrBlock']
                default     = "Default" if vpc['IsDefault'] else "---"
                columns     = None
                subnetsDict = []
                azs         = []
                # Asked to list the subnets of each VPC?
                if listSubnets:
                   subnets = ec2.describe_subnets( Filters=[{'Name': 'vpc-id','Values': [vpc['VpcId']]}])
                   idx_subnet_lin = 0

                   for subnet in subnets["Subnets"]:
                       idx_subnet_lin += 1
                       lblSubnet = subnet['SubnetId'] + "  (" + str(idx_subnet_lin) + ")"
                       cidrBlockSubnet = subnet['CidrBlock']
                       az = subnet['AvailabilityZone']
                       availableIpdAddressCount = subnet['AvailableIpAddressCount']
                       
                       if az not in azs:
                          azs.append(az)

                       columns = [ idx_lin, vpcId, cidrBlock, default, lblSubnet, cidrBlockSubnet, az, availableIpdAddressCount ]

                       # Asked to inform if the Subnet is Public? 
                       resultSubnetIsPublic = None
                       if subnetIsPublic:
                          resultSubnetIsPublic = "--- "
                          if self._checkSubnetIsPublic(subnet['SubnetId'], None) :
                             resultSubnetIsPublic = "PUBLIC"
                          columns.append(resultSubnetIsPublic)
                       if tableArgs.showTags:
                          tags = Utils.formatPrintTags(vpc['Tags'])
                          columns.append(tags)   

                       prettyTable.addRow(columns)
                       
                       publicPrivateSubnet = ""
                       if resultSubnetIsPublic:
                          publicPrivateSubnet = resultSubnetIsPublic
                       
                       subnetsDict.append({
                          "subnetId": subnet['SubnetId'],
                          "cidrBlock": subnet['CidrBlock'],
                          "az": subnet['AvailabilityZone'],
                          "availableIpAddressCount": subnet['AvailableIpAddressCount'],
                          "public": publicPrivateSubnet
                       })

                   prettyTable.addSeparatorGroup()    
                else:   
                   columns = [ idx_lin, vpcId, cidrBlock, default ]
                   if tableArgs.showTags:
                      tags = Utils.formatPrintTags(vpc['Tags'])
                      columns.append(tags)
                   prettyTable.addRow(columns)

                vpcName = ""
                if 'Tags' in vpc:
                  for tag in vpc['Tags']:
                     if tag["Key"].lower() == "name":
                        vpcName = tag["Value"]
                        break
                
                data["vpcs"].append({
                   "vpcId": vpcId,
                   "cidrBlock": cidrBlock,
                   "name": vpcName,
                   "default": vpc['IsDefault'],
                   "azs": azs,
                   "subnets": subnetsDict
                })

            if (int(tableArgs.sortCol) - 1) > len(columns):
                sortCol = "1"

            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.ascendingOrder(not tableArgs.desc)
            result = "VPCs " + "\n\n" + prettyTable.printMe("listVpc",self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_VPC]["name"], result, self.config, jsonResult, True, tableArgs)    
        else:
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_VPC]["name"], " No VPC found " + Emoticons.ops(), self.config, jsonResult, True, tableArgs)

    
    # Generate Data to create a traditional AWS VPC Networking diagram(VPCs, Subnets, CIDRBlocks, RTs, NACLs, etc.) for DrawIo CVS Import
    def drawNetworking(self):
        ec2 = self.botoSession().client('ec2')

        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        addRouteTables = False
        addNacls       = False
        addTgws        = False
        addRtTgws      = False
        subnetIsPublic = True

        if "routetables" in self.config.commandArguments:
           addRouteTables = True
        if "nacls" in self.config.commandArguments:
           addNacls       = True
        if "tgws" in self.config.commandArguments:
           addTgws        = True
        if "rttgws" in self.config.commandArguments:
           addRtTgws      = True  
        if "all" in self.config.commandArguments:
           addRouteTables = True
           addNacls       = True
           addTgws        = True
           addRtTgws      = True

        filters = []
        if self.config.awsTagsToFilter():
           # Tags from Environment
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )
        vpcs = ec2.describe_vpcs(Filters=filters)

        data         = {}
        data["vpcs"] = []
        data["tgws"] = []
        resultTxt = ""

        if addTgws:
           # Attachments TransitGateway
           attachmentByTgw = {}
           #attachments     = ec2.describe_transit_gateway_attachments(Filters=filters)
           attachments     = ec2.describe_transit_gateway_attachments()
           for attachment in attachments["TransitGatewayAttachments"]:

              if not attachment["TransitGatewayId"] in attachmentByTgw:
                 attachmentByTgw[attachment["TransitGatewayId"]] = []
               
              attachmentByTgw[attachment["TransitGatewayId"]].append({
                  "transitGatewayAttachmentId": attachment["TransitGatewayAttachmentId"],
                  "transitGatewayOwnerId": attachment["TransitGatewayOwnerId"],
                  "resourceOwnerId": attachment["ResourceOwnerId"],
                  "resourceType": attachment["ResourceType"],
                  "resourceId": attachment["ResourceId"],
                  "state": attachment["State"],
                  "association": {
                     "transitGatewayRouteTableId": attachment["Association"]["TransitGatewayRouteTableId"],
                     "state": attachment["Association"]["State"]
                  }
              })
           # Route Tables (with its Routes) for TransitGateway
           tgwRouteTableByTgw = {}
           #tgwRouteTables = ec2.describe_transit_gateway_route_tables(Filters=filters)
           tgwRouteTables = ec2.describe_transit_gateway_route_tables()
           for tgwRt in tgwRouteTables["TransitGatewayRouteTables"]:
               if not tgwRt["TransitGatewayId"] in tgwRouteTableByTgw:
                  tgwRouteTableByTgw[tgwRt["TransitGatewayId"]] = []

               # Search Routes for the TGW Route Table
               routesTgwRouteTable = ec2.search_transit_gateway_routes(TransitGatewayRouteTableId=tgwRt["TransitGatewayRouteTableId"],
                     Filters=[
                        {
                              'Name': 'state',
                              'Values': [
                                 'active',
                              ]
                        },
                     ])
               
               routes = []
               for route in routesTgwRouteTable["Routes"]:
                  attchs = []
                  for att in route["TransitGatewayAttachments"]:
                      attchs.append({
                         "transitGatewayAttachmentId": att["TransitGatewayAttachmentId"],
                         "resourceId": att["ResourceId"],
                         "resourceType": att["ResourceType"]
                      })
                  routes.append({
                      "destinationCidrBlock": route["DestinationCidrBlock"],
                      "attachments": attchs
                  })
               tgwRouteTableByTgw[tgwRt["TransitGatewayId"]].append({
                  "routeTableId": tgwRt["TransitGatewayRouteTableId"],
                  "routes": routes
               })

           tgws = ec2.describe_transit_gateways(Filters=filters)
           for tgw in tgws["TransitGateways"]:

               data["tgws"].append({
                  "transitGatewayId": tgw["TransitGatewayId"],
                  "description": tgw["Description"] if "Description" in tgw else "",
                  "state": tgw["State"],
                  "ownerId": tgw["OwnerId"],
                  "options": {
                     "associationDefaultRouteTableId": tgw["Options"]["AssociationDefaultRouteTableId"] if "AssociationDefaultRouteTableId" in tgw["Options"] else "",
                     "defaultRouteTablePropagation": tgw["Options"]["DefaultRouteTablePropagation"] if "DefaultRouteTablePropagation" in tgw["Options"] else "",
                     "propagationDefaultRouteTableId": tgw["Options"]["PropagationDefaultRouteTableId"] if "PropagationDefaultRouteTableId" in tgw["Options"] else ""
                  },
                  "attachments": attachmentByTgw[tgw["TransitGatewayId"]] if tgw["TransitGatewayId"] in attachmentByTgw else [],
                  "routeTables": tgwRouteTableByTgw[tgw["TransitGatewayId"]] if tgw["TransitGatewayId"] in tgwRouteTableByTgw else []
               })
        
        if len(vpcs["Vpcs"]) >= 1:
            resultTxt = "List of VPCs, total of " + Style.GREEN + str(len(vpcs["Vpcs"])) + Style.RESET + "\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"

            idx_lin=0
            for vpc in vpcs["Vpcs"]:
                idx_lin += 1

                vpcId       = vpc['VpcId']
                cidrBlock   = vpc['CidrBlock']
                default     = "Default" if vpc['IsDefault'] else "---"
                subnetsDict = []
                azs         = []
                # Asked to list the subnets of each VPC?
                
                subnets = ec2.describe_subnets( Filters=[{'Name': 'vpc-id','Values': [vpc['VpcId']]}])
                idx_subnet_lin = 0
 
                for subnet in subnets["Subnets"]:
                   idx_subnet_lin          += 1
                   cidrBlockSubnet          = subnet['CidrBlock']
                   az                       = subnet['AvailabilityZone']
                   availableIpdAddressCount = subnet['AvailableIpAddressCount']
                   name                     = ""

                   if "Tags" in subnet:
                      for t in subnet["Tags"]:
                         if t["Key"].upper() == "NAME":
                            name = t["Value"]
                            break
                   
                   if az not in azs:
                     azs.append(az)

                   # Get its Route Tables if asked
                   routeTables = []
                   if addRouteTables:
                      rts = ec2.describe_route_tables( Filters=[{'Name': 'association.subnet-id','Values': [subnet['SubnetId']]}])
                      if len(rts["RouteTables"]) == 0:
                         # In this case, when the Subnet is not directly associate with a user's created Route Table
                         # Get the Main Route Table of the VPC where it is located this Subnet (default association)
                         rts = ec2.describe_route_tables( Filters=[{'Name': 'association.main','Values':['true']},{'Name': 'vpc-id','Values':[vpc['VpcId']]}])
                      for routeTable in rts["RouteTables"]:
                          routeTables.append({
                             "routeTableId": routeTable["RouteTableId"],
                             "routeTableId5Digts": routeTable["RouteTableId"][-5:]
                          })
                   
                   # Get its NACLs if asked
                   nacls = []
                   if addNacls:
                      ncls = ec2.describe_network_acls( Filters=[{'Name': 'association.subnet-id','Values': [subnet['SubnetId']]}])
                      for nacl in ncls["NetworkAcls"]:
                          nacls.append({
                             "naclId": nacl["NetworkAclId"],
                             "nacl5Digts": nacl["NetworkAclId"][-5:]
                          })
                  
                   # Check if the Subnet is Public or Private 
                   # Asked to inform if the Subnet is Public? 
                   if subnetIsPublic:
                      resultSubnetIsPublic = "--- "
                      if self._checkSubnetIsPublic(subnet['SubnetId'], None) :
                         resultSubnetIsPublic = "PUBLIC"
                   publicPrivateSubnet = True if resultSubnetIsPublic.upper() == "PUBLIC" else False
                   # For tests
                   #publicPrivateSubnet = "PRIVATE" if int(random.randint(0,1)) == 1 else "PUBLIC"

                   subnetsDict.append({
                     "subnetId": subnet['SubnetId'],
                     "name": name,
                     "cidrBlock": subnet['CidrBlock'],
                     "az": subnet['AvailabilityZone'],
                     "availableIpAddressCount": subnet['AvailableIpAddressCount'],
                     "public": publicPrivateSubnet,
                     "routeTables": routeTables,
                     "nacls": nacls
                   })

                vpcName = ""
                if 'Tags' in vpc:
                  for tag in vpc['Tags']:
                     if tag["Key"].lower() == "name":
                        vpcName = tag["Value"]
                        break
                
                data["vpcs"].append({
                   "vpcId": vpcId,
                   "cidrBlock": cidrBlock,
                   "name": vpcName,
                   "default": vpc['IsDefault'],
                   "azs": azs,
                   "subnets": subnetsDict
                })

        #if True:
            #data = Utils.loadJsonFile("d:\\Downloads\\data.json.json")
            #if os.path.exists("D:\\Downloads\\data.json"):
            #   os.remove("D:\\Downloads\\data.json")
            #Utils.saveDictAsJson("D:\\Downloads\\data.json",data)

            csvDrawIo = CsvDrawIoNetworking(self.config)
            file = csvDrawIo.generateNetworkingGraph('networkingDiagram_template.csv', data, addRouteTables, addNacls, addTgws, addRtTgws)
            #file = csvDrawIo.generateNetworkingGraph('networkingDiagram_template.csv', data, True, True, True, True)
            
            print("")
            print("  --> " + Style.IGREEN + file + Style.GREEN + " generated!" + Style.RESET)
            print("  --> " + Style.IGREEN + "The content is also in your Clipboard, just go to DrawIo Menu" + Style.IBLUE + " --> " + Style.IGREEN + "Arrange" + Style.IBLUE + " --> " + Style.IGREEN + "Insert" + Style.IBLUE + " --> " + Style.IGREEN + "Advanced" + Style.IBLUE + " --> " + Style.IGREEN + "CSV..." + Style.RESET)
            print("  --> " + Style.IGREEN + "Paste the CSV content generated here" + Style.RESET)
            print("") 
            return ""
        else:
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_VPC]["name"], " No VPC found " + Emoticons.ops(), self.config, jsonResult, True, tableArgs)

    # List all Route Tables
    def listRouteTables(self):
        ec2 = self.botoSession().client('ec2')

        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        showRoutes       = False

        if "show-routes" in self.config.commandArguments:
           showRoutes = True   

        data                = {}
        data["RouteTables"] = []
        filters             = []
        if self.config.awsTagsToFilter():
           # Tags from Environment
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )
        routeTables = ec2.describe_route_tables(Filters=filters)

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
           jsonResult = Utils.dictToJson(routeTables)

        resultTxt = ""
        if len(routeTables["RouteTables"]) >= 1:
            resultTxt = "List of Route Tables, total of " + Style.GREEN + str(len(routeTables["RouteTables"])) + Style.RESET + "\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"

            idx_lin=0
            header = ["#","VPC Id", "Route Table Id", "Associations"]
            if showRoutes:
               header = ["#","VPC Id", "Route Table Id", "Associations", "Routes"]   
            if tableArgs.showTags:
               header.append("Route Table Tags")       

            prettyTable = PrettyTable(header)
            for routeTable in routeTables["RouteTables"]:
                idx_lin += 1

                vpcId             = routeTable['VpcId']
                routeTableId      = routeTable['RouteTableId']
                columns           = [ idx_lin, vpcId, routeTableId ]
                associationsLines = []
                routeLines        = []

                
                subnets = []
                routes  = []
                # Save all the Associations in an array
                if "Associations" in routeTable:
                   associationsLines, subnets = self.listRouteTablesAddAssociations(routeTable)
                # Save all the Routes in an array (if requested)
                if showRoutes:
                   if "Routes" in routeTable:
                       routeLines, routes = self.listRouteTablesAddRoutes(routeTable, prettyTable)

                data["RouteTables"].append({
                   "vpcId": routeTable['VpcId'],
                   "routeTableId": routeTable['RouteTableId'],
                   "routeTableIdNickName": routeTable['RouteTableId'][-5:],
                   "subnets": subnets,
                   "routes": routes
                })
                
                # Check which one of the Arrays is larger (n.o of occurrences)
                #  choose the larger to guide the interation checking if the other (smaller) has a line with the same index, when it does print it, otherwise fill it with spaces
                if len(associationsLines) > len (routeLines):
                   # In case there are more Associations then Routes
                   for i, assoc in enumerate(associationsLines):
                       columns.append(assoc)
                       if showRoutes:
                           if i < len(routeLines):
                              columns.append(routeLines[i])
                           else:
                              columns.append("") 
                       if tableArgs.showTags:
                          tags = Utils.formatPrintTags(routeTable['Tags'])
                          columns.append(tags)
                       prettyTable.addRow(columns)
                       columns = [ idx_lin, vpcId, routeTableId ]
                else:
                   # In case there are more Routes then Associations
                   for i, route in enumerate(routeLines):
                       if i < len(associationsLines):
                          columns.append(associationsLines[i])
                       else:
                          columns.append("")
                       columns.append(route)
                       if tableArgs.showTags:
                          tags = Utils.formatPrintTags(routeTable['Tags'])
                          columns.append(tags)
                       prettyTable.addRow(columns)
                       columns = [ idx_lin, vpcId, routeTableId ]

                prettyTable.addSeparatorGroup() 

            if (int(tableArgs.sortCol) - 1) > len(columns):
                sortCol = "1"

            #print(Utils.saveDictAsJson("Json_Test_Rts.json",data))
            
            if tableArgs.csvDrawIo:
               csvDrawIo = CsvDrawIo(self.config)
               file = csvDrawIo.generateListRouteTables('listRouteTables_template.csv', data)
               print("")
               print("  --> " + Style.IGREEN + file + Style.GREEN + " generated!" + Style.RESET)
               print("")

            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.ascendingOrder(not tableArgs.desc)
            result = "Route Tables " + "\n\n" + prettyTable.printMe("listRouteTables",self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_ROUTE_TABLES]["name"], result, self.config, jsonResult, True, tableArgs)    
        else:
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_ROUTE_TABLES]["name"], " No Route Table found " + Emoticons.ops(), self.config, jsonResult, True, tableArgs)
   
    def listRouteTablesAddAssociations(self, routeTable):
       idx_associac_lin  = 0
       associationsLines = []
       subnets = []
       for association in routeTable["Associations"]:
          if "SubnetId" in association:
             idx_associac_lin += 1
             subnetId = association['SubnetId'] + "  (" + str(idx_associac_lin) + ")"
             if "AssociationState" in association:
                  subnetId += subnet + " ( %s)".format(association["AssociationState"]["State"])
             associationsLines.append(subnetId)
             subnets.append({
                "subnetId": association['SubnetId'],
                "main": association["Main"],
                "routeTableAssociationId": association["RouteTableAssociationId"]
             })
          else:
             subnetId = ""
             associationsLines.append(subnetId)
       return associationsLines, subnets

    def listRouteTablesAddRoutes(self, routeTable, prettyTable):
       idx_route_lin  = 0
       routeLines     = []
       chgdHeader     = False
       routes         = []
       for route in routeTable["Routes"]:
          idx_route_lin += 1

          cidrblock = ""
          if "DestinationCidrBlock" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["DestinationCidrBlock"]
             cidrblock            = route["DestinationCidrBlock"]
          elif "DestinationIpv6CidrBlock" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["DestinationIpv6CidrBlock"]
             cidrblock            = route["DestinationIpv6CidrBlock"]
          elif "DestinationPrefixListId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["DestinationPrefixListId"]
             cidrblock            = route["DestinationPrefixListId"]
          elif "EgressOnlyInternetGatewayId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["EgressOnlyInternetGatewayId"]
             cidrblock            = route["EgressOnlyInternetGatewayId"]
          elif "GatewayId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["GatewayId"]
             cidrblock            = route["GatewayId"]
          elif "InstanceId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["InstanceId"]
             cidrblock            = route["InstanceId"]
          elif "InstanceOwnerId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["InstanceOwnerId"]
             cidrblock            = route["InstanceOwnerId"]
          elif "NatGatewayId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["NatGatewayId"]
             cidrblock            = route["NatGatewayId"]
          elif "TransitGatewayId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["TransitGatewayId"]
             cidrblock            = route["TransitGatewayId"]
          elif "LocalGatewayId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["LocalGatewayId"]
             cidrblock            = route["LocalGatewayId"]
          elif "CarrierGatewayId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["CarrierGatewayId"]
             cidrblock            = route["CarrierGatewayId"]
          elif "NetworkInterfaceId" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["NetworkInterfaceId"]
             cidrblock            = route["NetworkInterfaceId"]
          elif "Origin" in route:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + route["Origin"]
             cidrblock            = route["Origin"]
          else:
             destinationCidrBlock = "(" + "{:02d}".format(idx_route_lin) + ") " + str(route)
             cidrblock            = str(route)
         
          target     = ""
          state      = route["State"]
          targetType = ""  
          if "TransitGatewayId" in route:
             target     = route['TransitGatewayId'] 
             targetType = "TransitGateway"
          elif "GatewayId" in route:
             target     = route['GatewayId']
             targetType = "Gateway"
          elif "InstanceId" in route:
             target     = route['InstanceId']
             targetType = "Instance"
          elif "NatGatewayId" in route:
             target     = route['NatGatewayId']
             targetType = "NatGateway"
          elif "VpcPeeringConnectionId" in route:
             target     = route['VpcPeeringConnectionId']
             targetType = "VPC Peering"
          else:
             target = str(route)

          line = destinationCidrBlock.ljust(24," ")  + " | " + target.ljust(25," ") + " | " + state.ljust(10," ")

          if not chgdHeader:
             entriesHeader = "CIDR Block".ljust(24," ")  + " | " + "Target".ljust(25," ") + " | " + "State".ljust(10," ")
             prettyTable.header = ["#","VPC Id", "Route Table Id", "Associations", entriesHeader]   
             chgdHeader = True

          routes.append({
             "target": target,
             "targetType": targetType,
             "cidrblock": cidrblock,
             "state": state
          })
          routeLines.append(line)
       return routeLines, routes

    # List Network Access Control List
    def listNacls(self):
        ec2 = self.botoSession().client('ec2')

        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        showEntries  = False

        if "show-entries" in self.config.commandArguments:
           showEntries = True   

        filters = []
        if self.config.awsTagsToFilter():
           # Tags from Environment
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )
        nacls = ec2.describe_network_acls(Filters=filters)

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
           jsonResult = Utils.dictToJson(nacls)

        resultTxt = ""
        if len(nacls["NetworkAcls"]) >= 1:
            resultTxt = "List of Route Tables, total of " + Style.GREEN + str(len(nacls["NetworkAcls"])) + Style.RESET + "\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"

            idx_lin=0
            header = ["#","VPC Id", "NACL Id", "Associations"]
            if showEntries:
               header = ["#","VPC Id", "NACL Id", "Associations", "Entries"]   
            if tableArgs.showTags:
               header.append("NACL Table Tags")       

            prettyTable = PrettyTable(header)
            for nacl in nacls["NetworkAcls"]:
                idx_lin += 1

                vpcId             = nacl['VpcId']
                naclId            = nacl['NetworkAclId']
                columns           = [ idx_lin, vpcId, naclId ]
                associationsLines = []
                entryLines        = []

                # Save all the Associations in an array
                if "Associations" in nacl:
                   associationsLines = self.listNaclsAddAssociations(nacl)
                # Save all the Entries in an array (if requested)
                if showEntries:
                   if "Entries" in nacl:
                       entryLines = self.listNaclsAddEntries(nacl, prettyTable)
                
                # Check which one of the Arrays is larger (n.o of occurrences)
                #  choose the larger to guide the interation checking if the other (smaller) has a line with the same index, when it does print it, otherwise fill it with spaces
                if len(associationsLines) > len (entryLines):
                   # In case there are more Associations then Entries
                   for i, assoc in enumerate(associationsLines):
                       columns.append(assoc)
                       if showEntries:
                           if i < len(entryLines):
                              columns.append(entryLines[i])
                           else:
                              columns.append("") 
                       if tableArgs.showTags:
                          tags = Utils.formatPrintTags(nacl['Tags'])
                          columns.append(tags)
                       prettyTable.addRow(columns)
                       columns = [ idx_lin, vpcId, naclId ]
                else:
                   # In case there are more Entries then Associations
                   for i, entry in enumerate(entryLines):
                       if i < len(associationsLines):
                          columns.append(associationsLines[i])
                       else:
                          columns.append("")
                       columns.append(entry)
                       if tableArgs.showTags:
                          tags = Utils.formatPrintTags(nacl['Tags'])
                          columns.append(tags)
                       prettyTable.addRow(columns)
                       columns = [ idx_lin, vpcId, naclId ]

                prettyTable.addSeparatorGroup() 

            if (int(tableArgs.sortCol) - 1) > len(columns):
                sortCol = "1"

            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.ascendingOrder(not tableArgs.desc)

            if tableArgs.csvDrawIo:
               csvDrawIo = CsvDrawIo(self.config)
               file = csvDrawIo.generateListNacls('listNacls_template.csv', prettyTable.header, prettyTable.content)
               print("")
               print("  --> " + Style.IGREEN + file + Style.GREEN + " generated!" + Style.RESET)
               print("")

            result = "Network Access Control List " + "\n\n" + prettyTable.printMe("listNacls",self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_ROUTE_TABLES]["name"], result, self.config, jsonResult, True, tableArgs)
        else:
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_ROUTE_TABLES]["name"], " No Network Access Control List found " + Emoticons.ops(), self.config, jsonResult, True, tableArgs)

    
    def listNaclsAddAssociations(self, nacl):
       idx_associac_lin  = 0
       associationsLines = []
       for association in nacl["Associations"]:
          if "SubnetId" in association:
             idx_associac_lin += 1
             subnetId = association['SubnetId'] + "  (" + str(idx_associac_lin) + ")"
             if "AssociationState" in association:
                  subnetId += subnet + " ( %s)".format(association["AssociationState"]["State"])
             associationsLines.append(subnetId)
          else:
             subnetId = ""
             associationsLines.append(subnetId)
       return associationsLines

    def listNaclsAddEntries(self, nacl, prettyTable):
       idx_route_lin  = 0
       entries        = []
       chgdHeader     = False
       for entry in nacl["Entries"]:
          idx_route_lin += 1
          cidrBlock  = "(" + "{:02d}".format(idx_route_lin) + ") " + entry["CidrBlock"]
          type       = "Egress" if entry["Egress"] else ""
          protocol   = str(entry["Protocol"])
          ruleAction = entry["RuleAction"] 
          ruleNumber = str(entry["RuleNumber"])
          line = cidrBlock.ljust(24," ")  + " | " + type.ljust(10," ") + " | " + ruleAction.ljust(8," ") + " | " + ruleNumber.ljust(5," ") + " | " + protocol.ljust(8," ")

          if not chgdHeader:
             entriesHeader = "CDIR Block".ljust(24," ")  + " | " + "Type".ljust(10," ") + " | " + "Action".ljust(8," ") + \
                             " | " + "Num".ljust(5," ") + " | " + "Protocol".ljust(8," ")
             prettyTable.header = ["#","VPC Id", "NACL Id", "Associations", entriesHeader]
             chgdHeader = True

          entries.append(line)
       return entries

    # List all Ec2 Instances
    def listEc2(self):
       ec2              = self.botoSession().client('ec2')
       instanceId       = None
       privateIPFilter  = None
       vpcIdFilter      = None
       subnetIdFilter   = None
       showSg           = False
       showVpc          = False
       showSubnet       = False
       showImage        = False
       showCpu          = False
       hideName         = False

       tableArgs = TableArgs()
       tableArgs.setArguments(self.config.commandArguments)
       if "," in self.config.commandArguments:
          for arg in self.config.commandArguments.split(","):
              if "i-" in arg:
                 instanceId = arg
              elif arg == "sg":
                 showSg = True
              elif arg == "vpc":
                 showVpc = True    
              elif arg == "subnet":
                 showSubnet = True   
              elif arg == "image":
                 showImage = True 
              elif arg == "cpu":
                 showCpu = True
              elif arg == "noname":
                 hideName = True
              elif arg.startswith("vpc-"):
                 vpcIdFilter = arg
              elif arg.startswith("subnet-"):
                 subnetIdFilter = arg              
              else:
                 # Check IP
                 if Utils.isNumber(arg[0:2]):
                    privateIPFilter = arg

       else:
          arg = self.config.commandArguments
          if "i-" in arg:
            instanceId = arg
          elif arg == "sg":
             showSg = True
          elif arg == "vpc":
             showVpc = True    
          elif arg == "subnet":
             showSubnet = True   
          elif arg == "image":
             showImage = True 
          elif arg == "cpu":
             showCpu = True
          elif arg == "noname": 
             hideName = True
          elif arg.startswith("vpc-"):
             vpcIdFilter = arg
             print(arg)
          elif arg.startswith("subnet-"):
             subnetIdFilter = arg   
          else:
             # Check IP
             if Utils.isNumber(arg[0:2]):
                privateIPFilter = arg


       filters=[]   

       if instanceId:
          filters.append({'Name': 'instance-id','Values': [instanceId]})   
       if privateIPFilter:   
          filters.append({'Name': 'private-ip-address','Values': [privateIPFilter]})
       if vpcIdFilter:   
          filters.append({'Name': 'vpc-id','Values': [vpcIdFilter]})
       if subnetIdFilter:   
          filters.append({'Name': 'subnet-id','Values': [subnetIdFilter]})         

       if self.config.awsTagsToFilter():
           # Environment Tags set
           for tag in self.config.awsTags: 
               filters.append({'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]})   

       # Tags from command line arguments
       if len(tableArgs.tagsTemp) > 0:
          for tag in tableArgs.tagsTemp: 
              filters.append({'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]})        

       reservations = ec2.describe_instances( Filters=filters )        

       jsonResult = ""
       if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
          jsonResult = Utils.dictToJson(reservations)

       if reservations and len(reservations["Reservations"]) > 0:
  
          idx_lin = 0

          if hideName:
             header = ["#","Instance Id",       "Type","Launch Time", "Private IP", "Public IP", "State"]
          else:   
             header = ["#","Instance Id","Name","Type","Launch Time", "Private IP", "Public IP", "State"]

          if showSg:             
             header.append("Security Groups")
          if showImage:          
             header.append("Image Id")
          if showCpu:            
             header.append("CPU Options")
          if showVpc:            
             header.append("VPC")
          if showSubnet:         
             header.append("Subnet")
          if tableArgs.showTags: 
             header.append("Tags")

          prettyTable = PrettyTable(header)

          totalListed = 0

          for instanceGroup in reservations["Reservations"]:
              for instance in instanceGroup["Instances"]:
                  idx_lin     += 1
                  totalListed += 1

                  if not hideName:
                     name = ""
                     for t in instance['Tags']:
                         if t["Key"] == "Name":
                            name = t["Value"]

                  launchTimeDate = ""
                  if instance['LaunchTime']:
                     launchTimeDate = instance['LaunchTime'].strftime("%d-%b-%y %H:%M")

                  privateIp = instance['PrivateIpAddress'] if "PrivateIpAddress" in instance else ""
                  publicIp  = instance["PublicIpAddress"] if "PublicIpAddress" in instance else ""
                  state     = instance["State"]["Name"]
                  state     = Style.CYAN + state + Style.RESET if state == "stopped" else state

                  if hideName:
                     columns = [ str(idx_lin), str(instance['InstanceId']), instance['InstanceType'], launchTimeDate, privateIp, publicIp, state ]
                  else:   
                     columns = [ str(idx_lin), str(instance['InstanceId']), name, instance['InstanceType'], launchTimeDate, privateIp, publicIp, state ]

                  if showSg:
                     securityGroups = ""
                     for sg in instance["SecurityGroups"]:             
                         if securityGroups != "": securityGroups += ","
                         securityGroups += sg["GroupId"]
                     columns.append(securityGroups)    
                  if showImage:          
                     columns.append(instance["ImageId"])       
                  if showCpu:   
                     cpu  = Style.MAGENTA + "Core:"    + Style.GREEN + str(instance["CpuOptions"]["CoreCount"]) + Style.RESET + " "
                     cpu += Style.MAGENTA + "Threads:" + Style.GREEN + str(instance["CpuOptions"]["ThreadsPerCore"])
                     columns.append(cpu)       
                  if showVpc:            
                     vpc = instance["VpcId"]
                     columns.append(vpc)
                  if showSubnet:         
                     subnet = instance["SubnetId"]
                     columns.append(subnet)
                  if tableArgs.showTags:
                     tags = Utils.formatPrintTags(instance['Tags'])
                     columns.append(tags)

                  prettyTable.addRow(columns)

          resultTxt = ""

          if instanceId:
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      Instance Id........: " + Style.GREEN + instanceId + Style.RESET
          if privateIPFilter:   
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      Private IP Address.: " + Style.GREEN + privateIPFilter + Style.RESET
          if vpcIdFilter:   
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      VPC Id.............: " + Style.GREEN + vpcIdFilter + Style.RESET
          if subnetIdFilter:   
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      Subnet Id..........: " + Style.GREEN + subnetIdFilter + Style.RESET

          resultTxt = resultTxt + "\n\n Total of EC2s...: " + Style.GREEN + format(totalListed,",") + Style.RESET   

          if (int(tableArgs.sortCol) - 1) > len(columns):
              tableArgs.sortCol = "1"
          prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
          prettyTable.ascendingOrder(not tableArgs.desc)

          result = resultTxt + "\n\n" + prettyTable.printMe("listEc2",self.config.tableLineSeparator, tableArgs)
          return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_EC2]["name"], result, self.config,jsonResult, True, tableArgs), prettyTable.content
       else:
          resultTxt = ""
          resultTxt = "No EC2 Instance was found. " + Emoticons.ops()
          return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_EC2]["name"], resultTxt, self.config, "", True, tableArgs), None

    def botoSession(self):
        return self.config.botoSession()

if __name__ == '__main__':
    config = Config()
    config.awsProfile = "ecomm"
    config.awsRegion = "eu-central-1"
    config.printResults = True
    #config.awsTags["Environment"] = "production"
    config.tableLineSeparator = False
    
    
    # subnets, is-public (only with subnets active)
    # sort1,desc (when requested together with subnets, the group lines will be omitted)
    if len(sys.argv) > 1:
       config.commandArguments = sys.argv[1]
    pyEc2CP = PyEc2CP(config)
    report = pyEc2CP.listEc2()
    Utils.addToClipboard(report)
    print(report)

    # TODO:
    # findEc2 (by IP, by InstanceId, by Tag, etc.)
    # Result show: IP, t3.medium, region, subnet, vpc, security group, (attached Load Balancer optional), (Security Groups Rules optional)
