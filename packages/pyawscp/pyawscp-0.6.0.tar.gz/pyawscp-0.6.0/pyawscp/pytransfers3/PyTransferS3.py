import os, time
import logging
import sys, threading
import boto3
import configparser
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from datetime import datetime
from os.path import expanduser
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import base64
from enum import Enum

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from pyawscp.PrettyTable import PrettyTable
from pyawscp.TableArgs import TableArgs

FILE_INI               = expanduser("~") + "/.pytransfers3/" + "pytransfers3.ini"
FILE_DB                = expanduser("~") + "/.pytransfers3/" + "#_pytransfers3.json"
SEPARATOR_FILES_UPLOAD = 112

# Check if the object exists
# aws s3api head-object --bucket www.codeengine.com --key index.html
#
# Dependencies
# pip install botocore
# pip install boto3
# pip install tinydb   or   grab it here "https://github.com/msiemens/tinydb/" and pip install .
#

class Style:
    UNDERLINE = '\033[4m'
    RESET     = '\033[0m'

    # Regular Colors
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    MAGENTA   = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'

    # Bold
    BBLACK    ="\033[30m"
    BRED      ="\033[31m"
    BGREEN    ="\033[32m"
    BYELLOW   ="\033[33m"
    BBLUE     ="\033[34m"
    BMAGENTA  ="\033[35m"
    BCYAN     ="\033[36m"
    BWHITE    ="\033[37m"

    # Background Colors
    BG_BLACK  = '\033[40m'
    BG_RED    = '\033[41m'
    BG_GREEN  = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE   = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN   = '\033[46m'
    BG_WHITE  = '\033[47m'

    # High Intensty
    IBLACK    ="\033[90m"
    IRED      ="\033[91m"
    IGREEN    ="\033[92m"
    IYELLOW   ="\033[93m"
    IBLUE     ="\033[94m"
    IMAGENTA  ="\033[95m"
    ICYAN     ="\033[96m"
    IWWHITE   ="\033[97m"

    # Bold High Intensty
    BIBLACK   ="\033[90m"
    BIRED     ="\033[91m"
    BIGREEN   ="\033[92m"
    BIYELLOW  ="\033[93m"
    BIBLUE    ="\033[94m"
    BIPURPLE  ="\033[95m"
    BICYAN    ="\033[96m"
    BIWHITE   ="\033[97m"

    # High Intensty backgrounds
    On_IBLACK ="\033[100m"
    On_IRED   ="\033[101m"
    On_IGREEN ="\033[102m"
    On_IYELLOW="\033[103m"
    On_IBLUE  ="\033[104m"
    On_IPURPLE="\033[;95m"
    On_ICYAN  ="\033[106m"
    On_IWHITE ="\033[107m"
    

class Emoticons:
    _PROMPT      = ['⛅','⛅']
    _WAITING     = ['💤💤💤','☕☕☕']
    _SEE_YA      = ['👋','✌']
    _ERROR       = ['❌💣','❌☠']
    _TOOL        = ['🔧','⚒']
    _THUMBS_UP   = ['👍','✔']
    _POINT_RIGHT = ['👉','❖']
    _WINK        = ['😉','☻']
    _OPS         = ['😕','☹']
    _PIN         = ['📌','✎']
    _ENV         = ['📝','✍']
    _TIME        = ['🕘','☕']
    _WAIT_DISTR  = ['🍺','♨']
    _WAIT_DISTR2 = ['🍼','⚾']
    _MAGNIFIER   = ['🔍','☌']
    _BLOCKS      = ['📦','❒']
    _REDMARK     = ['🔴','⚫']
    _UPLOAD      = ['📤','✈']
    _UPLOAD_PART = ['🔹','➩']
    _FOLDER      = ['🔹','➩']
    _OK          = ['✅','✅']
    _IMGS        = [
                     ['🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛','🕐','🕑'],
                     ['☰','☱','☲','☴','☵','☶','☷','☶','☴']
                   ]  
    @staticmethod
    def isWindows():
        return 1 if os.name == "nt" else 0
    
    @staticmethod
    def prompt():
        return Emoticons._PROMPT[Emoticons.isWindows()]
    @staticmethod
    def waiting():
        return Emoticons._WAITING[Emoticons.isWindows()]    
    @staticmethod
    def seeYa():
        return Emoticons._SEE_YA[Emoticons.isWindows()]
    @staticmethod
    def error():
        return Emoticons._ERROR[Emoticons.isWindows()]
    @staticmethod
    def tool():
        return Emoticons._TOOL[Emoticons.isWindows()]
    @staticmethod
    def thumbsUp():
        return Emoticons._THUMBS_UP[Emoticons.isWindows()] 
    @staticmethod
    def pointRight():
        return Emoticons._POINT_RIGHT[Emoticons.isWindows()]
    @staticmethod
    def wink():
        return Emoticons._WINK[Emoticons.isWindows()]
    @staticmethod
    def pin():
        return Emoticons._PIN[Emoticons.isWindows()]
    @staticmethod
    def env():
        return Emoticons._ENV[Emoticons.isWindows()]
    @staticmethod
    def time():
        return Emoticons._TIME[Emoticons.isWindows()]
    @staticmethod
    def waitDistract():
        return Emoticons._WAIT_DISTR[Emoticons.isWindows()]
    @staticmethod
    def waitDistract2():
        return Emoticons._WAIT_DISTR2[Emoticons.isWindows()]
    @staticmethod
    def ops():
        return Emoticons._OPS[Emoticons.isWindows()]
    @staticmethod
    def magnifier():
        return Emoticons._MAGNIFIER[Emoticons.isWindows()]
    @staticmethod
    def blocks():
        return Emoticons._BLOCKS[Emoticons.isWindows()]
    @staticmethod
    def redMark():
        return Emoticons._REDMARK[Emoticons.isWindows()]
    @staticmethod
    def upload():
        return Emoticons._UPLOAD[Emoticons.isWindows()]
    @staticmethod
    def uploadPart():
        return Emoticons._UPLOAD_PART[Emoticons.isWindows()]
    @staticmethod
    def folder():
        return Emoticons._FOLDER[Emoticons.isWindows()]                    
    @staticmethod
    def ok():
        return Emoticons._OK[Emoticons.isWindows()] 
    @staticmethod
    def imgs():
        return Emoticons._IMGS[Emoticons.isWindows()]                            

