# coding=utf-8
#
# Author: Ualter Otoni Pereira
# ualter.junior@gmail.com
#

import os, sys
import math
from pyawscp.Utils import Utils, Style

class Leaf:
    def __init__(self, label):
        self.order       = 0
        self.label       = label
        self.leaves      = []
        self.parent      = None
        self.colSize     = 0
        self.marginSize  = 0
        self.level       = 0
        self.center      = 0
        self.widthBox    = 0
        self.offset      = 0
        self.prevSibling = None
        self.nextSibling = None

    def add(self, leaf):
        leaf.parent = self
        if len(self.leaves) > 0:
           self.leaves[-1].nextSibling = leaf
           leaf.prevSibling = self.leaves[-1]
        self.leaves.append(leaf) 
    def childLeaves(self):
        return self.leaves
    def qtdeChildLeaves(self):
        return len(self.leaves)
    def hasChildren(self):
        if self.qtdeChildLeaves() > 0:
           return True
        return False
    def myRealSize(self):
        return int(self.marginSize + self.widthBox + self.offset)


class Layout:
    def __init__(self, layout):
       self._layout           = layout
       self._background       = [" "," "]
       #self._background       = ["•","░"]
       self._fill             = [" "," "]
       self._lateralBar       = ["|","│"]
       self._line             = ["-","─"]  
       self._topRightCorner   = ["+","┐"]
       self._topLeftCorner    = ["+","┌"]
       self._belowRightCorner = ["+","┘"]
       self._belowLeftCorner  = ["+","└"]
       
    def fill(self):
       return self._fill[self._layout-1]
    def lateralBar(self):
       return str(self._lateralBar[self._layout-1])
    def line(self):
       return str(self._line[self._layout-1])      
    def topRightCorner(self):
       return self._topRightCorner[self._layout-1]
    def topLeftCorner(self):
       return self._topLeftCorner[self._layout-1]   
    def belowRightCorner(self):
       return self._belowRightCorner[self._layout-1]
    def belowLeftCorner(self):
       return self._belowLeftCorner[self._layout-1]      
    def background(self):
       return self._background[self._layout-1]   
        
