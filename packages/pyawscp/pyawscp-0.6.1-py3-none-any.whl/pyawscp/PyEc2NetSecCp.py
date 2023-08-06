#!/usr/bin/env python3

import boto3
import logging
import sys
import json
import os, re
from botocore.exceptions import ClientError
from datetime import datetime
from pyawscp.Functions import Functions
from pyawscp.Utils import Utils, Style
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.CsvDrawIo import CsvDrawIo
from pyawscp.TableArgs import TableArgs
from pyawscp.CsvDrawIo import CsvDrawIo
from pygments import highlight, lexers, formatters

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

class PyEc2NetSecCP:

    def __init__(self, config):
        self.config = config
        self.tempCredentials = None

    
    # List all Security Groups
    def listSecurityGroup(self):
        ec2 = self.botoSession().client('ec2')

        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        listResourcesAssociated = False
        listIpPermissions       = False
        
        if "list-associated" in self.config.commandArguments:
           listResourcesAssociated    = True
        if "list-permissions" in self.config.commandArguments:
           listIpPermissions          = True 

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
        securityGroups = ec2.describe_security_groups(Filters=filters)

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
           jsonResult = Utils.dictToJson(securityGroups)

        resultTxt = ""
        if len(securityGroups["SecurityGroups"]) >= 1:
            idx_lin             = 0
            data                = {}
            data["sgs"]         = []
            ipPermissions       = []
            ipPermissionsEgress = []
            for securityGroup in securityGroups["SecurityGroups"]:
                idx_lin += 1
                securityGroupId          = securityGroup['GroupId']
                tagsSg                   = securityGroup['Tags'] if "Tags" in securityGroup else None
                networkingInterfacesData = []

                # Collect Network Interfaces associated with the Security Group
                if listResourcesAssociated:

                   filterNetworkInterfaces = [{
                      'Name':'group-id','Values':[securityGroupId]
                   }]
                   networkInterfaces = ec2.describe_network_interfaces(Filters=filterNetworkInterfaces)
                   if len(networkInterfaces) > 0:
                      for ni in networkInterfaces["NetworkInterfaces"]:
                          networkingInterfacesData.append({
                              'NetworkInterfaceId': ni['NetworkInterfaceId'],
                              'Description': ni['Description'],
                              'PrivateIpAddress': ni['PrivateIpAddress'],
                              'VpcId': ni['VpcId']
                           })
               
                if listIpPermissions:
                   if len(securityGroup["IpPermissions"]) > 0:
                      ipPermissions = []
                      for ipp in securityGroup["IpPermissions"]:
                          ipRanges = []
                          for ipRange in ipp["IpRanges"]:
                             ipRanges.append({
                                "cidrIp": ipRange["CidrIp"],
                                "description": ipRange["Description"] if "Description" in ipRange else None
                             }) 
                          ipPermissions.append({
                            "fromPort": ipp["FromPort"] if "FromPort" in ipp else None,
                            "toPort": ipp["ToPort"] if "ToPort" in ipp else None,
                            "ipProtocol": ipp["IpProtocol"],
                            "ipRanges": ipRanges
                          })

                   if len(securityGroup["IpPermissionsEgress"]) > 0:
                      ipPermissionsEgress = []
                      for ippEgress in securityGroup["IpPermissionsEgress"]:
                          ipRangesEgress = []
                          for ipRangeEgress in ippEgress["IpRanges"]:
                             ipRangesEgress.append({
                                "cidrIp": ipRangeEgress["CidrIp"],
                                "description": ipRangeEgress["Description"] if "Description" in ipRangeEgress else None
                             }) 
                          ipPermissionsEgress.append({
                            "ipProtocol": ippEgress["IpProtocol"],
                            "ipRanges": ipRangesEgress
                          })

                data["sgs"].append({
                   "sg": {
                      "index": idx_lin,
                      "id":securityGroupId,
                      "vpcId": securityGroup['VpcId'],
                      "networkInterfaces": networkingInterfacesData,
                      "ipPermissions": ipPermissions if ipPermissions else [],
                      "ipPermissionsEgress": ipPermissionsEgress if ipPermissionsEgress else [],
                      "tags": tagsSg
                   }
                })
            
            #print(Utils.saveDictAsJson("TESTSSGs",data))

            ## Print Report from Data Collected
            resultTxt = "List of Security Groups, total of " + Style.GREEN + str(len(securityGroups["SecurityGroups"])) + Style.RESET + "\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"
            
            header = ["#","SG Id", "VPC"]
            if listResourcesAssociated:
               header.append("Network Intf")
               header.append("Description")
               header.append("Private IP")
            if listIpPermissions:
               header.append("I-Prot | I-PortRange | I-Source             | I-Description                    (Ingress)")
               header.append("E-Prot | E-Source             | E-Description                    (Egress)")
            if tableArgs.showTags:
               header.append("SG Tags")       

            prettyTable = PrettyTable(header)
            for securityGroup in data["sgs"]:

                securityGroupId = securityGroup["sg"]["id"]
                vpc             = securityGroup["sg"]["vpcId"] 
                columns         = [ securityGroup["sg"]["index"], securityGroupId, vpc ]

                if listResourcesAssociated and not listIpPermissions:
                   for ni in securityGroup["sg"]["networkInterfaces"]:
                       columns.append(ni["NetworkInterfaceId"])
                       columns.append(ni["Description"] if ni["Description"] != "" else "EC2" )
                       columns.append(ni["PrivateIpAddress"])
                       
                       if tableArgs.showTags:
                          tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                          columns.append(tags)

                       prettyTable.addRow(columns)
                       columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                   prettyTable.addSeparatorGroup()

                elif not listResourcesAssociated and listIpPermissions:
                   for index, val in enumerate(securityGroup["sg"]["ipPermissions"]):
                       protocol = "All" if val["ipProtocol"] == -1 else str(val["ipProtocol"]).upper()
                       if len(val["ipRanges"]) > 0:
                           for ip in val["ipRanges"]:

                                 desc = ip["description"] if ip["description"] else "" 
                                 desc = (desc[:38] + '..') if len(desc) > 38 else desc

                                 if val["fromPort"] != val["toPort"]:
                                    ports = (str(val["fromPort"]) + "-" + str(val["toPort"])).ljust(11," ")
                                 else:
                                    ports = str(val["fromPort"]).ljust(11," ")

                                 line = str(protocol).upper().ljust(6," ") + Style.RESET + " | " + Style.GREEN + \
                                        ports + Style.RESET + " | " + Style.GREEN + \
                                        str(ip["cidrIp"] ).ljust(20," ") + Style.RESET + " | " + Style.GREEN + \
                                        desc
                                 columns.append(line)
                                 columns.append("")
                                 if tableArgs.showTags:
                                    tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                                    columns.append(tags)
                                 prettyTable.addRow(columns)
                                 columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                       else:
                           line = str(protocol).upper().ljust(6," ") + Style.RESET + " | " + Style.GREEN + \
                                  str(val["fromPort"] ).ljust(5," ")
                           columns.append(line)
                           columns.append("")
                           if tableArgs.showTags:
                              tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                              columns.append(tags)
                           prettyTable.addRow(columns)
                           columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]

                   for index, val in enumerate(securityGroup["sg"]["ipPermissionsEgress"]):
                       protocol = "All" if val["ipProtocol"] == -1 else str(val["ipProtocol"]).upper()
                       if len(val["ipRanges"]) > 0:
                           for ip in val["ipRanges"]:
                                 desc = ip["description"] if ip["description"] else "" 
                                 desc = (desc[:38] + '..') if len(desc) > 38 else desc

                                 line = str(protocol).ljust(6," ") + Style.RESET + " | " + Style.GREEN + \
                                       str(ip["cidrIp"] ).ljust(20," ") + Style.RESET + " | " + Style.GREEN + \
                                       desc

                                 columns.append(" ")   
                                 columns.append(line)

                                 if tableArgs.showTags:
                                    tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                                    columns.append(tags)
                                 prettyTable.addRow(columns)
                                 columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                       else:
                           columns.append("")
                           line = str(protocol).ljust(6," ")
                           columns.append(line)
                           
                           if tableArgs.showTags:
                              tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                              columns.append(tags)
                           prettyTable.addRow(columns)
                           columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]

                   prettyTable.addSeparatorGroup() 

                elif listResourcesAssociated and listIpPermissions:
                   for ni in securityGroup["sg"]["networkInterfaces"]:
                       columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                       columns.append(ni["NetworkInterfaceId"])
                       columns.append(ni["Description"] if ni["Description"] != "" else "EC2" )
                       columns.append(ni["PrivateIpAddress"])

                       for index, val in enumerate(securityGroup["sg"]["ipPermissions"]):
                           protocol = "All" if val["ipProtocol"] == -1 else str(val["ipProtocol"]).upper()
                           if len(val["ipRanges"]) > 0:
                                 for ip in val["ipRanges"]:

                                       desc = ip["description"] if ip["description"] else "" 
                                       desc = (desc[:38] + '..') if len(desc) > 38 else desc

                                       if val["fromPort"] != val["toPort"]:
                                          ports = (str(val["fromPort"]) + "-" + str(val["toPort"])).ljust(11," ")
                                       else:
                                          ports = str(val["fromPort"]).ljust(11," ")

                                       line = str(protocol).ljust(6," ") + Style.RESET + " | " + Style.GREEN + \
                                             ports + Style.RESET + " | " + Style.GREEN +\
                                             str(ip["cidrIp"] ).ljust(20," ") + Style.RESET + " | " + Style.GREEN + \
                                             desc
                                       columns.append(line)
                                       columns.append("")
                                       if tableArgs.showTags:
                                          tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                                          columns.append(tags)
                                       prettyTable.addRow(columns)
                                       columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                                       columns.append(ni["NetworkInterfaceId"])
                                       columns.append(ni["Description"] if ni["Description"] != "" else "EC2" )
                                       columns.append(ni["PrivateIpAddress"])
                           else:
                                 line = str(protocol).ljust(6," ") + Style.RESET + " | " + Style.GREEN + \
                                       str(val["fromPort"] ).ljust(5," ")
                                 columns.append(line)
                                 columns.append("")
                                 if tableArgs.showTags:
                                    tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                                    columns.append(tags)
                                 prettyTable.addRow(columns)
                                 columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                                 columns.append(ni["NetworkInterfaceId"])
                                 columns.append(ni["Description"] if ni["Description"] != "" else "EC2" )
                                 columns.append(ni["PrivateIpAddress"])
                        
                       for index, val in enumerate(securityGroup["sg"]["ipPermissionsEgress"]):
                           protocol = "All" if val["ipProtocol"] == -1 else str(val["ipProtocol"]).upper()
                           if len(val["ipRanges"]) > 0:
                                 for ip in val["ipRanges"]:
                                       desc = ip["description"] if ip["description"] else "" 
                                       desc = (desc[:38] + '..') if len(desc) > 38 else desc

                                       line = str(protocol).ljust(6," ") + Style.RESET + " | " + Style.GREEN + \
                                             str(ip["cidrIp"] ).ljust(20," ") + Style.RESET + " | " + Style.GREEN + \
                                             desc

                                       columns.append(" ")   
                                       columns.append(line)

                                       if tableArgs.showTags:
                                          tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                                          columns.append(tags)
                                       prettyTable.addRow(columns)
                                       columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                                       columns.append(ni["NetworkInterfaceId"])
                                       columns.append(ni["Description"] if ni["Description"] != "" else "EC2" )
                                       columns.append(ni["PrivateIpAddress"])
                           else:
                                 columns.append("")
                                 line = str(protocol).ljust(6," ")
                                 columns.append(line)
                                 
                                 if tableArgs.showTags:
                                    tags = Utils.formatPrintTags( securityGroup["sg"]["tags"])
                                    columns.append(tags)
                                 prettyTable.addRow(columns)
                                 columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                                 columns.append(ni["NetworkInterfaceId"])
                                 columns.append(ni["Description"] if ni["Description"] != "" else "EC2" )
                                 columns.append(ni["PrivateIpAddress"])
                       
                       # Separator
                       columns = [ securityGroup["sg"]["index"], securityGroupId, vpc ]
                       columns.append("-".ljust(20,"-"))
                       columns.append("-".ljust(50,"-"))
                       columns.append("-".ljust(14,"-"))
                       columns.append("-".ljust(70,"-"))
                       columns.append("-".ljust(70,"-"))
                       if tableArgs.showTags:
                          columns.append("-".ljust(30,"-"))
                       prettyTable.addRow(columns)
                   
                   prettyTable.addSeparatorGroup()

                else:
                   if tableArgs.showTags:
                      tags = Utils.formatPrintTags( securityGroup["sg"]["tags"] )
                      columns.append(tags)
                   prettyTable.addRow(columns)

            if (int(tableArgs.sortCol) - 1) > len(columns):
                sortCol = "1"

            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.ascendingOrder(not tableArgs.desc)

            if tableArgs.csvDrawIo:
               csvDrawIo = CsvDrawIo(self.config)
               file = csvDrawIo.generateListSg('listSg_template.csv', prettyTable.header, data)
               print("")
               print("  --> " + Style.IGREEN + file + Style.GREEN + " generated!" + Style.RESET)
               print("")

            result = resultTxt + prettyTable.printMe("listSgs",self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_SG]["name"], result, self.config, jsonResult, True, tableArgs)    
        else:
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_SG]["name"], " No Security Group found " + Emoticons.ops(), self.config, jsonResult, True, tableArgs)


    def botoSession(self):
        return self.config.botoSession()