UploadState = Enum('UploadState', 'STARTED FINISHED')

class UtilTransferS3:
    @staticmethod
    def formatBytesView(bytes,rightAlign=True):
        result = "Ops..."
        if bytes >= 1000000000:
           bytesInMega = round(((bytes / 1024) / 1024) / 1024,2)
           result = format(bytesInMega,",") + "GB"
        elif bytes >= 1000000:
           bytesInMega = round((bytes / 1024) / 1024,2)
           result = format(bytesInMega,",") + "MB"
        elif bytes >= 1024:
           bytesInKbyte = round((bytes / 1024),2)
           result = format(bytesInKbyte,",") + "KB" 
        else:   
           result = format(bytes,",") + "b"  
        if rightAlign:   
           diff = 9 - len(result)   
           return  " ".ljust(diff if diff > 0 else 0," ") + result 
        return result   

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size     = float(os.path.getsize(filename))
        self._progress = 0
        self._lock     = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:    
            self._progress += bytes_amount
            percentage = (self._progress / self._size) * 100

            msg = " ".ljust(42," ") +\
                  Style.IYELLOW + UtilTransferS3.formatBytesView(self._progress) + Style.GREEN + " of " + UtilTransferS3.formatBytesView(self._size) +\
                  "     (" + Style.IYELLOW + "{0:.2f}%".format(percentage) + Style.GREEN + ")"

            sys.stdout.write("\r     " + msg)
            sys.stdout.flush()

MULTIPART_UPLOAD      = "MULTIPART-UPLOAD"

