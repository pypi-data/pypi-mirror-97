# coding=utf-8
#
# Author: Ualter Azambuja Junior
# ualter.junior@gmail.com
#

import boto3
import logging
import sys, os
import json
import math
from pygments import highlight, lexers, formatters
from botocore.exceptions import ClientError
from datetime import datetime
from pyawscp.Functions import Functions
from pyawscp.Utils import Utils, Style
from pyawscp.PrettyTable import PrettyTable
from pyawscp.PyAsciiGraphs import PyAsciiGraphs, Leaf
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.TableArgs import TableArgs
from pyawscp.pymxgraph.PymxGraph import PymxGraph
from pyawscp.pymxgraph.PymxGraphTree import PymxGraphTree

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

FORM_WIDTH   = 162 #185
LINE         = "-"
CROSSROAD    = "+"
LATERAL      = "|"
MARGIN       = " ".ljust(4, " ")
MARGIN_CONN1 = " " + CROSSROAD + LINE + LINE
MARGIN_CONN2 = " " + LATERAL   + "  "
MARGIN_CONN3 = " " + CROSSROAD + LINE + ">"
FIELD_SIZE   = 23

class PyR53CP:
    config = None

    def __init__(self, config):
        self.config = config
    
    def _print_there(self, x, y, text):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
        sys.stdout.flush()

    def nslookupEc2R53(self):
        r53api       = self.botoSession().client('route53')
        dnsName      = ""
        tableArgs    = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)
        thinForm     = False
        graphDisplay = False

        if "," in self.config.commandArguments:
           dnsName = self.config.commandArguments.split(",")[0]
           tableArgs.setArguments(self.config.commandArguments)
           if "thin" in self.config.commandArguments:
              thinForm = True
           elif "graph" in self.config.commandArguments:
              graphDisplay = True   
        else:    
           dnsName = tableArgs.cleanPipelineArguments()

        if not dnsName:
           resultTxt = "Where is the DNS? You didn't tell me which DNS to look for " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.NSLOOKUP_EC2_R53,resultTxt, self.config, "", True, tableArgs)

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

        if dnsName.endswith("."):
           dnsName = dnsName[:len(dnsName)-1]
        words = dnsName.split(".")

        w                 = ""
        pos               = len(words) - 1
        found             = False
        result            = {}
        result["dnsName"] = dnsName

        # Seek for the Hosted Zoned and the
        # ResourceRecordSet with the DNSName passed as entry paramater
        Utils.clearScreen()
        while pos >= 0 and not found:
            w = "." + words[pos] + w
            if pos < len(words) - 1:
               domain = w + "."    
               if domain.startswith("."):
                  domain = domain[1:]
               self._print_there(3, 1, "Searching \033[35m{} \033[0mat \033[32m{}\033[0m".format(dnsName, domain))
               listHostedZones = r53api.list_hosted_zones_by_name(DNSName=domain,MaxItems='1') 
               if listHostedZones and len(listHostedZones["HostedZones"]) > 0:
                  for hz in listHostedZones["HostedZones"]:
                      nextRecordName          = None
                      nextRecordType          = None
                      listResourceResourceSet = r53api.list_resource_record_sets(HostedZoneId=hz["Id"])
                      if "IsTruncated" in listResourceResourceSet and listResourceResourceSet["IsTruncated"] == True:
                          nextRecordName      = listResourceResourceSet["NextRecordName"]
                          nextRecordType      = listResourceResourceSet["NextRecordType"]

                      line  = 0
                      page  = 0
                      while listResourceResourceSet and len(listResourceResourceSet["ResourceRecordSets"]) > 0:
                            for rs in listResourceResourceSet["ResourceRecordSets"]:
                                line += 1
                                if dnsName in rs["Name"] and  rs["Type"] == "A": 
                                   self._print_there(4, 1, "--> Page {} \033[32m <-- Found it!\033[0m".format(page+1) )
                                   result["route53"] = {}
                                   result["route53"]["hostedZoneId"] = hz["Id"] 
                                   found = True
                                   if "ResourceRecords" in rs:
                                       result["route53"]["ResourceRecords"] = []
                                       for v in rs["ResourceRecords"]:
                                           result["route53"]["ResourceRecords"].append(v)
                                   if "AliasTarget" in rs:
                                      result["route53"]["AliasTarget"] = {}
                                      result["route53"]["AliasTarget"]["DNSName"] = rs["AliasTarget"]["DNSName"]
                                      result["route53"]["AliasTarget"]["Type"]    = rs["Type"]
                                   break
                            # Not Found and there's more page, keep searching...     
                            if not found and nextRecordName:
                               self._print_there(4, 1, "--> Page {}".format(page+1) + " ".ljust(80," "))
                               listResourceResourceSet = r53api.list_resource_record_sets(HostedZoneId=hz["Id"],StartRecordName=nextRecordName,StartRecordType=nextRecordType)
                               #Utils.saveDictAsJson("listResourceResourceSet",listResourceResourceSet)
                               if "IsTruncated" in listResourceResourceSet and listResourceResourceSet["IsTruncated"] == True:
                                   nextRecordName = listResourceResourceSet["NextRecordName"]
                                   nextRecordType = listResourceResourceSet["NextRecordType"]
                                   page += 1
                               else:
                                   nextRecordName = None
                                   nextRecordType = None
                            else:
                               break        
               else:
                  print("nothing found for \033[32m{domain}\033[0m".format(domain=domain))       
            pos -= 1

        if found:
           # Found Hosted Zoned and ResourceRecordset
           # In case DNSName of a Load Balance
           if "AliasTarget" in result["route53"]:
              elbv2Api     = self.botoSession().client('elbv2')
              loadBalancers = elbv2Api.describe_load_balancers()
              for lb in loadBalancers["LoadBalancers"]:
                 if lb["DNSName"] in result["route53"]["AliasTarget"]["DNSName"]:
                    result["elb"] = {}
                    result["elb"]["DNSName"]           = lb["DNSName"]
                    result["elb"]["AvailabilityZones"] = lb["AvailabilityZones"]
                    result["elb"]["LoadBalancerArn"]   = lb["LoadBalancerArn"]
                    result["elb"]["LoadBalancerName"]  = lb["LoadBalancerName"]
                    result["elb"]["Scheme"]            = lb["Scheme"]
                    result["elb"]["Type"]              = lb["Type"]
                    result["elb"]["VpcId"]             = lb["VpcId"]
                    result["elb"]["State"]             = lb["State"]
                    result["elb"]["SecurityGroups"]    = lb["SecurityGroups"]
                    result["elb"]["CreatedTime"]       = lb["CreatedTime"]
                    # Check For Existent Listener Rules
                    elbListeners  = elbv2Api.describe_listeners(LoadBalancerArn=result["elb"]["LoadBalancerArn"])
                    result["elb"]["TotalListeners"] = len(elbListeners)
                    result["elb"]["Listeners"]      = []
                    for elbListener in elbListeners["Listeners"]:
                        objDefaultActions = []
                        for defaultAction in elbListener["DefaultActions"]:
                            objRedirectConfig = None
                            if "RedirectConfig" in defaultAction:
                                objRedirectConfig = {
                                   "Protocol":defaultAction["RedirectConfig"]["Protocol"],
                                   "Port":defaultAction["RedirectConfig"]["Port"],
                                   "Host":defaultAction["RedirectConfig"]["Host"],
                                   "Path":defaultAction["RedirectConfig"]["Path"],
                                   "Query":defaultAction["RedirectConfig"]["Query"],
                                   "StatusCode":defaultAction["RedirectConfig"]["StatusCode"]
                                }
                            objDefaultAction = {
                               "Type":defaultAction["Type"],
                               "Order":defaultAction["Order"] if "Order" in defaultAction else ""
                            }    
                            if "TargetGroupArn" in defaultAction:
                               objDefaultAction["TargetGroupArn"] = defaultAction["TargetGroupArn"]
                            if objRedirectConfig:
                               objDefaultAction["RedirectConfig"] = objRedirectConfig
                            objDefaultActions.append(objDefaultAction)    
                        objListener = {
                           "ListenerArn": elbListener["ListenerArn"],
                           "LoadBalancerArn": elbListener["LoadBalancerArn"],
                           "Port": elbListener["Port"],
                           "Protocol": elbListener["Protocol"],
                           "DefaultActions": objDefaultActions
                        }

                        elbListenersRules = elbv2Api.describe_rules(ListenerArn=elbListener["ListenerArn"])
                        objListenerRules  = []
                        for elbListenerRule in elbListenersRules["Rules"]:
                            # Add CONDITIONS
                            conditions = []
                            if "Conditions" in elbListenerRule:
                               for condition in elbListenerRule["Conditions"]:
                                   conditions.append({
                                      "Field": condition["Field"],
                                      "Values": condition["Values"]
                                   })
                            # Add ACTIONS
                            actions = []
                            if "Actions" in elbListenerRule:
                               for action in elbListenerRule["Actions"]:
                                   actions.append({
                                      "Type": action["Type"],
                                      "TargetGroupArn": action["TargetGroupArn"] if "TargetGroupArn" in action else None,
                                      "Order": action["Order"] if "Order" in action else "",
                                   })
                            objListenerRule = {
                               "RuleArn": elbListenerRule["RuleArn"],
                               "Priority": elbListenerRule["Priority"],
                               "IsDefault": elbListenerRule["IsDefault"],
                               "Conditions": conditions,
                               "Actions": actions
                            }
                            objListenerRules.append(objListenerRule)

                        objListener["ListenerRules"] = objListenerRules
                        result["elb"]["Listeners"].append(objListener)
                    break
              
              target_groups = elbv2Api.describe_target_groups(LoadBalancerArn=result["elb"]["LoadBalancerArn"])
              result["targetGroup"] = []
              for tg in target_groups["TargetGroups"]:
                  t = {
                     "TargetGroupArn":tg["TargetGroupArn"],
                     "TargetGroupName":tg["TargetGroupName"],
                     "HealthCheckPath":tg["HealthCheckPath"],
                     "HealthCheckPort":tg["HealthCheckPort"],
                     "HealthCheckIntervalSeconds":tg["HealthCheckIntervalSeconds"],
                     "Port":tg["Port"],
                     "Protocol":tg["Protocol"],
                     "TargetType":tg["TargetType"],
                     "Targets": []
                  }
                  result["targetGroup"].append(t)

              ec2Api = self.botoSession().client('ec2')   
              for tg in result["targetGroup"]:
                  targetGroupHealth = elbv2Api.describe_target_health(TargetGroupArn=tg["TargetGroupArn"])
                  for tgh in targetGroupHealth["TargetHealthDescriptions"]:
                      id           = tgh["Target"]["Id"]    if ("Target"          in tgh and "Id"   in tgh["Target"]) else ""
                      port         = tgh["Target"]["Port"]  if ("Target"          in tgh and "Port" in tgh["Target"]) else ""
                      portHealth   = tgh["HealthCheckPort"] if ("HealthCheckPort" in tgh) else ""
                      descHealth   = tgh["TargetHealth"]["Description"]if ("TargetHealth" in tgh and "Description" in tgh["TargetHealth"]) else ""
                      reasonHealth = tgh["TargetHealth"]["Reason"]     if ("TargetHealth" in tgh and "Reason"      in tgh["TargetHealth"]) else ""

                      # Now, grab the rest of information about the Instance (IP, etc.) 
                      # in the ec2-describe-instance(InstanceIds="i-0c97d7df9ad273ee2 i-0c97d7df9ad273ee2")
                      privateIp       = ""
                      instanceType    = ""
                      privateDnsName  = ""
                      publicDnsName   = ""
                      securityGroups  = {}
                      state           = {}
                      subnetId        = ""
                      if id:
                         reservations = ec2Api.describe_instances(InstanceIds=[id])
                         for reservation in reservations["Reservations"]:
                            for instance in reservation["Instances"]:
                               if instance["InstanceId"] == id:
                                  privateIp       = instance["PrivateIpAddress"]
                                  instanceType    = instance["InstanceType"]
                                  privateDnsName  = instance["PrivateDnsName"]
                                  publicDnsName   = instance["PublicDnsName"]
                                  securityGroups  = instance["SecurityGroups"]
                                  state           = instance["State"]
                                  subnetId        = instance["SubnetId"]
                                  break

                         #print(highlight(Utils.dictToJson(ec2Info), lexers.JsonLexer(), formatters.TerminalFormatter()))      

                      target = {
                        "Id": id,
                        "Port": port,
                        "PrivateIpAddress": privateIp,
                        "InstanceType":instanceType,
                        "PrivateDnsName":privateDnsName,
                        "PublicDnsName":publicDnsName,
                        "SecurityGroups":securityGroups,
                        "State":state,
                        "SubnetId":subnetId,
                        "health": {
                           "Port": portHealth,
                           "Description": descHealth,
                           "Reason": reasonHealth
                        }
                      }
                      tg["Targets"].append(target)

           #print(highlight(Utils.dictToJson(result), lexers.JsonLexer(), formatters.TerminalFormatter()))      
           #print("\n----------------------------------------------------------------------------")   

           jsonResult = ""
           if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
              jsonResult = Utils.dictToJson(result)

           tree       = {}
           formResult = None
           if thinForm:
              formResult = self._buildSummaryForm(dnsName, result)
           elif graphDisplay:
              tree["root"] = {}
              tree["root"]["dnsName"] = result["dnsName"]
              tree["root"]["children"] = []
              
              if "elb" in result:
                 groupListeners = []
                 for objListeners in result["elb"]["Listeners"]:
                     listener = {}
                     listener["label"]    = "Listener"
                     listener["Port"]     = objListeners["Port"]
                     listener["Protocol"] = objListeners["Protocol"]
                     listener["children"] = []

                     groupListenerRules = []
                     for objDefaultActions in objListeners["DefaultActions"]:
                         listenerRule               = {}
                         listenerRule["label"]      = "Rule"
                         listenerRule["Type"]       = objDefaultActions["Type"]

                         if objDefaultActions["Type"] == "redirect" and ("RedirectConfig" in objDefaultActions and objDefaultActions["RedirectConfig"] != ""):
                            listenerRule["Rule"] = "{}://{}:{}{}{}".format(objDefaultActions["RedirectConfig"]["Protocol"],objDefaultActions["RedirectConfig"]["Host"],objDefaultActions["RedirectConfig"]["Port"],objDefaultActions["RedirectConfig"]["Path"],objDefaultActions["RedirectConfig"]["Query"])
                            groupListenerRules.append(listenerRule)
                         #elif objDefaultActions["Type"] == "forward":   
                         #   listenerRule["TargetGroupArn"] = objDefaultActions["TargetGroupArn"]
                         #   groupListenerRules.append(listenerRule)

                     for objListenerRules in objListeners["ListenerRules"]:
                         listenerRule = {}
                         listenerRule["label"] = "Rule"
                         if "IsDefault" in objListenerRules and objListenerRules["IsDefault"]:
                             listenerRule["IsDefault"] = True
                         for objActions in objListenerRules["Actions"]:
                             listenerRule["Type"]           = objActions["Type"]
                             listenerRule["TargetGroupArn"] = objActions["TargetGroupArn"]
                             listenerRule["children"]       = []
                             for targetGroup in result["targetGroup"]:
                                 if targetGroup["TargetGroupArn"] == objActions["TargetGroupArn"]:
                                    tgs = []
                                    for target in targetGroup["Targets"]:
                                       tgs.append({
                                          "label":"Target",
                                          "PrivateIpAddress":target["PrivateIpAddress"],
                                          "Id":target["Id"] if "Id" in target else "",
                                          "SubnetId":target["SubnetId"],
                                          "Port":target["Port"],
                                          "InstanceType":target["InstanceType"],
                                       })
                                    tGroup = {
                                       "label":"TargetGroup",
                                       "TargetGroupName":targetGroup["TargetGroupName"],
                                       "Protocol":targetGroup["Protocol"],
                                       "Port":targetGroup["Port"],
                                       "children": tgs
                                    }
                                    listenerRule["children"].append(tGroup)
                                    break
                         listenerRule["Condition"] = ""     
                         for objConditions in objListenerRules["Conditions"]:   
                             if len(listenerRule["Condition"]) > 0:
                                listenerRule["Condition"] += " AND "
                             listenerRule["Condition"] += objConditions["Field"] + " = " + str(objConditions["Values"])
                         if listenerRule["Type"] != "redirect" or listenerRule["Condition"] != "":
                            groupListenerRules.append(listenerRule)  

                     listener["children"] = groupListenerRules
                     groupListeners.append(listener)  
                 elb = {
                    "label":"ELB",
                    "LoadBalancerName":result["elb"]["LoadBalancerName"],
                    "children": groupListeners
                 }
                 route53 = {
                    "label": "Route53",
                    "DNSName": result["route53"]["AliasTarget"]["DNSName"],
                    "hostedZoneId": result["route53"]["hostedZoneId"],
                    "children": []
                 }
                 route53["children"].append(elb)
                 tree["root"]["children"].append(route53)
              # No ELB, A Direct IP(s) Assigned   
              elif "ResourceRecords" in result["route53"]:
                 records = []
                 for record in result["route53"]["ResourceRecords"]:
                    records.append({
                       "Value":record["Value"]
                    })
                 route53 = {
                    "label": "Route53",
                    "hostedZoneId": result["route53"]["hostedZoneId"],
                    "children": records
                 }   
                 tree["root"]["children"].append(route53)

              #pathToResources = "./pymxgraph"
              pathToResources = "./"
              pymxGraph = PymxGraph(pathToResources)
              pymxGraphTree = PymxGraphTree(pathToResources, pymxGraph.images, pymxGraph.htmlSnippets)

              #Utils.addToClipboard(Utils.dictToJson(tree))
              #print(highlight(Utils.dictToJson(tree), lexers.JsonLexer(), formatters.TerminalFormatter()))
              
              nodes         = ""
              indexNodeR53  = 0
              for childR53 in tree["root"]["children"]:
                  indexNodeR53 += 1
                  label = "<b>" + childR53["label"] + " </b><br> " + childR53["hostedZoneId"].replace("/hostedzone/","")
                  nodes += "var v{indexR53} = graph.insertVertex(parent, 'v{indexR53}', '{lbl}', 0, 0, widthLeaf, heightLeaf,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,lbl=label)
                  nodes += "graph.insertEdge(parent, null, '', root, v{indexR53});".format(indexR53=indexNodeR53)

                  indexNodeELB = 0
                  for childELB in childR53["children"]:
                     indexNodeELB += 1
                     label = "<b>" + childELB["label"] + " </b><br> " + childELB["LoadBalancerName"]
                     nodes += "var v{indexR53}{indexELB} = graph.insertVertex(parent, 'v{indexR53}{indexELB}', '{lbl}', 0, 0, widthLeaf, heightLeaf,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,lbl=label)
                     nodes += "graph.insertEdge(parent, null, '', v{indexR53}, v{indexR53}{indexELB});".format(indexR53=indexNodeR53,indexELB=indexNodeELB)

                     indexNodeListener = 0
                     for childListener in childELB["children"]:
                         indexNodeListener += 1
                         label  = "<b>" + childListener["label"] + "</b><br>{}:{}".format(childListener["Protocol"],childListener["Port"])
                         nodes += "var v{indexR53}{indexELB}{indexListener} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}', '{lbl}', 0, 0, 200, heightLeaf,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,lbl=label)
                         nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}, v{indexR53}{indexELB}{indexListener});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener)

                         indexNodeListenerRule = 0
                         for childListenerRule in childListener["children"]:
                            indexNodeListenerRule += 1
                            label = "<b>{}</b><br><i>{}</i>".format(childListenerRule["label"],childListenerRule["Type"])
                            if "IsDefault" in childListenerRule and childListenerRule["IsDefault"]:
                                label += "<br>{}".format("Default")
                            else:
                                label += "<br>"
                            if childListenerRule["Type"] == "redirect":
                               if "Rule" in childListenerRule:
                                  label += childListenerRule["Rule"]
                               if "Condition" in childListenerRule and childListenerRule["Condition"] != "":
                                  label += childListenerRule["Condition"].replace("'","\\'")
                            elif childListenerRule["Type"] == "forward":
                               if "Condition" in childListenerRule and childListenerRule["Condition"] != "":
                                  label += childListenerRule["Condition"].replace("'","\\'")
                            nodes += "var v{indexR53}{indexELB}{indexListener}{indexListenerRule} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}{indexListenerRule}', '{lbl}', 0, 0, 200, heightLeaf + 30,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,lbl=label)
                            nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}{indexListener}, v{indexR53}{indexELB}{indexListener}{indexListenerRule});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule)      
                            
                            if "children" in childListenerRule:
                               indexNodeTargetGroup = 0   
                               for childTargetGroup in childListenerRule["children"]:
                                  indexNodeTargetGroup += 1
                                  label  = "<b>" + childTargetGroup["label"] + "</b><br> " + childTargetGroup["TargetGroupName"] + " <br> " + "{}:{}".format(childTargetGroup["Protocol"],childTargetGroup["Port"])
                                  nodes += "var v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}', '{lbl}', 0, 0, 200, heightLeaf + 5,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup,lbl=label)
                                  nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}{indexListener}{indexListenerRule}, v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup)
      
                                  indexNodeTarget = 0
                                  for childTarget in childTargetGroup["children"]:
                                     indexNodeTarget += 1
                                     label  = "<b>" + childTarget["label"] + " </b><br> " + childTarget["PrivateIpAddress"] 
                                     if "Id" in childTarget:
                                         label += " <br> " + childTarget["Id"]
                                     if "InstanceType" in childTarget:
                                         label += " <br> " + childTarget["InstanceType"]    
                                     if "SubnetId" in childTarget:
                                         label += " <br> " + childTarget["SubnetId"]
                                     nodes += "var v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}{indexTarget} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}{indexTarget}', '{lbl}', 0, 0, 200, 85,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup,indexTarget=indexNodeTarget,lbl=label)
                                     nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}, v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}{indexTarget});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup,indexTarget=indexNodeTarget)
              
              str_tree = """
                            var widthLeaf  = 200;
                            var heightLeaf = 50;

                            var w = graph.container.offsetWidth;
                            var root = graph.insertVertex(parent, 'treeRoot', '"""+ tree["root"]["dnsName"] + """', w/2 - 30, 20, 250, heightLeaf,'whiteSpace=wrap;');

                            """ + nodes + """
                           
                            //toggleSubtree(graph, v2, false);
                            //graph.model.setCollapsed(v2, true);
              """
              
              pymxGraphTree.drawTree(str_tree)
           else:   
              formResult = self._buildCompleteForm(dnsName, result)

           Utils.clearScreen()
           if formResult:
              return Utils.formatResult(Functions.FUNCTIONS[Functions.NSLOOKUP_EC2_R53]["name"], formResult, self.config, jsonResult, False, tableArgs)
           else:
              if graphDisplay:
                 resultTxt = "  " + Emoticons.thumbsUp() + " The graphic for {} should be \n     opened in external browser window".format(Style.IBLUE + dnsName + Style.RESET) 
                 return Utils.formatResult(Functions.FUNCTIONS[Functions.NSLOOKUP_EC2_R53]["name"],resultTxt, self.config, jsonResult, False, tableArgs)
              else:
                 return ""   
        else:   
           Utils.clearScreen()
           resultTxt = "  " + Emoticons.ops() + " Nothing was found for the DNSName " + Style.IBLUE + dnsName + Style.RESET
           return Utils.formatResult(Functions.NSLOOKUP_EC2_R53,resultTxt, self.config, "", False, tableArgs)

    def _buildCompleteForm(self, dnsName, result):
         asciiForm     = ""
         lineSeparator = MARGIN + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         lineEmtpy     = MARGIN + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm    += lineSeparator
         asciiForm    += lineEmtpy                    
         # DNS Name Seeked
         line           = MARGIN_CONN1 + LATERAL + Style.IYELLOW + "  " + dnsName + Style.RESET
         asciiForm     += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
         lineEmtpy2     = MARGIN_CONN2 + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm     += lineEmtpy2
         lineSeparator2 = MARGIN_CONN2 + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         asciiForm     += lineSeparator2
         # Route 53
         asciiForm    += self._buildHeader(MARGIN_CONN3, "ROUTE R53")
         if "AliasTarget" in result["route53"]:
             asciiForm    += lineSeparator2
             asciiForm    += lineEmtpy2
             asciiForm    += self._buildLine(MARGIN_CONN2, "DNS Name", result["route53"]["AliasTarget"]["DNSName"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Type", result["route53"]["AliasTarget"]["Type"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Hosted Zone Id", result["route53"]["hostedZoneId"])
             asciiForm    += lineEmtpy2
             asciiForm    += lineSeparator2
             # ELB
             asciiForm    += self._buildHeader(MARGIN_CONN3, "ELB")
             asciiForm    += lineSeparator2
             asciiForm    += self._buildLine(MARGIN_CONN2, "Name", result["elb"]["LoadBalancerName"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "DNS Name", result["elb"]["DNSName"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "ARN", result["elb"]["LoadBalancerArn"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Create At", result["elb"]["CreatedTime"].strftime("%Y%m%d-%H%M%S"))
             asciiForm    += self._buildLine(MARGIN_CONN2, "Scheme", result["elb"]["Scheme"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Type", result["elb"]["Type"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Vpc Id", result["elb"]["VpcId"])
             asciiForm    += lineEmtpy2
    
             # AZs 
             line          = MARGIN_CONN2 + LATERAL + Style.BLUE + "  AVAILABILITY ZONES ({:02d})".format(len(result["elb"]["AvailabilityZones"])) + Style.RESET
             asciiForm    += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
             for az in result["elb"]["AvailabilityZones"]:
                asciiForm += self._buildLineSubItemHeader(MARGIN_CONN2,az["ZoneName"], az["SubnetId"])
             asciiForm    += lineEmtpy2 
             
             # Listeners 
             line       = MARGIN_CONN2 + LATERAL + Style.BLUE + "  LISTENERS ({:02d})".format(len(result["elb"]["Listeners"])) + Style.RESET
             asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
             for listener in result["elb"]["Listeners"]:
                asciiForm += self._buildLineSubItemHeader(MARGIN_CONN2,"Listener",listener["ListenerArn"])
                asciiForm += self._buildLineSubItem(MARGIN_CONN2,"Protocol / Port",listener["Protocol"] + " / " + str(listener["Port"]))
    
                if "DefaultActions" in listener:
                   asciiForm += self._addLine(MARGIN_CONN2, Style.BLUE + "     DEFAULT ACTIONS" + Style.RESET)
                   for defaultAction in listener["DefaultActions"]:
                      asciiForm += self._buildLineSubItemHeaderSecondLevel(MARGIN_CONN2, "Type", defaultAction["Type"])
                      asciiForm += self._buildLineSubItemSecondLevel(MARGIN_CONN2, "Order", str(defaultAction["Order"]))
                      if "RedirectConfig" in defaultAction:
                            label = "{}://{}:{}/{}?{} -- (Status Code: {})".format(defaultAction["RedirectConfig"]["Protocol"],defaultAction["RedirectConfig"]["Host"],defaultAction["RedirectConfig"]["Port"],defaultAction["RedirectConfig"]["Path"],defaultAction["RedirectConfig"]["Query"],defaultAction["RedirectConfig"]["StatusCode"])
                            asciiForm += self._buildLineSubItemSecondLevel(MARGIN_CONN2, "Redirect Config", label)
                      if "TargetGroupArn" in defaultAction:
                            asciiForm += self._buildLineSubItemSecondLevel(MARGIN_CONN2, "Target Group", str(defaultAction["TargetGroupArn"]))    
    
                if "ListenerRules" in listener:
                   asciiForm += self._addLine(MARGIN_CONN2, Style.BLUE + "     LISTENER RULES ({:02d})".format(len(listener["ListenerRules"])) + Style.RESET)
                   for rule in listener["ListenerRules"]:
                      asciiForm += self._buildLineSubItemHeaderSecondLevelTitle(MARGIN_CONN2, "RULE --> Priority \033[94m{}\033[0m".format(rule["Priority"]))
    
                      labelCondition = None
                      if "Conditions" in rule:
                         for condition in rule["Conditions"]:
                               labelCondition = "       \033[34mIF\033[32m {} \033[34m==\033[32m {} \033[34mTHEN\033[32m".format(condition["Field"],condition["Values"])
    
                      labelActions1 = None
                      labelActions2 = None
                      if "Actions" in rule:
                         for action in rule["Actions"]:
                               labelActions1     = "          {} \033[34m{}\033[34m".format(action["Type"],"TO" if action["TargetGroupArn"] else "")
                               if action["TargetGroupArn"]:
                                  labelActions2  = "          \033[32m{}\033[34m".format(action["TargetGroupArn"])
    
                      if labelCondition:
                         asciiForm += self._buildLine(MARGIN_CONN2, None, labelCondition)       
                      if labelActions1:   
                         asciiForm += self._buildLine(MARGIN_CONN2, None, labelActions1)   
                      if labelActions2:   
                         asciiForm += self._buildLine(MARGIN_CONN2, None, labelActions2)   

         if "targetGroup" in result:
            asciiForm      += lineEmtpy2
            asciiForm      += lineSeparator2
            margin          = MARGIN_CONN2
            idxTargetGroups = len(result["targetGroup"])
            # TARGET GROUPS
            asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUPS ({:02d})".format(idxTargetGroups))
            asciiForm    += lineSeparator2
            index = 0
            for targetGroup in result["targetGroup"]:
               index += 1
               if index == idxTargetGroups:
                  margin = MARGIN
               asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUP ({:02d})".format(index))
               asciiForm += self._buildLine(margin, "\033[37m•\033[94m Name", targetGroup["TargetGroupName"]) 
               asciiForm += self._buildLine(margin, "  ARN", targetGroup["TargetGroupArn"]) 
               asciiForm += self._buildLine(margin, "  Type", targetGroup["TargetType"]) 
               asciiForm += self._buildLine(margin, "  Protocol / Port","{} / {}".format(targetGroup["Protocol"], targetGroup["Port"])) 
               line       = margin + LATERAL + Style.BLUE + "    HEALTH CHECK" + Style.RESET
               asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
               asciiForm += self._buildLineSubItem(margin,"  Interval Seconds", "{:02d}".format(targetGroup["HealthCheckIntervalSeconds"]))
               asciiForm += self._buildLineSubItem(margin,"  Path", targetGroup["HealthCheckPath"])
               asciiForm += self._buildLineSubItem(margin,"  Port", targetGroup["HealthCheckPort"])
                  
               totalTargets = len(targetGroup["Targets"])
               asciiForm += self._addLine(margin, Style.BLUE + "    TARGETS ({:02d})".format(totalTargets) + Style.RESET) 
               for target in targetGroup["Targets"]:
                     asciiForm += self._buildLineSubItemHighlighted(margin,"\033[37m•\033[94m Instance Id", target["Id"])
                     asciiForm += self._buildLineSubItem(margin,"  Instance Type", target["InstanceType"])
                     asciiForm += self._buildLineSubItem(margin,"  Port", "{}".format(target["Port"]))
                     asciiForm += self._buildLineSubItem(margin,"  Private IP", target["PrivateIpAddress"])
                     asciiForm += self._buildLineSubItem(margin,"  Private DNS Name", target["PrivateDnsName"])
                     asciiForm += self._buildLineSubItem(margin,"  Public DNS Name", target["PublicDnsName"])
                     asciiForm += self._buildLineSubItem(margin,"  State", target["State"]["Name"])
                     asciiForm += self._buildLineSubItem(margin,"  Subnet Id", target["SubnetId"])
                     line       = margin + LATERAL + Style.BLUE + "       SECURITY GROUPS ({:02d})".format(len(target["SecurityGroups"])) + Style.RESET
                     asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
                     for sg in target["SecurityGroups"]:
                        asciiForm += self._buildLineSubItem(margin,"  \033[37m•\033[94m Group Id", sg["GroupId"])
                        asciiForm += self._buildLineSubItem(margin,"    Group Name", sg["GroupName"])
                     line       = margin + LATERAL + Style.BLUE + "       HEALTH" + Style.RESET
                     asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
                     asciiForm += self._buildLineSubItem(margin,"    Port", "{}".format(target["health"]["Port"]))
                     asciiForm += self._buildLineSubItem(margin,"    Description", target["health"]["Description"])
                     asciiForm += self._buildLineSubItem(margin,"    Reason", target["health"]["Reason"])
               asciiForm    += margin + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 

         if "ResourceRecords" in result["route53"]:
            asciiForm   += lineSeparator
            asciiForm   += lineEmtpy
            asciiForm   += self._buildLine(MARGIN, "  Hosted Zoned Id", result["route53"]["hostedZoneId"])
            totalRecords = len(result["route53"]["ResourceRecords"])
            line         = MARGIN + LATERAL + Style.BLUE + "    RECORDS ({:02d})".format(totalRecords) + Style.RESET
            asciiForm   += line + self._calculateRemainingSpace(line) + LATERAL + "\n" 
            for records in result["route53"]["ResourceRecords"]:
               asciiForm += self._buildLineSubItem(MARGIN,"  Value", "{}".format(records["Value"]))
            asciiForm    += lineEmtpy

         asciiForm += lineSeparator
         return asciiForm

    def _buildSummaryForm(self, dnsName, result):
         asciiForm     = ""
         lineSeparator = MARGIN + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         lineEmtpy     = MARGIN + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm    += lineSeparator
         asciiForm    += lineEmtpy                    
         # DNS Name Seeked
         line           = MARGIN_CONN1 + LATERAL + Style.IYELLOW + "  " + dnsName + Style.RESET
         asciiForm     += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
         lineEmtpy2     = MARGIN_CONN2 + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm     += lineEmtpy2
         lineSeparator2 = MARGIN_CONN2 + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         asciiForm     += lineSeparator2
         # Route 53
         asciiForm    += self._buildHeader(MARGIN_CONN3, "ROUTE R53")
         asciiForm    += lineSeparator2
         asciiForm    += lineEmtpy2
         asciiForm    += self._buildLine(MARGIN_CONN2, "DNS Name", result["route53"]["AliasTarget"]["DNSName"])
         asciiForm    += lineEmtpy2
         asciiForm    += lineSeparator2
         # ELB
         asciiForm    += self._buildHeader(MARGIN_CONN3, "ELB")
         asciiForm    += lineSeparator2
         asciiForm    += lineEmtpy2
         asciiForm    += self._buildLine(MARGIN_CONN2, "Name", result["elb"]["LoadBalancerName"])
         asciiForm    += lineEmtpy2
         
         asciiForm      += lineSeparator2
         margin          = MARGIN_CONN2
         idxTargetGroups = len(result["targetGroup"])
         # TARGET GROUPS
         asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUPS ({:02d})".format(idxTargetGroups))
         asciiForm    += lineSeparator2
         index = 0
         for targetGroup in result["targetGroup"]:
            index += 1
            if index == idxTargetGroups:
               margin = MARGIN
            asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUP ({:02d})".format(index))
            asciiForm += self._buildLine(margin, "\033[37m•\033[94m Name", targetGroup["TargetGroupName"]) 
            
            totalTargets = len(targetGroup["Targets"])
            asciiForm += self._addLine(margin, Style.BLUE + "    TARGETS ({:02d})".format(totalTargets) + Style.RESET) 
            for target in targetGroup["Targets"]:
                  asciiForm += self._buildLineSubItemHighlighted(margin,"\033[37m•\033[94m Instance Id", target["Id"])
                  asciiForm += self._buildLineSubItem(margin,"  Port", "{}".format(target["Port"]))
                  asciiForm += self._buildLineSubItem(margin,"  Private IP", target["PrivateIpAddress"])
                  asciiForm += self._buildLineSubItem(margin,"  State", target["State"]["Name"])
            asciiForm    += margin + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 

         asciiForm += lineSeparator
         return asciiForm     

    def _builAsciiGraph(self, dnsName, result):
        pygraph = PyAsciiGraphs()
        leafR53 = Leaf(dnsName)
        leafELB = Leaf("ELB: " + result["elb"]["LoadBalancerName"])
        leafR53.add(leafELB)
        for targetGroup in result["targetGroup"]:
            leafTargetGroup = Leaf(targetGroup["TargetGroupName"])
            for target in targetGroup["Targets"]:
                leafTarget = Leaf(target["Id"])
                leafTargetGroup.add(leafTarget)
            leafELB.add(leafTargetGroup)
               
        pygraph.drawTree(leafR53)

    def _buildHeader(self, margin, label):
        line  = margin + LATERAL + "  " + Style.GREEN + label + Style.RESET
        spaces        = self._calculateRemainingSpace(line) 
        return line + spaces + LATERAL + "\n"

    def _buildLineSubItemHeader(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-3) - len(Utils.removeCharsColors(label)),".") + ": "
        line = MARGIN_CONN2 + LATERAL + "   " + "• " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"
    def _buildLineSubItem(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-3) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "   " + "  " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"
    def _buildLineSubItemHighlighted(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-3) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "   " + "  " + Style.IBLUE + label + Style.RESET + suffix + Style.IYELLOW + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"    

    def _buildLineSubItemHeaderSecondLevel(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-6) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "    " + "  • " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"        
    def _buildLineSubItemHeaderSecondLevelTitle(self, margin, label):
        line = margin + LATERAL + "    " + "  • " + Style.BLUE + label + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"            
    def _buildLineSubItemSecondLevel(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-6) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "    " + "    " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"

    def _buildLine(self, margin, label, value):
        if label:
           suffix = ".".ljust(FIELD_SIZE - len(Utils.removeCharsColors(label)),".") + ": "
           line  = margin + LATERAL + "  " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET 
        else:  
           line  = margin + LATERAL + "  " + Style.GREEN + value + Style.RESET 
        spaces = self._calculateRemainingSpace(line) 
        return line + spaces + LATERAL + "\n"

    def _addLine(self,margin,line):
        spaces = self._calculateRemainingSpace(margin + LATERAL + line)
        return margin + LATERAL + line + spaces + LATERAL + "\n"
    def _calculateRemainingSpace(self, line):
        spaces = (len(MARGIN) + len(LATERAL) + FORM_WIDTH) - len(Utils.removeCharsColors(line))
        return " ".ljust(spaces, " ")
        
    def botoSession(self):
        return self.config.botoSession()

if __name__ == '__main__':
    config = Config()
    config.awsProfile   = "ecomm"
    config.awsRegion    = "eu-central-1"
    config.printResults = True
    #config.awsTags["Environment"] = "production"
    config.tableLineSeparator = False
    
    # python pyr53cp.py services.preprod.aps2.aws.emagin.eu
    # python pyr53cp.py onepay-services.uat.euc1.emagin.cloud.allianz
    # python pyr53cp.py jenkins.cicd.prod.emagin.cloud.allianz
    # python pyr53cp.py bux.uat.euc1.emagin.cloud.allianz
    # python PyR53Cp.py artifactory.cicd.prod.aws.emagin.eu <-- with Rules
    # python PyR53Cp.py magroup-webservice.uat.aws.emagin.eu
    # python PyR53Cp.py rdstest.uat.euc1.emagin.cloud.allianz  <-- Example Direct IP, no Load Balancer

    # aws elbv2 describe-rules --listener-arn arn:aws:elasticloadbalancing:eu-central-1:659915611011:listener/app/tf-lb-20200529110151957200000006/4d10ad47be839fbf/ef91534c7811e537 --profile ecomm --region eu-central-1env
    if len(sys.argv) > 1:
       config.commandArguments = sys.argv[1]
    pyr53CP = PyR53CP(config)
    report = pyr53CP.nslookupEc2R53()
    if report: 
       Utils.addToClipboard(report)
       print(report)

#def templateForTests(self):
#    ec2 = self.botoSession().client('ec2')
#    filters = []
#    if self.config.awsTagsToFilter():
#       for tag in self.config.awsTags: 
#           filters.append(
#               {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
#           )
#    vpcs = ec2.describe_vpcs(Filters=filters)
#
#    jsonResult = ""
#    if self.config.printResults: 
#       jsonResult = Utils.dictToJson(vpcs)
#    colorful_json = highlight(jsonResult, lexers.JsonLexer(), formatters.TerminalFormatter())
#    #print(colorful_json)    