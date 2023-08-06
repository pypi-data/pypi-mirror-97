import webbrowser
import os, sys
import threading
import pathlib
import logging

from pyawscp.pymxgraph.HttpServer import HttpServer
sys.path.append('..')
from pyawscp.Utils import Utils
from pyawscp.Emoticons import Emoticons

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

class PymxGraphAwsNavigator:

    def __init__(self, pathToResources, images, htmlSnippets, verbose=False):
        self.pathToResources = pathToResources
        self.images          = images
        self.htmlSnippets    = htmlSnippets
        self.verbose         = verbose
        self.httpServer      = None

    def startHttpServer(self):
        self.httpServer = HttpServer(self.verbose)
        self.httpServer.run()

    def stopHttpServer(self):
        self.httpServer.stop()

    def openHTML(self,html):
        directory = os.path.dirname(os.path.realpath(__file__))
        fileName  = os.path.join(str(directory),"aws-navigator.html")
        
        try:
            os.remove(fileName)
        except OSError:
            pass

        with open(fileName, "w") as file:
            file.write(html)
        webbrowser.open('file://' + os.path.realpath(fileName))   

    def drawAwsNavigator(self):
        html = """
        <html>
          <head>
             """ + self.htmlSnippets.htmlTitle('Hi There!') + """
             """ + self.htmlSnippets.jsLibraries()          + """
             <style type="text/css">
                .modalInfo {
                    position: absolute;
                    display: block;
                    top: 200px;
                    left: 200px;
                    background: rgb(245, 245, 245);
                    //width: 350px;
                    //height: 250px;
                    padding: 5px;
                    font-size: 0.875rem;
                    box-shadow: 0 0 2.5rem rgba(0, 0, 0, 0.5);
                    border-radius: 0.3125rem;
                    font-family: 'Source Sans Pro', sans-serif
                }
                .content {
                    font-size: 0.8rem;
                    font-family: 'Consolas', sans-serif
                }
                .tag {
                    border: 1.4px solid darkcyan;
                    padding: 3px;
                    border-radius: 8px;
                    background-color:rgb(0,220,220);
                    color:black;
                    display:inline;
                    font-size: 12px;
                }
                .tableInfo {
                    font-family: Consolas;
                    font-size: 13px;
                    border: 2px solid darkcyan;
                    padding: 0;
                    border-radius: 8px;
                }
                .cellHeader {
                    border-bottom: 1.5px darkcyan solid;
                    font-size: 15px;
                    font-weight: bold;
                    background-color: darkcyan;
                }
                .cellInfo {
                    padding: 10px 8px 10px 8px;
                }
                .cellTags {
                    border-top: 1.5px darkcyan solid;
                    padding: 8px 8px 15px 8px;
                }
                .buttonCopyClipboard {
                    margin-bottom: -3px;
                }
             </style>
             <script type="text/javascript">

                 """ + self.htmlSnippets.jsDataURIForImage()    + """
                 
                 var requestId   = 0;

                 const Http             = new XMLHttpRequest();
                 const url              = '"""+ self.htmlSnippets.serverURL +"""';
                 var   previousGraphXml = [];
                 var   previousCoord    = {"x":0, "y":0};

                 function moveMe(graph, cellId, valueX, valueY, addToIt) {
                    if ( graph.view.getScale() == 1 ) { 
                        try
                        {
                            var v1 = graph.getModel().getCell(cellId); 
                            graph.clearSelection();
                            graph.getModel().beginUpdate(); 
                            var geo = graph.getCellGeometry(v1);
                            geo  = geo.clone();

                            previousCoord.x = geo.x;
                            previousCoord.y = geo.y;
                            
                            if ( addToIt ) {
                                geo.x += valueX;
                                geo.y += valueY;
                            } else {
                                geo.x = valueX;
                                geo.y = valueY;
                            }
                            graph.getModel().setGeometry(v1, geo);
                        }
                        finally
                        {
                            var morph = new mxMorphing(graph, 0, 0, 0);
                            morph.addListener(mxEvent.DONE, function()
                            {
                                graph.getModel().endUpdate();
                            });
                            morph.startAnimation();
                            return previousCoord;
                        }
                    }
                 }

                 function historyGraphGoBack(graph) {
                    // Clean any ModalInfo Timer started before go back 
                    if ( timerShowModalSet != undefined ) {
                            clearTimeout(timerShowModalSet)
                    }
                    level           -= 1
                    var parentCellId = '';
                    try {
                        graph.getModel().beginUpdate();
                        graph.removeCells(graph.getChildVertices(graph.getDefaultParent()));
                        var xml = previousGraphXml.pop();
                        var doc = mxUtils.parseXml(xml);
                        var codec = new mxCodec(doc);
                        var model = codec.decode(doc.documentElement);

                        // Find out the parent of the previous level to highlight it with some animation. 
                        // Example: if we go back to List_VPC level, we need to find the first VPC Cell and use its ParecenCellId
                        for (var key in model.cells)
                        {
                            var tmp = model.getCell(key);
                            if ( tmp.data != undefined && tmp.data.parentCellId != undefined ) {
                                if ( LEVELS[level] == LIST_VPC && tmp.data.awsResourceType == "vpc" ) {
                                    parentCellId = tmp.data.parentCellId;
                                    break;
                                } else
                                if ( LEVELS[level] == LIST_SUBNET && tmp.data.awsResourceType == "subnet" ) {
                                    parentCellId = tmp.data.parentCellId;
                                    break;
                                }
                            }
                        }
                        graph.getModel().mergeChildren(model.getRoot().getChildAt(0), graph.getDefaultParent());
                    } finally {
                        graph.getModel().endUpdate();
                    }
                    // Animation
                    var xs = [10,-10,-5,5,20,25];
                    var ys = [10,-10,-5,5,20,25];
                    var x  = xs[Math.floor(Math.random() * (5 - 0) + 0)];
                    var y  = ys[Math.floor(Math.random() * (5 - 0) + 0)];
                    var previousCoord;
                    setTimeout(function(){
                        previousCoord = moveMe(graph,parentCellId,x,y,true);
                    },70);
                    setTimeout(function(){
                        moveMe(graph,parentCellId,previousCoord.x,previousCoord.y, false);
                    },450);
                 }

                 function showModalInfo(currentState) {
                    // Check if the Mouse is over the same Object/Icon for a specific amount of time (set it on the calling of this throuhg setTimeOut, down below) 
                    // If the mouse has moved away after some time, the ModalInfo should not be shown, otherwise should be shown
                    var sameRegionYet = (globalCurrentState == currentState) && (globalCurrentState != undefined) && (globalCurrentState.cell != undefined);
                    if (!sameRegionYet)
                        return;

                    var divContent = document.getElementById(divContentId);
                    divContent.innerHTML  = currentState.cell.modalInfo.html;

                    if ( !showModalRightBtnFixed )
                         document.querySelector("#imgBtnClose").style.display = "none";

                    x = currentState.cell.getGeometry().x + (currentState.cell.getGeometry().width);
                    y = currentState.cell.getGeometry().y - 50;
                    var div = document.getElementById(divModalInfoId);
                    
                    var win = window,
                        doc = document,
                        docElem = doc.documentElement,
                        body    = doc.getElementsByTagName('body')[0],
                        width   = win.innerWidth || docElem.clientWidth || body.clientWidth,
                        height  = win.innerHeight|| docElem.clientHeight|| body.clientHeight;

                    div.style.display = "block";    
                        
                    // Adjust the Y position of the Div accordingly with the screen height    		 
                    divModalInfoHeight = div.offsetHeight;
                    if ( (y + divModalInfoHeight) > height ) {
                        y = y - ((y + divModalInfoHeight) - height) - (currentState.cell.getGeometry().height * 1.8); 
                    }
                    if ( y < 0 ) {
                        y = currentState.cell.getGeometry().y + 30;
                    }

                    // Adjust the X position of the Div accordingly with the screen width and the cell width
                    divModalInfoWidth = div.offsetWidth;
                    if ( (x + divModalInfoWidth) > width ) {
                        x = x - (divModalInfoWidth + currentState.cell.getGeometry().width + 5); 
                    }
                    
                    div.style.display = "block";
                    div.style.left    = x;
                    div.style.top     = y;
                 }

                 var delayTimeShowModalInfo = 500; // one second
                 var timerShowModalSet      = undefined;
                 var divModalInfoWidth      = 350;
                 var divModalInfoHeight     = 250;
                 var globalCurrentState     = null;
                 var showModalRightBtnFixed = false;
                 var divModalInfo           = document.createElement("div");   
                 var divModalInfoId         = "divModalInfo"
                 divModalInfo.style.display = "none";
                 divModalInfo.className     = "modalInfo";
                 //divModalInfo.innerHTML     = "Header";
                 divModalInfo.id            = divModalInfoId;
                 var divContentId           = "divContentId";
                 var divContent             = document.createElement("div");
                 divContent.innerHTML       = "Here, you can put any additional information";
                 divContent.id              = divContentId;
                 divModalInfo.appendChild(divContent);    

                 function main(container)
                 {
                     document.body.appendChild(divModalInfo);   

                     """ + self.htmlSnippets.jsBrowserNotSupported() + """
                     else
                     {
                         // Speedup the animation
                         mxText.prototype.enableBoundingBox = false
                         mxEvent.disableContextMenu(document.body);

                         // Creates the graph inside the given container
                         var graph = new mxGraph(container);
                         
                         // Disables all built-in interactions
                         graph.setEnabled(false);
                         graph.setPanning(true);
                         graph.panningHandler.useLeftButtonForPanning = true;
                         graph.setHtmlLabels(true);
         
                         // Handles clicks on cells
                         graph.addListener(mxEvent.CLICK, function(sender, evt)
                         {
                             var rightButton;
                             if ( evt.properties != undefined && evt.properties.event != undefined && evt.properties.event.button != undefined ) {
                                 rightButton = evt.properties.event.button == 2 ? true : false;
                             }
                             if ( rightButton != undefined && rightButton == false ) {
                                  var cell = evt.getProperty('cell');
                                  if (cell != null)
                                  {
                                      // If the Cell clicked is a VPC Resource and we are at the level of LIST_SUBNET, so...
                                      // we are clicking at the center of the graph, that is, the root parent (VPC) of all Subnets 
                                      // Then, we must go back to the previous Level: LIST_VPC(1) ---> AWS (0)
                                      if ( cell.data != undefined && cell.data.awsResourceType == "vpc" && LEVELS[level] == LIST_SUBNET ) {
                                          historyGraphGoBack(graph);
                                      } else
                                      if ( cell.data != undefined && cell.data.awsResourceType == "subnet" && LEVELS[level] == LIST_EC2 ) {
                                          historyGraphGoBack(graph);
                                      } else {
                                          // Before going foward, clean any ModalInfo TimeOut Set
                                          if ( timerShowModalSet != undefined ) {
                                              clearTimeout(timerShowModalSet)
                                          }
                                          // Save snapshot of the previous graph to go back when requested
                                          var enc          = new mxCodec();
                                          var node         = enc.encode(graph.getModel());
                                          var tmpXml       = mxUtils.getXml(node);
                                          if ( callAWSGraphNavigation(graph, cell) ) {
                                              // Only save when any call was implemented
                                              previousGraphXml.push(tmpXml);    
                                          }
                                      }
                                  }
                             } else {
                                 // Right Mouse Button Pressed
                                 showModalRightBtnFixed = true;
                                 showModalInfo(globalCurrentState);
                             }
                         });

                         // Handles mouseOver, mouseOut - ModalInfo
                         graph.addMouseListener({
                            currentState: null,
                            mouseMove: function(sender, evt) {
                                 if ( !showModalRightBtnFixed ) {
                                    if (this.currentState != null && (evt.getState() == this.currentState || evt.getState() == null) ) {
                                        globalCurrentState = this.currentState;
                                        if ( timerShowModalSet != undefined ) {
                                            clearTimeout(timerShowModalSet)
                                        }
                                        timerShowModalSet = setTimeout(showModalInfo,delayTimeShowModalInfo,this.currentState);
                                        if ( evt.getState() ) {
                                            evt.getState().setCursor('pointer');
                                        }     
                                    }

                                    var tmp = graph.view.getState(evt.getCell()); 
                                    
                                    if ( tmp != this.currentState ) {
                                        var div = document.getElementById(divModalInfoId);
                                        div.style.display = "none";
                                        if ( timerShowModalSet != undefined ) {
                                            clearTimeout(timerShowModalSet)
                                        }
                                        if ( tmp != null && tmp.cell.isVertex() ) {
                                            this.currentState  = tmp;
                                            globalCurrentState = tmp;
                                        }
                                    }
                                 }
                            },
                            mouseDown: function(sender, evt) { },
                            mouseUp:   function(sender, evt) { },
                            dragEnter: function(evt, state) { },
                            dragLeave: function(evt, state) { }
                         });

                         // Mouse Wheel Zooming
                         mxEvent.addMouseWheelListener((evt, up) => {
                            if (mxEvent.isConsumed(evt)) {
                                return;
                            }
                            let gridEnabled = graph.gridEnabled;
                            // disable snapping
                            graph.gridEnabled = false;
                            let p1 = graph.getPointForEvent(evt, false);
                            if (up) {
                                graph.zoomIn();
                            } else {
                                graph.zoomOut();
                            }
                            let p2 = graph.getPointForEvent(evt, false);
                            let deltaX = p2.x - p1.x;
                            let deltaY = p2.y - p1.y;
                            let view = graph.view;
                            view.setTranslate(view.translate.x + deltaX, view.translate.y + deltaY);
                            graph.gridEnabled = gridEnabled;
                            mxEvent.consume(evt);
                         }, container);
                          
                         // Changes the default vertex style in-place
                         var style = graph.getStylesheet().getDefaultVertexStyle();
                         // Rectangle (rounded)
                         style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_RECTANGLE;
                         style[mxConstants.STYLE_ROUNDED] = true;
                         style[mxConstants.STYLE_PERIMETER] = mxPerimeter.RectanglePerimeter;
                         style[mxConstants.STYLE_GRADIENTCOLOR] = 'white';
                                         
                         // Gets the default parent for inserting new cells. This
                         // is normally the first child of the root (ie. layer 0).
                         var parent = graph.getDefaultParent();
         
                         var cx = graph.container.clientWidth / 2;
                         var cy = graph.container.clientHeight / 2;
                         
                         // Root of All
                         var awsImg = dataURIFor("aws-4.png").replace(";base64,",",");
                         var prefix = 'shape=image;image=' + awsImg + ";";

                         var cell       = graph.insertVertex(parent, 'AWS', 'AWS', cx - 20, cy - 15, 60, 40,prefix+'verticalLabelPosition=bottom;verticalAlign=top');
                         cell.data      = new CustomData('aws', 'root');
                         cell.modalInfo = new ModalInfoHTML("root",{"aws":"aws"});
                         
                         // Animates the changes in the graph model
                         graph.getModel().addListener(mxEvent.CHANGE, function(sender, evt)
                         {
                             var changes = evt.getProperty('edit').changes;
                             mxEffects.animateChanges(graph, changes);
                         });

                         """ +  self.htmlSnippets.jsMxToolBox("90","15") + """

                         var parameters = undefined;
                         postRequest(LIST_VPC,parameters,function(response) {
                             drillDown(graph, cell, response);
                         });
                     }
                 };

                 function closeModalInfo() {
                    var div = document.getElementById(divModalInfoId);
                    div.style.display      = "none";
                    showModalRightBtnFixed = false;
                 }

                 var LIST_VPC            = "listVpc";
                 var LIST_SUBNET         = "listSubnet";
                 var LIST_EC2            = "listEc2";
                 var LIST_SECURITY_GROUP = "listSecurityGroup";
                 var level               = 0;
                 var LEVELS              = ["ROOT", LIST_VPC, LIST_SUBNET, LIST_EC2];

                 function showLoading(show) {
                     if (show) {
                         document.querySelector("#loadingBackground").style.display = "";
                         document.querySelector("#loadingMessage").style.display = "";
                     } else {
                         document.querySelector("#loadingBackground").style.display = "none";
                         document.querySelector("#loadingMessage").style.display    = "none";
                     }
                 }

                 function callAWS(request, callback, event) {
                    showLoading(true);
                    postRequest(request.call,request.parameters,function(response, event) {
                        showLoading(false);
                        callback(response, event);
                    }, event);
                 }
                 function callListSecurityGroups(groupId, callback, event) {
                    var parameters  = [];
                    parameters.push({"name":"groupId","value":groupId});
                    var request = {
                        "call":LIST_SECURITY_GROUP,
                        "parameters": parameters
                    };
                    callAWS(request, callback, event);
                 }

                 function callAWSGraphNavigation(graph, cell) {
                     var callImplemented = false;
                     var awsResourceType = cell.data.awsResourceType;
                     if ( awsResourceType == "subnet" ) {
                         // Drill Down Subnets --> EC2s
                         showLoading(true);
                         callImplemented = true;
                         var parameters  = [];
                         parameters.push({"name":"vpcId","value":cell.data.awsResourceId},
                                         {"name":"subnetId","value":cell.data.awsResourceId});
                         postRequest(LIST_EC2,parameters,function(response) {
                             drillDown(graph, cell, response);
                             level = 3;
                         });
                     } else
                     if ( awsResourceType == "vpc" ) {
                         // Drill Down VPC --> Subnets
                         showLoading(true);
                         callImplemented = true;
                         var parameters  = [];
                         parameters.push({"name":"vpcId","value":cell.data.awsResourceId});
                         postRequest(LIST_SUBNET,parameters,function(response) {
                             drillDown(graph, cell, response);
                             level = 2;
                         });
                     } else
                     if ( awsResourceType == "aws" ) {
                         // Drill Down AWS --> VPCs
                         showLoading(true);
                         callImplemented = true;
                         var parameters  = undefined;
                         postRequest(LIST_VPC,parameters,function(response) {
                             drillDown(graph, cell, response);
                             level = 1;
                         });
                     }
                     return callImplemented;
                 }

                 function postRequest(action, parameters, callback, event) {
                     Http.open("POST", url, true);
                     Http.setRequestHeader('Content-type','application/json');
                     request = createRequest(action,parameters);
                     Http.onreadystatechange = (e) => {
                        if ( Http.readyState == 4 && Http.status == 200 ) {
                            callback(JSON.parse(Http.responseText), event)
                        } else {
                            //console.log("onreadystatechange = " + Http.status);
                        }
                     }
                     Http.onerror = (e) => {
                         showLoading(false);
                         alert("No connection available for " + url);
                     }
                     //Http.send(JSON.stringify(request));
                     Http.send(request);
                 }

                 function createRequest(action, params) {
                    var request        = {};
                    var parameters     = [];
                    request.action     = action;
                    request.parameters = parameters;

                    if ( params && params != undefined && params.length > 0 ) {
                        for (index = 0; index < params.length; ++index) {
                            request.parameters.push({
                                "name": params[index]["name"],
                                "value": params[index]["value"]
                            });
                        }
                    }
                    return JSON.stringify(request);
                }

                 // Loads the links for the given cell into the given graph
                 // by requesting the respective data in the server-side
                 // (implemented for this demo using the server-function)
                 function drillDown(graph, cell, json)
                 {
                     if (graph.getModel().isVertex(cell))
                     {
                         centerCell = cell;
                         var cx = graph.container.clientWidth / 2;
                         var cy = graph.container.clientHeight / 2;
                         
                         // Gets the default parent for inserting new cells. This
                         // is normally the first child of the root (ie. layer 0).
                         var parent = graph.getDefaultParent();
         
                         // Adds cells to the model in a single step
                         graph.getModel().beginUpdate();
                         try
                         {
                             var xml = jsonToGraphModel(cell.id, json);
                             var doc = mxUtils.parseXml(xml);
                             var dec = new mxCodec(doc);
                             var model = dec.decode(doc.documentElement);
         
                             // Removes all cells which are not in the response
                             for (var key in graph.getModel().cells)
                             {
                                 var tmp = graph.getModel().getCell(key);
                                 
                                 if (tmp != cell &&
                                     graph.getModel().isVertex(tmp))
                                 {
                                     graph.removeCells([tmp]);
                                 }
                             }
         
                             // Merges the response model with the client model
                             graph.getModel().mergeChildren(model.getRoot().getChildAt(0), parent);
         
                             // Moves the given cell to the center
                             var geo = graph.getModel().getGeometry(cell);
         
                             if (geo != null)
                             {
                                 geo = geo.clone();
                                 geo.x = cx - geo.width / 2;
                                 geo.y = cy - geo.height / 2;
         
                                 graph.getModel().setGeometry(cell, geo);
                             }
         
                             // Creates a list of the new vertices, if there is more
                             // than the center vertex which might have existed
                             // previously, then this needs to be changed to analyze
                             // the target model before calling mergeChildren above
                             var vertices = [];
                             
                             for (var key in graph.getModel().cells)
                             {
                                 var tmp = graph.getModel().getCell(key);
                                 
                                 if (tmp != cell && model.isVertex(tmp))
                                 {
                                     vertices.push(tmp);
         
                                     // Changes the initial location "in-place"
                                     // to get a nice animation effect from the
                                     // center to the radius of the circle
                                     var geo = model.getGeometry(tmp);
         
                                     if (geo != null)
                                     {
                                         geo.x = cx - geo.width / 2;
                                         geo.y = cy - geo.height / 2;
                                     }
                                 }
                             }
                             
                             // Arranges the response in a circle
                             var cellCount = vertices.length;
                             var phi = 2 * Math.PI / cellCount;
                             var r = Math.min(graph.container.clientWidth / 2.3,
                                              graph.container.clientHeight / 2.3);
                             
                             for (var i = 0; i < cellCount; i++)
                             {
                                 var geo = graph.getModel().getGeometry(vertices[i]);
                                 
                                 if (geo != null)
                                 {
                                     geo = geo.clone();
                                     geo.x += r * Math.sin(i * phi);
                                     geo.y += r * Math.cos(i * phi);
         
                                     graph.getModel().setGeometry(vertices[i], geo);
                                 }
                             }
                         }
                         finally
                         {
                             // Updates the display
                             graph.getModel().endUpdate();
                         }
                     }
                     showLoading(false);
                 };

                 
                 var colors      = ["rgb(0,0,255)","rgb(183,151,43)","rgb(110,105,89)","rgb(91,154,176)","rgb(255,0,9)","rgb(204,204,0)","rgb(128,128,128)","rgb(246,0,0)","rgb(246,178,103)","rgb(8,180,151)"];
                 var labelColors = {};
                 function colorForLabel(label) {
                    var color; 
                    if (labelColors[label] && labelColors[label] != undefined && labelColors[label] != "") {
                        color = labelColors[label];
                    }
                    if ( !color || color == undefined || color == "" ) {
                        var rnd = Math.floor(Math.random() * colors.length-1);
                        if ( rnd < 0 ) {
                            rnd = 3;
                        }
                        color = colors[rnd];
                        labelColors[label] = color;
                    }
                    return color;
                 }
                 function componentToHex(c) {
                    var hex = c.toString(16);
                    return hex.length == 1 ? "0" + hex : hex;
                 }
                 function rgbToHex(r, g, b) {
                    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
                 }
                 function rgbToHexStr(str) {
                    var cleanRGB = (str.replace("rgb(","").replace(")","")).split(","); 
                    return rgbToHex(parseInt(cleanRGB[0]), parseInt(cleanRGB[1]), parseInt(cleanRGB[2]));
                 }

                 function jsonToGraphModel(cellId, json)
                 {
                     // Creates a local graph with no display
                     var graph = new mxGraph();
                     
                     // Gets the default parent for inserting new cells. This
                     // is normally the first child of the root (ie. layer 0).
                     var parent = graph.getDefaultParent();
         
                     // Adds cells to the model in a single step
                     graph.getModel().beginUpdate();
                     try
                     {
                        if ( json != undefined ) {
                            action = json["aws"]["action"]

                            width  = 130;
                            height = 50;
                            
                            if (action == LIST_VPC) {
                                var v0  = graph.insertVertex(parent, cellId, 'AWS-Dummy', 0, 0, width, height);
                                v0.data    = new CustomData('root', undefined, json, '');
                                var prefix = 'shape=image;image=' + dataURIFor(AWS_VPC_IMG) + ";";
                                for( var key in json["aws"]["vpc"] ) {
                                    var vpc     = json["aws"]["vpc"][key];
                                    var id      = vpc.vpcId;
                                    var label   = "<b>" + vpc.vpcId + "</b><br>" + vpc.cidrBlock; 
                                    var v       = graph.insertVertex(parent, id, label, 0, 0, width, height, prefix+'verticalLabelPosition=bottom;verticalAlign=top;whiteSpace=wrap;');
                                    v.data      = new CustomData('vpc', vpc.vpcId, json, cellId);
                                    v.modalInfo = new ModalInfoHTML('vpc',vpc);
                                    var e       = graph.insertEdge(parent, null, '', v0, v);
                                }
                            } else
                            if (action == LIST_SUBNET) {
                                 var v0      = graph.insertVertex(parent, cellId, 'Vpc', 0, 0, width, height);
                                 v0.data     = new CustomData('vpc', undefined, json);
                                 var prefix1 = 'shape=image;image=' + dataURIFor(AWS_SUBNET_PRIVATE_IMG) + ";";
                                 var prefix2 = 'shape=image;image=' + dataURIFor(AWS_SUBNET_PUBLIC_IMG) + ";";
                                 var prefix  = prefix1;
                                 for( var key in json["aws"]["vpc"]["subnets"] ) {
                                    var subnet = json["aws"]["vpc"]["subnets"][key];
                                    var id           = subnet.subnetId;
                                    var defaultForAz = subnet.defaultForAz ? "<br>DEFAULT" : "";
                                    if (subnet.scope == "public") {
                                        prefix = prefix2
                                    } else {
                                        prefix = prefix1
                                    }
                                    var colorAz = colorForLabel(subnet.availabilitZone);
                                    var label   = "<b>" + subnet.subnetId + "</b><br>" + subnet.cidrBlock + "<br><span style='color:" + colorAz + ";'>" + subnet.availabilitZone + "</span>" + defaultForAz;
                                    var v       = graph.insertVertex(parent, id, label, 0, 0, width, height, prefix+'verticalLabelPosition=bottom;verticalAlign=top;whiteSpace=wrap;');
                                    v.data      = new CustomData('subnet', subnet.subnetId, json, cellId);
                                    v.modalInfo = new ModalInfoHTML('subnet',subnet);
                                    var e       = graph.insertEdge(parent, null,subnet.availabilitZone, v0, v,'strokeColor=' + rgbToHexStr(colorAz) + ';');
                                }
                            } else
                            if (action == LIST_EC2) {
                                 var v0     = graph.insertVertex(parent, cellId, 'Subnet', 0, 0, width, height);
                                 v0.data    = new CustomData('ec2', undefined, json);
                                 for( var key in json["aws"]["ec2"]["instances"] ) {
                                    var ec2instance = json["aws"]["ec2"]["instances"][key];

                                    var prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_IMG) + ";";
                                    if ( ec2instance.instanceType.startsWith("t2") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_T2_IMG) + ";";
                                    } else 
                                    if ( ec2instance.instanceType.startsWith("t3a") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_T3A_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("t3") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_T3_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("a1") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_A1_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("c4") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_C4_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("c5") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_C5_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("m4") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_M4_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("m5a") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_M5A_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("m5") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_M5_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("p2") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_P2_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("p3") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_P3_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("r4") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_R4_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("r5a") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_R5A_IMG) + ";";
                                    } else
                                    if ( ec2instance.instanceType.startsWith("r5") ) {
                                        prefix = 'shape=image;image=' + dataURIFor(AWS_EC2_R5_IMG) + ";";
                                    }
                                    
                                    var id           = ec2instance.instanceId;
                                    var colorInsType = colorForLabel(ec2instance.instanceType);
                                    var colorState   = colorForLabel(ec2instance.state.name.toUpperCase());
                                    var label        = "<b>" + ec2instance.instanceId + "</b><br>" + ec2instance.privateIpAddress + "<br><span style='color:" + colorInsType + ";'>" + ec2instance.instanceType + "</span>";
                                    var v            = graph.insertVertex(parent, id, label, 0, 0, width, height, prefix+'verticalLabelPosition=bottom;verticalAlign=top;whiteSpace=wrap;');
                                    v.data           = new CustomData('ec2', ec2instance.instanceId, json, v0.cellId);
                                    v.modalInfo      = new ModalInfoHTML('ec2',ec2instance);
                                    var e            = graph.insertEdge(parent,null,ec2instance.state.name.toUpperCase(), v0, v, 'strokeColor=' + rgbToHexStr(colorState) + ';');
                                }
                            }
                        } else {
                            console.log("json is not defined");
                        }
                     }
                     finally
                     {
                         // Updates the display
                         graph.getModel().endUpdate();
                     }
         
                     var enc = new mxCodec();
                     var node = enc.encode(graph.getModel());
                     
                     return mxUtils.getXml(node);
                 };

                 function CustomData(awsResourceType, awsResourceId, sourceData, parentCellId) {
                    this.awsResourceType = awsResourceType;
                    this.awsResourceId   = awsResourceId;
                    this.sourceData      = sourceData;
                    this.parentCellId    = parentCellId;
                 }

                 function ModalInfoHTML(resourceId, data) {
                    if ( resourceId == 'root' ) {
                       this.html = buildHtmlAwsModalInfo(data); 
                    } else
                    if ( resourceId == 'vpc' ) {
                       this.html = buildHtmlVpcModalInfo(data);
                    } else
                    if ( resourceId == 'subnet' ) {
                       this.html = buildHtmlSubnetModalInfo(data);   
                    } else
                    if ( resourceId == 'ec2' ) {
                       this.html = buildHtmlEc2ModalInfo(data);
                    } else {
                       this.html = "<h5>" + JSON.stringify(data) + "</h5>"; 
                    }
                 }


                 var tagBehavior = 'onmouseover="javascript:this.style.backgroundColor=' + "'" + 'rgb(0,175,175)' + "'" + ';this.style.cursor=' + "'" + 'pointer' + "'" + ';"onmouseout="javascript:this.style.backgroundColor=' + "'" + 'rgb(0,220,220)' + "';" + '"';
                 function buildHtmlVpcModalInfo(data) {
                     var html =
                         '<div id="imgBtnClose" style="position:absolute;top:7%;left:93%"><img  onMouseOver="this.style.cursor=' + "'" + 'pointer' + "'" + '" src=""" + self.images.close +""" onClick="javascript:closeModalInfo();"></div>'
                       + '<table class="tableInfo" width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">'
                       + ' <tr><td align="center" height="35px" colspan="2" class="cellHeader">VPC</td></tr>'  
                       + ' <tr><td class="cellInfo">'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.vpcId + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Vpc Id.......:&nbsp;<font style="color:blue;">' + data.vpcId + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.cidrBlock + "'"+ ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     CIDR Block...:&nbsp;<font style="color:blue;">' + data.cidrBlock + '</font>'
                       + ' <tr>'
                       + ' <tr><td colspan="2" class="cellTags">'
                       + '     Tags:<br><br>'
                       var tagsPerLine = 0;
                       for(var index = 0; index < data.tags.length; index++) {
                           var tag = data.tags[index];
                           html = html + '<div class="tag"' 
                                       + 'onclick="javascript:copyToClipboard(' + "'" + tag.key + "=" + tag.value + "'" + ');" '
                                       + tagBehavior + '>' + tag.key + '=' + tag.value + '</div>';
                           tagsPerLine += 1 
                           if (tagsPerLine >= 2) {
                               tagsPerLine = 0;
                               html = html + '<br><br>'
                           }
                       }
                       + ' </td>'
                       + '</table>'
                    return html;  
                 }

                 function buildHtmlSubnetModalInfo(data) {
                     var labelScope = data.scope == "public" ? "PUBLIC" : "PRIVATE";
                     var html =  
                         '<div id="imgBtnClose" style="position:absolute;top:5%;left:93%"><img  onMouseOver="this.style.cursor=' + "'" + 'pointer' + "'" + '" src=""" + self.images.close +""" onClick="javascript:closeModalInfo();"></div>'
                       + '<table class="tableInfo" width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">'
                       + ' <tr><td align="center" height="35px" colspan="2" class="cellHeader">' + labelScope + ' SUBNET</td></tr>'  
                       + ' <tr><td class="cellInfo">'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.subnetId + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Subnet Id.......:&nbsp;<font style="color:blue;">' + data.subnetId + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.availabilitZone + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     AZ..............:&nbsp;<font style="color:blue;">' + data.availabilitZone + ' (' + data.availabilitZoneId  + ')' + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.cidrBlock + "'"+ ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     CIDR Block......:&nbsp;<font style="color:blue;">' + data.cidrBlock + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.availableIpAddressCount + "'"+ ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Available IpV4..:&nbsp;<font style="color:blue;">' + data.availableIpAddressCount + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.vpcId + "'"+ ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     VPC Id..........:&nbsp;<font style="color:blue;">' + data.vpcId + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.defaultForAz + "'"+ ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Default for AZ..:&nbsp;<font style="color:blue;">' + data.defaultForAz + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.subnetArn + "'"+ ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Subnet ARN......:&nbsp;<font style="color:blue;font-size:9px;">' + data.subnetArn + '</font>'
                       + ' <tr>'
                       + ' <tr><td colspan="2" class="cellTags">'
                       + '     Tags:<br><br>'
                       var tagsPerLine = 0;
                       for(var index = 0; index < data.tags.length; index++) {
                           var tag = data.tags[index];
                           html = html + '<div class="tag"' 
                                       + 'onclick="javascript:copyToClipboard(' + "'" + tag.key + "=" + tag.value + "'" + ');" '
                                       + tagBehavior + '>' + tag.key + '=' + tag.value + '</div>';
                           tagsPerLine += 1 
                           if (tagsPerLine >= 2) {
                               tagsPerLine = 0;
                               html = html + '<br><br>'
                           }
                       }
                       + ' </td>'
                       + '</table>'
                    return html;  
                 }

                 function thousandSeparator(x) {
                    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
                 }

                 function callBackShowHtmlSecurityGroup(response, event) {
                     //TODO: Build the HTML Popup for Security Group
                     console.log(event);
                     console.log(response);
                 }

                 function buildHtmlEc2ModalInfo(data) {
                     var colorState;
                     if ( data.state.name.toUpperCase() == "RUNNING" ) {
                         colorState = "green";
                     } else
                     if ( data.state.name.toUpperCase() == "STOPPED" ) {
                         colorState = "red";
                     } else {
                         colorState = "black";
                     }
                     var dtToday      = new Date();
                     var dt           = data.launchTime.split("-")[1] + "-" + data.launchTime.split("-")[0] + "-" + data.launchTime.split("-")[2];
                     var dtLaunched   = new Date(dt);
                     var timeLaucnhed = milliseconds = Math.abs(dtLaunched - dtToday);
                     var hours        = "&nbsp;(<font color=gray;>" + thousandSeparator(parseInt((milliseconds / 36e5))) + " hours)</font>";
                     var publicIpAddressEntry = "";
                     if ( data.publicIpAddress && data.publicIpAddress != "" ){
                           publicIpAddressEntry = '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.publicIpAddress + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                                                + '     Public IP...........:&nbsp;<font style="color:blue;">' + data.publicIpAddress + '</font><br>';
                     }
                     var blockDevices = "";
                     if ( data.blockDeviceMappings ) {
                          var totalDevices = data.blockDeviceMappings.length
                          for( var i = 0; i < data.blockDeviceMappings.length; i++ ) {
                              var blockDevice = data.blockDeviceMappings[0];
                              var labelTotal  = '<font style="color:gray;">[' + (i+1) + ' of ' + totalDevices + ']</font>';
                              blockDevices =  blockDevices
                              + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + blockDevice.ebs.volumeId + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                              + '     EBS...............' + labelTotal + '..:&nbsp;<font style="color:blue;">' + blockDevice.deviceName + ' (' + blockDevice.ebs.volumeId +')&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font><br>'
                              + '&nbsp;&nbsp;&nbsp;&nbsp;|Status....................:&nbsp;<font style="color:blue;">' + blockDevice.ebs.status + '</font><br>'
                              + '&nbsp;&nbsp;&nbsp;&nbsp;|Attach Time...............:&nbsp;<font style="color:blue;">' + blockDevice.ebs.attachTime + '</font><br>'
                              + '&nbsp;&nbsp;&nbsp;&nbsp;|Delete on Terminatation...:&nbsp;<font style="color:blue;">' + blockDevice.ebs.deleteOnTermination + '</font><br>'  
                          }
                     }
                     var securityGroups = "";
                     if ( data.securityGroups ) {
                          var totalSecurityGroups = data.securityGroups.length
                          for( var i = 0; i < data.securityGroups.length; i++ ) {
                              var securityGroup = data.securityGroups[0];
                              var labelTotal  = '<font style="color:gray;">[' + (i+1) + ' of ' + totalSecurityGroups + ']</font>';
                              securityGroups =  securityGroups
                              + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + securityGroup.groupId + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                              + '     Security Group....' + labelTotal + '..:&nbsp;<font style="color:darkorange;text-decoration-line:underline;">'
                              + '<span onMouseOver="this.style.cursor=' + "'" + 'pointer' + "'" + '" onClick="javascript:callListSecurityGroups(' + "'" + securityGroup.groupId + "'" + ',callBackShowHtmlSecurityGroup, event);">' + securityGroup.groupId + '</span></font><br>'
                              + '&nbsp;&nbsp;&nbsp;&nbsp;|Group Name................:&nbsp;<font style="color:blue;">' + securityGroup.groupName + '</font><br>'
                          }
                     }
                     var html =  
                         '<div id="imgBtnClose" style="position:absolute;top:4%;left:93%"><img  onMouseOver="this.style.cursor=' + "'" + 'pointer' + "'" + '" src=""" + self.images.close +""" onClick="javascript:closeModalInfo();"></div>'
                       + '<table class="tableInfo" width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">'
                       + ' <tr><td align="center" height="35px" colspan="2" class="cellHeader">EC2 ' + data.instanceType.toUpperCase() + '</td></tr>'  
                       + ' <tr><td class="cellInfo">'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.instanceId + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Instance Id.................:&nbsp;<font style="color:blue;">' + data.instanceId + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.privateIpAddress + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Private IP..................:&nbsp;<font style="color:blue;">' + data.privateIpAddress + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.launchTime + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Launch Time.................:&nbsp;<font style="color:blue;">' + data.launchTime + '</font>' + hours + '<br>'
                       + publicIpAddressEntry
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.state.name.toUpperCase() + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     State.......................:&nbsp;<font style="color:' + colorState +';">' + data.state.name.toUpperCase() + '</font><br>'

                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.cpu.coreCount + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     CPU Core Count..............:&nbsp;<font style="color:blue;">' + data.cpu.coreCount + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.cpu.coreCount + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     CPU Threads Per Core........:&nbsp;<font style="color:blue;">' + data.cpu.threadsPerCore + '</font><br>'
                       + securityGroups
                       + blockDevices
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.subnetId + "'" + ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     Subnet Id...................:&nbsp;<font style="color:blue;">' + data.subnetId + '</font><br>'
                       + '     <input type="image" class="buttonCopyClipboard" onclick="javascript:copyToClipboard(' + "'" + data.vpcId + "'"+ ');" src=""" + self.images.copyClipboardPath +""" />'
                       + '     VPC Id......................:&nbsp;<font style="color:blue;">' + data.vpcId + '</font><br>'
                       + ' <tr>'
                       + ' <tr><td colspan="2" class="cellTags">'
                       + '     Tags:<br><br>'
                       var tagsPerLine = 0;
                       for(var index = 0; index < data.tags.length; index++) {
                           var tag = data.tags[index];
                           html = html + '<div class="tag"' 
                                       + 'onclick="javascript:copyToClipboard(' + "'" + tag.key + "=" + tag.value + "'" + ');" '
                                       + tagBehavior + '>' + tag.key + '=' + tag.value + '</div>';
                           tagsPerLine += 1 
                           if (tagsPerLine >= 2) {
                               tagsPerLine = 0;
                               html = html + '<br><br>'
                           }
                       }
                       + ' </td>'
                       + '</table>'
                    return html;  
                 }

                 function buildHtmlAwsModalInfo(data) {
                     var html =  
                         '<table class="tableInfo" width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">'
                       + ' <tr><td align="center" height="35px" colspan="2" class="cellHeader">AWS</td></tr>'  
                       + ' <tr><td class="cellInfo">'
                       + '    <font style="color:blue;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AWS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font><br>'
                       + ' <tr>'
                       + '</table>'
                    return html;  
                 }

                 function copyToClipboard(str) {
                    const el = document.createElement('textarea');
                    el.value = str;
                    document.body.appendChild(el);
                    el.select();
                    document.execCommand('copy');
                    document.body.removeChild(el);
                 }

                 """ + self.htmlSnippets.jsFormatXml() + """
                 function pad2(n) { return n < 10 ? '0' + n : n }

                 function timestamp() {
                    var date = new Date();
                    return  date.getFullYear().toString() + "/" + pad2(date.getMonth() + 1) + "/" +  pad2( date.getDate()) 
                    +  " " + pad2( date.getHours() ) + ":" + pad2( date.getMinutes() ) + ":" + pad2( date.getSeconds() ) + ":" + pad2( date.getMilliseconds() ) + " ";
                 }
             </script>
          </head>   
          """ + self.htmlSnippets.htmlCommonBody() + """
        </html>
        """
        self.openHTML(html)
        self.startHttpServer()
        print(Emoticons.ok() + " \033[93mNavigator exited!\033[0m")    
