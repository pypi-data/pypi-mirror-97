
import webbrowser
import os, sys
import threading

"""
# IMPORTS TO WORK AS MAIN MODULE (NOT "SUBFOLDED")
from HttpServer import HttpServer
from PymxGraphAwsNavigator import PymxGraphAwsNavigator
from PymxGraphTree import PymxGraphTree
"""
# IMPORTS TO WORK MODULE
from pyawscp.pymxgraph.HttpServer import HttpServer
from pyawscp.pymxgraph.PymxGraphAwsNavigator import PymxGraphAwsNavigator
from pyawscp.pymxgraph.PymxGraphTree import PymxGraphTree


IMAGES_SUBPATH = "/images"
JS_SUBPATH     = "/js"
STYLE_EC2 = "outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws3.ec2;fillColor=#F58534;gradientColor=none;"

class _Images:

    def __init__(self, pathToResources):
        self.pathToResources            = pathToResources
        self.gridImagePath              = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("grid.gif").replace(os.path.realpath('.'),"").replace("\\","/")
        self.zoomInImagePath            = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("zoom_in32.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.zoomOutImagePath           = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("zoom_out32.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.view1to1ImagePath          = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("view_1_132.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.printerImagePath           = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("print32.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.minimizeImagePath          = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("minimize.gif").replace(os.path.realpath('.'),"").replace("\\","/")
        self.maximizeImagePath          = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("maximize.gif").replace(os.path.realpath('.'),"").replace("\\","/")
        self.normalizeImagePath         = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("normalize.gif").replace(os.path.realpath('.'),"").replace("\\","/")
        self.exportImageImagePath       = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("exportImage.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.modelGraphExportImagePath  = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("modelGraphExport.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.editDrawIoImagePath        = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("editDrawIo.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.collapsedImagePath         = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("collapsed.gif").replace(os.path.realpath('.'),"").replace("\\","/")
        self.expandedImagePath          = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("expanded.gif").replace(os.path.realpath('.'),"").replace("\\","/")
        self.copyClipboardPath          = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("copy-clipboard.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.loadingPath                = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("loading.gif").replace(os.path.realpath('.'),"").replace("\\","/")
        self.close                      = self.pathToResources + IMAGES_SUBPATH + os.path.realpath("close.gif").replace(os.path.realpath('.'),"").replace("\\","/")

        self.awsVpcImg                  = "aws-vpc2.png"        
        self.awsSubnetPrivateImg        = "aws-subnet-private.png"
        self.awsSubnetPublicImg         = "aws-subnet-public.png"
        self.awsEc2Img                  = "aws-ec2.png"
        self.awsEc2T2Img                = "aws-ec2-t2.png"
        self.awsEc2T3Img                = "aws-ec2-t3.png"
        self.awsEc2T3aImg               = "aws-ec2-t3a.png"
        self.awsEc2A1Img                = "aws-ec2-a1.png"
        self.awsEc2C4Img                = "aws-ec2-c4.png"
        self.awsEc2C5Img                = "aws-ec2-c5.png"
        self.awsEc2M4Img                = "aws-ec2-m4.png"
        self.awsEc2M5Img                = "aws-ec2-m5.png"
        self.awsEc2M5aImg               = "aws-ec2-m5a.png"
        self.awsEc2P2Img                = "aws-ec2-p2.png"
        self.awsEc2P3Img                = "aws-ec2-p3.png"
        self.awsEc2R4Img                = "aws-ec2-r4.png"
        self.awsEc2R5Img                = "aws-ec2-r5.png"
        self.awsEc2R5aImg               = "aws-ec2-r5a.png"

        self.aws6Path                   = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath("aws-6.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.aws5Path                   = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath("aws-5.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.aws4Path                   = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath("aws-4.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.aws3Path                   = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath("aws-3.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.aws2Path                   = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath("aws-2.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.aws1Path                   = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath("aws-1.png").replace(os.path.realpath('.'),"").replace("\\","/")
        self.awsPath                    = self.aws4Path
        self.awsVpcPath                 = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath(self.awsVpcImg).replace(os.path.realpath('.'),"").replace("\\","/")
        self.awsSubnetPrivatePath       = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath(self.awsSubnetPrivateImg).replace(os.path.realpath('.'),"").replace("\\","/")
        self.awsSubnetPublicPath        = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath(self.awsSubnetPublicImg).replace(os.path.realpath('.'),"").replace("\\","/")
        self.awsEc2Path                 = self.pathToResources + IMAGES_SUBPATH + "/aws" + os.path.realpath(self.awsEc2Img).replace(os.path.realpath('.'),"").replace("\\","/")

class _HtmlSnippets:
    def __init__(self, pathToResources, images, serverURL):
        self.pathToResources = pathToResources
        self.images          = images
        self.serverURL       = serverURL

    def htmlTitle(self, title):
        return """
            <title>PyMxGraph - """ + title + """</title>
        """
    def jsLibraries(self):
        return """
            <!-- Sets the basepath for the library if not in same directory -->
            <script type="text/javascript">
                mxBasePath = '""" + self.pathToResources + """';
            </script>
        
            <!-- Loads and initializes the library -->
            <script type="text/javascript" src=\"""" + self.pathToResources + JS_SUBPATH + """/mxClient.js"></script>
        """
    def jsBrowserNotSupported(self):
        return """
                        if (!mxClient.isBrowserSupported())
                        {
                            mxUtils.error('Browser is not supported!', 200, false);
                        }
        """
    def jsExportModelGraph(self):
        return """
                            // Copy of the Graph
                            var cleanGraph = new mxGraph();
                            try {
                                    cleanGraph.getModel().beginUpdate();
                                    cleanGraph.getModel().mergeChildren(graph.getModel().getRoot().getChildAt(0), cleanGraph.getDefaultParent());
                                    // Clean unecessary info (crash the model conversion at Draw.IO)
                                    for (var key in cleanGraph.getModel().cells) {
                                        var tmp = cleanGraph.getModel().getCell(key);
                                        if (tmp != cell && cleanGraph.getModel().isVertex(tmp)) {
                                            if ( tmp.modalInfo ) {
                                                tmp.modalInfo = undefined;
                                            }
                                            if ( tmp.data ) {
                                                tmp.data = undefined;
                                            }
                                        }
                                    }
                            } finally {
                               cleanGraph.getModel().endUpdate();
                            }                                    
                            var encoder   = new mxCodec();
                            var result    = encoder.encode(cleanGraph.getModel());
                            var xml       = mxUtils.getXml(result);
                            pureDrawIOXml = removeHTMLTags(xml);
                            myWindow=window.open('','_blank','toolbar=no,scrollbars=no,resizable=yes,top=50,left=50,width=1024,height=720')
                            myWindow.document.write("<html><head></head><body><font style='font-family:Consolas;font-size:12px'><b>1.</b> Open the editor <a href='http://draw.io' target='blank'>http://draw.io</a></br><b>2.</b> Create a new Blank Diagram</br><b>3.</b> Navigate to Menu -> Extras -> Edit Diagram...</br><b>4.</b> <a href=javascript:document.getElementById('txtMx').focus();document.getElementById('txtMx').select()>Select</a> and copy the content below, paste it at Draw.IO and then... hit <b>OK</b></font></br></br><textarea readonly id='txtMx' style='width:100%;height:89%;background:#fdf0e3' onclick='javascript:this.select();' >" + formatXml(pureDrawIOXml) + "</textarea>");
                            myWindow.focus()
        """
    def jsEditAsDrawioDiagram(self):
        return """
                            var encoder = new mxCodec();
                            var result = encoder.encode(graph.getModel());
                            var xml = mxUtils.getXml(result);
                            xml     = removeHTMLTags(xml);
                            var form = document.getElementById("drawIoEdit")
                            form.action = '""" + self.pathToResources + """/localfile.html?mxfile=' + encodeURIComponent(xml);
                            form.submit() 
        """
    def jsDataURIForImage(self):
        return """
                const AWS_IMG                = "aws-4.png";        
                const AWS_VPC_IMG            = "aws-vpc2.png";        
                const AWS_SUBNET_PRIVATE_IMG = "aws-subnet-private.png";
                const AWS_SUBNET_PUBLIC_IMG  = "aws-subnet-public.png";
                const AWS_EC2_IMG            = "aws-ec2.png";
                const AWS_EC2_T2_IMG         = "aws-ec2-t2.png";
                const AWS_EC2_T3_IMG         = "aws-ec2-t3.png";
                const AWS_EC2_T3A_IMG        = "aws-ec2-t3a.png";
                const AWS_EC2_A1_IMG         = "aws-ec2-a1.png";
                const AWS_EC2_C4_IMG         = "aws-ec2-c4.png";
                const AWS_EC2_C5_IMG         = "aws-ec2-c5.png";
                const AWS_EC2_M4_IMG         = "aws-ec2-m4.png";
                const AWS_EC2_M5_IMG         = "aws-ec2-m5.png";
                const AWS_EC2_M5A_IMG        = "aws-ec2-m5a.png";
                const AWS_EC2_P2_IMG         = "aws-ec2-p2.png";
                const AWS_EC2_P3_IMG         = "aws-ec2-p3.png";
                const AWS_EC2_R4_IMG         = "aws-ec2-r4.png";
                const AWS_EC2_R5_IMG         = "aws-ec2-r5.png";
                const AWS_EC2_R5A_IMG        = "aws-ec2-r5a.png"

                var AWS_IMAGES = {};
                AWS_IMAGES[AWS_IMG]                = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQyIDc5LjE2MDkyNCwgMjAxNy8wNy8xMy0wMTowNjozOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpBNkI0RDUwM0M3NDQxMUVBODY3N0JERjAwMTQzNUE0RSIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpBNkI0RDUwNEM3NDQxMUVBODY3N0JERjAwMTQzNUE0RSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkE2QjRENTAxQzc0NDExRUE4Njc3QkRGMDAxNDM1QTRFIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkE2QjRENTAyQzc0NDExRUE4Njc3QkRGMDAxNDM1QTRFIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+riuEoQAAIMxJREFUeNrsXQecVdWZ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";
                AWS_IMAGES[AWS_VPC_IMG]            = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABECAYAAAB3TpBiAAABN2lDQ1BBZG9iZSBSR0IgKDE5OTgpAAAokZWPv0rDUBSHvxtFxaFWCOLgcCdRUGzVwYxJW4ogWKtDkq1JQ5ViEm6uf/oQjm4dXNx9AidHwUHxCXwDxamDQ4QMBYvf9J3fORzOAaNi152GUYbzWKt205Gu58vZF2aYAoBOmKV2q3UAECdxxBjf7wiA10277jTG+38yH6ZKAyNguxtlIYgK0L/SqQYxBMygn2oQD4CpTto1EE9AqZf7G1AKcv8ASsr1fBBfgNlzPR+MOcAMcl8BTB1da4Bakg7UWe9Uy6plWdLuJkEkjweZjs4zuR+HiUoT1dFRF8jvA2AxH2w3HblWtay99X/+PRHX82Vun0cIQCw9F1lBeKEuf1UYO5PrYsdwGQ7vYXpUZLs3cLcBC7dFtlqF8hY8Dn8AwMZP/fNTP8gAAAAJcEhZcwAACxMAAAsTAQCanBgAAAW7aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA1LjYtYzE0MiA3OS4xNjA5MjQsIDIwMTcvMDcvMTMtMDE6MDY6MzkgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyMC0wNy0xNlQwODoyMjozMSswMjowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjAtMDctMTZUMDg6NDc6MzIrMDI6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjAtMDctMTZUMDg6NDc6MzIrMDI6MDAiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MmIxYzI2MzgtOWFjYS0yNDQ3LWI4MWUtYmZlN2Q5YmEzMzY5IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjg3MkZDNEFEQzcyQzExRUE5M0Q2OUQ4NzM2QzdBNEM1IiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ODcyRkM0QURDNzJDMTFFQTkzRDY5RDg3MzZDN0E0QzUiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6ODcyRkM0QUFDNzJDMTFFQTkzRDY5RDg3MzZDN0E0QzUiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6ODcyRkM0QUJDNzJDMTFFQTkzRDY5RDg3MzZDN0E0QzUiLz4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MmIxYzI2MzgtOWFjYS0yNDQ3LWI4MWUtYmZlN2Q5YmEzMzY5IiBzdEV2dDp3aGVuPSIyMDIwLTA3LTE2VDA4OjQ3OjMyKzAyOjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDwvcmRmOlNlcT4gPC94bXBNTTpIaXN0b3J5PiA8L3JkZjpEZXNj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";
                AWS_IMAGES[AWS_SUBNET_PRIVATE_IMG] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQyIDc5LjE2MDkyNCwgMjAxNy8wNy8xMy0wMTowNjozOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpFRTMwOUM1OUM3NDYxMUVBODY3REU1Nzk4QzQwMURBRSIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpFRTMwOUM1QUM3NDYxMUVBODY3REU1Nzk4QzQwMURBRSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkVFMzA5QzU3Qzc0NjExRUE4NjdERTU3OThDNDAxREFFIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkVFMzA5QzU4Qzc0NjExRUE4NjdERTU3OThDNDAxREFFIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+OY4KKgAACmhJREFUeNrsXXlsHGcV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";
                AWS_IMAGES[AWS_SUBNET_PUBLIC_IMG]  = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQyIDc5LjE2MDkyNCwgMjAxNy8wNy8xMy0wMTowNjozOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpERDk2QzRERkM3NDYxMUVBODJDNEMzMDQ0NzdENDQwMiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpERDk2QzRFMEM3NDYxMUVBODJDNEMzMDQ0NzdENDQwMiI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkREOTZDNEREQzc0NjExRUE4MkM0QzMwNDQ3N0Q0NDAyIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkREOTZDNERFQzc0NjExRUE4MkM0QzMwNDQ3N0Q0NDAyIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+vmSl/QAACkRJREFUeNrsnQtQFdcZ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";
                AWS_IMAGES[AWS_EC2_IMG]            = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQyIDc5LjE2MDkyNCwgMjAxNy8wNy8xMy0wMTowNjozOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpDNjUwQ0U0M0M3NDkxMUVBQTY1MkEwMTg5RjJFQUI1NCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpDNjUwQ0U0NEM3NDkxMUVBQTY1MkEwMTg5RjJFQUI1NCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkM2NTBDRTQxQzc0OTExRUFBNjUyQTAxODlGMkVBQjU0IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkM2NTBDRTQyQzc0OTExRUFBNjUyQTAxODlGMkVBQjU0Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+376cbAAADdhJREFUeNrsXWmMHMUV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";
                AWS_IMAGES[AWS_EC2_T2_IMG]         = "data:image/png;base64,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"; 
                AWS_IMAGES[AWS_EC2_T3_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_T3A_IMG]        = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_A1_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_C4_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_C5_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_M4_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_M5_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_M5A_IMG]        = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_P2_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_P3_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_R4_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_R5_IMG]         = "data:image/png;base64,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";
                AWS_IMAGES[AWS_EC2_R5A_IMG]        = "data:image/png;base64,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";
                                
                
                function dataURIFor(imageName) {
                    // https://jgraph.github.io/drawio-tools/tools/base64.html
                    return AWS_IMAGES[imageName].replace(";base64,",",");
                }

                function replaceImagesToDataURIScheme(xml) {
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-4\.png/gm, dataURIFor(AWS_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-vpc2\.png/gm, dataURIFor(AWS_VPC_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-subnet-public\.png/gm, dataURIFor(AWS_SUBNET_PUBLIC_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-subnet-private\.png/gm, dataURIFor(AWS_SUBNET_PRIVATE_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2\.png/gm, dataURIFor("AWS_EC2_IMG") );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2\.png/gm, dataURIFor() );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-t2\.png/gm, dataURIFor(AWS_EC2_T2_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-t3\.png/gm, dataURIFor(AWS_EC2_T3_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-t3a\.png/gm, dataURIFor(AWS_EC2_T3A_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-a1\.png/gm, dataURIFor(AWS_EC2_A1_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-c4\.png/gm, dataURIFor(AWS_EC2_C4_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-c5\.png/gm, dataURIFor(AWS_EC2_C5_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-m4\.png/gm, dataURIFor(AWS_EC2_M4_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-m5\.png/gm, dataURIFor(AWS_EC2_M5_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-m5a\.png/gm, dataURIFor(AWS_EC2_M5A_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-p2\.png/gm, dataURIFor(AWS_EC2_P2_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-p3\.png/gm, dataURIFor(AWS_EC2_P3_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-r4\.png/gm, dataURIFor(AWS_EC2_R4_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-r5\.png/gm, dataURIFor(AWS_EC2_R5_IMG) );
                    xml = xml.replace(/file:\/\/\/[\.:\w+\/-]*aws-ec2-r5a\.png/gm, dataURIFor(AWS_EC2_R5A_IMG) );
                    return xml;
                }
        """
    def jsExportAsPng(self):
        return """
               var scale  = graph.view.scale;
               var bounds = graph.getGraphBounds();     
               var svgDoc = mxUtils.createXmlDocument();
               var root = (svgDoc.createElementNS != null) ? svgDoc.createElementNS(mxConstants.NS_SVG, 'svg') : svgDoc.createElement('svg');
               if (root.style != null) {
                   root.style.backgroundColor = '#FFFFFF';
               } else {
                   root.setAttribute('style', 'background-color:#FFFFFF');
               }
               
               if (svgDoc.createElementNS == null)  {
                   root.setAttribute('xmlns', mxConstants.NS_SVG);
               }
               root.setAttribute('width', Math.ceil(bounds.width * scale + 2) + 'px');
               root.setAttribute('height', Math.ceil(bounds.height * scale + 2) + 'px');   
               var imageW = Math.ceil(bounds.width * scale + 2) + 75
               var imageH = Math.ceil(bounds.height * scale + 2) + 75
               if (imageW < 800) {
                   imageW = 800;
               }
               if (imageH < 600) {
                   imageH = 600;
               }   
               root.setAttribute('xmlns:xlink', mxConstants.NS_XLINK);
               root.setAttribute('version', '1.1');   
               var group = (svgDoc.createElementNS != null) ? svgDoc.createElementNS(mxConstants.NS_SVG, 'g') : svgDoc.createElement('g');
               group.setAttribute('transform', 'translate(0.5,0.5)');
               root.appendChild(group);
               svgDoc.appendChild(root);   
               var svgCanvas = new mxSvgCanvas2D(group);
               svgCanvas.translate(Math.floor(1 / scale - bounds.x), Math.floor(1 / scale - bounds.y));
               svgCanvas.scale(scale);   
               var imgExport = new mxImageExport();
               imgExport.drawState(graph.getView().getState(graph.model.root), svgCanvas);
               var xml     = mxUtils.getXml(root);

               var html =   '<html>'
                          + ' <head>'
                          + '    <meta http-equiv="content-type" content="text/html; charset=UTF-8">'
                          + '    <title><\/title>'
                          + ' <\/head>'
                          + ' <body>'
                          + '    <div id="svg-container" style="display:none">' + xml  + '<\/div>'
                          + '    <canvas id="canvas" width="' + imageW + '" height="' + imageH + '"><\/canvas>'
                          + '    <div id="png-container"><\/div>'
                          + '    <script language="javascript">'
                          + '       var svgString = new XMLSerializer().serializeToString(document.querySelector("svg"));'
                          + '       var canvas    = document.getElementById("canvas");'
                          + '       var ctx       = canvas.getContext("2d");'
                          + '       var DOMURL    = self.URL || self.webkitURL || self;'
                          + '       var img       = new Image();'
                          + '       var svg       = new Blob([svgString], {type: "image/svg+xml;charset=utf-8"});'
                          + '       var url       = DOMURL.createObjectURL(svg);'
                          + '       img.onload = function() {'
                          + '            ctx.drawImage(img, 0, 0);'
                          + '            var png = canvas.toDataURL("image/png");'
                          + '            document.querySelector("#png-container").innerHTML = "<img src=" +  png + " download/>";'
                          + '            DOMURL.revokeObjectURL(png);'
                          + '       };'
                          + '       img.src = url;'
                          + '    <\/script>'
                          + '  <\/body>'
                          + '<\/html>';
               myWindow=window.open('','_blank','toolbar=no,scrollbars=no,resizable=yes,top=50,left=50,width=1024,height=720')
               myWindow.document.write(html);
               myWindow.focus()
        """    
    def jsMxToolBox(self, posY="88", posX=None):
        if not posX:
           posX = "(document.body.clientWidth / 2) - 120"
           
        return """
         
                """ + self.jsRemoveHTMLTags() + """

                var content = document.createElement('div');
                content.style.padding = '4px';   
                var tb = new mxToolbar(content);        
                tb.addItem('Zoom In', '""" + self.images.zoomInImagePath +"""',function(evt)
                {
                    graph.zoomIn();
                });        
                tb.addItem('Zoom Out', '""" + self.images.zoomOutImagePath +"""',function(evt)
                {
                    graph.zoomOut();
                });
                tb.addItem('Zoom Actual', '""" + self.images.view1to1ImagePath +"""',function(evt)
                {
                    graph.zoomActual();
                });
                tb.addItem('Print Preview', '""" + self.images.printerImagePath +"""',function(evt)
                {
                    var preview = new mxPrintPreview(graph,graph.zoomActual());
                    preview.open();
                });
                tb.addItem('Export PNG', '""" + self.images.exportImageImagePath +"""',function(evt)
                {
                    """ + self.jsExportAsPng()  + """
                });
                tb.addItem('Export Draw.IO mxGraphModel', '""" + self.images.modelGraphExportImagePath +"""',function(evt)
                {
                    """ + self.jsExportModelGraph() +  """
                });
                tb.addItem('Edit as Draw.IO', '""" + self.images.editDrawIoImagePath +"""',function(evt)
                {
                    """+ self.jsEditAsDrawioDiagram() + """
                });   
                toolH = (document.body.clientHeight * """ + posY + """) / 100;
                wnd = new mxWindow('Tools', content, """ + posX + """, toolH, 276, 65, true);
                wnd.setMaximizable(false);
                wnd.setScrollable(false);
                wnd.setResizable(false);
                wnd.setVisible(true);
        """    
    def jsFormatXml(self):
            return """
                    function formatXml(xml, tab) { // tab = optional indent value, default is tab (\t)
                        var formatted = '', indent= '';
                        tab = tab || '\t';
                        xml.split(/>\s*</).forEach(function(node) {
                            if (node.match( /^\/\w/ )) indent = indent.substring(tab.length); // decrease indent by one 'tab'
                            formatted += indent + '<' + node + '>\\r\\n';
                            if (node.match( /^<?\w[^>]*[^\/]$/ )) indent += tab;              // increase indent
                        });
                        return formatted.substring(1, formatted.length-3);
                    }
            """
    def jsRemoveHTMLTags(self):
            return """
                    function removeHTMLTags(xml) {
                        pureDrawIOXml = xml;
                        console.log(pureDrawIOXml);
                        //pureDrawIOXml = pureDrawIOXml.replace(//gm,' ')
                        pureDrawIOXml = pureDrawIOXml.replace(/&lt;b&gt;/gm,' ');   //<b>
                        pureDrawIOXml = pureDrawIOXml.replace(/&lt;\/b&gt;/gm,' '); //</b>
                        pureDrawIOXml = pureDrawIOXml.replace(/&lt;br&gt;/gm,' ');  //<br>
                        pureDrawIOXml = pureDrawIOXml.replace(/&lt;span style=\'color:rgb\(\d{1,3},\d{1,3},\d{1,3}\);\'&gt;[\w+|\-|\.]*&lt;\/span&gt;/gm,' ') // <span style='color:rgb(144,2,255);'>eu-central-1a</span>
                        return pureDrawIOXml; 
                    }
            """        
    def htmlCommonBody(self):
            return """
             <body onload="main(document.getElementById('graphContainer'))">
                <div id="loadingBackground" width="100%" height="100%" style="position: absolute;top: 0px;bottom: 0px;width: 100%;height: 100%;background:black; opacity: 0.1;z-index:1000;display:none;">
                </div>
                <div id="loadingMessage" style="display:inline-block;top:12%;left:12%;position:fixed;;z-index:1001;display:none;">
                      <table width="100%" height="100%">
                        <tr><td align="center"><img src='""" + self.images.loadingPath + """'/></td></tr>
                        <tr><td align="center"><font style="color:black;font-family:Consolas;font-weight:bold">Wait<br>&nbsp;&nbsp;Contacting AWS...</font></td></tr>
                      </table>
                </div>
                <div id="graphContainer"
                    style="position:relative;overflow:hidden;width:100%;height:100%;background:url('""" + self.images.gridImagePath + """');cursor:default;">
                </div>
                <form id="drawIoEdit" action="" method="POST" target="_blank"/>
            </body>
            """
    def htmlFormDrawIoEdit(self):
            return """
            <form id="drawIoEdit" action="" method="POST" target="_blank"/>
            """

class PymxGraph:

    def __init__(self, pathToResources):
        self.pathToResources = pathToResources
        self.images          = _Images(self.pathToResources)
        self.htmlSnippets    = _HtmlSnippets(self.pathToResources, self.images, "http://127.0.0.1:5679/")

    def startHttpServer(self):
        httpServer = HttpServer()
        httpServer.run()

    def drawFolding(self):
        html = """
        <html>
          <head>
             """ + self.htmlSnippets.htmlTitle('Hi There!') + """
             """ + self.htmlSnippets.jsLibraries()        + """
             <script type="text/javascript">
                 function main(container)
                 {
                     """ + self.htmlSnippets.jsBrowserNotSupported() + """
                     else
                     {
                         // Enables crisp rendering of rectangles in SVG
                         mxConstants.ENTITY_SEGMENT = 20;
                         
                         // Creates the graph inside the given container
                         var graph = new mxGraph(container);
                         graph.setDropEnabled(true);
                         
                         // Disables global features
                         graph.collapseToPreferredSize = false;
                         graph.constrainChildren = false;
                         graph.cellsSelectable = false;
                         graph.extendParentsOnAdd = false;
                         graph.extendParents = false;
                         graph.border = 10;
         
                         // Sets global styles
                         var style = graph.getStylesheet().getDefaultEdgeStyle();
                         style[mxConstants.STYLE_EDGE] = mxEdgeStyle.EntityRelation;
                         style[mxConstants.STYLE_ROUNDED] = true;
         
                         style = graph.getStylesheet().getDefaultVertexStyle();
                         style[mxConstants.STYLE_FILLCOLOR] = '#ffffff';
                         style[mxConstants.STYLE_SHAPE] = 'swimlane';
                         style[mxConstants.STYLE_STARTSIZE] = 30;
                         
                         style = [];
                         style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_RECTANGLE;
                         style[mxConstants.STYLE_STROKECOLOR] = 'none';
                         style[mxConstants.STYLE_FILLCOLOR] = 'none';
                         style[mxConstants.STYLE_FOLDABLE] = false;
                         graph.getStylesheet().putCellStyle('column', style);

                         // Installs auto layout for all levels
                         var layout = new mxStackLayout(graph, true);
                         layout.border = graph.border;
                         var layoutMgr = new mxLayoutManager(graph);
                         layoutMgr.getLayout = function(cell)
                         {
                             if (!cell.collapsed)
                             {
                                 if (cell.parent != graph.model.root)
                                 {
                                     layout.resizeParent = true;
                                     layout.horizontal = false;
                                     layout.spacing = 10;
                                 }
                                 else
                                 {
                                     layout.resizeParent = true;
                                     layout.horizontal = true;
                                     layout.spacing = 40;
                                 }
                                 
                                 return layout;
                             }
                             
                             return null;
                         };

                         """ +  self.htmlSnippets.jsMxToolBox() + """
                         
                         // Gets the default parent for inserting new cells. This
                         // is normally the first child of the root (ie. layer 0).
                         var parent = graph.getDefaultParent();
                                         
                         // Adds cells to the model in a single step
                         graph.getModel().beginUpdate();
                         try
                         {
                             var col1 = graph.insertVertex(parent, null, '', 0, 0, 120, 0, 'column');
                             
                             var v1 = graph.insertVertex(col1, null, '1', 0, 0, 100, 30);
                             v1.collapsed = true;
                             
                             var v11 = graph.insertVertex(v1, null, '1.1', 0, 0, 80, 30);
                             v11.collapsed = true;
                             
                             var v111 = graph.insertVertex(v11, null, '1.1.1', 0, 0, 60, 30);
                             var v112 = graph.insertVertex(v11, null, '1.1.2', 0, 0, 60, 30);
                             
                             var v12 = graph.insertVertex(v1, null, '1.2', 0, 0, 80, 30);
                             
                             var col2 = graph.insertVertex(parent, null, '', 0, 0, 120, 0, 'column');
                             
                             var v2 = graph.insertVertex(col2, null, '2', 0, 0, 100, 30);
                             v2.collapsed = true;
                             
                             var v21 = graph.insertVertex(v2, null, '2.1', 0, 0, 80, 30);
                             v21.collapsed = true;
         
                             var v211 = graph.insertVertex(v21, null, '2.1.1', 0, 0, 60, 30);
                             var v212 = graph.insertVertex(v21, null, '2.1.2', 0, 0, 60, 30);
                             
                             var v22 = graph.insertVertex(v2, null, '2.2', 0, 0, 80, 30);
         
                             var v3 = graph.insertVertex(col2, null, '3', 0, 0, 100, 30);
                             v3.collapsed = true;
         
                             var v31 = graph.insertVertex(v3, null, '3.1', 0, 0, 80, 30);
                             v31.collapsed = true;
         
                             var v311 = graph.insertVertex(v31, null, '3.1.1', 0, 0, 60, 30);
                             var v312 = graph.insertVertex(v31, null, '3.1.2', 0, 0, 60, 30);
                             
                             var v32 = graph.insertVertex(v3, null, '3.2', 0, 0, 80, 30);
                             
                             graph.insertEdge(parent, null, '', v111, v211);
                             graph.insertEdge(parent, null, '', v112, v212);
                             graph.insertEdge(parent, null, '', v112, v22);
         
                             graph.insertEdge(parent, null, '', v12, v311);
                             graph.insertEdge(parent, null, '', v12, v312);
                             graph.insertEdge(parent, null, '', v12, v32);
                         }
                         finally
                         {
                             // Updates the display
                             graph.getModel().endUpdate();
                         }
                     }
                 };
                 """ + self.htmlSnippets.jsFormatXml() + """
             </script>
             """ + self.htmlSnippets.htmlCommonBody() + """
          </head>
        </html>
        """
        self.openHTML(html)

    def drawTree(self):
        html = """
        <html>
         <head>
            """ + self.htmlSnippets.htmlTitle('Tree') + """
            """ + self.htmlSnippets.jsLibraries()        + """
            <script type="text/javascript">
                /*
                    Defines a custom shape for the tree node that includes the
                    upper half of the outgoing edge(s).
                */
                function TreeNodeShape() { };
        
                TreeNodeShape.prototype = new mxCylinder();
                TreeNodeShape.prototype.constructor = TreeNodeShape;
        
                // Defines the length of the upper edge segment.
                TreeNodeShape.prototype.segment = 20;
        
                // Needs access to the cell state for rendering
                TreeNodeShape.prototype.apply = function(state)
                {
                    mxCylinder.prototype.apply.apply(this, arguments);
                    this.state = state;
                };
                
                TreeNodeShape.prototype.redrawPath = function(path, x, y, w, h, isForeground)
                {
                    var graph = this.state.view.graph;
                    var hasChildren = graph.model.getOutgoingEdges(this.state.cell).length > 0;
                    
                    if (isForeground)
                    {
                        if (hasChildren)
                        {
                            // Painting outside of vertex bounds is used here
                            path.moveTo(w / 2, h + this.segment);
                            path.lineTo(w / 2, h);
                            path.end();
                        }
                    }
                    else
                    {
                        path.moveTo(0, 0);
                        path.lineTo(w, 0);
                        path.lineTo(w, h);
                        path.lineTo(0, h);
                        path.close();
                    }
                };
                
                mxCellRenderer.registerShape('treenode', TreeNodeShape);
        
                // Defines a custom perimeter for the nodes in the tree
                mxGraphView.prototype.updateFloatingTerminalPoint = function(edge, start, end, source)
                {
                    var pt = null;
                    
                    if (source)
                    {
                        pt = new mxPoint(start.x + start.width / 2,
                                start.y + start.height + TreeNodeShape.prototype.segment);
                    }
                    else
                    {
                        pt = new mxPoint(start.x + start.width / 2, start.y);
                    }
        
                    edge.setAbsoluteTerminalPoint(pt, source);
                };
            </script>
    
            <script type="text/javascript">
                function main()
                {
                    """ + self.htmlSnippets.jsBrowserNotSupported() + """
                    else
                    {
                        mxGraph.prototype.collapsedImage = new mxImage('""" + self.images.collapsedImagePath + """', 9, 9);
                        mxGraph.prototype.expandedImage = new mxImage('""" + self.images.expandedImagePath + """', 9, 9);

                        var container = document.createElement('div');
                        container.style.position = 'absolute';
                        container.style.overflow = 'hidden';
                        container.style.left = '0px';
                        container.style.top = '0px';
                        container.style.right = '0px';
                        container.style.bottom = '0px';
                        
                        if (mxClient.IS_IE) {
                            new mxDivResizer(container);
                        }

                        document.body.appendChild(container);

                        var graph = new mxGraph(container);

                        graph.keepEdgesInBackground = true;

                        var style = graph.getStylesheet().getDefaultVertexStyle();
                        style[mxConstants.STYLE_SHAPE] = 'treenode';
                        style[mxConstants.STYLE_GRADIENTCOLOR] = 'white';
                        style[mxConstants.STYLE_SHADOW] = true;
                        
                        style = graph.getStylesheet().getDefaultEdgeStyle();
                        style[mxConstants.STYLE_EDGE] = mxEdgeStyle.TopToBottom;
                        style[mxConstants.STYLE_ROUNDED] = true;

                        graph.setAutoSizeCells(true);
                        graph.setPanning(true);
                        graph.panningHandler.useLeftButtonForPanning = true;

                        var keyHandler = new mxKeyHandler(graph);
                        var layout = new mxCompactTreeLayout(graph, false);
                        layout.useBoundingBox = false;
                        layout.edgeRouting = false;
                        layout.levelDistance = 30;
                        layout.nodeDistance = 10;

                        // To allow wrapping
                        graph.setHtmlLabels(true);

                        var layoutMgr = new mxLayoutManager(graph);

                        layoutMgr.getLayout = function(cell) {
                            if (cell.getChildCount() > 0)
                            {
                                return layout;
                            }
                        };

                        graph.setCellsSelectable(false);

                        graph.isCellFoldable = function(cell) {
                            return this.model.getOutgoingEdges(cell).length > 0;
                        };
        
                        // Defines the position of the folding icon
                        graph.cellRenderer.getControlBounds = function(state) {
                            if (state.control != null) {
                                var oldScale = state.control.scale;
                                var w = state.control.bounds.width / oldScale;
                                var h = state.control.bounds.height / oldScale;
                                var s = state.view.scale;			
        
                                return new mxRectangle(state.x + state.width / 2 - w / 2 * s,
                                    state.y + state.height + TreeNodeShape.prototype.segment * s - h / 2 * s,
                                    w * s, h * s);
                            }
                            
                            return null;
                        };

                        // Implements the click on a folding icon
                        graph.foldCells = function(collapse, recurse, cells)
                        {
                            this.model.beginUpdate();
                            try
                            {
                                toggleSubtree(this, cells[0], !collapse);
                                this.model.setCollapsed(cells[0], collapse);
        
                                // Executes the layout for the new graph since
                                // changes to visiblity and collapsed state do
                                // not trigger a layout in the current manager.
                                layout.execute(graph.getDefaultParent());
                            }
                            finally
                            {
                                this.model.endUpdate();
                            }
                        };

                        
                        """ +  self.htmlSnippets.jsMxToolBox() + """

                        // Gets the default parent for inserting new cells. This
                        // is normally the first child of the root (ie. layer 0).
                        var parent = graph.getDefaultParent();
                                        
                        // Adds the root vertex of the tree
                        graph.getModel().beginUpdate();
                        try
                        {
                            var widthLeaf  = 120;
                            var heightLeaf = 50;

                            var w = graph.container.offsetWidth;
                            var root = graph.insertVertex(parent, 'treeRoot', 'Root for the all tree, this must wrap', w/2 - 30, 20, widthLeaf, heightLeaf,'whiteSpace=wrap;');
        
                            var v1 = graph.insertVertex(parent, 'v1', 'Child 1', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', root, v1);
                            
                            var v2 = graph.insertVertex(parent, 'v2', 'Child 2', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', root, v2);
        
                            var v3 = graph.insertVertex(parent, 'v3', 'Child 3', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', root, v3);
                            
                            var v11 = graph.insertVertex(parent, 'v11', 'Child 1.1', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', v1, v11);
                            
                            var v12 = graph.insertVertex(parent, 'v12', 'Child 1.2', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', v1, v12);
                            
                            var v21 = graph.insertVertex(parent, 'v21', 'Child 2.1', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', v2, v21);
                            
                            var v22 = graph.insertVertex(parent, 'v22', 'Child 2.2', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', v2, v22);
                            
                            var v221 = graph.insertVertex(parent, 'v221', 'Child 2.2.1', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', v22, v221);
                            
                            var v222 = graph.insertVertex(parent, 'v222', 'Child 2.2.2', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', v22, v222);
        
                            var v31 = graph.insertVertex(parent, 'v31', 'Child 3.1', 0, 0, widthLeaf, heightLeaf);
                            graph.insertEdge(parent, null, '', v3, v31);

                            toggleSubtree(graph, v2, false);
                            graph.model.setCollapsed(v2, true);
                            layout.execute(graph.getDefaultParent());
                        }
                        finally
                        {
                            // Updates the display
                            graph.getModel().endUpdate();
                        }
                    }
                };
                // Updates the visible state of a given subtree taking into
                // account the collapsed state of the traversed branches
                function toggleSubtree(graph, cell, show)
                {
                    show = (show != null) ? show : true;
                    var cells = [];
                    
                    graph.traverse(cell, true, function(vertex)
                    {
                        if (vertex != cell)
                        {
                            cells.push(vertex);
                        }
        
                        // Stops recursion if a collapsed cell is seen
                        return vertex == cell || !graph.isCellCollapsed(vertex);
                    });
        
                    graph.toggleCells(show, cells, true);
                };

                """ + self.htmlSnippets.jsFormatXml() + """
            </script>
         </head>
            <body onload="main();">
            </body>
            """ + self.htmlSnippets.htmlFormDrawIoEdit() + """
        </html>
        """
        self.openHTML(html)

    def helloWorld(self):
        html = """
        <html>
         <head>
            """ + self.htmlSnippets.htmlTitle('Hi There!') + """
            """ + self.htmlSnippets.jsLibraries()        + """
            <script type="text/javascript">
                function main(container)
                {
                    """ + self.htmlSnippets.jsBrowserNotSupported() + """
                    else
                    {
                        mxEvent.disableContextMenu(container);

                        var root = new mxCell();
                        var layer0 = root.insert(new mxCell());
                        var layer1 = root.insert(new mxCell()); 
                        var model = new mxGraphModel(root);
                        
                        var graph = new mxGraph(container, model);
                        graph.setPanning(true);
                        graph.centerZoom = false;
                        graph.panningHandler.useLeftButtonForPanning = true;

                        """ +  self.htmlSnippets.jsMxToolBox() + """

                        var highlight = new mxCellTracker(graph, '#00FF00');

                        // Enables rubberband selection
                        new mxRubberband(graph);
                        
                        // Gets the default parent for inserting new cells. This
                        // is normally the first child of the root (ie. layer 0).
                        var parent = graph.getDefaultParent();
                                        
                        // Adds cells to the model in a single step
                        model.beginUpdate();
                        try
                        {
                            //var v1 = graph.insertVertex(layer0, null, 'Hello,', 20, 20, 80, 30,'fillColor=blue');
                            var v1 = graph.insertVertex(layer0, null, 'Hello,', 20, 20, 80, 30,'"""+ STYLE_EC2 +"""');
                            var v2 = graph.insertVertex(layer0, null, 'World!', 200, 150, 80, 30,'"""+ STYLE_EC2 +"""');
                            var e1 = graph.insertEdge(layer1, null, '', v1, v2);
                        }
                        finally
                        {
                            model.endUpdate();
                        }
                        document.body.appendChild(mxUtils.button('Show/Hide Layer 0', function()
                        {
                           model.setVisible(layer0, !model.isVisible(layer0));
                        }));
                        document.body.appendChild(mxUtils.button('Show/Hide Layer 1', function()
                        {
                            model.setVisible(layer1, !model.isVisible(layer1));
                        }));
                    }
                };
                """ + self.htmlSnippets.jsFormatXml() + """
            </script>
         </head>
         """ + self.htmlSnippets.htmlCommonBody() + """
        </html>
        """
        self.openHTML(html)

    def openHTML(self,html):
        fileName = "mxgraph-file.html"
        try:
            os.remove(fileName)
        except OSError:
            pass
        print(html)
        with open(fileName, "w") as file:
            file.write(html)
        webbrowser.open('file://' + os.path.realpath(fileName))

if __name__ == '__main__':
    pathToResources = "." + sys.argv[0].lower().replace("pymxgraph.py","").replace("\\","")
    pymxGraph = PymxGraph(pathToResources)
    pymxGraphTree = PymxGraphTree(pathToResources, pymxGraph.images, pymxGraph.htmlSnippets)
    pymxGraphTree.drawTree()
    #pymxGraphAwsNavigator = PymxGraphAwsNavigator(pathToResources, pymxGraph.images, pymxGraph.htmlSnippets)
    #pymxGraphAwsNavigator.drawAwsNavigator()
    #pymxgraph.helloWorld()
    #pymxgraph.drawTree()
    #pymxgraph.drawFolding()
    #pymxGraph.drawAwsNavigator();
    
    
