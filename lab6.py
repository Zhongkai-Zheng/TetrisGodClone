#lab 6
#Alexander Zhongkai Zheng; azzheng
#partner: Sandy Pan; sqp

from tkinter import *
import math, string, copy, random

####################################
# customize these functions
####################################

def init(data):
    data.cols=10
    data.rows=15
    data.cellSize=20
    data.margin=20
    # load data.xyz as appropriate
    # if a cell is empty, paint it blue
    data.emptyColor="blue"
    data.score=0
    #stands for Falling Piece Row and 
    #Falling Piece Column
    data.fpr=0
    data.fpc=data.cols//2
    # a list that contains what color each cell is
    data.board=copy.deepcopy(make2dList(data.rows, data.cols, data.emptyColor))
    #Seven "standard" pieces (tetrominoes)
    iPiece = [
    [ True,  True,  True,  True]
    ]
  
    jPiece = [
    [ True, False, False ],
    [ True, True,  True]
    ]
  
    lPiece = [
    [ False, False, True],
    [ True,  True,  True]
    ]
  
    oPiece = [
    [ True, True],
    [ True, True]
    ]
  
    sPiece = [
    [ False, True, True],
    [ True,  True, False ]
    ]
  
    tPiece = [
    [ False, True, False ],
    [ True,  True, True]
    ]

    zPiece = [
    [ True,  True, False ],
    [ False, True, True]
    ]

    data.tetrisPieces=[iPiece, jPiece, lPiece, 
                        oPiece, sPiece, tPiece, zPiece]
    data.pieceColors=["red", "yellow", "magenta", 
                    "pink", "cyan", "green", "orange"]
    #selects first falling piece and also defines it
    newFallingPiece(data)

def make2dList(rows, cols, entries):
#makes a 2d list with some rows and some cols
#and all entries are equal to entries
    result, median = [], []
    for row in range(rows):
        for col in range(cols):
            median.append(entries)
        result.append(median)
        median=[]
    return result

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if(event.keysym == "Left"): 
        moveFallingPiece(data, 0, -1)
    elif(event.keysym == "Right"):
        moveFallingPiece(data, 0, 1)
    elif(event.keysym == "Up"):
        rotatePiece(data)
    elif(event.keysym == "Down"):
        moveFallingPiece(data, 1, 0)

def timerFired(data):
    moveFallingPiece(data, 1, 0)

def redrawAll(canvas, data):
    # draw in canvas
    if(data.game):
        canvas.create_rectangle(0, 0, data.width, 
                         data.height, fill="orange")
        drawGrid(canvas, data)
        drawScore(canvas, data)
    else: 
        canvas.create_text(data.width/2, data.height/2, 
                    text="You Lost! You're Score is " + str(data.score),
                    anchor=CENTER, fill="blue", font="Times 12")

def drawScore(canvas, data):
    canvas.create_text(data.width/2, 2, 
                    text="Score:",
                    anchor=NE, fill="blue", font="Times 15")
    canvas.create_text(data.width/2, 2, 
                    text=data.score,
                    anchor=NW, fill="blue", font="Times 15")

def drawGrid(canvas, data):
#draws all the cells
    for row in range(0, data.rows):
        for col in range(0, data.cols):
            drawCell(canvas, data, row, col)
    drawFallingPiece(canvas, data)

def newFallingPiece(data):
#creates a new falling piece
#chooses one at random
    piecenum=random.randint(0,6)
    data.fallingPiece=data.tetrisPieces[piecenum]
    data.fallingColor=data.pieceColors[piecenum]
    data.fpr=0
    data.fpc=data.cols//2

def drawFallingPiece(canvas, data):
#draws the falling piece to the board
    for row in range (0,len(data.fallingPiece)):
        for col in range(0,len(data.fallingPiece[row])):
            if data.fallingPiece[row][col]==True:
                drawCell(canvas, data, 
                        data.fpr+row, data.fpc+col, False)

