import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
import random
from matplotlib.lines import Line2D


class Mondrian:
    def __init__(self):
        self.attributes = [[],[],[]]
        self.DEFAULT_COLOUR = 'white'

    def isValid(self):
        """Check whether representation is valid"""

        # Check vertical lines are valid
        valid = True
        for l in self.attributes[0]:
            for i in l.lineValues:
                if i >= len(self.attributes[1]):
                    valid = False

                    
        # Check horizontal lines are valid
        for l in self.attributes[1]:
            for i in l.lineValues:
                if i >= len(self.attributes[0]):
                    valid = False

        # Check number of rectangles
        if len(self.attributes[2]) != ((len(self.attributes[0]) - 1) *
                                       (len(self.attributes[1]) - 1)):
            valid = False
                    
        return(valid)

    def orderByPosition(self):
        """Order lines by positions"""
        self.attributes[0] = sorted(self.attributes[0], key= lambda Line : Line.position)
        self.attributes[1] = sorted(self.attributes[1], key= lambda Line : Line.position)
        

    def generateRectangles(self):
        """Generates rectangles if all lines are already created
The default colour is set to DEFAULT_COLOUR"""
        for i in range(len(self.attributes[0]) - 1):
            for j in range(len(self.attributes[1]) - 1):
                r = Rectangle(self.attributes[0][i],self.attributes[0][i + 1],
                              self.attributes[1][j],self.attributes[1][j + 1],
                              self.DEFAULT_COLOUR)
                r.lineRepresentation()

                new = mpatches.Rectangle((r.x1,r.y1),r.x2-r.x1,r.y2-r.y1)
                self.attributes[2].append(new)
        

    def generateRandom(self):
        """Generates a random Mondrain object"""

        # Clear previous attributes
        self.attributes = [[],[],[]]

        verticalLines = []
        horizontalLines = []

        # Find number of vertical lines
        verticalLinesAmount = random.randint(3,10)

        # Find number of horizontal lines
        horizontalLinesAmount = random.randint(3,10)

        # Create lines on borders
        verticalLines.append([0.])
        verticalLines.append([1.])
        horizontalLines.append([0.])
        horizontalLines.append([1.])


        # Find position of each vertical line
        for i in range(verticalLinesAmount):
            
            # Check not too close to other lines
            acceptablePosition = False
            while acceptablePosition == False:
                p = random.random()
                acceptablePosition = True
                
                for j in range(len(verticalLines)):
                    if abs(verticalLines[j][0] - p) < 0.05:
                        acceptablePosition = False
                        
            verticalLines.append([p])

        

        # Find position of each horizontal line
        for i in range(horizontalLinesAmount):

            # Check not too close to other lines
            acceptablePosition = False
            while acceptablePosition == False:
                p = random.random()
                acceptablePosition = True
                
                for j in range(len(horizontalLines)):
                    if abs(horizontalLines[j][0] - p) < 0.05:
                        acceptablePosition = False
                        
            horizontalLines.append([p])


        # Choose interscetions for each vertical line
        for l in verticalLines:
            l.append(sorted(random.sample(range(len(horizontalLines)),
                                   random.randint(2,4))))
            

        # Choose intersections for each horizontal line
        for l in horizontalLines:
            l.append(sorted(random.sample(range(len(verticalLines)),
                                   random.randint(2,4))))
            
        # Make lines
        for l in verticalLines:
            print("making vetical line with position " + str(l[0]) + " and lineValues " + str(l[1]))
            line = Line(l[0],l[1])
            self.attributes[0].append(line)
            
        for l in horizontalLines:
            print("making horizontal line with position " + str(l[0]) + " and lineValues " + str(l[1]))
            line = Line(l[0],l[1])
            self.attributes[1].append(line)

        # Order lines by position
        self.orderByPosition()
        
        # Create rectangles
        self.generateRectangles()

        for r in self.attributes[2]:
            rnum = random.random()
            if rnum > 0.3:
                r.set_facecolor("white")
            elif rnum > 0.2:
                r.set_facecolor("blue")
            elif rnum > 0.1:
                r.set_facecolor("red")
            else:
                r.set_facecolor("yellow")

        
        

        

        
