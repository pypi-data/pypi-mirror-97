import datetime
from pyawscp.Utils import Utils, Style

class CookieTempCredentials:

    def __init__(self):
        self.accessKey       = None
        self.secretAccessKey = None
        self.sessionToken    = None
        self.expirationDate  = None
    
    def isExpired(self):
        return self.expirationDate < datetime.datetime.now()

    def humanReadFormatExpirationDate(self):
        return self.expirationDate.strftime("%d-%m-%Y %H:%M:%S")

    def timeToExpire(self):
        if self.expirationDate:
           if self.isExpired():
              return -1
           diff = (self.expirationDate - datetime.datetime.now())
           if diff.seconds > 60:
               min  = int(diff.seconds / 60)
               secs = int(((diff.seconds / 60) - min) * 60)
               return "00:{:02d}:{:02d} minutes".format(min, secs)
           else:   
              return "00:00:{:02d} seconds".format(diff.seconds)
        return 0

    def dateToString(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def stringToDate(self, strDate):
        return datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")


    @staticmethod
    def headerCookieSTS():
        output  = "\n\n" + Style.RESET
        output += "======================"
        output += "\n"
        output += Style.IGREEN + "TEMPORARY SESSION ROLE"
        output += "\n" + Style.RESET
        output += "======================"
        output += "\n"
        return output

   
    @staticmethod
    def invalidCookie():
        output  = CookieTempCredentials.headerCookieSTS()
        output += Style.IRED + "Not found!"
        output += "\n"
        output += Style.GREEN + "There's no active/valid Temporary Session Role"
        output += "\n"
        output += "\n"
        return output

    @staticmethod
    def printCookie(isValid, role, serial, expiration ):
        output = CookieTempCredentials.headerCookieSTS()
        if isValid:
           output += Style.GREEN + "Role.............: " +  Style.IBLUE + role + Style.RESET
           output += "\n"
           output += Style.GREEN + "MFA Serial.......: " +  Style.IBLUE + serial + Style.RESET
           output += "\n"
           output += Style.GREEN + "Time Remaining...: " + Style.IBLUE + str(expiration) + Style.RESET
           output += "\n" 
        else:
           output += Style.IRED + "Not found!"
           output += "\n"
           output += Style.GREEN + "There's no active/valid Temporary Session Role"
           output += "\n"
           output += "\n"
        return output
    
