import boto3
import os
import re
import sys
import datetime
from datetime import timedelta
from os.path import expanduser
from pyawscp.Utils import Utils, Style
from pyawscp.CookieTempCredentials import CookieTempCredentials
import configparser

class Config:
 
    TMP_CREDENTIALS_FILE = expanduser("~") + "/.pyawscp/tmp.bin"

    def __init__(self):
        self.awsProfile               = ""
        self.awsRegion                = ""
        self.awsTags                  = {}
        self.command                  = ""
        self.commandArguments         = ""
        self.tableLineSeparator       = True
        self.interactive              = False
        self.printResults             = False
        self.uploadChunkSizeMultipart = 10
        self.uploadThresholdMultipart = 100
        self.assumeRole               = None
        self.mfaSerial                = None
        self.mfaPassCode              = None

    def awsTagsToFilter(self):
        if self.awsTags and len(self.awsTags) > 0:
            return True
        return False

    # AssumeRole
    def assumeRoleSession(self, roleArn, mfaToken):
        tempCredentials = boto3.client('sts').assume_role(
            RoleArn=roleArn,
            RoleSessionName="mysession",
            DurationSeconds=3600,
            SerialNumber=self.mfaSerial,
            TokenCode=mfaToken
        )
        return tempCredentials


    def evalCmdToDate(self, cmdDate):
        txt = str(cmdDate)

        ## Method 1
        # nums = re.search('\d{4}.*,',txt).group(0).split(",")
        # print(nums)
        # year  = int(nums[0])
        # month = int(nums[1])
        # day   = int(nums[2])
        # hour  = int(nums[3])
        # minu  = int(nums[4])
        # seco  = int(nums[5])
        # expiration = datetime.datetime(year, month, day, hour, minu, seco)

        # Method 2
        dt = eval(re.sub(",\s{1,}tzinfo=tzutc\(\)","",txt), {'datetime': datetime}, dict())
        return dt
        # Add the duration (1h)
        return dt + timedelta(hours=1)

    def dateToString(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def stringToDate(self, strDate):
        return datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")

    def cookieTempCredentials(self):
        return self.loadCookieTempCredentials()

    def isValidCookieTempCredentials(self):
        cookie = self.loadCookieTempCredentials()
        if cookie and not cookie.isExpired():
           return True
        return False

    def saveCookieTempCredentials(self, tempCredentials):
        file = configparser.ConfigParser(allow_no_value=True) 
        file.add_section("COOKIE")
        file.set("COOKIE","access-key",        tempCredentials['Credentials']['AccessKeyId'])
        file.set("COOKIE","secret-access-key", tempCredentials['Credentials']['SecretAccessKey'])
        file.set("COOKIE","session-token",     tempCredentials['Credentials']['SessionToken'])

        expirationDate = tempCredentials['Credentials']['Expiration']
        # Add the duration (1h)
        expirationDate = expirationDate + timedelta(hours=1)
        file.set("COOKIE","expiration", self.dateToString(expirationDate))

        with open(self.TMP_CREDENTIALS_FILE,'w') as configfile:
             file.write(configfile)

    def loadCookieTempCredentials(self):
        if os.path.exists(self.TMP_CREDENTIALS_FILE):
           file = configparser.ConfigParser()
           file.read(self.TMP_CREDENTIALS_FILE) 
           cookie = CookieTempCredentials()
           cookie.accessKey       = file["COOKIE"]["access-key"]
           cookie.secretAccessKey = file["COOKIE"]["secret-access-key"]
           cookie.sessionToken    = file["COOKIE"]["session-token"]  
           cookie.expirationDate  = self.stringToDate(file["COOKIE"]["expiration"])
           return cookie
        return None

    def credentialsExpired(self, expirationDate):
        return expirationDate < datetime.datetime.now()

    def createCookieRoleSession(self):
        if not self.mfaSerial:
           output = "\n\n\n"
           output += Style.RED  + "=".ljust(108,"=") +"\n"
           output += Style.BLUE + " The Assume Role " + Style.RESET + "\"" + Style.GREEN + self.assumeRole + Style.RESET + "\"" + Style.BLUE + " is configured for the environment" + Style.RESET + "\n" 
           output += Style.BLUE + " A MFA Serial is needed in order to establish a valida session, command:  " + Style.GREEN+ " set mfa-serial {arn:aws:iam::...}" + Style.RESET + "\n" 
           output += Style.RED  + "=".ljust(108,"=") +"\n\n"
           print(output)
           sys.exit()
        
        if not self.mfaPassCode:
           output = "\n\n\n"
           output += Style.RED  + "=".ljust(97,"=") +"\n"
           output += Style.BLUE + " The Assume Role " + Style.RESET + "\"" + Style.GREEN + self.assumeRole + Style.RESET + "\"" + Style.BLUE + " is configured for the environment" + Style.RESET + "\n" 
           output += Style.BLUE + " Please, set a valid MFA PassCode to this Session using the command:  " + Style.GREEN+ " set mfa {passcode}" + Style.RESET + "\n" 
           output += Style.RED  + "=".ljust(97,"=") +"\n\n"
           print(output)
           sys.exit()

        tempCredentials = self.assumeRoleSession(self.assumeRole, self.mfaPassCode) 
        self.saveCookieTempCredentials(tempCredentials)

        cookie = CookieTempCredentials()
        cookie.accessKey       = tempCredentials['Credentials']['AccessKeyId']
        cookie.secretAccessKey = tempCredentials['Credentials']['SecretAccessKey']
        cookie.sessionToken    = tempCredentials['Credentials']['SessionToken']
        cookie.expirationDate  = self.dateToString(tempCredentials['Credentials']['Expiration'])
        return cookie

    def deleteCookieTemporaryCredentials(self):
        if os.path.exists(self.TMP_CREDENTIALS_FILE):
           os.remove(self.TMP_CREDENTIALS_FILE)
        
        
    def botoSession(self):
        if self.assumeRole:
           isNewCookie = False
           cookie      = self.loadCookieTempCredentials()
           if not cookie or cookie.isExpired():
              cookie      = self.createCookieRoleSession()
              isNewCookie = True

           newSession = None 
           if not self.awsRegion:
              newSession = boto3.session.Session(
                  aws_access_key_id=cookie.accessKey,
                  aws_secret_access_key=cookie.secretAccessKey,
                  aws_session_token=cookie.sessionToken
              )
           else:   
              newSession = boto3.session.Session(
                  aws_access_key_id=cookie.accessKey,
                  aws_secret_access_key=cookie.secretAccessKey,
                  aws_session_token=cookie.sessionToken,
                  region_name=self.awsRegion
              )
           return newSession   
        return self.botoSessionCredentialsOwner()

    def startSessionWithTheNewCookie(self):
        self.botoSession().client('ec2').describe_vpcs() # doesnt matter the result, as long as the connection to create the Cookie is established (to not waste the given MFA password)
        cookie = self.loadCookieTempCredentials()
        output = CookieTempCredentials.printCookie(self.isValidCookieTempCredentials(), \
                                                   self.assumeRole, \
                                                   self.mfaPassCode, \
                                                   cookie.timeToExpire())
        return output

    def botoSessionCredentialsOwner(self):
        if not self.awsProfile and not self.awsRegion:
           session = boto3.Session()
        elif not self.awsProfile and     self.awsRegion:    
           session = boto3.Session(region_name=self.awsRegion)
        elif     self.awsProfile and not self.awsRegion:   
           session = boto3.Session(profile_name=self.awsProfile)
        else:
           session = boto3.Session(profile_name=self.awsProfile,region_name=self.awsRegion) 
        return session

    def isThereAwsCredentials(self):
        AWS_CREDENTIALS_DIR  = expanduser("~") + "/.aws/"
        AWS_CREDENTIALS_FILE = AWS_CREDENTIALS_DIR + "credentials"
        if not os.path.exists(AWS_CREDENTIALS_DIR) or not os.path.exists(AWS_CREDENTIALS_FILE):
           print("") 
           print("")
           print("\033[31m ---> Ops!\033[33m AWS CREDENTIALS NOT FOUND!")
           print("") 
           print("") 
           print("\033[34m ---> \033[33mPlease, configure your AWS Credentials:")
           print("\033[34m      \033[33m1. Create the folder \033[35m{}\033[0m".format(AWS_CREDENTIALS_DIR))
           print("\033[34m      \033[33m2. Create the file \033[35m{}credentials\033[33m with the  content:".format(AWS_CREDENTIALS_DIR))
           print("\033[34m      \033[94m   [default]")
           print("\033[34m      \033[94m   aws_access_key_id = YOUR_ACCESS_KEY")
           print("\033[34m      \033[94m   aws_secret_access_key = YOUR_SECRET_KEY")
           print("\033[34m      \033[33m3. Optionally, create the file \033[35m{}config\033[33m with your default region:".format(AWS_CREDENTIALS_DIR))
           print("\033[34m      \033[94m   [default]")
           print("\033[34m      \033[94m   region=us-east-1")
           print("\033[0m")
           print("")
           return False
        return True


    