class PyAsciiGraphs:
    def __init__(self):
        self.layoutOpt  = 2
        self.structure  = ""
        _rows, _columns = os.popen('stty size', 'r').read().split()
        self.columns    = int(_columns)
        self.rows       = int(_rows)
        self.center     = int(self.columns / 2)
        self.layout     = Layout(self.layoutOpt)

        self.tree            = {} 
        self.treeSplitColumn = 0
        self.treeQtdeColumn  = 0

    def replicate(self,qtde,chars=" "):
        return chars.ljust(qtde,chars)

    def drawBox(self, labelContent, _cols=None, offset=0, printMe=True):
        lines = []
        if not _cols:
           cols = self.columns
        else:
           cols = _cols   
        center  = int(cols / 2)

        widthBox    = len(labelContent) + 2
        margin      = "".ljust(cols - (int(widthBox / 2) + center),self.layout.background())
        margin     += "".ljust(offset,self.layout.background())
        topLine     = margin + self.layout.topLeftCorner() + ( self.replicate(widthBox,self.layout.line())  ) + self.layout.topRightCorner()
        middleLine  = margin + self.layout.lateralBar() + self.layout.fill() + Style.GREEN + labelContent + Style.RESET + self.layout.fill() + self.layout.lateralBar()
        bottomLine  = margin + self.layout.belowLeftCorner() + ( self.replicate(widthBox,self.layout.line()) ) + self.layout.belowRightCorner()

        lines.append(topLine)
        lines.append(middleLine)
        lines.append(bottomLine)
        if printMe:
           for l in lines:
               print(l)

    def createTree(self,rootLeaf):
        self.createTreeLeaves(rootLeaf,0)

    def labelSize(self,label,length):
        return label + "".ljust(length-len(label)," ")

    def printTreeData(self):
        header  = self.labelSize("Label",30) + " | " + self.labelSize("Parent",25) + " | " + \
                 self.labelSize("Level",10) + " | " + self.labelSize("Order",10) + " | " + self.labelSize("ColSize",10) + " | " + \
                 self.labelSize("MarginSize",10) + " | " + self.labelSize("Center",10) + " | " + self.labelSize("WidthBox",10)
        print(header)
        for level in self.tree:
            for order in self.tree[level]:
                label      = self.labelSize(level + "," + order + "--> " + self.tree[level][order]["leaf"].label,30)
                parent     = self.labelSize(self.tree[level][order]["leaf"].parent.label if self.tree[level][order]["leaf"].parent else " ",25)
                _level     = self.labelSize(str(self.tree[level][order]["leaf"].level),10)
                _order     = self.labelSize(str(self.tree[level][order]["leaf"].order),10)
                colSize    = self.labelSize(str(self.tree[level][order]["leaf"].colSize),10)
                center     = self.labelSize(str(self.tree[level][order]["leaf"].center),10)
                marginSize = self.labelSize(str(self.tree[level][order]["leaf"].marginSize),10)
                widthBox   = self.labelSize(str(len(self.tree[level][order]["leaf"].label) +  2),10)

                line  = label + " | " + parent + " | " + _level + " | " + _order + " | " + colSize + " | " + marginSize + " | " + center + " | " + widthBox
                print(line)
            print("-".ljust(150,"-"))    

    def printIds(self,parent)         :
        for leaf in parent.leaves:
            label = leaf.label + "".ljust(8-len(leaf.label)," ")
            print(label + " level=" + str(leaf.level) + ", order=" + str(leaf.order))   
            self.printIds(leaf)

    def createTreeLeaves(self,parent,level):
        if str(level) not in self.tree:
           self.tree[str(level)] = {}
        parent.level = level
        #print(parent.label + ", level=" + str(parent.level) + ", order=" + str(parent.order))
        level += 1
        order  = 1
        if len(parent.leaves):
           if self.treeSplitColumn == 0 and len(parent.leaves) > 1:
              self.treeQtdeColumn  = len(parent.leaves)
              self.treeSplitColumn = level
           for leaf in parent.leaves:
               leaf.level = level
               leaf.order = order
               
               if str(level) not in self.tree:
                  self.tree[str(level)] = {}
               self.tree[str(level)][str(parent.order) + "." + str(order)] = {"leaf":leaf}

               #print(" ------> " + leaf.label + ", level=" + str(leaf.level) + ", order=" + str(leaf.order))
               self.createTreeLeaves(leaf,level)
               order += 1

    def calculateOffsetLeaf(self, leaf):
        # First get the level of the first column split of the tree, where all started to be in separated columns   
        orderParent     = 0
        orderGranParent = 0
        l               = leaf
        while True:
            if l.parent and l.parent.level == self.treeSplitColumn:
               orderParent = l.parent.order
               if l.parent.parent: 
                  orderGranParent = l.parent.parent.order
               break
            if not l.parent:
               break
            l = l.parent

        # Once found, if found, check if the neighbor main column has something printed or is empty
        if orderParent > 0:
           orderParentNeighbor = int(orderParent) - 1

           # Check if there is a neighbor for its parent
           keyLeaf = str(orderGranParent) + "." + str(orderParentNeighbor)
           if keyLeaf in self.tree[str(self.treeSplitColumn)]:
              parentNeighborLeaf = self.tree[str(self.treeSplitColumn)][str(keyLeaf)]["leaf"]
              colSizeNeighbor    = parentNeighborLeaf.colSize
              hasChildren        = parentNeighborLeaf.hasChildren()
              if not hasChildren:
                 offset = colSizeNeighbor * orderParentNeighbor
                 #print("leaf:" + leaf.label +  ", orderParent=" + str(orderParent) +  ", colSizeNeighbor=" + str(colSizeNeighbor) +  ", hasChildren=" + str(hasChildren)\
                 #    +  ", offset=" + str(offset)) 
                 return offset
              else:
                 # Sum all the spaces occupied - the column total size  (Starting from the )
                 if (leaf.level - parentNeighborLeaf.level) > 1: 
                    # Not Ok, we should go down until find the rigth above level (diff 1, between Level child and parent)
                    # Go down 1 level below
                    levelsBelow = 1
                    nextLevel   = parentNeighborLeaf.level + 1
                    while  (leaf.level - nextLevel) > 1:
                      nextLevel   += 1
                      levelsBelow += 1
                    keyLeaf = str(orderGranParent + levelsBelow) + "." + str(orderParentNeighbor)
                    while keyLeaf not in self.tree[str(nextLevel)]:
                        # In case there's no neighbor direct parent, we go again in reverse direction (going up) to find the first neighbor parent level with leaves
                        nextLevel -= 1
                    parentNeighborLeaf = self.tree[str(nextLevel)][str(keyLeaf)]["leaf"]

                 # Calculate how many offset according the sum of colsizes of the children neighbor, 
                 # minus the colsize of the parent neighbor (difference)
                 spaceOcuppiedChildren = 0
                 for l in parentNeighborLeaf.leaves:
                     #spaceOcuppiedChildren += l.colSize
                     spaceOcuppiedChildren += l.myRealSize()
                 offset = parentNeighborLeaf.colSize - spaceOcuppiedChildren

                 # Just in case
                 if offset < 0:
                    offset = 0
                 return offset
        return 0    

    def offSetByCalculatingSpaceNotOccupiedByChildren(self, parentLeaf):
        spaceOcuppiedChildren = 0
        for l in parentLeaf.leaves:
            spaceOcuppiedChildren += l.myRealSize()
        offset = parentLeaf.colSize - spaceOcuppiedChildren
        return offset

    def calculateLayout(self):
        for _level in self.tree:
           if int(_level) > 0:
              for _order in self.tree[str(_level)]:
                  leaf        = self.tree[str(_level)][str(_order)]["leaf"]
                  #qtdeColumns = len(self.tree[str(_level)])
                  qtdeColumns = len(leaf.parent.leaves)

                  if int(_level) == 1:
                     colSpace = math.ceil( self.columns / qtdeColumns )
                  else:
                     parent   = leaf.parent
                     colSpace = math.ceil( parent.colSize /  qtdeColumns )   

                  center          = math.ceil(colSpace / 2)
                  widthBox        = len(Utils.removeCharsColors(leaf.label)) + 2
                  marginSize      = colSpace - (math.ceil(widthBox / 2) + center)
                  leaf.center     = center
                  leaf.colSize    = colSpace
                  leaf.widthBox   = widthBox
                  leaf.marginSize = marginSize

    def drawTree(self,rootLeaf):
        self.createTree(rootLeaf)
        self.calculateLayout()
        #self.printTreeData()
        # Only the root, the simplest thing
        self.drawBox(rootLeaf.label)
        # Print the Tree
        Matrix = {}
        for level in self.tree:
            totalColumnSize = 0
            Matrix[str(level)] = {}
            Matrix[str(level)]["topLine"]    = ""
            Matrix[str(level)]["middleLine"] = ""
            Matrix[str(level)]["bottomLine"] = ""
            for _order in self.tree[level]:
                leaf        = self.tree[str(level)][str(_order)]["leaf"]
                parentOrder = int(_order.split(".")[0])
                order       = int(_order.split(".")[1])

                #print(leaf.label)
                offset = 0
                if int(level) == self.treeSplitColumn:
                   # Second Line after root
                   baseColSize = leaf.colSize
                   
                if int(order) > 1 and int(level) == self.treeSplitColumn:
                   # how many main columns is built the tree (the first line that split in columns)
                   remainingSize = (baseColSize * (int(order)-1)) - totalColumnSize
                   if remainingSize > 0:
                      offset = offset + remainingSize  
                else:
                   # For the rest of levels, we need to check the "neighbor" column spaces printed (based on the level 1)
                   # Because if nothing is there, we need to "paint" the empty space to let the position properly idented
                   if int(order) == 1:
                      offset = self.calculateOffsetLeaf(leaf)
                   else:
                      diff = leaf.colSize - (len(leaf.label) + 2 + leaf.marginSize)   
                      offset = self.calculateOffsetLeaf(leaf)
                      if diff > 0:
                         offset = diff

                #print(leaf.label)
                #print("order="+str(order)) 
                #print("marginSize="+str(offset)) 
                #print("offset="+str(offset)) 
                #print("baseColSize="+str(baseColSize)) 
                #print("totalColumnSize="+str(totalColumnSize)) 
                #print("---")

                #marginSpaces = "|".ljust(leaf.marginSize - 1,self.layout.background())
                marginSpaces = "".ljust(leaf.marginSize,self.layout.background())
                offsetSpaces = "".ljust(offset,self.layout.background())

                leaf.offset = offset

                topLine     = offsetSpaces + marginSpaces + self.layout.topLeftCorner() + ( self.replicate(leaf.widthBox,self.layout.line())  ) + self.layout.topRightCorner()
                middleLine  = offsetSpaces + marginSpaces + self.layout.lateralBar() + self.layout.fill() + Style.GREEN + leaf.label + Style.RESET + self.layout.fill() + self.layout.lateralBar()
                bottomLine  = offsetSpaces + marginSpaces + self.layout.belowLeftCorner() + ( self.replicate(leaf.widthBox,self.layout.line()) ) + self.layout.belowRightCorner()

                Matrix[str(level)]["topLine"]    += topLine
                Matrix[str(level)]["middleLine"] += middleLine
                Matrix[str(level)]["bottomLine"] += bottomLine

                totalColumnSize += len(Utils.removeCharsColors(middleLine))
                #print(middleLine + "| --> " + str(totalColumnSize))

        for l in Matrix:
            if len(Matrix[l]["topLine"]) > 0:
               print(Matrix[l]["topLine"])
               print(Matrix[l]["middleLine"])
               print(Matrix[l]["bottomLine"])
        # End Print the Tree

