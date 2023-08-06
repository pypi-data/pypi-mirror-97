# coding=utf-8

import sys, cmd, os, ast, signal
from datetime import datetime
from os.path import expanduser
from arnparse import arnparse
import configparser
import json
import xlsxwriter
import dominate
from dominate.tags import *

from pyawscp.Config import Config
from pyawscp.Utils import Utils, Style, Emoticons
from pyawscp.Functions import Functions

TRANSFER_S3  = "TRANSFER_S3"
PREFERENCES = "PREFERENCES" 

# # python -m pyawscp.JustOneShot
class DoWhateverYouSupposeYouShouldDo:

    def __init__(self):
        self.preferences = Config()
        if self.preferences.isValidCookieTempCredentials():
           roleActived = True
           intro  = "\n"
           intro += Style.GREEN + "  " + Emoticons.cookie() + Emoticons.cookie() + Emoticons.cookie() + " " + Emoticons.pointRight() + \
                    " AWS Temporary "+Style.IBLUE+"Session"+Style.GREEN+" Credentials is still "+Style.IBLUE+"valid"+Style.GREEN+" and activated!"
           intro += "\n"
           intro += Style.GREEN + "            Expires at: " + Style.IBLUE + self.preferences.cookieTempCredentials().humanReadFormatExpirationDate() + " (Remaining: " + str(self.preferences.cookieTempCredentials().timeToExpire()) + ")"
           intro += "\n"
           print(intro)
    
        configFileIni = configparser.ConfigParser()
        configFileIni.read(expanduser("~") + "/.pyawscp/pyawscp.ini")
        self.preferences.awsProfile               = configFileIni[PREFERENCES]["aws-profile"]
        self.preferences.awsRegion                = configFileIni[PREFERENCES]["aws-region"]
        self.preferences.awsTags                  = ast.literal_eval(configFileIni[PREFERENCES]["aws-tags"])
        self.preferences.printResults             = configFileIni[PREFERENCES]["print-results"] in ['True','true']
        self.preferences.tableLineSeparator       = configFileIni[PREFERENCES]["table-line-separator"] in ['True','true']
        self.preferences.uploadChunkSizeMultipart = configFileIni[TRANSFER_S3]["chunkSize"]
        self.preferences.uploadThresholdMultipart = configFileIni[TRANSFER_S3]["threshold"]
    
        if "assume-role" in configFileIni[PREFERENCES]:
           self.preferences.assumeRole           = configFileIni[PREFERENCES]["assume-role"]
        else:
           self.preferences.assumeRole           = ""
        if "mfa-serial" in configFileIni[PREFERENCES]:
           self.preferences.mfaSerial           = configFileIni[PREFERENCES]["mfa-serial"]
        else:
           self.preferences.mfaSerial           = ""

    def botoSession(self):
        return self.preferences.botoSession()
    


    def doIt(self):
        self.getAllResources()

        

    ## List Resources 
    ## BEGIN
    def getAllResources(self):
        client = self.botoSession().client('resourcegroupstaggingapi')

        resourceDict              = {}
        resourceDict["resources"] = []

        pages     = 1
        resources = client.get_resources()
        self.processAllResourcesPage(resources, pages, resourceDict)
        tokenPagination = resources["PaginationToken"] if "PaginationToken" in resources else None
        
        if tokenPagination:
           while True:
              pages    += 1
              resources = client.get_resources(PaginationToken=tokenPagination)
              self.processAllResourcesPage(resources, pages, resourceDict)
              tokenPagination = resources["PaginationToken"] if "PaginationToken" in resources else None
              if not tokenPagination:
                 break
              # if pages > 1:
              #    break
        
        print(Style.IGREEN + "Total Pages Processed.....: " + str(pages))
        print(Style.GREEN)

        # Grouping
        totalByResourceType = []
        totalByService      = []
        totalBy             = {}

        for resource in resourceDict["resources"]:
            if not resource["resourceType"] in totalByResourceType:
               totalByResourceType.append(resource["resourceType"]) 

            if not resource["service"] in totalByService:
               totalByService.append(resource["service"])

            awsService = "{}_{}".format(resource["service"],resource["resourceType"])
            if  awsService in totalBy:
                totalBy[awsService]["total"] = totalBy[awsService]["total"] + 1
            else:
                totalBy[awsService] = {
                    "total": 1,
                    "resourceType": resource["resourceType"],
                    "service": resource["service"]
                }

        
        jsonContent = Utils.dictToJson(resourceDict)
        #print(jsonContent)
        print("Writing JSON List AWS Resources...")
        with open("d:\Downloads\\resources_{}.json".format(Utils.labelTimestamp()), 'w') as fout:
            fout.write(jsonContent)
            fout.flush()

        # Write an Excel
        print("Writing Excel List AWS Resources...")
        workbook = xlsxwriter.Workbook("d:\Downloads\\resources_{}.xlsx".format(Utils.labelTimestamp()))
        worksheet = workbook.add_worksheet("AWS Resources List")
        worksheet.write("A1", "Service")
        worksheet.write("B1", "Resource Type")
        worksheet.write("C1", "Name")
        worksheet.write("D1", "Account")
        worksheet.write("E1", "Region")
        worksheet.write("F1", "ARN")
        excelRow = 1
        for resource in resourceDict["resources"]:
            excelRow += 1
            worksheet.write("A" + str(excelRow), resource["service"])
            worksheet.write("B" + str(excelRow), resource["resourceType"])
            worksheet.write("C" + str(excelRow), resource["name"])
            worksheet.write("D" + str(excelRow), resource["accountId"])
            worksheet.write("E" + str(excelRow), resource["region"])
            worksheet.write("F" + str(excelRow), resource["arn"])

        excelRow = 1    
        worksheetSummary = workbook.add_worksheet("AWS Resources Summary")
        worksheetSummary.write("A1", "Service")
        worksheetSummary.write("B1", "Resource Type")
        worksheetSummary.write("C1", "Total")
        for key in totalBy:
            excelRow += 1
            worksheetSummary.write("A" + str(excelRow), totalBy[key]["service"])
            worksheetSummary.write("B" + str(excelRow), totalBy[key]["resourceType"])
            worksheetSummary.write("C" + str(excelRow), totalBy[key]["total"])
        workbook.close()
        
        # Write an HTML Summary
        h = html()
        with h.add(body()):
            with div(id='content'):
                attr(style='font-family:Arial')
                hr()
                h1('AWS Resources Summary')
                with table():
                    attr(cellpadding=3)
                    attr(cellspacing=0)
                    attr(style='width:100%;border:1px black solid;font-family:Arial;font-size: 12px;')
                    lheader = tr()
                    with lheader:
                        attr(align="center")
                        attr(style="background:black;color:white;font-weight:bolder;font-size:15px")
                        with td('Service'):
                            pass
                        with td('Resource Type'):
                            pass
                        with td('Total'):
                            pass
                    colorEven = "#D3D3D3"
                    colorOdd  = "#FFFFFF"
                    idx       = 0
                    for key in totalBy:
                        lineBackColor  = colorEven if idx % 2 == 0 else colorOdd
                        l = tr()
                        with l:
                            styleTd = "font-size:12px;font-family:Consolas;background:{background};color:black;font-weight:bolder;border-top:1px solid black;border-right:1px solid black".format(background=lineBackColor)
                            with td(totalBy[key]["service"]):
                                attr(style=styleTd)
                            with td(totalBy[key]["resourceType"] if totalBy[key]["resourceType"] else ""):
                                attr(style=styleTd)
                            with td(totalBy[key]["total"]):
                                attr(style=styleTd)
                        idx += 1

        print("Writing HTML Summary AWS Resources...")
        with open("d:\Downloads\\resources_summary_{}.html".format(Utils.labelTimestamp()), 'w') as fout:
        #with open("d:\Downloads\\resources_summary.html", 'w') as fout:
             fout.write(str(h))
        
        # Write Complete HTML List
        h = html()
        with h.add(body()):
            with div(id='content'):
                attr(style='font-family:Arial')
                hr()
                h1('AWS Resources')
                with table():
                    attr(cellpadding=3)
                    attr(cellspacing=0)
                    attr(style='width:100%;border:1px black solid;font-family:Arial;font-size: 12px;')
                    lheader = tr()
                    with lheader:
                        attr(align="center")
                        attr(style="background:black;color:white;font-weight:bolder;font-size:15px")
                        with td('#'):
                            pass
                        with td('Service'):
                            pass
                        with td('Resource Type'):
                            pass
                        with td('Name'):
                            pass
                        with td('Account'):
                            pass
                        with td('Region'):
                            pass
                        with td('ARN'):
                            pass
                    
                    colorEven = "#D3D3D3"
                    colorOdd  = "#FFFFFF"
                    idx       = 0
                    for resource in resourceDict["resources"]:
                        lineBackColor  = colorEven if idx % 2 == 0 else colorOdd
                        l = tr()
                        with l:
                            styleTd = "font-size:12px;font-family:Consolas;background:{background};color:black;font-weight:bolder;border-top:1px solid black;border-right:1px solid black".format(background=lineBackColor)
                            with td(str(idx+1)):
                                attr(style=styleTd)
                            with td(str(resource["service"])):
                                attr(style=styleTd)
                            with td(str(resource["resourceType"])):
                                attr(style=styleTd)
                            with td(str(resource["name"])):
                                attr(style=styleTd)
                            with td(str(resource["accountId"])):
                                attr(style=styleTd)
                            with td(str(resource["region"])):
                                attr(style=styleTd)
                            with td(str(resource["arn"])):
                                attr(style=styleTd)
                        idx += 1

        print("Writing HTML List AWS Resources...")
        with open("d:\Downloads\\resources_{}.html".format(Utils.labelTimestamp()), 'w') as fout:
        #with open("d:\Downloads\\resources.html", 'w') as fout:
             fout.write(str(h))

    def processAllResourcesPage(self, resources, pages, resourceDict):
        print(Style.IGREEN + 'Processing page... '+ str(pages) + Style.RESET)

        for resource in resources["ResourceTagMappingList"]:

            arn           = arnparse(resource["ResourceARN"])
            name          = ""
            service       = arn.service
            region        = arn.region
            accountId     = arn.account_id
            resource_type = arn.resource_type 

            #print("\033[32mService:\033[96m{}\n\033[32mName:\033[96m{}\n\033[32mResource Type:\033[96m{}\n".format(service, name, resource_type))

            for tag in resource["Tags"]:
                if "NAME" == tag["Key"].upper():
                    name = tag["Value"]
                    break
            
            resourceDict["resources"].append({
                "arn": resource["ResourceARN"],
                "name": name,
                "service": service,
                "region": region,
                "accountId": accountId,
                "resourceType": resource_type
            })
    ## List Resources 
    ## END

def main():
    doWhateverItNeedsToBeDone = DoWhateverYouSupposeYouShouldDo()
    doWhateverItNeedsToBeDone.doIt()
    # val = input("Enter your value: ") 
    # print(val) 
    # AWS_CREDENTIALS_DIR = "~/.aws/"
    # print("") 
    # print("")
    # print("\033[31m ---> Ops!\033[33m AWS CREDENTIALS NOT FOUND!")
    # print("") 
    # print("") 
    # print("\033[34m ---> \033[33mPlease, configure your AWS Credentials:")
    # print("\033[34m      \033[33m1. Create the folder \033[35m{}\033[0m".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[33m2. Create the file \033[35m{}credentials\033[33m with the  content:".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[94m   [default]")
    # print("\033[34m      \033[94m   aws_access_key_id = YOUR_ACCESS_KEY")
    # print("\033[34m      \033[94m   aws_secret_access_key = YOUR_SECRET_KEY")
    # print("\033[34m      \033[33m3. Optionally, create the file \033[35m{}config\033[33m with your default region:".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[94m   [default]")
    # print("\033[34m      \033[94m   region=us-east-1")
    # print("")
    # print("")


if __name__ == '__main__':
    # python -m pyawscp.JustOneShot
    main()    
        