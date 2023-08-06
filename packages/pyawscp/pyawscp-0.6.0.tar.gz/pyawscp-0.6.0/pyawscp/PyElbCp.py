import boto3
import logging
import sys
import json
from botocore.exceptions import ClientError
from datetime import datetime
from arnparse import arnparse
from pygments import highlight, lexers, formatters
from pyawscp.Functions import Functions
from pyawscp.TableArgs import TableArgs
from pyawscp.Utils import Utils, Style
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

class PyElbCP:

    config = None

    def __init__(self, config):
        self.config = config

    # A main function called from user
    # List the Target Groups, Health Checks and its connected ELBs
    def listTargetGroups(self):
        elbv2       = self.botoSession().client('elbv2')
        tgArn       = []
        elbArn      = None
        showElbArn  = False
        showTgArn   = False
        healthInfo  = False

        tableArgs = TableArgs()

        tableArgs.setArguments(self.config.commandArguments)
        if "," in self.config.commandArguments: 
           for arg in self.config.commandArguments.split(","):
               if "health" in arg:
                  healthInfo = True
               elif "elbarn" in arg:
                  showElbArn = True
               elif "tgarn" in arg:
                  showTgArn = True      
               elif ":targetgroup/" in arg:
                  if ";" in arg: 
                     for tg in arg.split(";"): 
                        tgArn.append(tg)
                  else:   
                     tgArn.append(arg)   
               elif ":loadbalancer/" in arg:
                  elbArn = arg
        else:
           if "health" in self.config.commandArguments:
               healthInfo = True
           if ":targetgroup/" in self.config.commandArguments:
               if ";" in self.config.commandArguments: 
                  for tg in self.config.commandArguments.split(";"): 
                        tgArn.append(tg)
               else:   
                  tgArn.append(self.config.commandArguments)    
           if ":loadbalancer/" in self.config.commandArguments:
               elbArn = self.config.commandArguments      
           if "elbarn" in self.config.commandArguments:
               showElbArn = True
           if "tgarn" in self.config.commandArguments:
               showTgArn = True          

        target_groups = None
        if tgArn:
           target_groups = elbv2.describe_target_groups(TargetGroupArns=tgArn)
        elif elbArn:
           target_groups = elbv2.describe_target_groups(LoadBalancerArn=elbArn)
        else:
           target_groups = elbv2.describe_target_groups()   

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(target_groups)

        resultTxt = "" 
        targetGroups = target_groups['TargetGroups']
        if len(targetGroups) >= 1:
           resultTxt  = "Total of " + Style.GREEN + str(len(targetGroups)) + Style.RESET + " Target Groups\n"
           resultTxt  = resultTxt + Utils.separator()  + "\n\n"
           idx_lin    = 0
           header     = ["#","Target Group","VPC Id","Target Type","Protocol","Port","Load Balancer"]

           if healthInfo:
              header.append("HC Protocol")
              header.append("HC Enabled")
              header.append("HC Interval Sec")
              header.append("HC Path")
              header.append("HC Timeout Sec")
              header.append("Healthy Threshold Count")
              header.append("Unhealthy Threshold Count")
              header.append("Matcher")

           prettyTable    = PrettyTable(header)

           for targetGroup in targetGroups:
               idx_lin += 1

               labelTg = targetGroup['TargetGroupName']
               if showTgArn:
                  labelTg  = targetGroup['TargetGroupArn']

               labelElb = ""
               if len(targetGroup['LoadBalancerArns']) > 0:
                  if not showElbArn:
                     arnELB   = arnparse(targetGroup['LoadBalancerArns'][0])
                     labelElb = arnELB.resource
                  else:
                     labelElb = targetGroup['LoadBalancerArns'][0]


               columns = [ str(idx_lin), labelTg, \
                                         targetGroup['VpcId'], \
                                         targetGroup['TargetType'], \
                                         targetGroup['Protocol'], \
                                         targetGroup['Port'], \
                                         labelElb   
                         ]

               if healthInfo:
                  columns.append(targetGroup['HealthCheckProtocol'])            
                  columns.append(targetGroup['HealthCheckEnabled'])            
                  columns.append(targetGroup['HealthCheckIntervalSeconds'])
                  columns.append(targetGroup['HealthCheckPath'])
                  columns.append(targetGroup['HealthCheckTimeoutSeconds'])
                  columns.append(targetGroup['HealthyThresholdCount'])
                  columns.append(targetGroup['UnhealthyThresholdCount'])
                  if targetGroup['Matcher']['HttpCode']:
                     columns.append("HttpCode: " + targetGroup['Matcher']['HttpCode'])
                  else:   
                     columns.append("")

               prettyTable.addRow(columns)

           if (int(tableArgs.sortCol) - 1) > len(columns):
               tableArgs.sortCol = "1"
           prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
           prettyTable.ascendingOrder(not tableArgs.desc)
           result = ""
           if tgArn:
              if len(tgArn) > 1:
                 result  = result + "Target Groups: \n"
                 for tg in tgArn:
                     result  = result + "  - " + Style.GREEN + str(tg) + Style.RESET + "\n" 
                 result = result + "\n"
              else:   
                 result  = result + "Target Group...: " + Style.GREEN + str(tgArn) + Style.RESET + "\n\n"
           elif elbArn:
              result  = result + "Load Balancer..: " + Style.GREEN + elbArn + Style.RESET +  "\n\n"   

           if healthInfo:   
              result = result + "(HC) " + Style.GREEN + "Health Check" + Style.RESET + "\n\n"
           result = result + prettyTable.printMe("listTargetGroups",self.config.tableLineSeparator, tableArgs)
           return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_TARGET_GROUPS]["name"],result, self.config, jsonResult, False, tableArgs)
        else:
           return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_TARGET_GROUPS]["name"],resultTxt, self.config, "", False)     
    
    # A main function called from user
    # Find Load Balancers and Target Groups pointing to an EC2 Instance
    # arguments: instanceId
    def findInstancesElbsTgs(self):
        elbv2       = self.botoSession().client('elbv2')
        instanceId  = None
        showTgArn   = False
        showElbArn  = False
        tableArgs   = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)
        
        if "," in self.config.commandArguments: 
           instanceId = self.config.commandArguments.split(",")[0]
           for arg in self.config.commandArguments.split(","):
               if "elbarn" in arg:
                  showElbArn = True
               elif "tgarn" in arg:
                  showTgArn = True      
        else:
           instanceId = tableArgs.cleanPipelineArguments()

        tableArgs.setArguments(self.config.commandArguments)

        if not instanceId:
           resultTxt = "Where is the Instance Id? You didn't tell me which EC2 Instance to look for... " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.FIND_ELBS_EC2,resultTxt, self.config, "", True, tableArgs)

        tableArgs.setArguments(self.config.commandArguments)

        target_groups = elbv2.describe_target_groups();

        dictResult = {}
        if len(target_groups) >= 1:
           resultTxt  = ""
           idx_lin    = 0 
           header = ["#","Instance Id","Load Balancer","Target Group", "Vpc Id", "Target Health"]

           prettyTable    = PrettyTable(header)
           printSeparator = False
           columns        = None

           for tg in target_groups['TargetGroups']:
                 targetsHealth = elbv2.describe_target_health(TargetGroupArn=tg["TargetGroupArn"])
                 for targetHealthDescription in targetsHealth["TargetHealthDescriptions"]:
                    if targetHealthDescription["Target"]["Id"] == instanceId:
                       idx_lin += 1

                       labelTg = tg['TargetGroupName']
                       if showTgArn:
                          labelTg  = tg['TargetGroupArn']
                       labelElb = ""
                       if len(tg['LoadBalancerArns']) > 0:
                          if not showElbArn:
                             arnELB   = arnparse(tg['LoadBalancerArns'][0])
                             labelElb = arnELB.resource
                          else:
                             labelElb = tg['LoadBalancerArns'][0]

                       labelTargetHealth = ""
                       if "State" in targetHealthDescription["TargetHealth"]:
                          if targetHealthDescription["TargetHealth"]["State"] == "healthy":
                             labelTargetHealth = "Healthy"
                          else:
                             labelTargetHealth = "Unhealthy"
                             #if "Reason" in targetHealthDescription["TargetHealth"]:
                             #    labelTargetHealth += ", " + targetHealthDescription["TargetHealth"]["Reason"]
                             if "Description" in targetHealthDescription["TargetHealth"]:
                                 labelTargetHealth += ", " + targetHealthDescription["TargetHealth"]["Description"]    

                       dictResult["instanceId"]   = instanceId
                       dictResult["loadBalancer"] = labelElb
                       dictResult["targetGroup"]  = labelTg
                       dictResult["vpcId"]        = tg["VpcId"]  
                       dictResult["targetHealth"] = labelTargetHealth         

                       columns = [ str(idx_lin), \
                                         instanceId, \
                                         labelElb, \
                                         labelTg, \
                                         tg["VpcId"], \
                                         labelTargetHealth
                                 ]
                       prettyTable.addRow(columns)                  

           jsonResult = ""
           if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
              jsonResult = Utils.dictToJson(dictResult)            

           if columns:
               if (int(tableArgs.sortCol) - 1) > len(columns):
                     tableArgs.sortCol = "1"
               prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
               prettyTable.ascendingOrder(not tableArgs.desc)
               result = ""
               result = result + "EC2 Instance..: " + Style.GREEN + instanceId + Style.RESET +  "\n\n"   
               result = result + prettyTable.printMe("findInstancesElbsTgs",self.config.tableLineSeparator, tableArgs)
               return Utils.formatResult(Functions.FUNCTIONS[Functions.FIND_ELBS_EC2]["name"],result, self.config, jsonResult, False, tableArgs)
           else:
               resultTxt = "EC2 Instance..: " + Style.GREEN + instanceId + Style.MAGENTA + " wasn't found in any ELB/TargetGroup" + Style.RESET +  "\n"        
               return Utils.formatResult(Functions.FUNCTIONS[Functions.FIND_ELBS_EC2]["name"],resultTxt, self.config,"", False, tableArgs)
        else:
           resultTxt = Style.MAGENTA + " None Target Group was found! " + Style.RESET +  "\n"        
           return Utils.formatResult(Functions.FUNCTIONS[Functions.FIND_ELBS_EC2]["name"],resultTxt, self.config,"", False, tableArgs)
        
    def botoSession(self):
        return self.config.botoSession();

