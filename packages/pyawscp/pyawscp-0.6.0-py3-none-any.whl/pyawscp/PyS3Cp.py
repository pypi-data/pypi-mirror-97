import boto3
import logging
import sys, os
import json
import math
import locale
import requests
from pygments import highlight, lexers, formatters
from botocore.exceptions import ClientError
from datetime import datetime
from datetime import timedelta  
from pyawscp.Functions import Functions
from pyawscp.Utils import Utils, Style
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.TableArgs import TableArgs
from pyawscp.pytransfers3.PyTransferS3 import PyTransferS3

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

class PyS3CP:
    config = None

    def __init__(self, config):
        self.config = config

    def listBucketsS3(self):
        s3api      = self.botoSession().client('s3')
        csvFile    = None

        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        if "," in self.config.commandArguments:
           tableArgs.setArguments(self.config.commandArguments)
           if ",csv" in self.config.commandArguments:
              csvFile = 'results/' + datetime.now().strftime("%Y%m%d-%H%M%S") + "_listBucketsS3.csv"
        else:    
           if "csv" in self.config.commandArguments:
              csvFile = 'results/' + datetime.now().strftime("%Y%m%d-%H%M%S") + "_listBucketsS3.csv"

        filters=[]
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

        #Prefix="general/artifactory/"
        listBuckets = s3api.list_buckets()

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(listBuckets)

        header = ["#","Name", "Creation Date"]
        prettyTable = PrettyTable(header)

        idx_lin    = 0
        totalCount = 0

        if csvFile:
           try:
               os.remove(csvFile)
           except OSError:
               pass

        #locale.setlocale(locale.LC_ALL, '')       

        for bucket in listBuckets["Buckets"]:

           idx_lin += 1

           bucketName   = bucket["Name"]
           creationDate = bucket["CreationDate"].strftime("%Y-%b-%d %H:%M")

           columns = [ str(idx_lin), bucketName, creationDate ]

           prettyTable.addRow(columns)

           #CVS File
           if csvFile:
              if not os.path.exists("results"):
                 os.makedirs("results")
              with open(csvFile, 'a') as the_file:
                 the_file.write(str(idx_lin) + "," + bucketName + "," + creationDate + "\n")

           totalCount += 1      


        resultTxt = ""
        resultTxt = " The List of S3 Buckets, total of..: " + Style.GREEN + format(totalCount,",") + Style.RESET
        
        if (int(tableArgs.sortCol) - 1) > len(columns):
            tableArgs.sortCol = "1"
            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)

        prettyTable.sortByColumn(0)   
        prettyTable.numberSeparator = True
        prettyTable.ascendingOrder(not tableArgs.desc)
        result = resultTxt + "\n\n" + prettyTable.printMe("listBucketsS3",self.config.tableLineSeparator, tableArgs)
        return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_BUCKETS_S3]["name"], result, self.config, jsonResult, True, tableArgs)    
    
    def listObjectsBucketS3(self):
        s3api      = self.botoSession().client('s3')
        bucketName = ""
        prefix     = ""
        csvFile    = None

        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        if "," in self.config.commandArguments:
           bucketName = self.config.commandArguments.split(",")[0]
           tableArgs.setArguments(self.config.commandArguments)
           if ",csv" in self.config.commandArguments:
              csvFile = 'results/' + datetime.now().strftime("%Y%m%d-%H%M%S") + '_listObjectS3_' + bucketName.replace("/","_") + (prefix.replace("/","_") if prefix else "") + '.csv'           
        else:    
           bucketName = tableArgs.cleanPipelineArguments()

        if not bucketName:
           resultTxt = "Where is the bucket? You didn't tell me which Bucket " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.LIST_OBJECTS_BUCKETS_S3,resultTxt, self.config, "", True, tableArgs)

        if bucketName.find("/") > -1:
           prefix     = bucketName[bucketName.find("/")+1:]   
           bucketName = bucketName[:bucketName.find("/")]   

        filters=[]
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

        #Prefix="general/artifactory/"
        bucketName = bucketName.replace("/","")
        prefix     = "" if prefix == "/" else prefix
        if prefix.startswith("/"):
           prefix = prefix[1:]
        try:   
            bucketObjects = s3api.list_objects_v2(Bucket=bucketName, Delimiter = "/", Prefix=prefix)
        except ClientError as ex:
            if ex.response['Error']['Code'] == "NoSuchBucket" or ex.response['Error']['Code'] == "AllAccessDisabled":
               resultTxt = Style.IRED + " Ops.. " + Emoticons.ops() + Style.RESET + " Most likely Bucket \"" + Style.GREEN + bucketName + prefix + Style.RESET + "\" does not exist!" +  Style.RESET
               return Utils.formatResult(Functions.LIST_OBJECTS_BUCKETS_S3,resultTxt, self.config, "", True, tableArgs)
            else:   
               resultTxt = Style.IRED + " Ops.. " + Emoticons.ops() + Style.RESET + " ERROR " + Style.GREEN + "\"" + ex.response['Error']['Code'] + "\"" + Style.RESET
               return Utils.formatResult(Functions.LIST_OBJECTS_BUCKETS_S3,resultTxt, self.config, "", True, tableArgs)
        else:
            if ("CommonPrefixes" not in bucketObjects) and ("Contents" not in bucketObjects): 
               resultTxt = " Ops.. " + Emoticons.ops() + " Nothing else to list inside \"" + Style.GREEN + bucketName + prefix + "\"" + Style.RESET
               return Utils.formatResult(Functions.LIST_OBJECTS_BUCKETS_S3,resultTxt, self.config, "", True, tableArgs)

            jsonResult = None
            if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
               jsonResult = {}
               jsonResult["s3Objects"] = []
            header = ["#","Object", "Count","Size (KB)","Last Modified", "Size (KB)", "Size (MB)", "Size (GB)","Storage Class"]
            prettyTable = PrettyTable(header)
            if csvFile:
               try:
                     os.remove(csvFile)
               except OSError:
                     pass
            #listObjectsBucketS3 onepay-us,prefix=logs/AWSLogs/659915611011/ | logs <-- List the content of each Bucket inside this one
            #listObjectsBucketS3 onepay-us,prefix=logs/AWSLogs/659915611011 | logs  <-- List the Current Bucket
            #locale.setlocale(locale.LC_ALL, '')       
            result = self._listObjectsBucketS3AppendCommonPrefixes(prettyTable, header, bucketObjects, csvFile, bucketName, prefix, s3api, jsonResult)
            totalSizeUnit = ""
            if result["totalSize"] > 0 and result["totalSize"] <= 1024:        
               totalSizeUnit = "Bytes"
            elif result["totalSize"] > 1024 and result["totalSize"] < 1000000:        
               result["totalSize"] = result["totalSize"] / 1000       
               totalSizeUnit = "KB"   
            elif result["totalSize"] >= 1000000 and result["totalSize"] < 1000000000:        
               result["totalSize"] = result["totalSize"] / 1000000       
               totalSizeUnit = "MB"
            else:   
               result["totalSize"] = result["totalSize"] / 1000000000        
               totalSizeUnit = "GB"
            
            resultTxt = ""
            resultTxt = " The S3 Bucket " + Style.GREEN + bucketName + "/" + prefix + Style.MAGENTA + " (not recursive)" + \
                        Style.RESET + "\n     Count of Objects.........: " + Style.GREEN + format(result["totalCount"],",") + \
                        Style.RESET + "\n     Size  of Objects.........: " + Style.GREEN + locale.format("%.2f",result["totalSize"], grouping=True) + " " + totalSizeUnit + Style.RESET
            
            #if (int(tableArgs.sortCol) - 1) > len(columns):
            #    tableArgs.sortCol = "1"
            #    prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.sortByColumn(0)   
            prettyTable.numberSeparator = True
            prettyTable.ascendingOrder(not tableArgs.desc)
            result = resultTxt + "\n\n" + prettyTable.printMe("listObjectsBucketS3",self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_OBJECTS_BUCKETS_S3]["name"], result, self.config, Utils.dictToJson(jsonResult), True, tableArgs)

    def _listObjectsBucketS3AppendCommonPrefixes(self, prettyTable, header, bucketObjects, csvFile, bucketName, prefix, s3api, jsonResult):
        result     = {}
        idx_lin    = 0
        totalSize  = 0
        totalCount = 0

        if "CommonPrefixes" in bucketObjects:
            for object in bucketObjects["CommonPrefixes"]:
                subFolder = object["Prefix"]
                #Count Contents subfolder previously ?!  or not!
                subFolderObjects    = s3api.list_objects_v2(Bucket=bucketName, Delimiter = "/", Prefix=subFolder)
                #print(subFolderObjects)
                subFolderTotalCount = 0
                subFolderTotalSize  = 0
                if "Contents" in subFolderObjects:
                   subFolderTotalCount = len(subFolderObjects["Contents"])
                   for objectSubfolder in subFolderObjects["Contents"]:
                       subFolderTotalSize += objectSubfolder["Size"]
                subFolderTotalSize = subFolderTotalSize / 1000       

                idx_lin += 1
                columns = [ str(idx_lin), subFolder, subFolderTotalCount, math.ceil(subFolderTotalSize) , "--" , "--", "--", "--", "--" ]
    
                if jsonResult:
                   jsonResult["s3Objects"].append({
                      "key": subFolder,
                      "countObjectsInside": subFolderTotalCount,
                      "sizeInKbObjectsInside": subFolderTotalSize,
                      "lastModified": "",
                      "sizeInKb": 0,
                      "sizeInMega": 0,
                      "sizeInGiga": 0
                   })   
    
                prettyTable.addRow(columns)
                if csvFile:
                   if not os.path.exists("results"):
                      os.makedirs("results")
                   with open(csvFile, 'a') as the_file:
                      the_file.write(str(idx_lin) + "," + subFolder + "," + "" +  ","+ "" + ","+ "" + "," + "" + "," + "" + "," + "" + "," + "" + "\n")   

        if "Contents" in bucketObjects:
            for object in bucketObjects["Contents"]:
                key = object["Key"]
                if True:
                #if key != prefix:
                   idx_lin += 1          
                   size        = object["Size"]
                   totalCount += 1
                   totalSize  += size
       
                   sizeInKb   = size / 1024
                   sizeInMega = size / 1000000
                   sizeInGiga = size / 1000000000       
       
                   columns = [ str(idx_lin), key, "--", "--", object["LastModified"].strftime("%d-%b-%y %H:%M"),
                               round(sizeInKb,2), round(sizeInMega,2), round(sizeInGiga,2), object["StorageClass"] ]        
       
                   if jsonResult:
                      jsonResult["s3Objects"].append({
                         "key": key,
                         "countObjectsInside": 0,
                         "sizeInKbObjectsInside": 0,
                         "lastModified": object["LastModified"].strftime("%d-%b-%y %H:%M"),
                         "sizeInKb": sizeInKb,
                         "sizeInMega": round(sizeInMega,2),
                         "sizeInGiga": round(sizeInGiga,2)
                      })            
                   
                   prettyTable.addRow(columns)
       
                   if csvFile:
                      if not os.path.exists("results"):
                         os.makedirs("results")
                      with open(csvFile, 'a') as the_file:
                         the_file.write(str(idx_lin) + "," + key + ",,," + object["LastModified"].strftime("%d-%b-%y %H:%M") + "," + str(sizeInKb)
                         + str(round(sizeInMega,2)) + "," + str(round(sizeInGiga,2)) + "," + object["StorageClass"] + "\n")

        result["idx_lin"]    = idx_lin
        result["totalSize"]  = totalSize
        result["totalCount"] = totalCount
        return result

    """
    # Replaced by the PyTransferS3 Function (same functionality)
    def listMultiPartUploads(self):
        s3api       = self.botoSession().client('s3')
        isRecursive = False
        bucketName  = ""
        prefix      = ""
        csvFile     = None

        tableArgs   = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        if "," in self.config.commandArguments:
           bucketName = self.config.commandArguments.split(",")[0]
           tableArgs.setArguments(self.config.commandArguments)
           if ",recursive" in self.config.commandArguments:
              isRecursive = True
           if "prefix" in self.config.commandArguments:
              for arg in self.config.commandArguments.split(","):
                  if "prefix" in arg:
                      prefix = arg.split("=")[1]
           if ",csv" in self.config.commandArguments:
              csvFile = 'multiPartUpload_' + bucketName.replace("/","_") + (prefix.replace("/","_") if prefix else "") + '.csv'           
        else:    
           bucketName = tableArgs.cleanPipelineArguments()

        if not bucketName:
           resultTxt = "Where is the bucket? You didn't tell me which Bucket " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.LIST_MULTIPART_UPLOADS_S3,resultTxt, self.config, "", True, tableArgs)

        if bucketName.find("/") > -1:
           prefix     = bucketName[bucketName.find("/")+1:]   
           bucketName = bucketName[:bucketName.find("/")]    

        filters=[]
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

        originalPrefix = prefix
        bucketName = bucketName.replace("/","")
        prefix     = "" if prefix == "/" else prefix
        if prefix.startswith("/"):
           prefix = prefix[1:]
        #bucketObjects  = s3api.list_multipart_uploads(Bucket=bucketName, Delimiter = "/", Prefix=prefix)
        bucketObjects  = s3api.list_multipart_uploads(Bucket=bucketName)

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
           jsonResult = Utils.dictToJson(bucketObjects)

        #Debug
        #colorful_json = highlight(Utils.dictToJson(bucketObjects), lexers.JsonLexer(), formatters.TerminalFormatter())
        #print(colorful_json)

        header = ["#","Path","Key", "Initiated", "StorageClass", "Initiator ID", "Initiator Name"]
        prettyTable = PrettyTable(header)

        idx_lin = 0
        idxLin  = [idx_lin]
        if csvFile:
           try:
               os.remove(csvFile)
           except OSError:
               pass

        uploads = False
        columns = []
        if "Uploads" in bucketObjects:
            uploads = True
            path    = bucketObjects["Bucket"]
            for object in bucketObjects["Uploads"]:
                path          = bucketName + "/" + prefix
                key           = object["Key"]
                initiated     = object["Initiated"].strftime("%Y-%b-%d %H:%M") 
                storageClass  = object["StorageClass"]
                initiatorId   = object["Initiator"]["ID"]
                initiatorName = object["Initiator"]["DisplayName"]
                
                idx_lin += 1
                idxLin   = [idx_lin]
                columns  = [ str(idx_lin), path, key, initiated , storageClass, initiatorId, initiatorName ]        

                prettyTable.addRow(columns)

                if csvFile:
                   line = str(idx_lin) + "," + path + "," + key + "," + initiated + "," + storageClass + "," + initiatorId + "," + initiatorName + "\n"
                   #CVS File
                   with open(csvFile, 'a') as the_file:
                        the_file.write(line)
        
        if "CommonPrefixes" in bucketObjects and isRecursive:
            idxLin = [idx_lin]
            for children in bucketObjects["CommonPrefixes"]:
                prefix = children["Prefix"]
                self._listMultiPartUploadsChild(s3api,bucketName,prefix,idxLin,prettyTable,isRecursive,csvFile)

        resultTxt = ""
        resultTxt = " The S3 Bucket " + Style.GREEN + bucketName + "/" + originalPrefix + Style.MAGENTA + \
                    Style.RESET + "\n has total of " + Style.GREEN + format(idxLin[0],",") + \
                    Style.RESET + " multipart uploads not finished" + Style.RESET
        
        #if (int(tableArgs.sortCol) - 1) > len(columns):
        #    tableArgs.sortCol = "1"
        #    prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)

        if uploads or len(prettyTable.content) > 1:
           prettyTable.sortByColumn(0)   
           prettyTable.numberSeparator = True
           prettyTable.ascendingOrder(not tableArgs.desc)
           result = resultTxt + "\n\n" + prettyTable.printMe("originName",self.config.tableLineSeparator, tableArgs)
           return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_MULTIPART_UPLOADS_S3]["name"], result, self.config,jsonResult, True, tableArgs)
        else:
           result = resultTxt + "\n\n" + Style.GREEN + " No Uploads found" + Style.RESET
           return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_MULTIPART_UPLOADS_S3]["name"], result, self.config,jsonResult, True, tableArgs)

    def _listMultiPartUploadsChild(self,s3api,bucketName,prefix,idxLin,prettyTable,isRecursive,csvFile):
        bucketObjects = s3api.list_multipart_uploads(Bucket=bucketName, Delimiter = "/", Prefix=prefix)

        #Debug
        #colorful_json = highlight(Utils.dictToJson(bucketObjects), lexers.JsonLexer(), formatters.TerminalFormatter())
        #print(colorful_json)

        if "Uploads" in bucketObjects:
            for object in bucketObjects["Uploads"]:
                path          = bucketName + "/" + prefix
                key           = object["Key"]
                initiated     = object["Initiated"].strftime("%Y-%b-%d %H:%M") 
                storageClass  = object["StorageClass"]
                initiatorId   = object["Initiator"]["ID"]
                initiatorName = object["Initiator"]["DisplayName"]

                idxLin[0] = idxLin[0] + 1
                columns  = [ str(idxLin[0]), path, key, initiated , storageClass, initiatorId, initiatorName ]        

                prettyTable.addRow(columns)

                if csvFile:
                   line = str(idxLin[0]) + "," + path + "," + key + "," + initiated + "," + storageClass + "," + initiatorId + "," + initiatorName + "\n"
                   #CVS File
                   with open(csvFile, 'a') as the_file:
                        the_file.write(line)

        if "CommonPrefixes" in bucketObjects and isRecursive:
            for children in bucketObjects["CommonPrefixes"]:
                prefix = children["Prefix"]
                self._listMultiPartUploadsChild(s3api,bucketName,prefix,idxLin,prettyTable,isRecursive,csvFile)
    """            

    # TODO: Add this as a function to Shell
    def preSignURL(self):
        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        # one week
        #expiration = 604800
        # Default: One hour 
        expiration = 3600

        verbose = False
        args = tableArgs.cleanPipelineArguments()
        if not "," in args:
           print(Emoticons.ops() + " --> "+ Style.RED + "Ops... " + Style.RESET + " No arguments?!?\n       Check how to use it: " + Style.IBLUE + "help s3PreSignedURL\n")
           return None
        else:
           a = args.split(",")
           bucketName = a[0]
           objectName = a[1]
           if bucketName == "verbose" or objectName == "verbose":
              print(Emoticons.ops() + " --> "+ Style.RED + "Ops... " + Style.RESET + " The Bucket and Object must be the first and second paramater informed. Check it:" + Style.IBLUE + " help s3PreSignedURL\n")
              return None
           if len(a) > 2:
              if a[2] == "verbose":
                 verbose = True
              else:
                 try:
                    expiration = int(a[2])
                 except:
                    pass
           if len(a) > 3:
              if a[3] == "verbose":
                 verbose = True
              else:
                 try:
                    expiration = int(a[3])
                 except:
                    pass
        
        if expiration < 900 or expiration > 604800:
           print(Emoticons.ops() + " --> "+ Style.RED + "Ops... " + Style.RESET + " Expiration: minimum is " + Style.IGREEN + "15 minutes" + Style.RESET + ", maximum is " + Style.IGREEN + "7 days" + Style.RESET + ", please verify!" + Style.IBLUE + "   help s3PreSignedURL\n")
           return None
            
        s3api = self.botoSession().client('s3')
        # To Access the object
        url = s3api.generate_presigned_url('get_object',
                                             Params={
                                                'Bucket': bucketName,
                                                'Key': objectName
                                             },
                                             ExpiresIn=expiration,
                                             HttpMethod="GET")
        Utils.addToClipboard(url)
        if verbose:
           response = requests.get(url)
           print(Style.IGREEN + Emoticons.wink() + " --> Status")
           print(response)
           print(Style.IGREEN + Emoticons.wink() + " --> Object Content:")
           print(response.text)
        print(Style.IGREEN + Emoticons.wink() + " --> Ok!")
        print(Style.GREEN + "-".ljust(80,"-") + "\n" + Style.IBLUE + url + Style.IBLUE + "\n" + Style.GREEN + "-".ljust(80,"-"))
        print(Emoticons.wink() + " --> " + Style.IGREEN +"The " + Style.IBLUE + "URL" + Style.GREEN + " it copied to your clipboard already!\n\n")
        return url

    def ajustProfile(self):
        return "default" if not self.config.awsProfile or self.config.awsProfile == "" else self.config.awsProfile

    def listUploads(self):
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        args = tableArgs.cleanPipelineArguments()
        if "," in args:
           bucket  = args.split(",")[0]
        else:
           bucket  = args

        if not bucket or bucket == "":
           msg = "\n" + \
                 Style.IRED + Emoticons.error() + Style.GREEN + " Ops! First, you need to tell the name of the Bucket..." + \
                 Style.RESET + "\n"
           return msg
           

        prefix = None
        if "/" in bucket:
           prefix = bucket[bucket.find("/")+1:]    
           bucket = bucket[:bucket.find("/")]   
           if prefix[len(prefix)-1:] != "/":
              prefix = prefix + "/"

        pyTransferS3 = PyTransferS3(True,self.config,bucket,self.ajustProfile(),self.config.awsRegion,prefix)
        response     = pyTransferS3.listUploads()
        jsonResult   = response["jsonResult"]
  
        header      = ["#","Key", "Initiated Date","Upload Id"]
        prettyTable = PrettyTable(header)
        idx_lin     = 0

        if (response["foundBucket"]):
           if "Uploads" in jsonResult:
              for u in jsonResult["Uploads"]:
                    idx_lin += 1
                    columns = [ str(idx_lin), u["Key"], u["Initiated"].strftime("%Y-%m-%d %H:%M"),u["UploadId"] ]
                    prettyTable.addRow(columns)
                 
              prettyTable.sortByColumn(0)   
              prettyTable.numberSeparator = True
              prettyTable.ascendingOrder(not tableArgs.desc)
              resultTxt = " The S3 Bucket " + Style.GREEN + bucket + ("/" + prefix if prefix else "") + Style.MAGENTA + \
                          Style.RESET + "\n has total of " + Style.GREEN + format(response["total"],",") + \
                          Style.RESET + " multipart uploads not finished" + Style.RESET
              result = resultTxt + "\n\n" + prettyTable.printMe("listUploads",self.config.tableLineSeparator, tableArgs)                                     
           else:
              result = "\033[32mNo Uploads found for \033[35m{}\033[0m".format(bucket)
        else:
           result = response["result"]
          
        return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_UPLOADS_S3]["name"], result, self.config, Utils.dictToJson(jsonResult), False, tableArgs)

    def abortUploads(self):
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        args = tableArgs.cleanPipelineArguments()
        if "," in args:
           bucket  = args.split(",")[0]
        else:
           bucket  = args

        prefix = None
        if "/" in bucket:
           prefix = bucket[bucket.find("/")+1:]    
           bucket = bucket[:bucket.find("/")]   
           if prefix[len(prefix)-1:] != "/":
              prefix = prefix + "/"

        pyTransferS3 = PyTransferS3(True,self.config,bucket,self.ajustProfile(),self.config.awsRegion,prefix)
        response     = pyTransferS3.abortUploads()

        header       = ["#","Upload Id", "Key"]
        prettyTable  = PrettyTable(header)
        idx_lin      = 0
        if not response["found"]:
           result = "Bucket \033[32m{}\033[0m was not found!".format(response["bucket"])   
        elif not response["nothing"]:
           for u in response["uploadsAborted"]:
              idx_lin += 1
              columns = [ str(idx_lin), u["uploadId"], u["key"] ]
              prettyTable.addRow(columns)
   
           prettyTable.sortByColumn(0)   
           prettyTable.numberSeparator = True
           prettyTable.ascendingOrder(not tableArgs.desc)
           resultTxt = " The S3 Bucket " + Style.GREEN + bucket + ("/" + prefix if prefix else "") + Style.MAGENTA + \
                       Style.RESET + "\n had total of " + Style.GREEN + format(response["total"],",") + \
                       Style.RESET + " multipart uploads not finished, now \033[31maborted!\033[0m" + Style.RESET
           result = resultTxt + "\n\n" + prettyTable.printMe("abortUploads",self.config.tableLineSeparator, tableArgs)    
        else:
           result = "Nothing to abort at \033[32m{}\033[0m".format(response["bucket"])   
        return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_UPLOADS_S3]["name"], result, self.config, Utils.dictToJson(response), False, tableArgs)

    def transferToS3(self):
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        args = tableArgs.cleanPipelineArguments()
        if "," in args:
           bucket    = args.split(",")[0]
           path      = args.split(",")[1]
           recursive = True if len(args.split(",")) > 2 and args.split(",")[2] == "recursive" else False
        else:
           bucket  = args
           path    = None

        if not bucket:
           msg = "\n" + \
                 Style.IRED + Emoticons.error() + Style.GREEN + " Ops! First, you need to tell the bucket to copy to...\n" + \
                 " Ex: " + Style.BLUE + "\n      transferToS3 \033[95mupload-temp-logs\033[34m,C:\MyFiles\Logs-2015-08-28.tar.gz" + \
                 Style.RESET + "\n"
           return msg
        if not path:   
           msg = "\n" + \
                 Style.IRED + Emoticons.error() + Style.GREEN + " Ops! You also need to tell the File/Folder to copy to \033[95m{}\033[0m\n".format(bucket) + \
                 " Ex: " + Style.BLUE + "\n      transferToS3 {},\033[95mC:\MyFiles\Logs-2015-08-28.tar.gz\033[0m".format(bucket) + \
                 Style.RESET + "\n"
           return msg

        prefix = None
        if "/" in bucket:
           prefix = bucket[bucket.find("/")+1:]    
           bucket = bucket[:bucket.find("/")]   
           if prefix[len(prefix)-1:] != "/":
              prefix = prefix + "/"

        pyTransferS3        = PyTransferS3(True,self.config,bucket,self.ajustProfile(),self.config.awsRegion,prefix)
        pyTransferS3.target = path
        pyTransferS3.transfer(recursive)
        return ""

    def showTargetsS3(self):
        pyTransferS3 = PyTransferS3(True,self.config,"",self.ajustProfile(),self.config.awsRegion,None)
        pyTransferS3.showTargets()
    def showTargetUploadsS3(self):
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 
        args = tableArgs.cleanPipelineArguments()

        if args == "":
           msg = "\n" + \
                 Style.IRED + Emoticons.error() + Style.GREEN + " Missing target parameter..." + \
                 Style.RESET + "\n"
           print(msg)            
           return msg

        if "," in args:
           target    = args.split(",")[0]
           showAll   = True if args.split(",")[1].lower() == "showAll".lower() else False
        else:
           target  = args
           showAll = False

        pyTransferS3 = PyTransferS3(True,self.config,"",self.ajustProfile(),self.config.awsRegion,None)
        pyTransferS3.target = target
        pyTransferS3.initDb()
        pyTransferS3.showTargetUploads(showAll)

    def showTargetUploadPartsS3(self):
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 
        args = tableArgs.cleanPipelineArguments()

        if "," in args:
           target    = args.split(",")[0]
           key       = args.split(",")[1] 
        else:
           msg = "\n" + \
                 Style.IRED + Emoticons.error() + Style.GREEN + " Missing the key to show its uploded parts..." + \
                 Style.RESET + "\n"
           print(msg)            
           return msg

        pyTransferS3 = PyTransferS3(True,self.config,"",self.ajustProfile(),self.config.awsRegion,None)
        pyTransferS3.target = target
        pyTransferS3.initDb()
        pyTransferS3.showTargetUploadsParts(key)

    def removeTargetS3(self):
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 
        args = tableArgs.cleanPipelineArguments()

        if args == "":
           msg = "\n" + \
                 Style.IRED + Emoticons.error() + Style.GREEN + " Missing target parameter..." + \
                 Style.RESET + "\n"
           print(msg)      
           return msg
        target = args

        pyTransferS3 = PyTransferS3(True,self.config,"",self.ajustProfile(),self.config.awsRegion,None)
        pyTransferS3.target = target
        pyTransferS3.initDb()
        pyTransferS3.removeTargetHistory()

    def botoSession(self):
        return self.config.botoSession()

if __name__ == '__main__':
    config = Config()
    config.awsProfile   = "default"
    config.awsRegion    = "eu-west-3"
    #config.awsProfile   = "ecomm"
    #config.awsRegion    = "eu-central-1"
    config.printResults = True
    #config.awsTags["Environment"] = "production"
    config.tableLineSeparator = False
    
    # subnets, is-public (only with subnets active)
    # sort1,desc (when requested together with subnets, the group lines will be omitted)
    if len(sys.argv) > 1:
       config.commandArguments = sys.argv[1]
    #else:
    #   config.commandArguments = "emagin-delivery,prefix=general/oracle/"
    pyS3CP = PyS3CP(config)
    report = pyS3CP.preSignURL("pyawscp","PythonAWSCP_SimpleFunction_listVPC.mp4")
    if report: 
       Utils.addToClipboard(report)
       print(report)
