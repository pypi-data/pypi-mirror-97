# coding=utf-8
#
# Author: Ualter Otoni Pereira
# ualter.junior@gmail.com
#
import os
import logging
import sys
from os.path import expanduser
import signal
from pyawscp.Functions import Functions
from pyawscp.Utils import Style, Utils
from pyawscp.Config import Config
from pyawscp.PyEc2Cp import PyEc2CP
from pyawscp.PyElbCp import PyElbCP
from pyawscp.PyAwsShell import PyAwsShell

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

signal.signal(signal.SIGINT, signal.SIG_DFL)

class PyAwsCp:
    def __init__(self):
        FILE_LOG = expanduser("~") + "/.pyawscp/" + "log"
        if not os.path.exists(FILE_LOG):
           os.makedirs(FILE_LOG)

        rootLogger = logging.getLogger()
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        fileHandler = logging.FileHandler("{0}/{1}.log".format(FILE_LOG, "py-awscp"))
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.WARN)
        rootLogger.addHandler(fileHandler)

        #consoleHandler = logging.StreamHandler(sys.stdout)
        #consoleHandler.setFormatter(logFormatter)
        #consoleHandler.setLevel(logging.DEBUG)
        #rootLogger.addHandler(consoleHandler)

        self.start()

    def start(self):  
        if len(sys.argv) > 1:      
           if sys.argv[1] == "list" or sys.argv[1] == "help":
              Utils.clearScreen()
              Functions.showFunctions()
           elif sys.argv[1] == "-l" or sys.argv[1] == "-h":
              Utils.clearScreen()
              Functions.showFunctionsSummary()
           else:
              # One-way function execution
              s   = ""
              for arg in sys.argv:
                 s += arg
                 s += ","
              s = s[:len(s) - 1] 
              PyAwsShell().onewayFunction(s)  
           sys.exit()

        # Interactive 
        config = Config()
        config.interactive = True
        if not config.isThereAwsCredentials():
           sys.exit()
        try:
           PyAwsShell().cmdloop()
        except KeyboardInterrupt:
           print("ERROR")
           pass   

def main():
    """Start Python AWS Shell Cockpit v0.5"""
    pyAwsCp = PyAwsCp()

if __name__ == '__main__':
    #pyAwsCp = PyAwsCp()
    main()


