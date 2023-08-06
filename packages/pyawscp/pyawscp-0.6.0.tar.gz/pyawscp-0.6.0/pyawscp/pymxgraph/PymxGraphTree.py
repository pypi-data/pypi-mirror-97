import webbrowser
import os, sys
import threading


class PymxGraphTree:

    def __init__(self, pathToResources, images, htmlSnippets):
        self.pathToResources = pathToResources
        self.images          = images
        self.htmlSnippets    = htmlSnippets

    def openHTML(self,html):
        directory = os.path.dirname(os.path.realpath(__file__))
        fileName  = os.path.join(str(directory),"tree.html")
        try:
            os.remove(fileName)
        except OSError:
            pass

        with open(fileName, "w") as file:
            file.write(html)
        webbrowser.open('file://' + os.path.realpath(fileName))    


    def drawTree(self, objTree):
        html = """
        <html>
         <head>
            """ + self.htmlSnippets.htmlTitle('Tree') + """
            """ + self.htmlSnippets.jsLibraries()        + """
            <script type="text/javascript">
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
                            """ + objTree + """
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