def testTree1():
    pygraph = PyAsciiGraphs()

    rootLeaf = Leaf("Root")

    l1_0 = Leaf("1.0")
    l2_0 = Leaf("2.0")
    l3_0 = Leaf("3.0")

    l1_1 = Leaf("1.1")
    l1_2 = Leaf("1.2")

    l2_1 = Leaf("2.1")
    l2_2 = Leaf("2.2")
    l2_3 = Leaf("2.3")

    l3_1 = Leaf("3.1")
    l3_2 = Leaf("3.2")

    l1_0.add(l1_1)
    l1_0.add(l1_2)

    l2_0.add(l2_1)
    l2_0.add(l2_2)
    l2_0.add(l2_3)

    l3_0.add(l3_1)
    l3_0.add(l3_2)

    rootLeaf.add(l1_0)
    rootLeaf.add(l2_0)
    rootLeaf.add(l3_0)

    pygraph.drawTree(rootLeaf)

def test2():
    pygraph = PyAsciiGraphs()

    rootLeaf = Leaf("services.com.uk")
    site1 = Leaf("site1.services.com.uk")
    site2 = Leaf("site2.services.com.uk")
    site1London = Leaf("london.site2.services.com.uk")
    site2irish  = Leaf("irih.site2.services.com.uk")
    site2wales  = Leaf("wals.site2.services.com.uk")


    #site1.add(site1London)
    site1.add(Leaf("liverpool.site2.services.com.uk"))

    site2dublin = Leaf("dublin.irih.site2.services.com.uk")   
    site2irish.add(site2dublin) 

    site2.add(site2irish)
    site2.add(site2wales)
    rootLeaf.add(site1)
    rootLeaf.add(site2)
    pygraph.drawTree(rootLeaf)

