import sys
import os, re
from random import randrange
from os.path import expanduser
from pyawscp.Utils import Utils
from pyawscp.CsvDrawIo import CsvDrawIo
from pygments import highlight, lexers, formatters

class CsvDrawIoNetworking(CsvDrawIo):

    DEFAULT_WIDTH  = 50
    DEFAULT_HEIGHT = 50

    VPC_COLS        = 2
    VPC_XCOORD      = 20
    VPC_YCOORD      = 20
    VPC_WIDTH       = 1000
    VPC_HEIGHT      = 550
    VPC_GAP_ROWS    = 100
    VPC_GAP_COLS    = 80
    VPC_BOTTOM      = int(VPC_HEIGHT - 48) # Position in Px of the bottom of the Subnets boxes

    SUBNET_COLS     = 4
    SUBNET_XMARGIN  = 50
    SUBNET_YMARGIN  = 40
    SUBNET_GAP_ROWS = 20
    SUBNET_GAP_COLS = 30
    SUBNET_WIDTH    = 210
    SUBNET_HEIGHT   = 180
    SUBNET_BOTTOM   = int(SUBNET_HEIGHT - 65)

    ROUTETABLE_WIDTH   = 60
    ROUTETABLE_HEIGHT  = 60
    ROUTETABLE_XMARGIN = 40
    ROUTETABLE_YMARGIN = (int(SUBNET_HEIGHT / 4)) + 8

    NACLS_WIDTH   = 60
    NACLS_HEIGHT  = 60
    NACLS_XMARGIN = 110
    NACLS_YMARGIN = (int(SUBNET_HEIGHT / 4)) + 8

    TGWS_XCOORD      = 80
    TGWS_YCOORD      = 5
    TGWS_GAP_COLS    = 400
    TGWS_GAP_ROWS    = 80
    TGWS_HEIGHT      = 60
    TGWS_WIDTH       = 120
    TGWS_HEIGHT_ICON = 60
    TGWS_WIDTH_ICON  = 60
    TGWS_COLS        = 6

    TGWATTACHMENTS_XCOORD   = -800
    TGWATTACHMENTS_YCOORD   = -10
    TGWATTACHMENTS_GAP_COLS = 20
    TGWATTACHMENTS_GAP_ROWS = 100
    TGWATTACHMENTS_WIDTH    = 700
    TGWATTACHMENTS_COLS     = 1

    TGWROUTETABLE_XCOORD   = 50
    TGWROUTETABLE_YCOORD   = -400
    TGWROUTETABLE_WIDTH    = 650
    TGWROUTETABLE_GAP_COLS = 50

    AZ_WIDTH       = 1050
    AZ_HEIGHT      = 250

    def __init__(self, config):
        super().__init__(config)
        self.graph = Graph()
    
    def adjustments(self, data, addRouteTables, addNacls, addTgws, addRtTgws):
        totalAzs = []
        # WIDTH VPC by Qtde Subnets per AZs in VPC
        qtdeSubnetsByVpcAz = {}
        for vpc in data["vpcs"]:
            for subnet in vpc["subnets"]:
                # Azs by VPC
                groupByKey = "{}_{}".format(vpc["vpcId"],subnet["az"])
                if groupByKey in qtdeSubnetsByVpcAz:
                   qtdeSubnetsByVpcAz[groupByKey]["total"] = qtdeSubnetsByVpcAz[groupByKey]["total"] + 1
                else:
                   qtdeSubnetsByVpcAz[groupByKey] = {
                       "total": 1
                   }
                
                # total Azs
                if not subnet["az"] in totalAzs:
                   totalAzs.append(subnet["az"])
                
        qtdeSubnetsByAz = 0
        for t in qtdeSubnetsByVpcAz:
            if qtdeSubnetsByVpcAz[t]["total"] > qtdeSubnetsByAz:
               qtdeSubnetsByAz = qtdeSubnetsByVpcAz[t]["total"]
        if qtdeSubnetsByAz > 4:
           self.SUBNET_COLS = 4
        else:
           self.SUBNET_COLS = qtdeSubnetsByAz
        self.VPC_WIDTH  = (self.SUBNET_COLS * (self.SUBNET_WIDTH  + self.SUBNET_GAP_COLS)) + self.SUBNET_XMARGIN

        # Calculate Size of the AZ (Rows to accomodate the most "crowed" VPC)
        biggerQtdeAzs = 0
        for i in qtdeSubnetsByVpcAz:
            if qtdeSubnetsByVpcAz[i]["total"] > biggerQtdeAzs:
               biggerQtdeAzs = qtdeSubnetsByVpcAz[i]["total"]
        rowsForAz  = int(biggerQtdeAzs / 4)
        rowsForAz += (0 if ( (biggerQtdeAzs / 4) == int(biggerQtdeAzs / 4) ) else 1)
        self.AZ_HEIGHT = self.AZ_HEIGHT * (rowsForAz if rowsForAz > 0 else 1)

        if addTgws:
           self.VPC_YCOORD = 150
        
        # Calculate Size of the VPC
        self.VPC_HEIGHT = (self.AZ_HEIGHT + 25) * len(totalAzs)
        self.VPC_BOTTOM = int(self.VPC_HEIGHT - 45)

    ##
    ## Generate the AWS Networking Diagram
    ##
    def generateNetworkingGraph(self, templateName, data, addRouteTables, addNacls, addTgws, addRtTgws):
        self.adjustments(data, addRouteTables, addNacls, addTgws, addRtTgws)
        template = self.openTemplate(templateName)

        fileName = os.path.join(expanduser("~"), 'networkingDiagram_' + Utils.labelTimestamp() + ".csv")
        try:
           os.remove(fileName)
        except OSError:
           pass
        
        # The order matters!!! don't change it!
        self.addVPCs(data)
        self.addAZs(data)
        self.addSubnets(data)
        if addRouteTables:
           self.addRouteTables(data)
        if addNacls:
           self.addNacls(data)
        if addTgws:
           self.addTgws(data)
        if addRtTgws:
           self.addRtTgws(data) 

        linesForClipboard = ""

        # Save File
        with open(fileName, 'w') as csvFile:
             csvFile.write(template + '\n')
             linesForClipboard += (template + '\n')
             for line in self.graph.csvLines:
                 csvFile.write(line + '\n')

        # Copy to Clipboard
        for l in self.graph.csvLines:
            linesForClipboard += (l + "\n")
        Utils.addToClipboard(linesForClipboard)

        return fileName
    
    def addRtTgws(self, data):
        xcoord      = self.TGWROUTETABLE_XCOORD
        ycoord      = self.TGWROUTETABLE_YCOORD
        widthTable  = self.TGWROUTETABLE_WIDTH
        gapCol      = self.TGWROUTETABLE_GAP_COLS

        colorEven   = "#D3D3D3"
        colorOdd    = "#FFFFFF"
        totalTables = 0

        for tgw in data["tgws"]:
            refs = tgw["transitGatewayId"]

            for rt in tgw["routeTables"]:
                """ colorful_json = highlight(Utils.dictToJson(rt), lexers.JsonLexer(), formatters.TerminalFormatter())
                print(" {} ".format(rt["routeTableId"]))
                print(colorful_json)
                print("-".ljust(80,"-")) """

                tgwRouteTableUrl  = "<a style='text-decoration:none;color:yellow;' href='{}'>{}</a>".format(self.buildLink("transitgatewayroutetable", \
                                                                 rt["routeTableId"]), rt["routeTableId"])
                totalTables      += 1
                idx               = 0
                htmlTable  = "\"<table width=100% cellspacing=0 cellpadding=3 style='background:white;border:1px black solid;font-family: Courier New, Courier, monospace;font-size: 12px;'>"
                htmlTable += "<tr style='border-bottom:1px black solid'><td colspan='4' style='background:#2F4F4F;color:white;'>" + \
                             "<span style='text-align:center;font-style:italic;'>Transit Gateway Route Table</span>" + \
                             "<br>{}</br></td></tr>".format(tgwRouteTableUrl)
                htmlTable += "<tr style='background:#696969;color:white;'><td align='center' style='border-right:1px black solid;border-top:1px black solid'>CIDR</td>" + \
                                "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Attachment</td>" + \
                                "<td align='center' style='border-top:1px black solid'>Resource Type</td>" + \
                             "</tr>"

                totalRoutes = 0
                for route in rt["routes"]:
                    for routeAtt in route["attachments"]:
                        totalRoutes += 1

                        lineBackColor = colorEven if idx % 2 == 0 else colorOdd
                        lineTable     = "<tr style='background:{linebackcolor};'><td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                            "<td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                            "<td style='border-top:1px black solid'>{}</td>" + \
                                        "</tr>"
                        
                        attachmentLabel = "<a href='{}'>{}</a>".format(self.buildLink("transitgatewayattachment", routeAtt["transitGatewayAttachmentId"]),routeAtt["transitGatewayAttachmentId"])
                        resourceLabel   = routeAtt["resourceId"]
                        if routeAtt["resourceType"] == "vpc":
                           resourceLabel = "<a href='{}'>{}</a>".format(self.buildLink("vpc", routeAtt["resourceId"]),routeAtt["resourceId"]) 
                        htmlTable += lineTable \
                                    .format(route["destinationCidrBlock"], \
                                     "{} | {}".format(attachmentLabel,resourceLabel), \
                                     routeAtt["resourceType"], \
                                     linebackcolor=lineBackColor)
                        idx+=1

                htmlTable  += "</table>\""
                heightTable = idx * 38
                xcoord      = (widthTable * (totalTables-1)) + (gapCol if totalTables > 1 else 0)
                self.graph.csvLines.append(self.createLineTgwRouteTable(rt, htmlTable,  xcoord, ycoord, widthTable, heightTable, refs))

    def addTgws(self, data):
        xcoord = self.TGWS_XCOORD
        ycoord = self.TGWS_YCOORD

        #TGWS
        colorEven = "#D3D3D3"
        colorOdd  = "#FFFFFF"

        gapCol    = self.TGWS_GAP_COLS
        gapRow    = self.TGWS_GAP_ROWS
        cols      = 1
        colsAttch = 1
        totalHeightAttachments = 0
        for tgw in data["tgws"]:
            idx               = 0
            refs              = "\""
            attachmentsTable  = "\"<table width=100% cellspacing=0 cellpadding=3 style='background:white;border:1px black solid;font-family: Courier New, Courier, monospace;font-size: 12px;'>"
            attachmentsTable += "<tr style='background:#696969;color:white;'><td align='center' style='border-right:1px black solid;border-top:1px black solid'>TGW Attachment</td>" + \
                                  "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>TGW Route Table</td>" + \
                                  "<td align='center' style='border-right:1px black solid;border-top:1px black solid'>Resource</td>" + \
                                  "<td align='center' style='border-top:1px black solid'>Resource Owner</td>" + \
                               "</tr>"

            totalAttachments   = 0
            for attachment in tgw["attachments"]:
                totalAttachments += 1

                lineBackColor        = colorEven if idx % 2 == 0 else colorOdd
                lineAttachmentsTable = "<tr style='background:{linebackcolor};'><td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                         "<td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                         "<td style='border-right:1px black solid;border-top:1px black solid'>{}</td>" + \
                                         "<td style='border-top:1px black solid'>{}</td>" + \
                                       "</tr>"
                if refs != "\"":
                   refs += ","
                refs += attachment["resourceId"]

                tgwRouteTableUrl = "<a href='{}'>{}</a>".format(self.buildLink("transitgatewayroutetable", attachment["association"]["transitGatewayRouteTableId"]),attachment["association"]["transitGatewayRouteTableId"])
                attachmentsTable += lineAttachmentsTable \
                                    .format(attachment["transitGatewayAttachmentId"], \
                                            tgwRouteTableUrl, \
                                            attachment["resourceId"], \
                                            attachment["resourceOwnerId"], \
                                            linebackcolor=lineBackColor)
                idx+=1

            attachmentsTable += "</table>\""
            refs += "\""
            self.graph.csvLines.append(self.createLineTgw(tgw, xcoord, ycoord, refs, self.TGWS_WIDTH_ICON, self.TGWS_HEIGHT_ICON))
            if totalAttachments > 0:
               height     = 40 * totalAttachments
               width      = self.TGWATTACHMENTS_WIDTH
               colsAttch += 1
               if colsAttch > self.TGWATTACHMENTS_COLS:
                  xcoordTableAttachments  = self.TGWATTACHMENTS_XCOORD
                  ycoordTableAttachments  = totalHeightAttachments + self.TGWATTACHMENTS_GAP_ROWS
                  colsAttch = 1
               else:
                  xcoord += (self.TGWATTACHMENTS_WIDTH + TGWATTACHMENTS_GAP_COLS)
               totalHeightAttachments += height 
               lineParent, lineChild = self.createLineTgwTableAttachments(tgw, attachmentsTable, xcoordTableAttachments, ycoordTableAttachments, width, height)
               self.graph.csvLines.append(lineParent)
               self.graph.csvLines.append(lineChild)
            
            cols += 1
            if cols > self.TGWS_COLS:
               xcoord    = self.TGWS_XCOORD
               ycoord   += (self.TGWS_HEIGHT + gapRow)
               cols = 1
            else:
               xcoord += (self.TGWS_WIDTH + gapCol)

    def addVPCs(self, data):
        xcoord = self.VPC_XCOORD
        ycoord = self.VPC_YCOORD
        cols   = 1

        self.graph.vpcs["vpcs"] = []

        #VPCs 
        gapRow = self.VPC_GAP_ROWS
        gapCol = self.VPC_GAP_COLS
        for vpc in data["vpcs"]:
            
            for vpcAz in vpc["azs"]:
                # Store all the existent AZs 
                if vpcAz not in self.graph.azs:
                    self.graph.azs.append(vpcAz)
            
            self.graph.vpcs["vpcs"].append({
                "vpcid": vpc["vpcId"], "xcoord": xcoord, "ycoord": ycoord, "width": self.VPC_WIDTH, "height":  self.VPC_HEIGHT
            })
            self.graph.csvLines.append(self.createLineVpc(vpc, xcoord, ycoord, self.VPC_WIDTH, self.VPC_HEIGHT))
            
            cols += 1
            if cols > self.VPC_COLS:
               xcoord    = self.VPC_XCOORD
               ycoord   += (self.VPC_HEIGHT + gapCol)
               cols = 1
            else:
               xcoord += (self.VPC_WIDTH + gapRow)
        
    def addSubnets(self, data):
        layoutcol = self.SUBNET_COLS
        marginX   = self.SUBNET_XMARGIN
        marginY   = self.SUBNET_YMARGIN
        gapRow    = self.SUBNET_GAP_ROWS
        gapCol    = self.SUBNET_GAP_COLS

        self.graph.subnets["subnets"] = []

        for vpc in data["vpcs"]:
            row = 0
            col = 0

            sortedSubnets = sorted(vpc["subnets"], key=lambda k:(k["az"], k["public"]), reverse=True)
            currentAz     = None
            for subnet in sortedSubnets:
                if not currentAz:
                   currentAz = subnet["az"]

                # Starts another AZ (reset ROW to 0)
                if currentAz != subnet["az"]:
                   currentAz = subnet["az"]
                   row = 0 
                   col = 0

                # Query VPC coordinates
                vpcSubnet = self.findVpc(vpc["vpcId"])
                # Query AZ coordinates
                azVpc     = self.findAzVpc(vpc["vpcId"], subnet["az"])
      
                xcoord = azVpc["xcoord"]
                ycoord = azVpc["ycoord"]
                
                xcoord = (xcoord + marginX) + (self.SUBNET_WIDTH * col)  + ((gapCol * col) if col > 0 else 0)
                ycoord = (ycoord + marginY) + (self.SUBNET_HEIGHT * row) + ((gapRow * row) if row > 0 else 0)
                #print(row,col,xcoord,ycoord,vpc["vpcId"],subnet["az"],subnet["public"])

                self.graph.subnets["subnets"].append({
                    "subnetid": subnet["subnetId"], "xcoord": xcoord, "ycoord": ycoord, "width": self.SUBNET_WIDTH, "height":  self.SUBNET_HEIGHT, "vpcid": vpc["vpcId"]
                })

                self.graph.csvLines.append(self.createLineSubnet(subnet, xcoord, ycoord, subnet["name"], self.SUBNET_WIDTH, self.SUBNET_HEIGHT))
                
                if col >= (layoutcol - 1):
                   col  = 0
                   row += 1
                else:
                   col += 1
        
    def findVpc(self, vpcid):
        for vpc in self.graph.vpcs["vpcs"]:
            if vpcid == vpc["vpcid"]:
               return vpc
        raise ValueError("VPC not found in collection! Something went wrong in your logic, please verify!")
    
    def findAzVpc(self, vpcid, az):
        keyAzByVpc = "{}_{}".format(vpcid,az)
        #for vpc in self.graph.azByVpcs["vpcs"]:
        if keyAzByVpc in self.graph.azByVpcs:
           return self.graph.azByVpcs[keyAzByVpc]
        raise ValueError("AZ by VPC not found in collection! Something went wrong in your logic, please verify!")
    
    def addRouteTables(self, data):
        for vpc in data["vpcs"]:
            sortedSubnets = sorted(vpc["subnets"], key=lambda k:(k["az"], k["public"]))
            for subnet in sortedSubnets:
                subnetInDiagram = self.findRouteTableForSubnet(subnet["subnetId"])
                for rt in subnet["routeTables"]:
                    xcoord = subnetInDiagram["xcoord"] + self.ROUTETABLE_XMARGIN
                    ycoord = subnetInDiagram["ycoord"] + self.ROUTETABLE_YMARGIN
                    self.graph.csvLines.append(self.createLineRouteTable(rt, subnet, xcoord, ycoord, self.ROUTETABLE_WIDTH, self.ROUTETABLE_HEIGHT))

    def addNacls(self, data):
        for vpc in data["vpcs"]:
            sortedSubnets = sorted(vpc["subnets"], key=lambda k:(k["az"], k["public"]))
            for subnet in sortedSubnets:
                subnetInDiagram = self.findRouteTableForSubnet(subnet["subnetId"])
                for nacl in subnet["nacls"]:
                    xcoord = subnetInDiagram["xcoord"] + self.NACLS_XMARGIN
                    ycoord = subnetInDiagram["ycoord"] + self.NACLS_YMARGIN
                    self.graph.csvLines.append(self.createLineNacl(nacl, subnet, xcoord, ycoord, self.NACLS_WIDTH, self.NACLS_HEIGHT))

    def findRouteTableForSubnet(self, subnetid):
        for subnet in self.graph.subnets["subnets"]:
            if subnetid == subnet["subnetid"]:
               return subnet
        raise ValueError("Subnet not found in collection! Something went wrong in your logic, please verify!")

    def addAZs(self, data):
        #AZs
        AZs_Gap_FirstRow = 30
        AZs_Gap_Row      = 5
        for vpc in self.graph.vpcs["vpcs"]:
            idx = 0
            for az in self.graph.azs:
                xcoord = vpc["xcoord"] - int((self.AZ_WIDTH  - self.VPC_WIDTH) / 2)
                ycoord = vpc["ycoord"] + ((idx * (self.AZ_HEIGHT + AZs_Gap_Row)) + AZs_Gap_FirstRow)
                # Gat between AZs
                if idx > 0:
                   ycoord += AZs_Gap_Row
                # else:
                #    ycoord += AZs_Gap_FirstRow

                keyAzByVpcs = "{}_{}".format(vpc["vpcid"],az)
                if not keyAzByVpcs in self.graph.azByVpcs:
                   self.graph.azByVpcs[keyAzByVpcs] = {
                       "xcoord": xcoord,
                       "ycoord": ycoord
                   }

                self.graph.csvLines.append(self.createLineAz(az, vpc, xcoord, ycoord, self.AZ_WIDTH, self.AZ_HEIGHT))
                idx += 1
    
    def createLineAz(self, azid, vpc, x, y, width, height):
        return self.createLine(
                _type="az", _id="{}_{}".format(azid,vpc["vpcid"]), _refs="", 
                _x=x, _y=y, _az=azid, _width=width, _height=height, _tags="az {}".format(azid)
            )
    
    def createLineVpc(self, vpc, x, y, width, height):
        urlVpc = "{}".format(self.buildLink("vpc",vpc["vpcId"]),vpc["vpcId"])
        return self.createLine(
                _type="vpc", _id=vpc["vpcId"], _refs="", _x=x, _y=y, _vpcid=vpc["vpcId"], _cdirblock=vpc["cidrBlock"],
                _name=(vpc["name"] if vpc["name"].rstrip().lstrip() != "" else '" "'),
                _width=width, _height=height,
                _url=urlVpc,
                _tags="vpc"
            )
    
    def createLineSubnet(self, subnet, x, y, name, width, height):
        urlSubnet = "{}".format(self.buildLink("subnet",subnet["subnetId"]),subnet["subnetId"])
        styleSubnet = "publicsubnet" if subnet["public"] else "privatesubnet"
        tags  = "subnet"
        tags += " public" if styleSubnet == "publicsubnet" else " private"
        tags += " " + subnet["az"]
        return self.createLine(
                _type=styleSubnet, _id=subnet["subnetId"], _x=x, _y=y, _cdirblock=subnet["cidrBlock"],
                _width=width, _height=height, _url=urlSubnet, _tags=tags, _name=name
            )
    
    def createLineRouteTable(self, routeTable, subnet, x, y, width, height):
        idRouteTable  = "{}_{}".format(routeTable["routeTableId"],subnet['subnetId'])
        urlRouteTable = "{}".format(self.buildLink("routetable",routeTable["routeTableId"]),routeTable["routeTableId"])
        return self.createLine(
                _type="routetable", _id=idRouteTable, _x=x, _y=y,
                _width=width, _height=height,
                _url=urlRouteTable,
                _resourceidshort = routeTable["routeTableId5Digts"],
                _tags="rt routetable"
            )
    
    def createLineNacl(self, nacl, subnet, x, y, width, height):
        idNacl  = "{}_{}".format(nacl["naclId"],subnet['subnetId'])
        urlNacl = "{}".format(self.buildLink("nacl",nacl["naclId"]),nacl["naclId"])
        return self.createLine(
                _type="nacl", _id=idNacl, _x=x, _y=y,
                _width=width, _height=height,
                _url=urlNacl,
                _resourceidshort = nacl["nacl5Digts"],
                _tags="nacl networkaccesscontrollist"
            )
    
    def createLineTgw(self, tgw, x, y, refs, width, height):
        urlTgw = "{}".format(self.buildLink("transitgateway",tgw["transitGatewayId"]),tgw["transitGatewayId"])
        return self.createLine(
                _type="tgw", _id=tgw["transitGatewayId"], _ownerid=tgw["ownerId"],
                _x=x, _y=y, _refs=refs,
                _width=width, _height=height,
                _url=urlTgw,
                _tags="tgw transitgateway"
            )
    
    def createLineTgwTableAttachments(self, tgw, attachmentTable, x, y, width, height):
        # Parent Container
        parentId = "{}_attachments_container".format(tgw["transitGatewayId"])
        name = "\"&nbsp;<span style='font-size:10px;color:#696969'><i>ATTACHMENTS of </i></span>&nbsp;&nbsp;{}\"".format(tgw["transitGatewayId"])
        lineParent = self.createLine(
                _type="tgw-attachments-container", _id=parentId,
                _x=x, _y=y, _width=width, _height=height,
                _tgwattachmentTable=attachmentTable,
                _name=name,
                _tags="tgwattachments attachments"
            )

        # Child
        childId = "{}_attachments_child".format(tgw["transitGatewayId"])
        lineChild = self.createLine(
                _type="tgw-attachments-table", _id=childId, _ownerid=tgw["ownerId"],
                _resourceparent=parentId,
                _x=x, _y=y, _width=width, _height=height,
                _tgwattachmentTable=attachmentTable,
                _tags="tgwattachments attachments"
            )
        return lineParent, lineChild

    def createLineTgwRouteTable(self, tgwRt, htmlTable, x, y, width, height, refs):
        urlTgwRouteTable = ""
        idTgwRt = tgwRt["routeTableId"]
        return self.createLine(
                _type="tgw-route-table", _id=idTgwRt, _x=x, _y=y,
                _width=width, _height=height, _url=urlTgwRouteTable,
                _tags="tgw-routetable tgw",
                _tgwroutetable=htmlTable,
                _refs=refs
            )

    def createLine(self, **args):
        return "{type},{resourceid},{resourceparent},{refs},{x},{y},{width},{height},{vpcid},{subnetid},{cdirblock},{name},{az},{url},{bottomvpc},{bottomsubnet},{resourceidshort},{ownerid},{tgwattachmenttable},{tags},{tgwroutetable}" \
               .format( \
                type=args["_type"] if "_type" in args else "",
                resourceid=args["_id"] if "_id" in args else "",
                resourceparent=args["_resourceparent"] if "_resourceparent" in args else "\"\"",
                refs=args["_refs"] if "_refs" in args else "",
                x=args["_x"] if "_x" in args else "",
                y=args["_y"] if "_y" in args else "",
                width=args["_width"] if "_width" in args else self.DEFAULT_WIDTH,
                height=args["_height"] if "_height" in args else self.DEFAULT_HEIGHT,
                vpcid=args["_vpcid"] if "_vpcid" in args else "",
                subnetid=args["_subnetid"] if "_subnetid" in args else "",
                cdirblock=args["_cdirblock"] if "_cdirblock" in args else "",
                name=args["_name"] if "_name" in args else "",
                az=args["_az"] if "_az" in args else "",
                url="\"" + args["_url"] + "\"" if "_url" in args else "",
                bottomvpc=args["_bottomvpc"] if "_bottomvpc" in args else self.VPC_BOTTOM,
                bottomsubnet=args["_bottomsubnet"] if "_bottomsubnet" in args else self.SUBNET_BOTTOM,
                resourceidshort=args["_resourceidshort"] if "_resourceidshort" in args else "",
                ownerid=args["_ownerid"] if "_ownerid" in args else "",
                tgwattachmenttable=args["_tgwattachmentTable"] if "_tgwattachmentTable" in args else "",
                tags="\"" + args["_tags"] + "\"" if "_tags" in args else "",
                tgwroutetable=args["_tgwroutetable"] if "_tgwroutetable" in args else ""
            )

class Graph:

    def __init__(self):
        self.csvLines = []
        self.azs      = []
        self.azByVpcs = {}
        self.vpcs     = {}
        self.subnets  = {}


