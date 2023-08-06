import logging
import sys, cmd, os, ast, signal
from datetime import datetime
from os.path import expanduser
import configparser
import multiprocessing
from multiprocessing import Process, Pool
import time
import re

# Run temporarily local (python command)
#from pyawscp.utils import utils
from pyawscp.Utils import Utils, Style
from pyawscp.DiagramMgnt import DiagramMgnt
from pyawscp.Functions import Functions
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Config import Config
from pyawscp.Emoticons import Emoticons
from pyawscp.PyEc2Cp import PyEc2CP
from pyawscp.PyEc2NetSecCp import PyEc2NetSecCP
from pyawscp.PyElbCp import PyElbCP
from pyawscp.PyS3Cp import PyS3CP
from pyawscp.PyR53Cp import PyR53CP
from pyawscp.__init__ import __version__
from pyawscp.CookieTempCredentials import CookieTempCredentials
from pyawscp.pymxgraph.PymxGraph import PymxGraph
from pyawscp.pymxgraph.PymxGraphAwsNavigator import PymxGraphAwsNavigator

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

USER_DIR                   = expanduser("~") + "/.pyawscp/"
FILE_INI                   = USER_DIR + "pyawscp.ini"
LABEL_LENGTH_FUNCTION_NAME = 25
SIZE_SEPARATOR             = 95

PREFERENCES  = "PREFERENCES" 
TRANSFER_S3  = "TRANSFER_S3"

signal.signal(signal.SIGINT, signal.SIG_DFL)