class Line:
    def __init__(self,position,lineValues):
        self.position = position
        self.lineValues = lineValues

    def copy(self):
        newLineValues = []
        for i in self.lineValues:
            newLineValues.append(i)
        new = Line(self.position,newLineValues)

        return(new)
        


        

class Rectangle:
    def __init__(self, x1, x2, y1, y2, colour):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.colour = colour

    def lineRepresentation(self):
        """If x1 etc. are Lines converts to floats"""
        newX1 = self.x1.position
        newX2 = self.x2.position
        newY1 = self.y1.position
        newY2 = self.y2.position

        self.x1 = newX1
        self.x2 = newX2
        self.y1 = newY1
        self.y2 = newY2


def draw(M):
    """Draws a Mondrian style image"""
    figure = plt.figure(figsize=[3,3])
    ax = figure.add_subplot(1,1,1)
    c=[]

    for r in M.attributes[2]:
        r.set_linewidth(0)
        c.append(r)

    for j in range(len(M.attributes[0])):
        drawing = False
        start = 0
        end = 0
        for i in range(len(M.attributes[0][j].lineValues)):
            drawing = not drawing
            horizontalLineNumber = M.attributes[0][j].lineValues[i]
            if drawing:
                start = M.attributes[1][horizontalLineNumber].position
            else:
                end = M.attributes[1][horizontalLineNumber].position    
                if j != 0 and j != len(M.attributes[0]) -1:
                    line = Line2D([M.attributes[0][j].position],[start,end],
                                  c="black",lw=3)
                    ax.add_line(line)


    for j in range(len(M.attributes[1])):
        drawing = False
        start = 0
        end = 0
        for i in range(len(M.attributes[1][j].lineValues)):
            drawing = not drawing
            verticalLineNumber = M.attributes[1][j].lineValues[i]
            if drawing:
                start = M.attributes[0][verticalLineNumber].position
            else:
                end = M.attributes[0][verticalLineNumber].position
                if j != 0 and j != len(M.attributes[1]) - 1:
                    line = Line2D([start,end],[M.attributes[1][j].position],
                                  c="black",lw=3)
                    ax.add_line(line)
            
            

    collection = PatchCollection(c ,match_original=True)
    ax.add_collection(collection)
    plt.xticks([])
    plt.yticks([])
    plt.show()



def mutate(M):
    """Mutate the colour of Mondrian object M"""

    # Find the probability of mutation
    probability = 10./len(M.attributes[2])

    for r in M.attributes[2]:
        number = random.random()

        if number < probability:
           
            rnum = random.random()
            if rnum > 0.3:
               
                r.set_facecolor("white")
            elif rnum > 0.2:
             
                r.set_facecolor("blue")
            elif rnum > 0.1:
             
                r.set_facecolor("red")
            else:
               
                r.set_facecolor("yellow")




def crossoverLine(l1,l2,c1,c2,r):
    """l1, l2 are Lines
    c1, c2 are the boundaries of the crossover region
    r is the total range"""

    perpendicularLines1 = list(l1.lineValues)
    perpendicularLines2 = list(l2.lineValues)

    newPerpendicularLines = []
    
    drawing1 = False
    drawing2 = False
    for i in range(r + 1):
        print("i = " + str(i))
        if i in perpendicularLines1:
            drawing1 = not drawing1
        if i in perpendicularLines2:
            drawing2 = not drawing2


        if i < c1:
            if i in perpendicularLines1:
                newPerpendicularLines.append(i)
        elif i == c1:
            if (not drawing1 != i in perpendicularLines1) != drawing2:
                newPerpendicularLines.append(i)
            else:
                print"Shouldn't print"
                #if i not in perpendicularLines1:
                    #newPerpendicularLines.append(i)
        elif (c1 < i < c2):
            if i in perpendicularLines2:
                newPerpendicularLines.append(i)
        elif i == c2:
            if (not drawing2 != i in perpendicularLines2) != drawing1:
                
                newPerpendicularLines.append(i)
            else:
                print "Shouldn't print"
                #if i not in perpendicularLines2:
                    #newPerpendicularLines.append(i)
        elif i > c2:
            if i in perpendicularLines1:
                newPerpendicularLines.append(i)

    return(newPerpendicularLines)