def test3():
    pygraph = PyAsciiGraphs()

    rootLeaf = Leaf("AAAAAA")
    site1 = Leaf("BBBBB")
    site2 = Leaf("CCCCC")
    site3 = Leaf("DDDDD")

    b10 = Leaf("B1.0")
    b20 = Leaf("B2.0")
    #site1.add(b10)
    #site1.add(b20)

    d10 = Leaf("D1.0")
    d101 = Leaf("D1.0.1")
    d102 = Leaf("D1.0.2")
    dx   = Leaf("D1.0.1.1")
    d101.add(dx)
    d10.add(d101)
    d10.add(d102)
    d20 = Leaf("D2.0")
    site3.add(d10)
    site3.add(d20)

    rootLeaf.add(site1)
    rootLeaf.add(site2)
    rootLeaf.add(site3)
    pygraph.drawTree(rootLeaf)

def test4():
    pygraph = PyAsciiGraphs()

    rootLeaf = Leaf("services.com.uk")
    site1 = Leaf("site1.services.com.uk")

    elb = Leaf("elb")

    target1 = Leaf("Target Group 1")
    target2 = Leaf("Target Group 2")

    ec1 = Leaf("EC2 1")
    ec2 = Leaf("EC2 2")
    ec3 = Leaf("EC2 3")
    ec4 = Leaf("EC2 4")

    target1.add(ec1)
    target1.add(ec2)
    target2.add(ec3)
    target2.add(ec4)
    elb.add(target1)
    elb.add(target2)

    site1.add(elb)
    rootLeaf.add(site1)
    #if pygraph.columns > 150:
    #   pygraph.columns = 150
    pygraph.drawTree(rootLeaf)

