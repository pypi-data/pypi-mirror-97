import sys
import os, re
from random import randrange
from os.path import expanduser
from pyawscp.Utils import Utils

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from . import templates

class CsvDrawIo:

    def __init__(self, config):
        self.config = config
        self.region = self.config.awsRegion
    

    def buildLink(self, whichLink, resourceId):
        whichLink = whichLink.lstrip().rstrip().upper()

        if "SUBNET" == whichLink:
           return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#subnets:SubnetId={id}" \
                  .format(region=self.region,id=resourceId)
        elif "VPC" == whichLink:
            return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#vpcs:VpcId={id}" \
                  .format(region=self.region,id=resourceId)
        elif "EC2_PRIVATEIP" == whichLink:
           return "https://{region}.console.aws.amazon.com/ec2/v2/home?region={region}#Instances:privateIpAddress={id}" \
                  .format(region=self.region,id=resourceId)
        elif "EC2_INSTANCEID" == whichLink:
           return "https://{region}.console.aws.amazon.com/ec2/v2/home?region={region}#Instances:instanceId={id}" \
                  .format(region=self.region,id=resourceId)        
        elif "ELB" == whichLink:
           return "https://{region}.console.aws.amazon.com/ec2/v2/home?region={region}#LoadBalancers:search={id};sort=state" \
                  .format(region=self.region,id=resourceId)
        elif "SECURITYGROUP" == whichLink:
           return "https://{region}.console.aws.amazon.com/ec2/v2/home?region={region}#SecurityGroup:groupId={id}" \
                  .format(region=self.region,id=resourceId)
        elif "ROUTETABLE" == whichLink:
           return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#RouteTables:search={id};sort=desc:routeTableId" \
                  .format(region=self.region,id=resourceId)
        elif "NACL" == whichLink:
           return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#acls:networkAclId={id}" \
                  .format(region=self.region,id=resourceId)
        elif "TRANSITGATEWAY" == whichLink:
           return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#TransitGateways:search={id};sort=transitGatewayId" \
                  .format(region=self.region,id=resourceId)
        elif "TRANSITGATEWAYROUTETABLE" == whichLink:
           return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#TransitGatewayRouteTables:transitGatewayRouteTableId={id};sort=transitGatewayRouteTableId" \
                  .format(region=self.region,id=resourceId)
        elif "TRANSITGATEWAYATTACHMENT" == whichLink:
            return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#TransitGatewayAttachments:transitGatewayAttachmentId={id};sort=desc:transitGatewayId" \
                  .format(region=self.region,id=resourceId)
        elif "NATGATEWAY" == whichLink:
           return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#NatGateways:natGatewayId={id}" \
                  .format(region=self.region,id=resourceId)
        elif "INTERNETGATEWAY" == whichLink:
           return "https://{region}.console.aws.amazon.com/vpc/home?region={region}#igws:internetGatewayId={id}" \
                  .format(region=self.region,id=resourceId)

        raise ValueError("Not found link {} to be built!", whichLink)

    def openTemplate(self, templateName):
        return pkg_resources.read_text(templates, templateName)

    ##
    ## Route Tables
    ##
    def generateListRouteTables(self, templateName, data):
        template = self.openTemplate(templateName)

        #fileName = os.path.join(expanduser("~"), "listRouteTables.csv") 
        fileName = os.path.join(expanduser("~"), 'listRouteTables_' + Utils.labelTimestamp() + ".csv")
        try:
            os.remove(fileName)
        except OSError:
            pass
        
        csvLines = []
        for routeTable in data["RouteTables"]:
            rtId  = routeTable["routeTableId"]
            vpcId = routeTable["vpcId"] 

            listSubnets  = "\"<ul>"
            if "subnets" in routeTable:
               for subnet in routeTable["subnets"]:
                   subnetLabel = "<a href='{}'>{}</a>".format(self.buildLink("subnet",subnet["subnetId"]),subnet["subnetId"])
                   listSubnets += "<li>{}</li>".format(subnetLabel)
            listSubnets += "</ul>\""

            tableRoutes  = "\"<table width=100% cellpadding=3 cellspacing=0 style='background:white;border:1px black solid;font-family: Courier New, Courier, monospace;font-size: 12px;'>"
            tableRoutes += "<tr style='border-bottom:1px black solid'><td colspan='4' style='background:#2F4F4F;color:white;text-align:center;font-style:italic;font-weight:bolder;text-transform:uppercase;'>Routes</td></tr>"
            tableRoutes += "<tr style='background:#696969;color:white;'><td align='center' style='border-right:1px black solid;border-top:1px black solid'>Destination</td>" + \
                               "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Target</td>" + \
                               "<td align='center' style='border-top:1px black solid'>Status</td>" + \
                            "</tr>"

            colorEven = "#D3D3D3"
            colorOdd  = "#FFFFFF"
            idx       = 0
            for route in routeTable["routes"]:
                lineBackColor  = colorEven if idx % 2 == 0 else colorOdd

                if route["cidrblock"] == "0.0.0.0/0" and route["target"].startswith("igw-"):
                   colorLine     = "red;font-weigth:bolder;"
                   lineBackColor = "yellow"
                else:
                   colorLine = "blue"
                
                linkTarget = route["target"]
                if "tgw-" in route["target"]:
                    linkTarget = "<a href='{}'>{}</a>".format(self.buildLink("TRANSITGATEWAY",route["target"]),route["target"])
                elif "i-" in route["target"]:
                    linkTarget = "<a href='{}'>{}</a>".format(self.buildLink("EC2_INSTANCEID",route["target"]),route["target"])
                elif "nat-" in route["target"]:
                    linkTarget = "<a href='{}'>{}</a>".format(self.buildLink("NATGATEWAY",route["target"]),route["target"])
                elif "igw-" in route["target"]:
                    linkTarget = "<a href='{}'>{}</a>".format(self.buildLink("INTERNETGATEWAY",route["target"]),route["target"])

                lineTableRoute = "<tr style='background:{linebackcolor};'><td style='border-right:1px black solid;border-top:1px black solid;color:{colorLine}'>{}</td>" + \
                                   "<td style='border-right:1px black solid;border-top:1px black solid;color:{colorLine}'>{}</td>" + \
                                   "<td style='border-top:1px black solid;color:{colorLine}'>{}</td>" + \
                                 "</tr>"
                tableRoutes += lineTableRoute.format(route["cidrblock"], linkTarget, route["state"], linebackcolor=lineBackColor, colorLine=colorLine)
                idx += 1
            tableRoutes += "</table><br>\""

            labelVpcId = "\"<a href='{}'>{}</a>\"".format(self.buildLink("VPC",vpcId),vpcId)

            rtIdStamp = "&nbsp;&nbsp;&nbsp;&nbsp;<div style='border-color:black;border-width:1px;border-style:solid;border-radius:3px;display:inline;color:white;background:blue;font-size:16px'>&nbsp;&nbsp;" + \
                        rtId[-5:] + \
                        "&nbsp;&nbsp;</div>"
            labelRtId = "\"<b>"+rtId+"</b>" + rtIdStamp + "\""

            line = "{},{},{},{},{},{}".format(labelRtId,labelVpcId,listSubnets,tableRoutes, \
                                         "#E6E6E6", \
                                         self.buildLink("routetable",rtId))
            csvLines.append(line)


        with open(fileName, 'w') as csvFile:
             csvFile.write(template + '\n')
             for line in csvLines:
                 csvFile.write(line + '\n')
        return fileName

    ##
    ## Security Groups
    ##    
    def generateListSg(self, templateName, header, data):
        template = self.openTemplate(templateName)

        #fileName = os.path.join(expanduser("~"), "listSg.csv") 
        fileName = os.path.join(expanduser("~"), 'listSg_' + Utils.labelTimestamp() + ".csv")
        try:
            os.remove(fileName)
        except OSError:
            pass
        
        csvLines = []
        for securityGroup in data["sgs"]:
            sgId  = securityGroup["sg"]["id"] 
            vpcId = securityGroup["sg"]["vpcId"] 

            listNetWorkInterfaces  = "\"<ul>"
            if "networkInterfaces" in securityGroup["sg"]:
               for netIntf in securityGroup["sg"]["networkInterfaces"]:

                   if netIntf["Description"] == "":
                      descriptionResource = "<a href='{}'>EC2</a>".format(self.buildLink("EC2_PRIVATEIP",netIntf["PrivateIpAddress"]))
                   elif "ELB " in netIntf["Description"]:
                      elbName = re.sub(r'^ELB\s',"",netIntf["Description"])
                      descriptionResource = "<a href='{}'>{}</a>".format(self.buildLink("ELB",elbName), netIntf["Description"])
                   else:
                      descriptionResource = netIntf["Description"]

                   listNetWorkInterfaces += "<li>{} - {} ({})</li>".format(netIntf["NetworkInterfaceId"], descriptionResource, netIntf["PrivateIpAddress"])
            listNetWorkInterfaces += "</ul>\""
        
            colorEven = "#D3D3D3"
            colorOdd  = "#FFFFFF"
            idx       = 0

            tableIngress  = "\"<table width=100% cellspacing=0 cellpadding=3 style='background:white;border:1px black solid;font-family: Courier New, Courier, monospace;font-size: 12px;'>"
            tableIngress += "<tr style='border-bottom:1px black solid'><td colspan='4' style='background:#2F4F4F;color:white;text-align:center;font-style:italic;font-weight:bolder;text-transform:uppercase;'>Inbound Rules</td></tr>"
            tableIngress += "<tr style='background:#696969;color:white;'><td align='center' style='border-right:1px black solid;border-top:1px black solid'>Protocol</td>" + \
                               "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Port Range</td>" + \
                               "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Source</td>" + \
                               "<td align='center' style='border-top:1px black solid'>Description</td>" + \
                            "</tr>"

            if securityGroup["sg"]["ipPermissions"]:
               for ingress in securityGroup["sg"]["ipPermissions"]:
                   for ipRange in ingress["ipRanges"]:
                     
                       protocol = "All" if ingress["ipProtocol"].rstrip().lstrip() == "-1" else str(ingress["ipProtocol"]).upper()
   
                       portRange = str(ingress["fromPort"])
                       if ingress["fromPort"] != ingress["toPort"]:
                          portRange += ("-" + str(ingress["toPort"]))
   
                       lineBackColor  = colorEven if idx % 2 == 0 else colorOdd
                       lineTableIngress = "<tr style='background:{linebackcolor};'><td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                            "<td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                            "<td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                            "<td style='border-top:1px black solid'>{}</td>" + \
                                          "</tr>"
                       
                       tableIngress += lineTableIngress \
                                       .format(protocol, \
                                               portRange, \
                                               ipRange["cidrIp"], \
                                               ipRange["description"], \
                                               linebackcolor=lineBackColor)
                       idx+=1
            tableIngress += "</table>\""

            idx = 0

            tableEgress  = "\"<table width=100% cellspacing=0 cellpadding=3 style='background:white;border:1px black solid;font-family: Courier New, Courier, monospace;font-size: 12px;'>"
            tableEgress += "<tr style='border-bottom:1px black solid'><td colspan='4' style='background:#2F4F4F;color:white;text-align:center;font-style:italic;font-weight:bolder;text-transform:uppercase;'>Outbound Rules</td></tr>"
            tableEgress += "<tr style='background:#696969;color:white;'><td align='center' style='border-right:1px black solid;border-top:1px black solid'>Protocol</td>" + \
                              "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Port Range</td>" + \
                              "<td align='center' style='border-top:1px black solid'>Destination</td>" + \
                           "</tr>"
            for egress in securityGroup["sg"]["ipPermissionsEgress"]:

                protocol = "All" if egress["ipProtocol"].rstrip().lstrip() == "-1" else str(egress["ipProtocol"]).upper()

                for ipRange in egress["ipRanges"]:

                    lineBackColor  = colorEven if idx % 2 == 0 else colorOdd
                    lineTableEgress = "<tr style='background:{linebackcolor};'><td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                         "<td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                         "<td style='border-top:1px black solid'>{}</td>" + \
                                       "</tr>"
                    tableEgress += lineTableEgress.format(protocol, \
                                                          ipRange["cidrIp"], \
                                                          ipRange["description"], \
                                                          linebackcolor=lineBackColor)
                    idx+=1
            tableEgress += "</table>\""

            line = "{},{},{},{},{},{},{}".format(sgId,vpcId,listNetWorkInterfaces,tableIngress,tableEgress, \
                                         "#DFF2E2", \
                                         self.buildLink("SECURITYGROUP",sgId))
            csvLines.append(line)


        with open(fileName, 'w') as csvFile:
             csvFile.write(template + '\n')
             for line in csvLines:
                 csvFile.write(line + '\n')
        return fileName

    ##
    ## NACLs
    ##
    def generateListNacls(self, templateName, header, content):
        template = self.openTemplate(templateName)

        #fileName = os.path.join(expanduser("~"), "listNacls.csv") 
        fileName = os.path.join(expanduser("~"), 'listNacls_' + Utils.labelTimestamp() + ".csv")
        try:
            os.remove(fileName)
        except OSError:
            pass

        currentnaclId = None
        currentVpcId  = None
        csvLines      = []
        
        for row in content:
            vpcId    = row[1]
            naclId   = row[2]
            subnetId = row[3]
            entries  = row[4] if len(row) > 4 else ""

            if not currentnaclId or currentnaclId != naclId:
               if currentnaclId:
                  labelCurrentVpc = "\"<a href='{}'>{}</a>\"".format(self.buildLink("VPC",currentVpcId),currentVpcId) 
                  csvLines.append( self.createNaclLine(currentnaclId, indexRule, subnets, rules, labelCurrentVpc) )
                  
               currentnaclId      = naclId
               currentVpcId       = vpcId
               indexRule          = 0
               rules              = []
               subnets            = []
        
            if subnetId.rstrip().lstrip() != "":
               subnets.append(subnetId)

            # Rules
            entrySplit = entries.split("|")
            for idx, r in enumerate(entrySplit):
                if idx == 0:
                   cidrblock =  self.cleanRuleField(r)
                elif idx == 1:
                   type =  self.cleanRuleField(r)
                elif idx == 2:
                   state =  self.cleanRuleField(r)
                elif idx == 3:
                   number =  int(self.cleanRuleField(r))
                elif idx == 4:
                   protocol =  self.cleanRuleField(r) 
                   indexRule += 1
                   record = {"index": indexRule, "cidrblock": cidrblock,"type": type, "state": state, "number": number, "protocol": protocol}
                   rules.append(record)

        if currentnaclId:
           labelCurrentVpc = "\"<a href='{}'>{}</a>\"".format(self.buildLink("VPC",currentVpcId),currentVpcId)
           csvLines.append( self.createNaclLine(currentnaclId, indexRule, subnets, rules, labelCurrentVpc) )

        with open(fileName, 'w') as csvFile:
             csvFile.write(template + '\n')
             for line in csvLines:
                 csvFile.write(line + '\n')
        return fileName   
    def createNaclLine(self, currentnaclId, indexRule, subnets, rules, vpcId):
        subnetTable = "\"<table cellspacing=0 cellpadding=0>"
        for s in subnets:
            s = re.sub('\(\d*\)','',s)
            s = s.rstrip().lstrip()
            labelSubnet = "<a href='{}'>{}</a>".format(self.buildLink("SUBNET",s),s)
            subnetTable += "<tr><td>&nbsp;&nbsp;-&nbsp;" + labelSubnet + "</td></tr>"
        subnetTable += "</table>\""

        colorEven = "#D3D3D3"
        colorOdd  = "#FFFFFF"
        idx       = 0
        
        rulesTableInbound = "\"<table width=100% cellpadding=3 cellspacing=0 style='background:white;border:1px black solid;font-family: Courier New, Courier, monospace;font-size: 12px;'>"
        rulesTableInbound += "<tr style='border-bottom:1px black solid'><td colspan='4' style='background:#2F4F4F;color:white;text-align:center;font-style:italic;font-weight:bolder;text-transform:uppercase;'>Inbound Rules</td></tr>"
        rulesTableInbound += "<tr style='background:#696969;color:white;'><td align='center' style='border-right:1px black solid;border-top:1px black solid'>Rules Number</td>" + \
                                 "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Protocol</td>" + \
                                 "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Source</td>" + \
                                 "<td align='center' style='border-top:1px black solid'>Allow/Deny</td>" + \
                            "</tr>"
        
        
        for e in rules:
            if e["type"] == "Egress":
               lineBackColor  = colorEven if idx % 2 == 0 else colorOdd
               stateColor     = "red" if e["state"].lower() == "deny" else "blue"
               rulesTableInbound += "<tr style='border-bottom:1px black solid;background:{linebackcolor}'>".format(linebackcolor=lineBackColor)
               rulesTableInbound += "  <td style='border-right:1px black solid;border-top:1px black solid;color:{}'>".format(stateColor) + ("*" if e["number"] == 32767 else str(e["number"])) + "</td>"
               rulesTableInbound += "  <td style='border-right:1px black solid;border-top:1px black solid;color:{}'>".format(stateColor) + ("All" if e["protocol"] == "-1" else e["protocol"]) + "</td>"
               rulesTableInbound += "  <td style='border-right:1px black solid;border-top:1px black solid;color:{}'>".format(stateColor) + e["cidrblock"] + "</td>"
               rulesTableInbound += "  <td style='border-top:1px black solid;color:{}'>".format(stateColor) + e["state"].capitalize() + "</td>"
               rulesTableInbound += "</tr>"
               idx+=1
        rulesTableInbound   += "</table>\""

        idx = 0

        rulesTableOutbound = "\"<table width=100% cellpadding=3 cellspacing=0 style='background:white;border:1px black solid;font-family: Courier New, Courier, monospace;font-size: 12px;'>"
        rulesTableOutbound += "<tr style='border-bottom:1px black solid'><td colspan='4' style='background:#2F4F4F;color:white;text-align:center;font-style:italic;font-weight:bolder;text-transform:uppercase;'>Outbound Rules</td></tr>"
        rulesTableOutbound += "<tr style='background:#696969;color:white;'><td align='center' style='border-right:1px black solid;border-top:1px black solid'>Rules Number</td>" + \
                                 "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Protocol</td>" + \
                                 "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Source</td>" + \
                                 "<td align='center' style='border-top:1px black solid'>Allow/Deny</td>" + \
                            "</tr>"
        for e in rules:
            if e["type"] != "Egress":
               lineBackColor  = colorEven if idx % 2 == 0 else colorOdd
               stateColor     = "red" if e["state"].lower() == "deny" else "blue"
               rulesTableOutbound += "<tr style='border-bottom:1px black solid;background:{linebackcolor}'>".format(linebackcolor=lineBackColor)
               rulesTableOutbound += "  <td style='border-right:1px black solid;border-top:1px black solid;color:{}'>".format(stateColor) + ("*" if e["number"] == 32767 else str(e["number"])) + "</td>"
               rulesTableOutbound += "  <td style='border-right:1px black solid;border-top:1px black solid;color:{}'>".format(stateColor) + ("All" if e["protocol"] == "-1" else e["protocol"]) + "</td>"
               rulesTableOutbound += "  <td style='border-right:1px black solid;border-top:1px black solid;color:{}'>".format(stateColor) + e["cidrblock"] + "</td>"
               rulesTableOutbound += "  <td style='border-top:1px black solid;color:{}'>".format(stateColor) + e["state"].capitalize() + "</td>"
               rulesTableOutbound += "</tr>"
               idx+=1
        rulesTableOutbound   += "</table>\""

        naclid5digits = currentnaclId[-5:]
        naclidStamp   = "&nbsp;&nbsp;&nbsp;&nbsp;<div style='border-color:black;border-width:1px;border-style:solid;border-radius:3px;display:inline;color:white;background:blue;font-size:16px'>&nbsp;&nbsp;" + naclid5digits + "&nbsp;&nbsp;</div>"
        finalLine     = "\"<b>"+currentnaclId+"</b>" + naclidStamp + "\"" \
                    + "," \
                    + vpcId \
                    + "," + \
                    subnetTable   \
                    + "," + \
                    rulesTableInbound \
                    + "," + \
                    rulesTableOutbound   \
                    + "," + \
                    "#dae8fc" \
                    + "," + \
                    self.buildLink("NACL",currentnaclId)
        return finalLine
    def cleanRuleField(self, field):
        return re.sub('\(\d*\)','',field.rstrip().lstrip())

    
    