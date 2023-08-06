import json
import os
import sys
from io import StringIO
import clipboard
from datetime import datetime
from pyawscp.Emoticons import Emoticons
from pygments import highlight, lexers, formatters

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

REMAIN_START = 72

class Utils:

    @staticmethod 
    def saveToFile(fileName, response) :
        if not os.path.exists("results"):
            os.makedirs("results")
        with open("results/" + fileName, 'w') as fout:
            json.dump(response, fout, indent=4)

    @staticmethod 
    def saveJsonToFile(fileName, jsonContent) :
        if not os.path.exists("results"):
            os.makedirs("results")
        with open("results/" + fileName, 'w') as fout:
            fout.write(jsonContent)
            fout.flush()
            print("OK Save")

    @staticmethod
    def saveDictAsJson(name, dict):
        if os.path.exists(name):
           os.delete(name)
        f = open(name + ".json", "a")
        f.write(json.dumps(dict))
        f.close()

    @staticmethod
    def loadJsonFile(fileName) :
        return json.load(open(fileName, 'r'))

    @staticmethod 
    def separator():
        return "-".ljust(52,'-')

    @staticmethod
    def addHeader(result):
        output = "\n"
        output += Style.MAGENTA + "*".ljust(REMAIN_START,'*') + "\n"
        output += Style.YELLOW
        output += " ___ ___ ___ _   _ _  _____  _ " + "\n"
        output += "| _ \ __/ __| | | | ||_   _|(_)" + "\n"
        output += "|   / _|\__ \ |_| | |__| |   _ " + "\n"
        output += "|_|_\___|___/\___/|____|_|  (_)" + "\n"
        output += " " + Style.MAGENTA + "\n"
        output += "*".ljust(REMAIN_START,'*') + "\n"
        return output

    @staticmethod
    def formatPrintTags(tags):
        output = ""
        if isinstance(tags,list):
           for tag in tags:
              output += Style.GREEN + tag["Key"] + Style.WHITE + "=" + Style.MAGENTA + tag["Value"] + Style.RESET + ", "
           return output   
        else:
           for tag in tags:
              output += Style.GREEN + str(tag) + Style.WHITE + "=" + Style.MAGENTA + str(tags[tag])+  Style.RESET + ", "
        if len(output)  > 2:    
           return output[:len(output)-2]    
        return Style.MAGENTA + "---" +  Style.RESET   

    @staticmethod
    def formatResult(functionName, result, config, jsonResult, tagsApply, tableArgs):
        # Show result at screen (verbose mode)
        if jsonResult != "" and (tableArgs.verbose or config.printResults):
           colorful_json = highlight(jsonResult, lexers.JsonLexer(), formatters.TerminalFormatter())
           print(" ")
           print(colorful_json)

        # Save to a file the JSON result
        if tableArgs and tableArgs.saveToFile and jsonResult != "":
           now = datetime.now()   
           fileName = now.strftime("%Y%m%d-%H%M%S") + "_" + functionName.replace("/","_").replace(".","_").replace(" ","-") + ".json"
           Utils.saveJsonToFile(fileName , jsonResult)             

        output = Utils.addHeader(result)
        output += Style.RESET + " " + Emoticons.pin() + " >>---> " + Style.GREEN + functionName +  Style.RESET + " <---<< "+ Emoticons.pin() + "\n"

        if config.awsTagsToFilter and tagsApply:
           output += "\n " + Emoticons.magnifier() + " Filters  \n      Environment Tags...: " + Style.GREEN + Utils.formatPrintTags(config.awsTags) + Style.RESET + "\n"
        if tableArgs and len(tableArgs.tagsTemp) > 0:
           output += "      Arguments   Tags...: " + Style.GREEN + Utils.formatPrintTags(tableArgs.tagsTemp) + Style.RESET + "\n"   

        output += " " + "\n"
        output += Style.RESET + result + "\n"
        output += " " + "\n"
        output += Style.MAGENTA + "*".ljust(REMAIN_START,'*') + "\n"
        output += " " + Style.RESET + "\n"
        return output

    @staticmethod 
    def dictToJson(response) :
        strObj = StringIO()
        json.dump(response, strObj, default=str, indent=4, sort_keys=True)
        return strObj.getvalue()

    @staticmethod
    def formatNumber(number, group, decimalPlaces, americanFormat=False):
        strNumber = str(number)
        if strNumber.find(".") > 1:
           intPart     = strNumber[:strNumber.find(".")]
           decimalPart = strNumber[strNumber.find(".")+1:]
        else:   
           intPart       = strNumber
           decimalPart   = ""
           decimalPlaces = 0

        groupSeparator   = "."
        decimalSeparator = ","
        if americanFormat:
           groupSeparator   = ","
           decimalSeparator = "."

        group     = 3
        strNumber = ""
        for c in reversed(intPart):
            strNumber = c + strNumber
            group -= 1
            if group == 0:
                strNumber = groupSeparator + strNumber
                group = 3
        
        if strNumber.startswith("."):
           strNumber = strNumber[1:]

        if decimalPlaces == 0 or decimalPart == "":
           return strNumber
        else:
           strNumber = strNumber + decimalSeparator
           for c in decimalPart:
               strNumber = strNumber + c
               decimalPlaces -= 1
               if decimalPlaces == 0:
                   break
           return strNumber

    @staticmethod
    def labelTimestamp():
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def clearScreen():
        if sys.platform == "linux" or sys.platform == "linux2":
           os.system('clear')
        elif sys.platform == "win32" or sys.platform == "win64":
           os.system('cls')   
        elif sys.platform == "darwin":
           os.system('clear')      
        else:
           os.system('clear')       

    # Try to copy a value to Clipboard
    @staticmethod
    def addToClipboard(text):
        try:
            textNoColor = Utils.removeCharsColors(text)
            if textNoColor:
               clipboard.copy(textNoColor.strip())
        except:
            pass      
        #
        # Option just for Ubuntu Linux (native)
        #try:
        #   command = 'echo "' + text + '" | xsel --clipboard'
        #   os.system(command)
        #except ValueError:
        #   # Ignore this error
        #   print(ValueError)

    @staticmethod
    def isNumber(s):
        try:
            int(s)
            return True
        except ValueError:
            return False   

            
    
    @staticmethod
    def removeCharsColors(text):
        if isinstance(text, str):
           text = text.replace(Style.UNDERLINE,"") \
                      .replace(Style.RESET,"") \
                      .replace(Style.BLACK,"") \
                      .replace(Style.RED,"") \
                      .replace(Style.GREEN,"") \
                      .replace(Style.YELLOW,"") \
                      .replace(Style.BLUE,"") \
                      .replace(Style.MAGENTA,"") \
                      .replace(Style.CYAN,"") \
                      .replace(Style.WHITE,"") \
                      .replace(Style.BBLACK,"") \
                      .replace(Style.BRED,"") \
                      .replace(Style.BGREEN,"") \
                      .replace(Style.BYELLOW,"") \
                      .replace(Style.BBLUE,"") \
                      .replace(Style.BMAGENTA,"") \
                      .replace(Style.BCYAN,"") \
                      .replace(Style.BWHITE,"") \
                      .replace(Style.BG_BLACK,"") \
                      .replace(Style.BG_RED,"") \
                      .replace(Style.BG_GREEN,"") \
                      .replace(Style.BG_YELLOW,"") \
                      .replace(Style.BG_BLUE,"") \
                      .replace(Style.BG_PURPLE,"") \
                      .replace(Style.BG_CYAN,"") \
                      .replace(Style.BG_WHITE,"") \
                      .replace(Style.IBLACK,"") \
                      .replace(Style.IRED,"") \
                      .replace(Style.IGREEN,"") \
                      .replace(Style.IYELLOW,"") \
                      .replace(Style.IBLUE,"") \
                      .replace(Style.IMAGENTA,"") \
                      .replace(Style.ICYAN,"") \
                      .replace(Style.IWWHITE,"") \
                      .replace(Style.BIBLACK,"") \
                      .replace(Style.BIRED,"") \
                      .replace(Style.BIGREEN,"") \
                      .replace(Style.BIYELLOW,"") \
                      .replace(Style.BIBLUE,"") \
                      .replace(Style.BIPURPLE,"") \
                      .replace(Style.BICYAN,"") \
                      .replace(Style.BIWHITE,"") \
                      .replace(Style.On_IBLACK,"") \
                      .replace(Style.On_IRED,"") \
                      .replace(Style.On_IGREEN,"") \
                      .replace(Style.On_IYELLOW,"") \
                      .replace(Style.On_IBLUE,"") \
                      .replace(Style.On_IPURPLE,"") \
                      .replace(Style.On_ICYAN,"") \
                      .replace(Style.On_IWHITE,"")
        return text