def drawCell(canvas, data, row, col, empty=True):
#checks if the box has stuff
    if empty==True: color=data.board[row][col]
    else: color=data.fallingColor
    m=1
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)

def getCellBounds(row, col, data):
#Cite: Got this function from 
#S17 15112 course page
#returns the coordinates of a
#cell on some row and some col
    x0 = data.margin + col * data.cellSize
    x1 = data.margin + (col+1) * data.cellSize
    y0 = data.margin + row * data.cellSize
    y1 = data.margin + (row+1) * data.cellSize
    return (x0, y0, x1, y1)

def fallingPieceIsLegal(data, drow, dcol):
#checks if there is anything in the way 
#of the falling piece
    for row in range (0,len(data.fallingPiece)):
        for col in range(0,len(data.fallingPiece[row])):
            if data.fallingPiece[row][col]==True:
                r=data.fpr+row+drow
                c=data.fpc+col+dcol
                if r>=data.rows: return False
                if r<0: return False
                if c<0: return False
                if c>=data.cols: return False
                if data.board[r][c]!=data.emptyColor:
                    return False
    return True

def moveFallingPiece(data, drow, dcol):
#moves the falling piece in some direction
    if fallingPieceIsLegal(data, drow, dcol)==True:
        data.fpr+=drow
        data.fpc+=dcol
    elif fallingPieceFell(data, data.fallingPiece):
        placeFallingPiece(data)
        newFallingPiece(data)

def isRowComplete(data, row):
#checks if a row is all filled
    for col in row:
        if col==data.emptyColor: 
            return False
    return True

def deleteCompleteRows(data):
#deletes all rows that are completely filled
    for row in range (0,len(data.board)):
        if isRowComplete(data, data.board[row]):
            data.board.pop(row)
            newRow=makeNewRow(data)
            data.board.insert(0, newRow)
            data.score+=1

def makeNewRow(data):
#makes a list which is a new row
    result=[]
    for i in range(0, data.cols):
        result.append(data.emptyColor)
    return result

def rotatePieceIsLegal(data, piece):
#sees if you can rotate the piece or not
    for row in range(0,len(piece)):
        for col in range(0,len(piece[0])):
            if piece[row][col]==True:
                r=data.fpr+row
                c=data.fpc+col
                if r>=data.rows: return False
                if c<0: return False
                if c>=data.cols: return False
                if data.board[r][c]!=data.emptyColor:
                    return False
    return True

def rotatePiece(data):
#rotates piece counter clockwise 90 degrees
    rows=len(data.fallingPiece[0])
    cols=len(data.fallingPiece)
    piece=[]
    for i in range (0,rows):
        piece.append(getCol(data.fallingPiece, rows-i-1))
    if rotatePieceIsLegal(data, piece): 
        data.fallingPiece=piece

def getCol(list, col):
#gets a column of a 2d list
    result=[]
    for row in list:
        result.append(row[col])
    return result

def placeFallingPiece(data):
#places the falling piece on to the board
    for row in range(0,len(data.fallingPiece)):
        for col in range(0,len(data.fallingPiece[0])):
            if data.fallingPiece[row][col]==True:
                r=row+data.fpr
                c=col+data.fpc
                data.board[r][c]=data.fallingColor
    deleteCompleteRows(data)
    if(hasLost(data)): data.game=False


def fallingPieceFell(data, piece):
#checks if the falling piece has
#fallen completely or not
    for row in range(0,len(piece)):
        for col in range(0,len(piece[0])):
            if piece[row][col]==True:
                r=data.fpr+row+1
                c=data.fpc+col
                if r>=data.rows: return True
                if data.board[r][c]!=data.emptyColor:
                    return True
    return False

def hasLost(data):
    for col in data.board[0]:
        if col!=data.emptyColor:
            return True
    return False



####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.timerDelay = 100 # milliseconds
    data.width=width
    data.height=height
    data.game=True
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris():
    rows, cols=15, 10
    cellSize=20
    margin=20
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height)

playTetris()