# For a Function Development
if __name__ == '__main__':
   config = Config()
   config.awsProfile = "ecomm"
   config.awsRegion = "eu-central-1"
   config.printResults = True
   #config.awsTags["Environment"] = "production"
   config.tableLineSeparator = False

   # subnets, is-public (only with subnets active)
   # sort1,desc (when requested together with subnets, the group lines will be omitted)
   #config.commandArguments = "health"
   #config.commandArguments = "sort3"
   #config.commandArguments = "arn:aws:elasticloadbalancing:eu-central-1:659915611011:loadbalancer/app/LB-Graylog/69198aad8d3f7668"
   #config.commandArguments = "arn:aws:elasticloadbalancing:eu-central-1:659915611011:loadbalancer/app/LB-Graylog/69198aad8d3f7668," + \
   #                          "arn:aws:elasticloadbalancing:eu-central-1:659915611011:targetgroup/TG-Graylog/3f4c285bea7970df"
      
   #config.commandArguments = "arn:aws:elasticloadbalancing:eu-central-1:659915611011:loadbalancer/app/LB-Graylog/69198aad8d3f7668," + \
   #                          "arn:aws:elasticloadbalancing:eu-central-1:659915611011:targetgroup/TG-Graylog/3f4c285bea7970df;" + \
   #                          "arn:aws:elasticloadbalancing:eu-central-1:659915611011:targetgroup/tf-20200602224957995200000001/0f8f9375912dfe3f,health"

   #config.commandArguments = "arn:aws:elasticloadbalancing:eu-central-1:659915611011:loadbalancer/app/LB-Graylog/69198aad8d3f7668,health,sort2"
   #config.commandArguments = "arn:aws:elasticloadbalancing:eu-central-1:659915611011:targetgroup/tf-20191023171348503100000005/d3cbc1b6a68a4fee"
   #config.commandArguments = "arn:aws:elasticloadbalancing:eu-central-1:659915611011:targetgroup/tf-20191023171348503100000005/d3cbc1b6a68a4fee;arn:aws:elasticloadbalancing:eu-central-1:659915611011:targetgroup/tf-20191023171348502800000004/ec3200de50acaed9,health"
   PyElbCP = PyElbCP(config)
   #report =  PyElbCP.findInstancesElbsTgs()
   report =  PyElbCP.listTargetGroups()
   Utils.addToClipboard(report)
   print(report)

   # To Do:
   # listLoadBalancers --> https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html

   