def crossover(m1,m2):
    """Performs random crossover on two Mondrian objects
    m1, m2 are the Mondrian objects
    Returns two new Mondrian objects"""





    
        
    def crossoverLines(l1,l2,c1,c2,r):
        """Performs crossover between two lines
        l1, l2 are the lines
        c1,c2 are the bounds on the crossover region
        r is the total range"""


        def convertToBits(lineValuesList,r):

            bitList = [False] * r

            drawing = False
            for i in range(r):
                if i in lineValuesList:
                    
                    drawing = not drawing
                bitList[i] = drawing
            return(bitList)

        
            

        def convertToLineValueList(bitList,r):
            """ Converts a given list of bits to a line value list"""

            lineValueList = []

            if bitList[0]:
                lineValueList.append(0)
            for i in range(1,r):
                if bitList[i] != bitList[i - 1]:
                    lineValueList.append(i)
            if bitList[r - 1]:
                lineValueList.append(r)

            return(lineValueList)


        
        
        lineValues1 = list(l1.lineValues)
        lineValues2 = list(l2.lineValues)

        bitList1 = convertToBits(lineValues1,r)
        bitList2 = convertToBits(lineValues2,r)


        newBitList = []

        for i in range(r):
            if not (c1 <= i < c2):
                
                newBitList.append(bitList1[i])
            else:
                newBitList.append(bitList2[i])
        


        newLineValues = convertToLineValueList(newBitList,r)

        line = Line(l1.position,newLineValues)

        return(line)




    # Compute the range of possible values
    xRange = random.sample(range(min(len(m1.attributes[0]),len(m2.attributes[0]))),2)
    yRange = random.sample(range(min(len(m1.attributes[1]),len(m2.attributes[1]))),2)

    # find indices of lines to crossover
    x1 = min(xRange)
    x2 = max(xRange)
    y1 = min(yRange)
    y2 = max(yRange)




    # Create new Mondrian objects
    newM1 = Mondrian()
    newM2 = Mondrian()

    # Copy attributes
    for i in range(2):
        for j in range(len(m1.attributes[i])):
            newM1.attributes[i].append(m1.attributes[i][j].copy())

    newM1.generateRectangles()

    for i in range(2):
        for j in range(len(m2.attributes[i])):
            newM2.attributes[i].append(m2.attributes[i][j].copy())

    newM2.generateRectangles()

    # Colour crossover for newM1
    yLength = len(newM1.attributes[1]) - 1

    for i in range(len(newM1.attributes[2])):
        if (y1 <= (i % (yLength)) < y2) and (x1 * yLength <= i < (x2 * yLength)):
            newM1.attributes[2][i].set_facecolor(m2.attributes[2][i].get_facecolor())
        else:
            newM1.attributes[2][i].set_facecolor(m1.attributes[2][i].get_facecolor())

    # Colour crossover for newM2
    yLength = len(newM2.attributes[1]) - 1

    for i in range(len(newM2.attributes[2])):
        if (y1 <= (i % (yLength)) < y2) and (x1 * yLength <= i < (x2 * yLength)):
            newM2.attributes[2][i].set_facecolor(m1.attributes[2][i].get_facecolor())
        else:
            newM2.attributes[2][i].set_facecolor(m2.attributes[2][i].get_facecolor())

    

    # Find maximum width or grid
    totalHeight = min([len(newM1.attributes[0]),len(newM2.attributes[0])])
    totalWidth = min([len(newM1.attributes[1]),len(newM2.attributes[1])])
    


    # Perform crossover of vertical lines in region
    for i in range(x1, x2 + 1):
        
        m1Line = m1.attributes[0][i]
        m2Line = m2.attributes[0][i]
        
        newM1Line = crossoverLines(m1Line,m2Line,y1,y2,totalHeight)
        newM2Line = crossoverLines(m2Line,m1Line,y1,y2,totalHeight)

        newM1.attributes[0][i] = newM1Line
        newM2.attributes[0][i] = newM2Line


    # Perform crossover of horizontal lines
    for i in range(y1, y2 + 1):
        
        m1Line = m1.attributes[1][i]
        m2Line = m2.attributes[1][i]
        
        newM1Line = crossoverLines(m1Line,m2Line,x1,x2,totalWidth)
        newM2Line = crossoverLines(m2Line,m1Line,x1,x2,totalWidth)

        newM1.attributes[1][i] = newM1Line
        newM2.attributes[1][i] = newM2Line
        


    return(newM1,newM2)
                    

    
    