class PyTransferS3:

    def __init__(self, useConfigAwsCockpit, configAwsCockPit, bucketName, profileName, regionName, prefix=None):
        self.bucketName                 = bucketName
        self.prefix                     = prefix
        self.target                     = ""
        self.multiPartUploadPreferences = None 
        self.database                   = None
        self.s3client                   = None
        self.s3Client                   = boto3.session.Session(profile_name=profileName,region_name=regionName).client("s3")
        self.partSizeBlockMegabytes     = 10
        ################################  Qt                            KB     MB
        self.partSizeBlockBytes         = self.partSizeBlockMegabytes * 1000 * 1000

        # Log init
        USER_DIR = expanduser("~") + "/.pytransfers3/"
        if not os.path.exists(USER_DIR):
           os.makedirs(USER_DIR)
        FILE_LOG = USER_DIR + "log"
        if not os.path.exists(FILE_LOG):
           os.makedirs(FILE_LOG)

        rootLogger = logging.getLogger()
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        fileHandler = logging.FileHandler("{0}/{1}.log".format(FILE_LOG, "py-transfers3"))
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.WARN)
        rootLogger.addHandler(fileHandler)

        # Config init
        if not useConfigAwsCockpit:
           if os.path.exists(FILE_INI):
              config = configparser.ConfigParser(allow_no_value=True)
              config.read(FILE_INI)
              self.multiPartUploadPreferences = config[MULTIPART_UPLOAD]["threshold"]
           else:   
              config = configparser.ConfigParser(allow_no_value=True)
              config.add_section(MULTIPART_UPLOAD)
              config.set(MULTIPART_UPLOAD, "# The size is in Megabytes")
              config.set(MULTIPART_UPLOAD, "threshold","100")
              with open(FILE_INI,'w') as configfile:
                  config.write(configfile)
              config = configparser.ConfigParser(allow_no_value=True)
              config.read(FILE_INI)
              self.multiPartUploadPreferences = config[MULTIPART_UPLOAD]["threshold"]
        else:
            self.partSizeBlockMegabytes     = int(configAwsCockPit.uploadChunkSizeMultipart)
            #####################################################  Qt            KB     MB
            self.partSizeBlockBytes         = int(self.partSizeBlockMegabytes) * 1000 * 1000
            self.multiPartUploadPreferences = configAwsCockPit.uploadThresholdMultipart

    def initDb(self):
        # DB init
        databaseFileName = FILE_DB.replace("#",self.encodeString(self.target))
        self.database = TinyDB(databaseFileName, indent=4)

        # Use this in case a high intesive I/O operations (to cache a little), but with caution!
        # you should use the method below to garantee that the operations are recorded and not lost consistency:   
        #  with self.database as db:  
        #       db.insert(...)
        #self.database = TinyDB(databaseFileName, indent=4, storage=CachingMiddleware(JSONStorage))   

    def encodeString(self, str):
        bytes        = str.encode("utf-8")
        base64_bytes =  base64.b64encode(bytes)
        return base64_bytes.decode("utf-8")
    def decodeString(self, str):
        bytes        = str.encode("utf-8")
        base64_bytes =  base64.b64decode(bytes)
        return base64_bytes.decode("utf-8")

    def transfer(self, recursive):
        if not self._checkBucketExist(self.bucketName):
           msg = "\n" + Style.IRED + Emoticons.error() + Style.GREEN + " The Bucket \033[95m{}\033[32m does not exit...".format(self.bucketName) + "\n"
           print(msg)
           return ""

        if self.target[1:2] == ":":
           # At Windows convert driver letter to Uppercase (it fails in Lowercase)
           self.target = self.target[0:1].upper() + ":" + self.target[2:] 
        elif self.target[0:1] == "~":
           # At Linux, expand the user home alias
           self.target = expanduser("~") + self.target[1:]

        self.initDb()
        isOnlyAFile = self.isFile(self.target)
        print("")

        if isOnlyAFile:
            # Transfer file
            file     = self.target[self.target.rfind("/")+1:]
            filePath = self.target.replace(file,"")
            keyPath  = file
            self.checkUploadFile(keyPath, self.target)
        else:
            if recursive:    
               # Transfer everything inside each folder
                for root, dirs, files in os.walk(self.target):
                    for file in files:
                        filePath = os.path.join(root, file)
                        keyPath  = self.defineKeyPathFromTarget(root,file)
                        self.checkUploadFile(keyPath, filePath)   
            else:
               # Transfer only the files inside the requested folder
                for file in os.listdir(self.target):
                    if self.isFile(self.target + "/" + file):
                        # Transfer file 
                        keyPath  = self.defineKeyPathFromTarget(self.target,file)
                        self.checkUploadFile(keyPath, self.target + "/" + file)

        self.database.close()
        print("")                

    def checkUploadFile(self, keyPath, filePath):
        Upload = Query()
        upload = self.database.get(Upload.key == keyPath)

        if upload and "finish" in upload and upload["finish"] != "":
           self.showMessage(Emoticons.pin() + " File " + Style.BLUE + filePath + Style.GREEN + \
                        " was already transfered to " + Style.BLUE + "s3://" + self.bucketName + "/" + keyPath + Style.GREEN +\
                        " at " + Style.BLUE + upload["finish"] + "\n         \033[33mSize " + "\033[34m~{0:.1f}MB\033[0m".format(upload['file']['length'] / 1024 / 1024))
           msg = " \033[34m--->\033[33m " + Emoticons.pin() + "\033[32m Maybe it was delete from S3 Bucket, and we did not know yet, so... \n         Would like to \033[94mgo ahead\033[33m anyway ? " + \
                 "[\033[94mY\033[33m/\033[94mN\033[33m]: "                
           val = input(msg)       
           if val.upper() == "Y":
              # Clean DB's record of the Upload
              self.database.remove(where('key') == keyPath) 
              upload = self.database.get(Upload.key == keyPath)
              print(" \033[34m--->\033[0m " + Emoticons.pin() + " Ok, let's do it...\n")
              self.transferFile(keyPath,filePath,upload)
        else:
           self.transferFile(keyPath,filePath,upload)

    def removeTargetHistory(self):
        target = self.encodeString(self.target) + "_pytransfers3.json"
        dir    = expanduser("~") + "/.pytransfers3/"
        # Clean DB
        records = self.database.all()
        for r in records:
            self.database.remove(where('key') == r['key']) 
        self.database.close()    
        filePath = dir + target
        os.remove(filePath)
        print("")
        self.showMessage(" Target history for \033[94m{}\033[33m deleted!".format(self.target))
        print("")

    def showTargets(self):
        tableArgs   = TableArgs()
        dir         = expanduser("~") + "/.pytransfers3/"
        header      = ["#","Target"]
        prettyTable = PrettyTable(header)
        idx_lin     = 1

        print("")
        self.showMessage(" Targets you have used for Uploads")
        for root, dirs, files in os.walk(dir):
            files = [ fi for fi in files if fi.endswith(".json") ]
            for file in files:
                target = self.decodeString(file.replace("_pytransfers3","").replace(".json",""))
                columns    = [ str(idx_lin), target ]
                prettyTable.addRow(columns)
                idx_lin = idx_lin + 1

        if not prettyTable.isEmpty():
           prettyTable.sortByColumn(0)   
           prettyTable.numberSeparator = True
           prettyTable.ascendingOrder(True)
           print(prettyTable.printMe("showTargets",False, tableArgs))
           self.showMessage(" You can see more info using \033[95mshowTargetUploads \033[94m[TARGET]\033[0m")
           self.showMessage(" You can delete the target history \033[95mremoveTargetHistory \033[94m[TARGET]\033[0m")
           print("")
        else:
           msg = "\n" + \
                 Style.IYELLOW + Emoticons.pointRight() + Style.GREEN + " No records found..." + \
                 Style.RESET + "\n"
           print(msg)      

    def showTargetUploads(self, showAllData=False):
        tableArgs  = TableArgs()
        records = self.database.all()

        multiPartListed = False
        keySample       = None

        print("")
        self.showMessage(" Upload registry for target \033[94m{}\033[33m".format(self.target))
        if len(records) > 0:
           if showAllData:
              header       = ["#","Key", "Bucket","Start","Finish","State","UploadId","Part Size","Total Parts","File Name","File Length"]
           else:
              header       = ["#","Key", "Bucket","Start","Finish","Parts"]
           prettyTable  = PrettyTable(header)
           idx_lin      = 1
           for r in records:
               multiParts = len(r["parts"])
               if multiParts > 0:
                  keySample = r["key"]
                  multiPartListed = True
               if showAllData:
                  columns    = [ str(idx_lin), r["key"], r["bucket"], r["start"], r["finish"], r["state"], r["uploadId"], 
                                 r["partSize"],multiParts,r["file"]["name"], r["file"]["length"] ]
               else:    
                  if multiParts == 0:
                     multiParts = 1
                  columns    = [ str(idx_lin), r["key"], r["bucket"], r["start"], r["finish"], multiParts ]
   
               prettyTable.addRow(columns)
               idx_lin = idx_lin + 1
   
           if not prettyTable.isEmpty():
              prettyTable.sortByColumn(0)   
              prettyTable.numberSeparator = True
              prettyTable.ascendingOrder(True)
              print(prettyTable.printMe("showTargetUploads",False, tableArgs))
              if multiPartListed:
                 self.showMessage(" You can view parts of a MultiPart Upload using \n       \033[95mshowTargetUploadParts \033[94m{}\033[33m,\033[94m{}\033[0m".format(self.target,keySample))
                 print("")
           else:
              msg = "\n" + \
                    Style.IYELLOW + Emoticons.pointRight() + Style.GREEN + " No records found..." + \
                    Style.RESET + "\n"
              print(msg)      
        else:
           self.showMessage(" No records found!")

    def showTargetUploadsParts(self, key):
        tableArgs  = TableArgs()
        records = self.database.search(where('key') == key)

        print("")
        self.showMessage(" Uploaded Parts registry for target \033[94m{}\033[33m key:\033[94m{}\033[33m".format(self.target,key))
        if len(records) > 0 and len(records[0]["parts"]) > 0:
           self.showMessage(" Total of parts uploaded \033[94m{}\033[33m".format(len(records[0]["parts"]))) 
           header       = ["#","PartNumber", "ETag","Uploaded Bytes"]
           prettyTable  = PrettyTable(header)
           idx_lin      = 1
           for r in records:
               for p in r["parts"]:
                   columns = [ str(idx_lin), p["PartNumber"], p["ETag"], p["UploadedBytes"] ]
                   prettyTable.addRow(columns)
                   idx_lin = idx_lin + 1
   
           if not prettyTable.isEmpty():
              prettyTable.sortByColumn(0)   
              prettyTable.numberSeparator = True
              prettyTable.ascendingOrder(True)
              print(prettyTable.printMe("showTargetUploadsParts",False, tableArgs))
           else:
              msg = "\n" + \
                    Style.IYELLOW + Emoticons.pointRight() + Style.GREEN + " No records found..." + \
                    Style.RESET + "\n"
              print(msg)         
        else:
           self.showMessage(" No parts records found for \033[94m{}\033[0m".format(key))       


    def createUpload(self, keyPath, file, length, uploadId):
        partSize = self.partSizeBlockBytes
        # In case it is not a MultipartUpload, this value will not exist
        if not uploadId:
           uploadId  = ''
           partSize  = 1

        self.database.insert({
            'key': keyPath,
            'bucket':self.bucketName,
            'start': self.dateTimeNow(),
            'finish': '',
            'state': UploadState.STARTED.value,
            'uploadId':uploadId,
            'partSize': partSize,
            'parts':[],
            'file':{
                'name': file,
                'length': length,
            }
        })

    def updateMultiPartUpload(self, keyPath, part):
        Upload = Query()
        upload = self.database.get(Upload.key == keyPath)
        if not upload:
           raise ValueError(Emoticons.error() + ' The already start MultiPartUpload with the KeyPath=' + keyPath + ' was not found! It should be there!!')
        upload['parts'].append(part)
        self.database.update(upload, Upload.key == keyPath)

    def finishUpload(self, keyPath):
        Upload = Query()
        upload = self.database.get(Upload.key == keyPath)
        if not upload:
           raise ValueError(Emoticons.error() + '  The already Upload with the KeyPath=' + keyPath + ' was not found! It should be there!!')
        upload['finish'] = self.dateTimeNow()
        upload['state'] = UploadState.FINISHED.value
        self.database.update(upload, Upload.key == keyPath)

    def cleanNotFinishedUpload(self, keyPath):
        self.database.remove(where('key') == keyPath)    

    def transferFile2(self,keyPath,file):
        print("----")    

    def _checkBucketExist(self,bucketName):
        try:   
            self.s3Client.list_objects_v2(Bucket=bucketName, Delimiter = "/")
            return True
        except ClientError as ex:
            return False

    def showHeaderInfoUplad(self, isMultipart, keyPath, file, upload):
        print("-".ljust(SEPARATOR_FILES_UPLOAD,"-"))
        msg = Emoticons.tool() + " UPLOAD SETUP" + "\n" + \
              "      " + Emoticons.pointRight() + " Chunk Size....................: \033[34m {}MB\033[32m".format(self.partSizeBlockMegabytes) + "\n" + \
              "      " + Emoticons.pointRight() + " Threashold Multipart Uploads..: \033[34m{}MB\033[32m".format(self.multiPartUploadPreferences) + "\n\n" + \
              "      " + "   Hit \033[94mCTRL+C\033[32m to \033[94mcancel/pause\033[32m the download, you can \033[34mresume\033[32m later, executing the same command again"   
        self.showMessage(msg)
        print("-".ljust(SEPARATOR_FILES_UPLOAD,"-"))
        print("      " + Style.GREEN + Emoticons.pointRight() + " Uploading... \033[94m{}\033[33m to \033[94ms3://{}\033[33m".format(file.replace("\/","\\"),self.bucketName) )
        print("")

    def transferFile(self,keyPath,file,upload):
        try:
            if os.path.exists(file):
               totalBytes             = os.stat(file).st_size
               fileSizeAboveThreshold = True if ((totalBytes / 1024) / 1024) >= int(self.multiPartUploadPreferences) else False
   
               # Multipart upload already start, must continue where it stops
               # File size bigger than the threshold, starting a multipart upload
               if (upload and "uploadId" in upload) or fileSizeAboveThreshold:
                   self.showHeaderInfoUplad(True,keyPath,file,upload)
                   self.transferFileUsingMultipartUpload(keyPath, file, totalBytes, upload)
               else:
                   self.showHeaderInfoUplad(False,keyPath,file,upload)
                   self.transferFileAtOnce(keyPath, file, totalBytes)
            else:
               self.showMessage(Emoticons.error() + " Path \033[91m" + file + "\033[32m was not found!") 

        except:
            LOG.error("Unexpected error:" + str(sys.exc_info()[0]))
            self.showMessage(Emoticons.error() + " Unexpected error:\033[91m" + str(sys.exc_info()[0]) + "\033[32m")
            raise

    def calculateQtdeParts(self,totalBytes,partSize):    
        qtdeParts = int(totalBytes / partSize)
        if ((totalBytes / partSize) - int(totalBytes / partSize)) > 0:
            qtdeParts += 1
        return qtdeParts   

    def _messageAndRemoveNotFinishUploadWithUploadId(self,uploadId):
        print("") 
        self.showMessage(Emoticons.error() + " Ops... " + Style.RED + "Error! " + Style.GREEN + "Sorry, MultiPartUpload with id\n      " + Style.BLUE + uploadId + Style.GREEN + \
               " wasn't found!\n      Probably someone has deleted the unfinished Multipart Upload registry from AWS S3, unfortunately you'll have to start it again from the beginning." + \
               "\n      This entry was delete from your database, please relaunch the command and your Upload will start.")
        self.database.remove(where('uploadId') == uploadId)
        print("")

    def transferFileUsingMultipartUpload(self,keyPath,file,totalBytes,upload):        
        totalBytesUploaded   = 0
        totalBytesRemaning   = 0
        partSequenceUploaded = 0
        partSize             = self.partSizeBlockBytes
        qtdeParts            = 0

        resumingUpload = True if upload else False

        if resumingUpload:
           partSize             = upload["partSize"]
           partAlreadyUploaded  = upload["parts"]
           totalBytesUploaded   = 0
           qtdeParts            = self.calculateQtdeParts(totalBytes,partSize)
           partSequenceUploaded = len(partAlreadyUploaded)
           for p in partAlreadyUploaded:
               totalBytesUploaded    += int(p["UploadedBytes"])
           totalBytesRemaning = totalBytes - totalBytesUploaded
           self.message(Emoticons.upload() + " Resuming uploading in " + format(qtdeParts,",") + " blocks " + Emoticons.blocks() + " of " + UtilTransferS3.formatBytesView(partSize,False) + \
                        ", remaining " + Style.BLUE + UtilTransferS3.formatBytesView(totalBytesRemaning,False) + Style.GREEN + " of " +\
                        Style.BLUE + UtilTransferS3.formatBytesView(totalBytes,False) + Style.GREEN + ", file\n      " + Style.IBLUE + file + Style.GREEN)
        else:
           qtdeParts = self.calculateQtdeParts(totalBytes,partSize)    
           self.message(Emoticons.upload() + " Uploading in " + format(qtdeParts,",") + " blocks " + Emoticons.blocks() + " of " + UtilTransferS3.formatBytesView(partSize,False) + \
                        " a total of " + Style.BLUE + UtilTransferS3.formatBytesView(totalBytes,False) + Style.GREEN + ", file \n" \
                        + Style.IBLUE + "      " + file + Style.RESET)

        doItUpload  = False
        mpu         = None
        mpu_id      = None
        ## create upload registry
        if not resumingUpload:
           # Create MPU
           mpu    = self.s3Client.create_multipart_upload(Bucket=self.bucketName, Key=keyPath)
           mpu_id = mpu["UploadId"]
           
           self.createUpload(keyPath, file, totalBytes, mpu_id)

           doItUpload = True
        else:
           #mpu_id = upload["uploadId"] 
           #doItUpload = True

           # Here get Upload (check if exists)   
           mpus = self.s3Client.list_multipart_uploads(Bucket=self.bucketName)
           if "Uploads" in mpus:
               for u in mpus["Uploads"]:
                   if u["UploadId"] == upload["uploadId"]:
                      mpu_id = upload["uploadId"]
                      doItUpload = True   
                      break
               if not doItUpload:
                  self._messageAndRemoveNotFinishUploadWithUploadId(upload["uploadId"])
           else:
               self._messageAndRemoveNotFinishUploadWithUploadId(upload["uploadId"])

        if doItUpload:
           # Upload Parts
           parts = []
           if resumingUpload:
              # Add Parts already upload before 
              for part in upload["parts"]:
                  parts.append({"PartNumber": part["PartNumber"], "ETag": part["ETag"]})
           uploadedBytes = totalBytesUploaded
           imgIdx = 0
           imgs   = Emoticons.imgs()
           #imgs   = ['🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛','🕐','🕑']
           with open(file, "rb") as f:
               # Position at the part we still have to upload (in case first time, the value will be zeros)
               f.seek(uploadedBytes) 
               i = partSequenceUploaded + 1

               firstLoop = True
               while True:
                   data = f.read(partSize)
                   if not len(data):
                      break
   
                   sys.stdout.write("\r      " + Emoticons.uploadPart() + " " + Style.GREEN + "Uploading part... " + Style.IYELLOW + format(i,",") + Style.GREEN + " of " \
                                    + Style.IYELLOW + format(qtdeParts,",") + Style.RESET)
                   if firstLoop:
                      #time.sleep(1) 
                      firstLoop = False                  
   
                   part = self.s3Client.upload_part(Body=data,
                                               Bucket=self.bucketName,
                                               Key=keyPath,
                                               UploadId=mpu_id,
                                               PartNumber=i)
   
                   parts.append({"PartNumber": i, "ETag": part["ETag"]})
                   # Update Upload Part
                   self.updateMultiPartUpload(keyPath,{
                       "PartNumber": i, 
                       "ETag": part["ETag"],
                       "UploadedBytes": len(data)
                   })
                   uploadedBytes += len(data)
                   msg = Style.IYELLOW + UtilTransferS3.formatBytesView(uploadedBytes) + Style.GREEN + " of " + Style.GREEN + UtilTransferS3.formatBytesView(totalBytes)
                   msg = msg + Style.GREEN + "     " + \
                         "(" + Style.IYELLOW  + "{0:.2f}%".format(self.asPercent(uploadedBytes, totalBytes)) + Style.GREEN + ")" + Style.RESET
                   sys.stdout.write("\r                                     " + imgs[imgIdx] + "        " + msg)                                              
                   #print(msg)
                   i += 1
                   imgIdx +=1
                   if (imgIdx+1) > len(imgs):
                      imgIdx = 0

               sys.stdout.write("\r      " + Emoticons.ok() + " " + Style.GREEN + "Finished " + Style.RESET) 
               print(Style.RESET + "\n-".ljust(SEPARATOR_FILES_UPLOAD,"-"))      
   
           # Complete MPU
           result = self.s3Client.complete_multipart_upload(Bucket=self.bucketName, Key=keyPath,\
                                                       UploadId=mpu_id,
                                                       MultipartUpload={"Parts": parts})
           self.finishUpload(keyPath)

           return result

    def dateTimeNow(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    def defineKeyPathFromTarget(self,dir,file):
        keyPath = dir.replace(self.target,"") + "/" + file
        return self.keyPathCleanFirstSlash(keyPath)

    # Helper
    def asPercent(self,num, denom):
        return float(num) / float(denom) * 100.0

    def transferFile3(self,keyPath,file):
        print(self.bucketName  + keyPath)

    def keyPathCleanFirstSlash(self, keyPath):
        if keyPath.startswith("/"):
           return keyPath[1:]
        return keyPath   

    def transferFileAtOnce(self,keyPath,file,totalBytes):     
        # Simple Upload
        config = TransferConfig(
                   multipart_threshold=1024 * 25,\
                   max_concurrency=10,\
                   multipart_chunksize=1024 * 25,\
                   use_threads=True)
        try:
            self.createUpload(keyPath, file, totalBytes, None)
            self.message(Emoticons.upload() + " Uploading file \n      " + Style.IBLUE + file + Style.GREEN)
            self.s3Client.upload_file(file, self.bucketName, keyPath,
                               #ExtraArgs={'ACL':'public-read','ContentType': 'text/pdf'},
                               Config=config,
                               Callback=ProgressPercentage(file))   
            self.finishUpload(keyPath)
            print(Emoticons.ok() + " " + Style.GREEN + "Finished " + Style.RESET) 
        except:
            self.cleanNotFinishedUpload(keyPath)
            print(" " + Emoticons.error() + " " + Style.RED + "Error " + Style.RESET + "{0} when uploadinf the file {1}...".format(sys.exc_info()[0],file))
            raise
        print(Style.RESET + "-".ljust(SEPARATOR_FILES_UPLOAD,"-"))      
        print("")

    def abortUploads(self,printMe=True):
        result            = {}
        found             = True
        result["bucket"]  = self.bucketName
        result["found"]   = True
        try:
            mpus   = self.s3Client.list_multipart_uploads(Bucket=self.bucketName)
        except ClientError as ex:
            #reason = ex.response['Error']['Code']
            found = False
            result["found"] = False

        if not found:
            result["found"] = False
            if printMe:
               print("")
               self.message(Emoticons.pin() + " Bucket not found!")        
               print("")
        elif "Uploads" in mpus:
            total = len(mpus["Uploads"])   

            result["nothing"] = False
            result["total"]   = total
            result["uploadsAborted"] = []

            if printMe:
               print("") 
               self.message(Emoticons.pin() + " ABORTING... " + str(total) +  (" UPLOADS:" if total > 1 else " UPLOAD:"))
            id = 0
            for u in mpus["Uploads"]:
                id += 1
                uploadId  = u["UploadId"]
                key       = u["Key"]
                msgResult = self.s3Client.abort_multipart_upload(Bucket=self.bucketName, Key=key, UploadId=uploadId)

                result["uploadsAborted"].append({
                    "id":str(id),
                    "uploadId":u["UploadId"],
                    "key":u["Key"]
                })

                if printMe:
                   self.message("   " + Emoticons.redMark() + " [" + str(id) + "] Aborted " + Style.BLUE + u["UploadId"] + "-" + u["Key"] + Style.GREEN)
            if printMe:       
               print("")        
        else:
            if printMe:
               print("")
               self.message(Emoticons.pin() + " Nothing to abort")        
               print("")
            result["nothing"] = True
        return result    

    def listUploads(self):    
        result = ""
        id     = 0
        mpus   = None
        found  = True
        if self.prefix and self.prefix != "":
           self.bucketName = self.bucketName.replace("/","") 
           self.prefix = "" if self.prefix == "/" else self.prefix
           if self.prefix.startswith("/"):
              self.prefix = self.prefix[1:]
           mpus = self.s3Client.list_multipart_uploads(Bucket=self.bucketName,Delimiter="/",Prefix=self.prefix)   
        else:      
           try: 
               mpus = self.s3Client.list_multipart_uploads(Bucket=self.bucketName)
           except ClientError as ex:
               #reason = ex.response['Error']['Code']
               found = False

        if not found:    
            result += "\n"
            result += self.message(Emoticons.pin() + " The bucket \033[35m{}\033[32m was not found".format(self.bucketName))
            result += "\n"
        elif "Uploads" in mpus:
            result += "\n"
            total = len(mpus["Uploads"])   
            result += self.message(Emoticons.pin() + " LISTING total of " + str(total) +  (" UPLOADS:" if total > 1 else " UPLOAD:"))
            for u in mpus["Uploads"]:
                id += 1
                result += self.message(Emoticons.folder() + " [" + "{:02d}".format(id) + "] " + Style.BLUE + u["Key"] + Style.GREEN + " - " + u["Initiated"].strftime("%Y-%m-%d %H:%M") + " - " + u["UploadId"])
            result += "\n"
        else:
            result += "\n"
            result += self.message(Emoticons.pin() + " There's no Multipart Upload in course")
            result += "\n"

        return {
            "foundBucket": found,
            "jsonResult":mpus,
            "result":result,
            "total": id
        }    

    def isFile(self, p):
        return not os.path.isdir(p)

    def message(self, msg, level=0):
        #print(Style.BLUE + " ---> " + Style.GREEN + msg + Style.RESET)    
        return Style.BLUE + " ---> " + Style.GREEN + msg + Style.RESET + "\n"

    def showMessage(self, msg, level=0):
        print(Style.BLUE + " ---> " + Style.GREEN + msg + Style.RESET)    


# python pytransfers3.py transfer,uploadsujr,/home/osboxes/Developer/tmp-upload/,recursive
# python pytransfers3.py transfer,uploadsujr,/home/osboxes/Developer/tmp-upload/dir1/,recursive
# python pytransfers3.py transfer,uploadsujr,/home/osboxes/Developer/tmp-upload/myfile2.tar
# python pytransfers3.py transfer,uploadsujr,/home/osboxes/Developer/tmp-upload/myfile2.tar
# python pytransfers3.py transfer,uploadsujr,/home/osboxes/Developer/tmp-upload/dir2
# python pytransfers3.py listuploads
# python pytransfers3.py abortuploads

def syntax():
    print("")
    print(Style.GREEN + "--------------------------------------------------------------------------------------------------------------------------")
    print(Style.GREEN + "  Available Commands: " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "[listuploads|abortuploads|transfer|showTargets|showTargetUploads|showTargetUploadsParts|removeTargetHistory]")
    print(Style.GREEN + "  Usages: ")
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "listuploads BUCKET_NAME")     
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "abortuploads BUCKET_NAME")
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "transfer BUCKET_NAME,FILE|FOLDER,[recursive]")     
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "showTargets")
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "showTargetUploads FILE|FOLDER")
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "showTargetUploads FILE|FOLDER,showAll")
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "showTargetUploadsParts FILE|FOLDER,KEY")     
    print(Style.GREEN + "         " + Style.WHITE + "python " + Style.GREEN + "pytransfer.py " + Style.BLUE + "removeTargetHistory TARGET")
    print(Style.GREEN + "--------------------------------------------------------------------------------------------------------------------------")
    print(Style.RESET)