def test5():
    pygraph = PyAsciiGraphs()

    rootLeaf = Leaf("Root")
    l1_0 = Leaf("1.0")
    l2_0 = Leaf("2.0")

    l1_1 = Leaf("1.1")
    l1_0.add(l1_1)

    l2_1 = Leaf("2.1")
    l2_2 = Leaf("2.2")
    l2_3 = Leaf("2.3")
    l2_4 = Leaf("2.4")
    l2_1_1 = Leaf("2.1.1")
    l2_1_2 = Leaf("2.1.2")
    
    l2_1_2.add(Leaf("2.1.2.1"))

    l2_1.add(l2_1_1)
    l2_1.add(l2_1_2)

    l2_0.add(l2_1)
    l2_0.add(l2_2)
    l2_0.add(l2_3)
    l2_0.add(l2_4)

    rootLeaf.add(l1_0)
    rootLeaf.add(l2_0)
    rootLeaf.add(Leaf("3.0"))
    pygraph.drawTree(rootLeaf)

def test6():
    pygraph = PyAsciiGraphs()

    rootLeaf = Leaf("Root")
    l1_0 = Leaf("1.0")
    l2_0 = Leaf("2.0")
    l3_0 = Leaf("3.0")

    #l1_0.add(Leaf("1.1"))

    l3_1 = Leaf("3.1")
    l3_2 = Leaf("3.2")
    l3_3 = Leaf("3.3")
    l3_4 = Leaf("3.4")
    l3_1_1 = Leaf("3.1.1")
    l3_1_2 = Leaf("3.1.2")
    
    l3_1_2.add(Leaf("3.1.2.1"))

    l3_1.add(l3_1_1)
    l3_1.add(l3_1_2)

    l3_0.add(l3_1)
    l3_0.add(l3_2)
    l3_0.add(l3_3)
    l3_0.add(l3_4)

    rootLeaf.add(l1_0)
    rootLeaf.add(l2_0)
    rootLeaf.add(l3_0)
    pygraph.columns = 188
    pygraph.drawTree(rootLeaf)    

if __name__ == '__main__':
    testTree1()
    #print("\n**********************************************************************************************\n")
    #test2()
    #print("\n**********************************************************************************************\n")
    #test4()
    #print("\n**********************************************************************************************\n")
    #test5()
    #print("\n**********************************************************************************************\n")
    #test6()
   

    
    

        