class PyAwsShell(cmd.Cmd):
    Utils.clearScreen()
    if not os.path.exists(USER_DIR):
       os.makedirs(USER_DIR)

    preferences   = Config()

    intro =  "\n" + \
             Style.CYAN  + "   Wellcome to " + Style.RESET + "AWS" + Style.CYAN + " C:\> " + Style.RESET + "Shell" + Style.CYAN + " $:~" +  Style.RESET + " Cockpit" + Style.CYAN + " version " + Style.RESET + __version__ + Style.RESET + "\n\n" + \
             Style.YELLOW  + \
             "      ___        ______   " + Style.CYAN + " ____  _          _ _  " + Style.BLUE + "  ____           _          _ _   " + "\n" + Style.YELLOW + \
             "     / \ \      / / ___|  " + Style.CYAN + "/ ___|| |__   ___| | | " + Style.BLUE + " / ___|___   ___| | ___ __ (_) |_ " + "\n" + Style.YELLOW + \
             "    / _ \ \ /\ / /\___ \  " + Style.CYAN + "\___ \| '_ \ / _ \ | | " + Style.BLUE + "| |   / _ \ / __| |/ / '_ \| | __|" + "\n" + Style.YELLOW + \
             "   / ___ \ V  V /  ___) | " + Style.CYAN + " ___) | | | |  __/ | | " + Style.BLUE + "| |__| (_) | (__|   <| |_) | | |_ " + "\n" + Style.YELLOW + \
             "  /_/   \_\_/\_/  |____/  " + Style.CYAN + "|____/|_| |_|\___|_|_| " + Style.BLUE + " \____\___/ \___|_|\_\ .__/|_|\__|" + "\n" + Style.YELLOW + \
             "                          " + Style.CYAN + "                       " + Style.BLUE + "                     |_|          " + "\n\n" + \
             Style.GREEN + "  Enter " + Style.BLUE + "menu" + Style.GREEN + " or " + Style.BLUE + "ls [-l] " + Style.GREEN + "to list all available AWS functions " + Style.RESET + "\n" + \
             Style.GREEN + "  Enter " + Style.BLUE + "help" + Style.GREEN + " or " + Style.BLUE + "?" + Style.GREEN + "       to list of all commands " + Style.GREEN + "\n" + \
             Style.GREEN + "  Enter " + Style.BLUE + "env" + Style.GREEN + "             to view and setup your environment configuration " + Style.RESET + "\n"  + \
             Style.GREEN + "  Use   " + Style.BLUE + "<TAB>" + Style.GREEN + "           to autocomplete or view commands " + Style.RESET + "\n" + \
             Style.GREEN + "  Use   " + Style.BLUE + "{command} <TAB>" + Style.GREEN + " to autocomplete or view arguments " + Style.RESET + "\n" + \
             Style.GREEN + "  Enter " + Style.BLUE + "navigator" + Style.GREEN + "       to try one of the features... " + Style.CYAN + Emoticons.seeYa() + Style.RESET + "\n"

    roleActived = False
    if preferences.isValidCookieTempCredentials():
       roleActived = True
       intro += "\n"
       intro += Style.GREEN + "  " + Emoticons.cookie() + Emoticons.cookie() + Emoticons.cookie() + " " + Emoticons.pointRight() + \
                " AWS Temporary "+Style.IBLUE+"Session"+Style.GREEN+" Credentials is still "+Style.IBLUE+"valid"+Style.GREEN+" and activated!"
       intro += "\n"
       intro += Style.GREEN + "            Expires at: " + Style.IBLUE + preferences.cookieTempCredentials().humanReadFormatExpirationDate() + " (Remaining: " + str(preferences.cookieTempCredentials().timeToExpire()) + ")"
       intro += "\n"
             
    prompt = '(\033[33maws\033[0m-\033[36mshell\033[0m-\033[34mcockpit\033[0m)\033[33m' + Emoticons.prompt() \
                                                                                        + (Emoticons.cookie() if roleActived else "") \
                                                                                        + '\033[0m:\033[33m~\033[0m '
    ruler      = '-'
    #undoc_header = 'undoc_header'
    doc_header = 'Commands (type help <command>):'
    last_output = ""

    
    configFileIni = None
    if not os.path.exists(FILE_INI):
        # Create the Default INI File
       configFileIni = configparser.ConfigParser(allow_no_value=True)
       configFileIni.add_section(PREFERENCES)
       configFileIni.set(PREFERENCES, "aws-profile","default")
       configFileIni.set(PREFERENCES, "aws-region","eu-central-1")
       configFileIni.set(PREFERENCES, "aws-tags",{})
       configFileIni.set(PREFERENCES, "print-results","false")
       configFileIni.set(PREFERENCES, "table-line-separator","false")

       configFileIni.set(PREFERENCES, "assume-role","")
       configFileIni.set(PREFERENCES, "mfa-serial","")

       configFileIni.add_section(TRANSFER_S3)
       configFileIni.set(TRANSFER_S3, "# The size is in Megabytes")
       configFileIni.set(TRANSFER_S3, "chunkSize","10")
       configFileIni.set(TRANSFER_S3, "threshold","100")

       with open(FILE_INI,'w') as configfile:
           configFileIni.write(configfile)
       configFileIni = configparser.ConfigParser(allow_no_value=True)

    configFileIni = configparser.ConfigParser()
    configFileIni.read(FILE_INI)
    preferences.awsProfile               = configFileIni[PREFERENCES]["aws-profile"]
    preferences.awsRegion                = configFileIni[PREFERENCES]["aws-region"]
    preferences.awsTags                  = ast.literal_eval(configFileIni[PREFERENCES]["aws-tags"])
    preferences.printResults             = configFileIni[PREFERENCES]["print-results"] in ['True','true']
    preferences.tableLineSeparator       = configFileIni[PREFERENCES]["table-line-separator"] in ['True','true']
    preferences.uploadChunkSizeMultipart = configFileIni[TRANSFER_S3]["chunkSize"]
    preferences.uploadThresholdMultipart = configFileIni[TRANSFER_S3]["threshold"]

    if "assume-role" in configFileIni[PREFERENCES]:
       preferences.assumeRole           = configFileIni[PREFERENCES]["assume-role"]
    else:
       preferences.assumeRole           = ""
    if "mfa-serial" in configFileIni[PREFERENCES]:
       preferences.mfaSerial           = configFileIni[PREFERENCES]["mfa-serial"]
    else:
       preferences.mfaSerial           = ""
    
    def do_bye(self, arg):
        "Exit shell\n\n"
        self.close()

    def do_version(self, arg):
        "Version\n"
        print(__version__)

    def do_exit(self, arg) :
        "Exit shell\n\n"
        self.close()

    def do_e(self, arg) :
        "[SHORTCUT for \"exit\"]\nQuit shell\n\n"
        self.close()        

    def do_q(self, arg) :
        "[SHORTCUT for \"quit\"]\nQuit shell\n\n"
        self.close()    

    def do_quit(self, arg) :
        "Quit shell\n\n"
        self.close()        

    def do_clear(self,arg):
        "Clear screen\n\n"
        Utils.clearScreen()

    def emptyline(self):
        return cmd.Cmd.emptyline(self)

    def onewayFunction(self, line):
        if not line or len(line.split(",")) < 2:
           return self.default(line)
        programName  = line.split(",")[0]
        functionName = line.split(",")[1]
        args         = line.replace(functionName + ",","").replace(programName + ",","")
        func         = None
        try:
            func = getattr(self, 'do_' + functionName)
            return func(args)    
        except AttributeError:
            return self.default(line.split(",")[1])

    def do_shell(self, line):
        "Run a shell command"
        print ("running shell command:", line)
        output = os.popen(line).read()
        print (output)
        self.last_output = output
    
    def do_echo(self, line):
        "Print the input, replacing '$out' with the output of the last shell command"
        # Obviously not robust
        print (self.last_output)

    def default(self, line):
        LABEL_LENGTH_FUNCTION_NAME = 17
        SIZE_SEPARATOR             = 60
        output  = "-".ljust(SIZE_SEPARATOR,"-") + "\n"           
        output += "   " + Emoticons.tool() + "   " + Style.CYAN + "A W S    C O C K P I T" + Style.RESET + "" + "\n"
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"
        output += Style.RESET + "  Function  " + Style.GREEN + line + Style.RESET + \
                  "  do not exist " + Style.CYAN  + "\n  Use the argument \"-h\" or the command \n  \"ls -l\" to see all available options" + Style.RESET + "\n\n"
        self.stdout.write(output)

    def close(self):
        self.savePreferences()
        print(" ")
        print(" See ya! " + Emoticons.seeYa())
        print(" ")
        sys.exit()

    def savePreferences(self):
        if os.path.exists(FILE_INI):
           os.remove(FILE_INI)  

        configFileIni = configparser.ConfigParser()
        configFileIni[PREFERENCES] = {}
        configFileIni[PREFERENCES]["aws-profile"] = self.preferences.awsProfile
        configFileIni[PREFERENCES]["aws-region"] = self.preferences.awsRegion
        configFileIni[PREFERENCES]["assume-role"] = self.preferences.assumeRole
        configFileIni[PREFERENCES]["mfa-serial"] = self.preferences.mfaSerial
        configFileIni[PREFERENCES]["aws-tags"] = str(self.preferences.awsTags)
        configFileIni[PREFERENCES]["print-results"] = str(self.preferences.printResults)
        configFileIni[PREFERENCES]["table-line-separator"] = str(self.preferences.tableLineSeparator)

        configFileIni[TRANSFER_S3] = {}
        configFileIni[TRANSFER_S3]["chunksize"] = self.preferences.uploadChunkSizeMultipart
        configFileIni[TRANSFER_S3]["threshold"] = self.preferences.uploadThresholdMultipart

        with open(FILE_INI, "w") as file:
            configFileIni.write(file)
    
    def complete_ad(self,text,line,begidx,endidx):
        return [i for i in ('tags') if i.startswith(text)]
    def do_add(self,arg):
        "Modify environment variables/preferences adding values(type env to see all the available options)\n\n"
        if "tags" in arg:
            tags=arg.replace("tags","")
            if tags:
                for tag in tags.split(","):
                    key = tag.split("=")[0].replace(" ","")
                    vlr = tag.split("=")[1]
                    self.preferences.awsTags[key] = vlr
        else:
            print(" " + Emoticons.error() + " The environment variable/preference " + Style.GREEN + arg.split(" ")[0] + Style.RESET + " is not a collection, use set to chenge its value " + Style.RESET + "\n")

    
    def complete_set(self,text,line,begidx,endidx):
        return [i for i in ('tags','profile','region,''verbose','tables-line','chunk-size','threshold') if i.startswith(text)]

    def do_unset(self,arg):
        "Remove environment variables/preferences (type env to see all the available options)\n\n"
        if "tags" in arg:
            self.preferences.awsTags = {}
            print(" " + Emoticons.thumbsUp() + " Tags unset " + Style.RESET + "\n")
        elif "profile" in arg:
            self.preferences.awsProfile=""
            print(" " + Emoticons.thumbsUp() + " Profile unset " + Style.RESET + "\n")
        elif "region" in arg:
            self.preferences.awsRegion=""
            print(" " + Emoticons.thumbsUp() + " Region unset " + Style.RESET + "\n")
        elif "assume-role" in arg:
            self.preferences.assumeRole=""
            print(" " + Emoticons.thumbsUp() + " Assume Role unset " + Style.RESET + "\n")         
        elif "mfa-serial" in arg:
            self.preferences.mfaSerial=""
            print(" " + Emoticons.thumbsUp() + " MFA Serial unset " + Style.RESET + "\n")         
        else:
            print(" " + Emoticons.error() + " Ops... No unset option to the preference "+ arg + Style.RESET + "\n")
            return None
    def complete_unset(self,text,line,begidx,endidx):
        return [i for i in ('tags','profile','region','assume-role','mfa-serial') if i.startswith(text)]

    def do_set(self,arg):
        "Modify environment variables/preferences (type env to see all the available options)\n\n"
        if "tags" in arg:
            tags=arg.replace("tags","")
            if tags:
                self.preferences.awsTags = {}
                for tag in tags.split(","):
                    key = tag.split("=")[0].replace(" ","")
                    vlr = tag.split("=")[1]
                    self.preferences.awsTags[key] = vlr
            else:
               self.preferences.awsTags = {}
        elif len(arg.split(" ")) < 2:
            print(" " + Emoticons.error() + " Ops... Bad command! The syntax is: " + Style.GREEN + "set {VARIABLE} {NEW-VALUE}" + Style.RESET + "\n")
            return None
        elif "profile" in arg:
            value=arg.split(" ")[1]
            self.preferences.awsProfile=value
            print(" " + Emoticons.thumbsUp() + " Profile AWS susccessfully modified to " + Style.GREEN + value + Style.RESET + "\n")
        elif "region" in arg:
            value=arg.split(" ")[1]
            self.preferences.awsRegion=value
            print(" " + Emoticons.thumbsUp() + " Region AWS susccessfully modified to " + Style.GREEN + value + Style.RESET + "\n")
        elif "assume-role" in arg:
            value=arg.split(" ")[1]
            self.preferences.assumeRole=value
            print(" " + Emoticons.thumbsUp() + " Assume Role susccessfully configured to " + Style.GREEN + value + Style.RESET + "\n")         
            print("    Please, "+ Style.IRED + "DON'T FORGET!"+ Style.RESET + " Set your "+ Style.GREEN + "MFA Serial"+ Style.RESET + " and the "+ Style.GREEN + "MFA PassCode"+ Style.RESET + ", see:")     
            print("    " + Style.GREEN + "set mfa-serial {arn:aws:iam::...}" )     
            print("    " + Style.GREEN + "set mfa {passcode}\n" )     
        elif "mfa-serial" in arg:
            value=arg.split(" ")[1]
            self.preferences.mfaSerial=value
            print(" " + Emoticons.thumbsUp() + " MFA Serial susccessfully configured to " + Style.GREEN + value + Style.RESET + "\n")         
            print("    Please, "+ Style.IRED + "DON'T FORGET"+ Style.RESET + " to set your "+ Style.GREEN + "MFA PassCode"+ Style.RESET + " for the session, see:")     
            print("    " + Style.GREEN + "set mfa {passcode}\n" )
        elif "mfa" in arg:
            value=arg.split(" ")[1]
            self.preferences.mfaPassCode=value
            print(" " + Emoticons.thumbsUp() + " MFA Passcode susccessfully configured to " + Style.GREEN + value + Style.RESET + "\n")
            if not self.preferences.mfaSerial or self.preferences.mfaSerial == "":
               print("    Please, "+ Style.IRED + "DON'T FORGET"+ Style.RESET + " to set your "+ Style.GREEN + "MFA Serial"+ Style.RESET + ", see:")     
               print("    " + Style.GREEN + "set mfa-serial {arn:aws:iam::...}\n" )
            print(self.preferences.startSessionWithTheNewCookie())
        elif "verbose" in arg:
            result = (arg.split(" ")[1]).lower() in ("True","true")
            self.preferences.printResults=result
            print(" " + Emoticons.thumbsUp() + " Verbose susccessfully modified to " + Style.GREEN + self.convertsBoolToEnableDisable(result) + Style.RESET + "\n")
        elif "tables-line" in arg:
            result = (arg.split(" ")[1]).lower() in ("True","true")
            self.preferences.tableLineSeparator=result
            print(" " + Emoticons.thumbsUp() + " Tables line susccessfully modified to " + Style.GREEN + self.convertsBoolToEnableDisable(result) + Style.RESET + "\n")
        elif "chunk-size" in arg:
            value=arg.split(" ")[1]    
            self.preferences.uploadChunkSizeMultipart = value
            print(" " + Emoticons.thumbsUp() + " Multipart Upload Chunk-size susccessfully modified to " + Style.GREEN + value + Style.RESET + "\n")
        elif "threshold" in arg:
            value=arg.split(" ")[1]    
            self.preferences.uploadThresholdMultipart = value
            print(" " + Emoticons.thumbsUp() + " Multipart Upload Threshold susccessfully modified to " + Style.GREEN + value + Style.RESET + "\n")    
        else:
            print(" " + Emoticons.error() + " Ops... No preference with the name "+ arg + Style.RESET + "\n")
            return None     

    def complete_get(self,text,line,begidx,endidx):
        return [i for i in ('tags','profile','region','verbose','tables-line','chunk-size','threshold') if i.startswith(text)]
    def do_get(self,arg):        
        "Show a value configured to a environment variable/preference (type env to see all the available options)\n\n"
        if "profile" in arg:
            print(" " + Emoticons.pointRight() + " Profile AWS is " + Style.GREEN + ("default" if self.preferences.awsProfile == "" else self.preferences.awsProfile) + Style.RESET + "\n")
        elif "region" in arg:
            print(" " + Emoticons.pointRight() + " Region AWS is " + Style.GREEN + self.preferences.awsRegion + Style.RESET + "\n")    
        elif "assume-role" in arg:
            print(" " + Emoticons.pointRight() + " Assume Role set to " + Style.GREEN + self.preferences.assumeRole + Style.RESET + "\n")        
        elif "mfa-serial" in arg:
            print(" " + Emoticons.pointRight() + " MFA Serial set to " + Style.GREEN + ("None" if not self.preferences.mfaSerial else self.preferences.mfaSerial) + Style.RESET + "\n")    
        elif "mfa" in arg:
            print(" " + Emoticons.pointRight() + " MFA PassCode set to " + Style.GREEN + ("None" if not self.preferences.mfaPassCode else self.preferences.mfaPassCode) + Style.RESET + "\n")            
        elif "tags" in arg:
            print(" " + Emoticons.pointRight() + " Tags Filters are " + Style.GREEN + str(self.preferences.awsTags) + Style.RESET + "\n")        
        elif "verbose" in arg:
            print(" " + Emoticons.pointRight() + " Verbose is set to " + Style.GREEN + self.convertsBoolToEnableDisable(self.preferences.printResults) + Style.RESET + "\n")    
        elif "tables-line" in arg:
            print(" " + Emoticons.pointRight() + " Tables line is set to " + Style.GREEN + self.convertsBoolToEnableDisable(self.preferences.tableLineSeparator) + Style.RESET + "\n")
        elif "chunk-size" in arg:
            print(" " + Emoticons.pointRight() + " Multipart Upload Chunk-size is set to " + Style.GREEN + self.preferences.uploadChunkSizeMultipart + Style.RESET + "\n")
        elif "threshold" in arg:
            print(" " + Emoticons.pointRight() + " Multipart Upload Threshold is set to " + Style.GREEN + self.preferences.uploadThresholdMultipart + Style.RESET + "\n")        

    def do_env(self, arg):    
        "[SHORTCUT for \"environment\"]\nShow Environment Configuration\n\n"
        self.do_environment(arg)

    def do_environment(self, arg):    
        "Show Environment Configuration\n\n"

        WIDTH_TEXT     = 60
        MARGIN_TEXT    = 20
        SIZE_SEPARATOR = 85
        output  ="-".ljust(SIZE_SEPARATOR,"-") + "\n"           
        
        output += "   " + Emoticons.env() + "   " + Style.CYAN + "E N V I R O N M E N T" + Style.RESET + "" + "\n"           
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n" 
        output += "  " + Emoticons.pin() + " " + Style.CYAN + "Variables:" + Style.RESET + "" + "\n"
        output +=Style.BLUE + "  AWS Profile.....: " + Style.GREEN + ("default" if self.preferences.awsProfile == "" else self.preferences.awsProfile) + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "Profile to be used, values set at AWS configuration\n                    file ($USER_HOME/.aws/credentials)" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to set:" + Style.GREEN+ " set profile {PROFILE}" + Style.RESET + "\n"
        output += "\n"
        output +=Style.BLUE + "  AWS Region......: " + Style.GREEN + self.preferences.awsRegion + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "AWS Region to be used, values can set at AWS configuration\n                    file ($USER_HOME/.aws/config)" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to set:" + Style.GREEN+ " set region {REGION}" + Style.RESET + "\n"
        output += "\n"
        output +=Style.BLUE + "  Assume Role.....: " + Style.GREEN + self.preferences.assumeRole + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "Role to be assumed in case needed STS Token, for MFA or \n                    Accessing another account" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to set..:" + Style.GREEN+ " set assume-role {ROLE}" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to clean:" + Style.GREEN+ " unset assume-role" + Style.RESET + "\n"
        output += "\n"
        output +=Style.BLUE + "  MFA Serial......: " + Style.GREEN + ("None" if not self.preferences.mfaSerial else self.preferences.mfaSerial) + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "MFA Serial used to start the Session with Assume Role / MFA\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to set:" + Style.GREEN + " set mfa-serial {arn:aws:iam::...}" + Style.RESET + "\n"
        output += "\n"
        output +=Style.BLUE + "  MFA PassCode....: " + Style.GREEN + ("None" if not self.preferences.mfaPassCode else self.preferences.mfaPassCode) + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "MFA PassCode used to start the Session with Assume Role / MFA\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to set:" + Style.GREEN + " set mfa {passcode}" + Style.RESET + "\n"
        output += "\n"
        output +=Style.BLUE + "  Tags............: " + Style.GREEN + str(self.preferences.awsTags) + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + Functions.formatDescr("Tags that's is going to be used as Filters in all AWS Functions (when applicable).",MARGIN_TEXT,WIDTH_TEXT) + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to set..:" + Style.GREEN+ " set tags {TAG_NAME=VALUE,TAG_NAME=VALUE}" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "     or to add..:" + Style.GREEN+ " add tags {TAG_NAME=VALUE,TAG_NAME=VALUE}" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to clean:" + Style.GREEN+ " unset tags" + Style.RESET + "\n"
        output += "\n"
        output += "\n"
        output += "  " + Emoticons.pin() + " " + Style.CYAN + "Preferences:" + Style.RESET + "" + "\n"
        output +=Style.BLUE + "  Verbose.........: " + Style.GREEN + (self.convertsBoolToEnableDisable(self.preferences.printResults)) + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "Show any further available information when launch a command." + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to modify:" + Style.GREEN+ " set verbose {true|false}" + Style.RESET + "\n"
        output += "\n"
        output +=Style.BLUE + "  Tables Line.....: " + Style.GREEN + (self.convertsBoolToEnableDisable(self.preferences.tableLineSeparator)) + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "Remove the lines between table's rows when applied." + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to modify:" + Style.GREEN+ " set tables-line {true|false}" + Style.RESET + "\n"
        output += "\n"
        output += "\n"
        output += "  " + Emoticons.pin() + " " + Style.CYAN + "S3 Multipart Uploads:" + Style.RESET + "" + "\n"
        output +=Style.BLUE + "  Chunk Size......: " + Style.GREEN + self.preferences.uploadChunkSizeMultipart + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "Upload block size for Multipart Uploads (Megabytes)" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to modify:" + Style.GREEN+ " set chunk-size 10" + Style.RESET + "\n"
        output +=Style.BLUE + "  Threshold.......: " + Style.GREEN + self.preferences.uploadThresholdMultipart + Style.RESET + "\n"
        output +=Style.CYAN + "                    " + "Level size which starts Multipart Uploads (Megabytes)" + Style.RESET + "\n"
        output +=Style.BLUE + "                    " + Style.BLUE + "Command to modify:" + Style.GREEN+ " set threshold 200" + Style.RESET + "\n"

        output +="-".ljust(SIZE_SEPARATOR,"-") + "\n"                      
        print(output)

    def convertsBoolToEnableDisable(self, value):
        if value:
           return "Enabled"
        return "Disabled"    

    def do_lg(self, arg):
        "List all available groups of functions\n"
        output  = "-".ljust(SIZE_SEPARATOR,"-") + "\n" 
        output += "   " + Emoticons.tool() + "   " + Style.CYAN + "A V A I L A B L E    F U N C T I O N S    G R O U P S" + Style.RESET + "" + "\n"
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"    
        for group in Functions.GROUPS:
            output += "  " + Emoticons.pointRight() + " " + Style.GREEN + group + Style.RESET + "\n" #+ \
                      #(" ".ljust(LABEL_LENGTH_FUNCTION_NAME - len(group) + 2,"-")) + "> "+ Functions.formatDescr("description ToDo", 34, 60) + "\n"
        print(output)
        print(Style.GREEN + " To list functions of a group: " + Style.IBLUE + "\n    ls -f networking")
        print(Style.GREEN + "    " + Style.IBLUE + "ls -l -f ec2")
        print("")

    def do_l(self, arg):
        "[SHORTCUT for \"ls -l\"]\nSame as type ls -l, list all available function\n   Arguments:\n   -l  Show usage details of AWS functions\n"
        self.do_ls("-l")    

    def do_menu(self, arg):
        "List all available function\n"
        self.do_ls("-l")

    def do_ls(self, arg):
        "List all available function\n   Arguments:\n   -l  Show usage details of AWS functions\n"
        output  = "-".ljust(SIZE_SEPARATOR,"-") + "\n" 
        output += "   " + Emoticons.tool() + "   " + Style.CYAN + "A V A I L A B L E    F U N C T I O N S" + Style.RESET + "" + "\n"
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"    
        groupPrinted = ""
        i = 0
        for key in Functions.FUNCTIONS:
            i += 1
            function      = Functions.FUNCTIONS[key]
            functionName  = self.convertFunctionsName(key)
            functionDescr = "  " + Emoticons.pointRight() + " " + Style.GREEN + functionName + Style.RESET + (" ".ljust(LABEL_LENGTH_FUNCTION_NAME - len(functionName) + 2,"-")) + \
                                  "> "+ Functions.formatDescr(function["description"], 34, 60) + "\n"
            printIt = True
            if "-f" in arg:
               groupFilter = arg[arg.find("-f") + 3:].split(" ")[0]
               if  function["group"].lower() != groupFilter.lower():
                   printIt = False

            if "-l" in arg:
                if printIt:
                   groupTitle = "  " + Style.IBLUE + function["group"].upper() + Style.RESET + "\n" + "-".ljust(SIZE_SEPARATOR,"-") + "\n"    
                   if groupPrinted != function["group"]:
                      output += groupTitle 
                      groupPrinted = function["group"]
                   output += functionDescr
                   output += Style.MAGENTA + "          Arguments: " + Style.RESET + "\n"
                   for args in function["arguments"]:
                       output += Style.BLUE + "               " + args["name"] + " ".ljust(args["biggerLabel"] - len(args["name"])," ") + Style.MAGENTA 
                       output += ("[Required]" if args["mandatory"] == True else "[Optional]")
                       output += Style.RESET + "....: " + Style.RESET + Functions.formatDescr(args["description"],51,45) + "\n" 
   
                   output += "          " + Style.MAGENTA + "Examples:" + Style.RESET + "\n"
                   for exs in function["examples-interactive"]:
                       output += "               " + exs["command"] + "\n"
                   output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"
            else:
                if printIt:
                   groupTitle    = ("\n" if i > 1 else "") + "  " + Style.IBLUE + function["group"].upper() + Style.RESET + "\n"
                   if groupPrinted != function["group"]:
                      output += groupTitle 
                      groupPrinted = function["group"]
                   output += functionDescr
        print(output)
    def complete_ls(self,text,line,begidx,endidx):
        return ([i for i in ('networking','ec2','s3','general') if i.startswith(text)])    
    
    # List a Help the one function only
    def helpFunction(self, key):    
        function = Functions.FUNCTIONS[key]

        output  = "-".ljust(SIZE_SEPARATOR,"-") + "\n"           
        output += "   " + Emoticons.tool() + " " + Style.CYAN +  function["name"].upper() + Style.RESET + "" + "\n"
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"    

        functionName = self.convertFunctionsName(key)
        functionDescr = "  " + Emoticons.pointRight() + " " + Style.GREEN + functionName + Style.RESET + (" ".ljust(LABEL_LENGTH_FUNCTION_NAME - len(functionName) + 2,"-")) + \
                                "> "+ Functions.formatDescr(function["description"], 26, 59) + "\n"
        output += functionDescr
        output += Style.MAGENTA + "          Arguments: " + Style.RESET + "\n"
        for args in function["arguments"]:
            output += Style.BLUE + "               " + args["name"] + " ".ljust(args["biggerLabel"] - len(args["name"])," ") + Style.MAGENTA 
            output += ("[Required]" if args["mandatory"] == True else "[Optional]")
            output += Style.RESET + "....: " + Style.RESET + Functions.formatDescr(args["description"],51,34) + "\n"
        output += "          " + Style.MAGENTA + "Examples:" + Style.RESET + "\n"
        for exs in function["examples-interactive"]:
            output += "               " + exs["command"] + "\n"
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"
        return output

    def convertFunctionsName(self,function):
        pos = function.find("-")
        while pos > 1 and pos < 20:
            capitalize = function[pos+1]
            function = function.replace("-"+capitalize,capitalize.upper())
            pos = function.find("-")
        return function


    #########################################################################################################
    # Execute a function, creating a paralell process to not block the UI, 
    # giving some interaction to user while executing a long time function (in case that happens)
    def executeFunction(self,f,arg,preferences=None):
        print (Emoticons.waiting() + " Wait...")
        if self.isWindows():
           p = multiprocessing.Process(target=f,args=(PyAwsShell,arg,preferences,))
           p.start()
           self.waitForCompletion(p)
           p.join()    
        else:    
           p = Process(target=f, args=(arg,preferences,))
           p.start()
           self.waitForCompletion(p)
           p.join()

    def waitForCompletion(self, p):
        tiempo = 0
        idx = 0
        while p.is_alive():
            idx += 1
            if idx == 1:
                sys.stdout.write("\r" + Emoticons.time() + " " + str(int(tiempo)) + " secs " + Emoticons.waitDistract() + "    ")
            elif idx == 2:   
                sys.stdout.write("\r" + Emoticons.time() + " " + str(int(tiempo)) + " secs " + Emoticons.waitDistract() + Emoticons.waitDistract() + "  ")
            elif idx == 3:   
                sys.stdout.write("\r" + Emoticons.time() + " " + str(int(tiempo)) + " secs " + Emoticons.waitDistract() + Emoticons.waitDistract() + Emoticons.waitDistract()) 
            else:   
                sys.stdout.write("\r" + Emoticons.time() + " " + str(int(tiempo)) + " secs   " + Emoticons.waitDistract2() + "  ")  
                idx = 0
            sys.stdout.flush()
            tiempo += 1
            time.sleep(1)

    def isWindows(self):
        if os.name == "nt":
            return True
        return False      

    #########################################################################################################
    def do_subnetIsPublic(self, arg):
        "Check if the subnet is public or not looking for Route Tables with 0.0.0.0/0 route, containing Internet Gateways (igw-*)\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.subnetIsPublic,arg,self.preferences)
        else:    
           self.executeFunction(self.subnetIsPublic,arg,self.preferences)

    def subnetIsPublic(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("subnet_","subnet-")
        pyEc2Cp = PyEc2CP(config)    
        print(pyEc2Cp.subnetIsPublic())
    def help_subnetIsPublic(self):
        print(self.helpFunction(Functions.SUBNET_IS_PUBLIC))
    def complete_subnetIsPublic(self,text,line,begidx,endidx):
        return ([i for i in ('subnet_074a9ad8389a90bb8','subnet_04863a881ede25af3','subnet_0ab39c4808d8c8c91') if i.startswith(text)])

    #########################################################################################################
    def do_listEc2(self, arg):
        "List EC2 Instances\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listEc2,arg,self.preferences)
        else:    
           self.executeFunction(self.listEc2,arg,self.preferences)
    def listEc2(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("i_","i-")
        pyEc2Cp = PyEc2CP(config)
        report, content  = pyEc2Cp.listEc2()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listEc2(self):
        print(self.helpFunction(Functions.LIST_EC2))            
    def complete_listEc2(self,text,line,begidx,endidx):
        return ([i for i in ('i_0902ce6ab97baa8e7','i_0bbb04a9cd37a4675','10.2.1.0','172.0.1.123','sg','vpc','subnet','image','cpu','noname','showtags','desc','tags','sort3','tags:Environment=production#Project=xpto') if i.startswith(text)])

    ### IN TESTING...
    #########################################################################################################
    def do_diagramlistEc2(self, arg):
        "Diagram List EC2 Instances\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.diagramlistEc2,arg,self.preferences)
        else:    
           self.executeFunction(self.diagramlistEc2,arg,self.preferences)
    def diagramlistEc2(self, arg, preferences):
        print("EXPIRMENTAL PHASE!!!")
        config = preferences
        config.commandArguments = arg.replace("i_","i-")
        diagramMgnt = DiagramMgnt(config)
        diagramMgnt.diagramVpcEc2()
        print("Done!")
    def help_diagramlistEc2(self):
        print(self.helpFunction(Functions.LIST_EC2))            
    def complete_diagramlistEc2(self,text,line,begidx,endidx):
        return ([i for i in ('i_0902ce6ab97baa8e7','i_0bbb04a9cd37a4675','10.2.1.0','172.0.1.123','sg','vpc','subnet','image','cpu','noname','showtags','desc','tags','sort3','tags:Environment=production#Project=xpto') if i.startswith(text)])

    #########################################################################################################
    def do_listSubnetsVpc(self, arg):
        "List all the Subnets of a VPC\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listSubnetsVpc,arg,self.preferences)
        else:    
           self.executeFunction(self.listSubnetsVpc,arg,self.preferences)
    def listSubnetsVpc(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("vpc_","vpc-")
        pyEc2Cp = PyEc2CP(config)
        report  = pyEc2Cp.listSubnetsVpc()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listSubnetsVpc(self):
        print(self.helpFunction(Functions.LIST_SUBNETS_VPC))            
    def complete_listSubnetsVpc(self,text,line,begidx,endidx):
        return ([i for i in ('vpc_01c6810fb391d215b','vpc_0834b01b2cecac1f3','ispublic','showtags','desc','tags','sort3') if i.startswith(text)])        

    #########################################################################################################
    def do_listVpc(self, arg):
        "List all the VPCs\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listVpc,arg,self.preferences)
        else:    
           self.executeFunction(self.listVpc,arg,self.preferences)
    def listVpc(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("is_","is")
        pyEc2Cp = PyEc2CP(config)
        report = pyEc2Cp.listVpc()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listVpc(self):
        print(self.helpFunction(Functions.LIST_VPC))    
    def complete_listVpc(self,text,line,begidx,endidx):
        return ([i for i in ('subnets','ispublic','showtags','excel','desc','tags','sort3') if i.startswith(text)])

    #########################################################################################################
    def do_listSg(self, arg):
        "List all the Security Groups\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listSg,arg,self.preferences)
        else:    
           self.executeFunction(self.listSg,arg,self.preferences)
    def listSg(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("is_","is")
        pyEc2NetSecCp = PyEc2NetSecCP(config)
        report = pyEc2NetSecCp.listSecurityGroup()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listSg(self):
        print(self.helpFunction(Functions.LIST_SG))    
    def complete_listSg(self,text,line,begidx,endidx):
        return ([i for i in ('list-associated','list-permissions','excel','drawio','showtags','desc','tags','sort3') if i.startswith(text)])

    #########################################################################################################
    def do_listRt(self, arg):
        "List all the Route Tables\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listRt,arg,self.preferences)
        else:    
           self.executeFunction(self.listRt,arg,self.preferences)
    def listRt(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("is_","is")
        pyEc2Cp = PyEc2CP(config)
        report = pyEc2Cp.listRouteTables()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listRt(self):
        print(self.helpFunction(Functions.LIST_ROUTE_TABLES))    
    def complete_listRt(self,text,line,begidx,endidx):
        return ([i for i in ('show-routes','drawio','showtags','desc','tags','sort3') if i.startswith(text)])

    #########################################################################################################
    def do_listNacls(self, arg):
        "List all the Network Access Control List\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listNacls,arg,self.preferences)
        else:    
           self.executeFunction(self.listNacls,arg,self.preferences)
    def listNacls(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("is_","is")
        pyEc2Cp = PyEc2CP(config)
        report = pyEc2Cp.listNacls()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listNacls(self):
        print(self.helpFunction(Functions.LIST_NACLS))    
    def complete_listNacls(self,text,line,begidx,endidx):
        return ([i for i in ('show-entries','showtags','excel','drawio','desc','tags','sort3') if i.startswith(text)])        

    #########################################################################################################
    def do_listTargetGroups(self, arg):
        "List all the Target Groups\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listTargetGroups,arg,self.preferences)
        else:   
           self.executeFunction(self.listTargetGroups,arg,self.preferences)
    def listTargetGroups(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyElbCP = PyElbCP(config)
        report = pyElbCP.listTargetGroups()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listTargetGroups(self):
        print(self.helpFunction(Functions.LIST_TARGET_GROUPS))    
    def complete_listTargetGroups(self,text,line,begidx,endidx):
        return ([i for i in ('health','sort3','desc') if i.startswith(text)])        

    #########################################################################################################
    def do_findElbsEc2(self, arg):
        "Find all the Load Balancer and Target Groups pointing to an EC2 Instance\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.findElbsEc2,arg,self.preferences)
        else:
           self.executeFunction(self.findElbsEc2,arg,self.preferences)    
    def findElbsEc2(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("i_","i-")
        pyElbCP = PyElbCP(config)
        report = pyElbCP.findInstancesElbsTgs()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_findElbsEc2(self):
        print(self.helpFunction(Functions.FIND_ELBS_EC2))            
    def complete_findElbsEc2(self,text,line,begidx,endidx):
        return ([i for i in ('i_0361f6405c08923b6','i_03ef7e40cc1ba806f','i_046adc50a97a02924','elbarn','tgarn','sort3','desc') if i.startswith(text)])        
    
    #########################################################################################################
    def do_listBucketsS3(self, arg):
        "List buckets of S3\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listBucketsS3,arg,self.preferences)
        else:
           self.executeFunction(self.listBucketsS3,arg,self.preferences)    
    def listBucketsS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        report = pyS3CP.listBucketsS3()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listBucketsS3(self):
        print(self.helpFunction(Functions.LIST_BUCKETS_S3))            

    #########################################################################################################
    def do_listObjectsBucketS3(self, arg):
        "List objects in a bucket\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.listObjectsBucketS3,arg,self.preferences)
        else:
           self.executeFunction(self.listObjectsBucketS3,arg,self.preferences)    
    def listObjectsBucketS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        report = pyS3CP.listObjectsBucketS3()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listObjectsBucketS3(self):
        print(self.helpFunction(Functions.LIST_OBJECTS_BUCKETS_S3))            
    def complete_listObjectsBucketS3(self,text,line,begidx,endidx):
        return ([i for i in ('prefix=') if i.startswith(text)])    

    #########################################################################################################
    def do_listUploadsS3(self, arg):
        "List Uploads that did not finished yet (know as MultiPart Uploads)\n"
        self.listUploadsS3(arg,self.preferences)
    def listUploadsS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        report = pyS3CP.listUploads()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_listUploadsS3(self):
        print(self.helpFunction(Functions.LIST_UPLOADS_S3))            

    #########################################################################################################
    def do_abortUploadsS3(self, arg):
        "Abort Uploads that did not finished yet (know as MultiPart Uploads)\n"
        self.abortUploadsS3(arg,self.preferences)
    def abortUploadsS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        report = pyS3CP.abortUploads()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_abortUploadsS3(self):
        print(self.helpFunction(Functions.ABORT_UPLOADS_S3))

    #########################################################################################################
    def do_transferToS3(self, arg):
        "Upload file/folder contents to a S3 Bucket\n"
        self.transferToS3(arg,self.preferences)
    def transferToS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        report = pyS3CP.transferToS3()
        if report and report != "":
           print(report)
    def help_transferToS3(self):
        print(self.helpFunction(Functions.TRANSFER_TO_S3)) 

    #########################################################################################################
    def do_showTargetsS3(self, arg):
        "Show all the targets used for Uploads (files, folders)\n"
        self.showTargetsS3(arg,self.preferences)
    def showTargetsS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        pyS3CP.showTargetsS3()
    def help_showTargetsS3(self):
        print(self.helpFunction(Functions.SHOW_TARGET_S3))

    #########################################################################################################
    def do_showTargetUploadsS3(self, arg):
        "List all uploads performed to a specific target (files/folder)\n"
        self.showTargetUploadsS3(arg,self.preferences)
    def showTargetUploadsS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        pyS3CP.showTargetUploadsS3()
    def help_showTargetUploadsS3(self):
        print(self.helpFunction(Functions.SHOW_TARGET_UPLOADS_S3))

    #########################################################################################################
    def do_showTargetUploadPartsS3(self, arg):
        "List all uploads performed to a specific target (files/folder)\n"
        self.showTargetUploadPartsS3(arg,self.preferences)
    def showTargetUploadPartsS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        pyS3CP.showTargetUploadPartsS3()
    def help_showTargetUploadPartsS3(self):
        print(self.helpFunction(Functions.SHOW_TARGET_UPLOAD_PARTS_S3))                            

    #########################################################################################################
    def do_removeTargetS3(self, arg):
        "Delete all the data of a target (File/folder) upload\n"
        self.removeTargetS3(arg,self.preferences)
    def removeTargetS3(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        pyS3CP.removeTargetS3()
    def help_removeTargetS3(self):
        print(self.helpFunction(Functions.REMOVE_TARGET_HISTORY_S3))                                

    #########################################################################################################
    
    def do_nslookupEc2R53(self, arg):
        "Query and describe the route path from a DNS domain until a EC2 Instance\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.nslookupEc2R53,arg,self.preferences)  
        else:    
           self.executeFunction(self.nslookupEc2R53,arg,self.preferences)
    def nslookupEc2R53(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyr53CP = PyR53CP(config)
        report = pyr53CP.nslookupEc2R53()
        Utils.addToClipboard(report)
        self.last_output = report
        print(report)
    def help_nslookupEc2R53(self):
        print(self.helpFunction(Functions.NSLOOKUP_EC2_R53))            
    def complete_nslookupEc2R53(self,text,line,begidx,endidx):
        return ([i for i in ('graph','thin','save','verbose') if i.startswith(text)])

    #########################################################################################################
    def do_navigator(self, arg):
        "Navigate through the Network information of the current AWS Account\n"
        self.navigator(arg,self.preferences)
    def navigator(self, arg, preferences):
        verbose = False
        config  = preferences
        config.commandArguments = arg
        if "verbose" in config.commandArguments:
            verbose = True
        #pathToResources = "./pymxgraph"
        pathToResources = "./"
        pymxGraph = PymxGraph(pathToResources)
        pymxGraphAwsNavigator = PymxGraphAwsNavigator(pathToResources, pymxGraph.images, pymxGraph.htmlSnippets, verbose)
        pymxGraphAwsNavigator.drawAwsNavigator()
    def help_navigator(self):
        print(self.helpFunction(Functions.AWS_NAVIGATOR))            
    def complete_navigator(self,text,line,begidx,endidx):
        return ([i for i in ('verbose','') if i.startswith(text)])
    
    #########################################################################################################
    def do_drawNetworking(self, arg):
        "Generate data for a tradicional AWS Networking Diagram using Drawio CVS Import\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.drawNetworking,arg,self.preferences)
        else:    
           self.executeFunction(self.drawNetworking,arg,self.preferences)
    def drawNetworking(self, arg, preferences):
        config = preferences
        config.commandArguments = arg.replace("is_","is")
        pyEc2Cp = PyEc2CP(config)
        report = pyEc2Cp.drawNetworking()
        self.last_output = report
        print(report)
    def help_drawNetworking(self):
        print(self.helpFunction(Functions.DRAW_NETWORKING))    
    def complete_drawNetworking(self,text,line,begidx,endidx):
        return ([i for i in ('routetables','nacls','tgws','rttgws','all') if i.startswith(text)])

    #########################################################################################################
    def do_s3PreSignedURL(self, arg):
        "PreSign a S3 URL\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.s3PreSignedURL,arg,self.preferences)
        else:    
           self.executeFunction(self.s3PreSignedURL,arg,self.preferences)
    def s3PreSignedURL(self, arg, preferences):
        config = preferences
        config.commandArguments = arg
        pyS3CP = PyS3CP(config)
        pyS3CP.preSignURL()
    def help_s3PreSignedURL(self):
        print(self.helpFunction(Functions.S3_PRESIGNED_URL))
    """ def complete_s3PreSignedURL(self,text,line,begidx,endidx):
        return ([i for i in ('verbose','') if i.startswith(text)]) """
    
    #########################################################################################################
    def do_roleLogoff(self, arg):
        "Logoff and Remove a Temporary Session Role\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.roleLogoff,arg,self.preferences)  
        else:    
           self.executeFunction(self.roleLogoff,arg,self.preferences)
    def roleLogoff(self, arg, preferences):
        if self.preferences.isValidCookieTempCredentials():
           output  = CookieTempCredentials.headerCookieSTS()
           self.preferences.deleteCookieTemporaryCredentials()
           self.preferences.assumeRole = "" 
           self.preferences.mfa = "" 
           output += Style.GREEN + "Temporary Session Role was removed!"
           output += "\n"
        else:
           output = CookieTempCredentials.invalidCookie()
        print(output)
    def help_roleLogoff(self):
        print(self.helpFunction(Functions.ROLE_LOGOFF))            
    #def complete_roleLogoff(self,text,line,begidx,endidx):
    #    return ([i for i in ('graph','thin','save','verbose') if i.startswith(text)])

    #########################################################################################################
    def do_roleInfo(self, arg):
        "Show info of a current Temporary Session Role\n"
        if self.isWindows():
           self.executeFunction(PyAwsShell.roleInfo,arg,self.preferences)  
        else:    
           self.executeFunction(self.roleInfo,arg,self.preferences)
    def roleInfo(self, arg, preferences):
        if not self.preferences.cookieTempCredentials():
           output = CookieTempCredentials.invalidCookie()
        else: 
           output = CookieTempCredentials.printCookie(self.preferences.isValidCookieTempCredentials(), \
                                                      self.preferences.assumeRole, \
                                                      self.preferences.mfaSerial, \
                                                      self.preferences.cookieTempCredentials().timeToExpire())
        print(output)   
    def help_roleLogoff(self):
        print(self.helpFunction(Functions.ROLE_INFO))            
    #def complete_roleLogoff(self,text,line,begidx,endidx):
    #    return ([i for i in ('graph','thin','save','verbose') if i.startswith(text)])