if __name__ == '__main__':
    if "transfer" in sys.argv[1] and len(sys.argv[1].split(",")) <= 2:
       syntax()
       sys.exit()
    
    command = sys.argv[1].split(",")[0].lower()
    bucket  = ""
    
    pyTransferS3 = PyTransferS3(False,None,bucket,"ecomm","eu-central-1",None)
    if "listuploads" in command:
        pyTransferS3.bucketName = sys.argv[1].split(",")[1]
        pyTransferS3.listUploads()
    elif "abortuploads" in command:
        pyTransferS3.bucketName = sys.argv[1].split(",")[1]
        pyTransferS3.abortUploads()    
    elif "transfer" in command:
        pyTransferS3.bucketName = sys.argv[1].split(",")[1]
        path      = sys.argv[1].split(",")[2]
        recursive = True if "recursive" in sys.argv[1] else False
        pyTransferS3.bucketName = bucket
        pyTransferS3.target     = path
        pyTransferS3.transfer(recursive)
    elif "showTargets".lower() == command.lower():
        pyTransferS3.showTargets()
    elif "showTargetUploads".lower() == command.lower():
        if "," in sys.argv[2]:
           target      = sys.argv[2].split(",")[0]
           showAllData = True if sys.argv[2].split(",")[1].lower() == "showAll".lower() else False
        else:
           target      = sys.argv[2]
           showAllData = False
        pyTransferS3.target = target #"D:\\Downloads\\test\\" "d:/Temp/file.zip"
        pyTransferS3.initDb()
        pyTransferS3.showTargetUploads(showAllData)
    elif "showTargetUploadsParts".lower() == command.lower():
        target    = sys.argv[2].split(",")[0]
        key       = sys.argv[2].split(",")[1]
        pyTransferS3.target = target #"D:\\Downloads\\test\\" "d:/Temp/file.zip"
        pyTransferS3.initDb()
        pyTransferS3.showTargetUploadsParts(key)
    elif "removeTargetHistory".lower() == command.lower():
        target    = sys.argv[2].split(",")[0]
        pyTransferS3.target = target #"D:\\Downloads\\test\\" "d:/Temp/file.zip"
        pyTransferS3.initDb()
        pyTransferS3.removeTargetHistory()
    else:
        print("Command " + Style.GREEN  + command + Style.RESET + " not recognized")    
  
