########
#Tetris game and AI
########

from tkinter import *
import math, string, copy, random

#cite: got most of this from lab 6, added 22 lines
def init(data):
    data.cols=10
    data.rows=22
    data.cellSize=20
    data.margin=20
    # load data.xyz as appropriate
    # if a cell is empty, paint it blue
    data.emptyColor="white"
    data.score=0
    #stands for Falling Piece Row and 
    #Falling Piece Column
    data.fpr=0
    data.fpc=data.cols//2
    data.menuwidth=240
    data.gamewidth=2*data.margin+data.cols*data.cellSize 
    # a list that contains what color each cell is
    data.board=copy.deepcopy(make2dList(data.rows, data.cols, data.emptyColor))
    #if AI is on, then this should be true
    data.ai=False
    #tells us which screen we are in
    #0 is menu, 1 is game, 2 is score, 3 is controls
    data.screen=1
    #the below variables are for the AI for testing test cases 
    data.testboard=copy.deepcopy(data.board)
    data.heights=[20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    data.holes=0
    data.aggregateHeight=0
    data.bumpiness=0
    data.completerows=0
    data.vector=[data.bumpiness, data.holes, data.aggregateHeight, data.completerows]
    #got this vector from: 
    #https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/    
    data.constantvector=[(-0.184),(-0.3566),(-0.51),0.7606]
    data.testscore=0
    #position and rotation and score of best piece
    data.besttestboard=None
    data.ai=False
    data.newpiece=False
    #below are the start col and end col of next-up window
    data.nextupstart=11
    data.nextupend=17
    #below are the start col and end col of hold window
    data.holdstart=data.nextupend+1
    data.holdend=data.holdstart+6
    #True if held was used for this turn
    data.held=False
    #below is the row of the ghost piece
    data.ghostrow=data.fpr
    #used for timing
    data.time=0
    data.paused=False
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
    data.fallingPieces=[]
    data.fallingColors=[]
    data.knownpieces=6
    data.heldpiece=[
    [ False, False, False ],
    [ False, False,  False]
    ]
    data.heldcolor="white"
    #selects first few falling pieces and also defines it
    newFallingPiece(data)

#cite: got this function from lab 6
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

#cite: got this function from lab 6
def mousePressed(event, data):
    # use event.x and event.y
    buttoneffects(data, event.x, event.y)

#cite: got this function from lab 6
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
    if(event.keysym=="space"):
        harddrop(data)
    if(event.keysym=="h") and not data.held:
        holdpiece(data)
    if(event.keysym=="t"):
        print(data.heights)
    if(event.keysym=="p"):
        data.paused=not(data.paused)

#cite: got this function from lab 6
def timerFired(data):
    if not data.paused:
        data.time+=1
        if data.time>=10:
            moveFallingPiece(data, 1, 0)
            data.time=0
        if data.ai:
            if data.newpiece: 
                getBestTestCase(data)
            aiMove(data)

#cite: got this function from lab 6, changed lines
def redrawAll(canvas, data):
    # draw in canvas
    if(data.screen==1):
        drawGrid(canvas, data)
        coverTopRows(canvas, data)
        drawScore(canvas, data)
        drawButtons(canvas, data)
        drawNextUp(canvas, data)
        drawhold(canvas, data)
    elif(data.screen==2) : 
        #stands for button width and button height, button x and button y
        bw, bh=80, 20
        bx, bx2=data.width//2-bw, data.width//2+bw
        by, by2=data.height//2, data.height//2+2*bh
        textwidth=(bx+bx2)//2
        textheight=(by+by2)//2
        textheight=data.height//2-bh-10
        #stands for button text x and y 
        btx, bty=(bx+bx2)//2, (by+by2)//2

        canvas.create_text(textwidth, textheight, 
                    text="You Lost! Your Score is " + str(data.score),
                    anchor=CENTER, fill="blue", font="Times 12")
        canvas.create_rectangle(bx, by, bx2, by2, fill="orange")
        canvas.create_text(btx, bty, 
                    text="PLAY AGAIN!",
                    anchor=CENTER, fill="white")
        canvas.create_rectangle(bx, by, bx2, by2, fill="orange")
        canvas.create_text(btx, bty, 
                    text="MAIN MENU",
                    anchor=CENTER, fill="white")

#harddrops the current piece
def harddrop(data):
    data.fpr=data.ghostrow
    moveFallingPiece(data,1,0)

#holds the current piece and switches with the held piece
#if no held piece then allows next piece to drop
def holdpiece(data):
    data.fpr=0
    data.fpc=data.cols//2    
    medianpiece=data.heldpiece
    mediancolor=data.heldcolor
    data.heldpiece=data.fallingPieces[0]
    data.heldcolor=data.fallingColors[0]
    data.fallingColors[0]=mediancolor
    if(medianpiece==[
    [ False, False, False ],
    [ False, False,  False]
    ]):
        newFallingPiece(data)
    else: data.fallingPieces[0]=medianpiece
    data.held=True

#gets the best move. More specifically,
#gets the column and the rotation of the next piece
#that minimizes score
def getBestTestCase(data):
    rotations=[]
    piece=data.fallingPieces[0]
    possibles=4
    if piece==data.tetrisPieces[3]:possibles=1
    elif (piece in [data.tetrisPieces[0],
        data.tetrisPieces[6],data.tetrisPieces[4]]):possibles=2 
    else: possibles==4
    for i in range(possibles):
        rotations.append(rotateTestPiece(data, piece, i))
    for i in range(len(rotations)):
        for c in range(0, data.cols):
            r=0
            if testPieceLegal(data, r, c, data.testboard, rotations[i]):
                while testPieceLegal(data, r+1, c, data.testboard, rotations[i]): r+=1
            else: continue
            placeFallingTestPiece(data, rotations[i], r, c)
            updateAll(data)
            if data.besttestboard==None:
                data.besttestboard=[r, c, i, data.testscore]
                data.best=[data.bumpiness, data.holes, data.aggregateHeight, data.completerows]
            else: 
                if data.besttestboard[3]<data.testscore:
                    data.besttestboard=[r, c, i, data.testscore]
                    data.best=[data.bumpiness, data.holes, data.aggregateHeight, data.completerows]
            data.testboard=copy.deepcopy(data.board)
    data.newpiece=False
    for i in range(data.besttestboard[2]):
        rotatePiece(data)

def aiMove(data):
#moves the current piece to the best move place determined
#by getbesttestcase
    if data.besttestboard!=None and data.fpc<data.besttestboard[1]:
        moveFallingPiece(data, 0, 1)
    elif data.besttestboard!=None and data.fpc>data.besttestboard[1]:
        moveFallingPiece(data, 0, -1)
    elif data.besttestboard!=None and data.fpr<data.besttestboard[0]:
        moveFallingPiece(data, 1, 0)
       
#always call update heights first
#for new test case, updates the heights of each column
def updateHeights(data):
    for i in range(data.cols):
        for j in range(data.rows):
            if data.testboard[j][i]!=data.emptyColor:
                data.heights[i]=j
                break
            data.heights[i]=data.rows
#for new test case, updates the aggregate height,
#which is the sum of the heights of the columns
def updateAggregateHeight(data):
    result=0
    for i in range(len(data.heights)):
        result+=data.rows-data.heights[i]
    data.aggregateHeight=result

#for new test case, updates number of holes
def updateHoles(data):
    result=0
    for i in range(0, data.cols):
        for j in range(data.heights[i], data.rows):
            if(data.testboard[j][i]==data.emptyColor):
                result+=1
    data.holes=result

#for new test case, updates the bumpiness
#bumpiness is defined as the standard deviation of
#the heights of the columns
def updateBumpiness(data):
    newheights=[]
    for i in data.heights:
        newheights.append(0)
    average=0
    bumpiness=0
    for i in range(len(data.heights)):
        newheights[i]=data.rows-data.heights[i]
        average+=data.rows-data.heights[i]
    average/=len(data.heights)
    for i in range(len(newheights)):
        bumpiness+=abs(average-newheights[i])
    data.bumpiness=bumpiness

#for each test case, updates all the above 5 functions
def updateAll(data):
    updateHeights(data)
    updateHoles(data)
    updateBumpiness(data)
    updateAggregateHeight(data)
    data.vector=[data.bumpiness, data.holes, data.aggregateHeight, data.completerows]
    updateTestScore(data)

def dotProduct(v1, v2):
#calculates dot product of two vectors assuming
#the two vectors are the same length
    result=0
    for i in range(len(v1)): 
        a=(v1[i]*v2[i])
        result+=a
    return result

#calculates the score of a test function
#always call this function last
def updateTestScore(data):
    v=dotProduct(data.constantvector,data.vector)
    data.testscore=v

#the top two rows in tetris should be hidden
def coverTopRows(canvas, data):
    for row in range(0, 2):
        for col in range(0, data.cols):
            drawNextUpCell(canvas, data, row, col, 'white', True)
    cell1=getCellBounds(0, 0, data)
    cell2=getCellBounds(0, 10, data)
    x=(cell1[0]+cell2[0])//2
    y=data.margin
    canvas.create_text(x, y, text="PLAYER ONE",
                        anchor=N, fill="grey", font="Arial 20")

#draws the next 5 pieces in a window right of the playing field
def drawNextUp(canvas, data):
    cell1=getCellBounds(0, data.nextupstart, data)
    cell2=getCellBounds(0, data.nextupend, data)
    x=(cell1[0]+cell2[0])//2
    y=data.margin
    canvas.create_text(x, y, text="NEXT UP",
                        anchor=N, fill="grey", font="Arial 20")
    shift=3
    for i in range(len(data.fallingPieces)-1):
        piece=data.fallingPieces[i+1]
        color=data.fallingColors[i+1]
        #below we are positioning the piece to the center
        #length and height of the piece
        lpiece=len(piece[0])
        hpiece=len(piece)
        length=data.nextupend-data.nextupstart
        start=(length-lpiece)//2+data.nextupstart
        end=start+lpiece
        #fill an empty row for aesthetic reasons
        for col in range(data.nextupstart, data.nextupend):
            drawNextUpCell(canvas, data, shift-1, col, "white")
        for col in range(data.nextupstart, data.nextupend):
            for row in range(i*3+shift, i*3+shift+3):
                if col>=start and col<end and (row-(i*3)-shift)<hpiece:
                    if piece[row-(i*3+shift)][col-start]:
                        drawNextUpCell(canvas, data, row, col, color)
                    else: drawNextUpCell(canvas, data, row, col, "white")
                else: drawNextUpCell(canvas, data, row, col, "white")

#draws a gray piece on the board that
#indicates where the current piece is going to fall
def drawGhostPiece(canvas, data):
    data.ghostrow=data.fpr
    while(testPieceLegal(data, data.ghostrow+1, data.fpc)):
        data.ghostrow+=1
    for row in range (0,len(data.fallingPieces[0])):
        for col in range(0,len(data.fallingPieces[0][row])):
            if data.fallingPieces[0][row][col]==True:
                drawNextUpCell(canvas, data, 
                        data.ghostrow+row, data.fpc+col, "lightgrey")

#draws the piece being held in a window right 
#of the next up pieces
def drawhold(canvas, data):
    cell1=getCellBounds(0, data.holdstart, data)
    cell2=getCellBounds(0, data.holdend, data)
    x=(cell1[0]+cell2[0])//2
    y=data.margin
    canvas.create_text(x, y, text="HOLD",
                        anchor=N, fill="grey", font="Arial 20")
    shift=3
    piece=data.heldpiece
    color=data.heldcolor
    #below we are positioning the piece to the center
    #length and height of the piece
    lpiece=len(piece[0])
    hpiece=len(piece)
    length=data.holdend-data.holdstart
    start=(length-lpiece)//2+data.holdstart
    end=start+lpiece
    starth=(6-hpiece)//2+shift
    endh=starth+hpiece
    #fill an empty row for aesthetic reasons
    for col in range(data.holdstart, data.holdend):
        drawNextUpCell(canvas, data, shift-1, col, "white")
    for col in range(data.holdstart, data.holdend):
        for row in range(shift, shift+6):
            if col>=start and col<end and row>=starth and row<endh:
                if piece[row-starth][col-start]:
                    drawNextUpCell(canvas, data, row, col, color)
                else: drawNextUpCell(canvas, data, row, col, "white")
            else: drawNextUpCell(canvas, data, row, col, "white")

#cite: got this function from lab 6, changed lines
#draws the score and the number of lines deleted
def drawScore(canvas, data):
    width=data.gamewidth
    width2=data.width-10
    height=400
    rowsize=30
    canvas.create_text(width, height, 
                    text="SCORE: ",
                    anchor=NW, fill="grey", font="Arial 20")
    canvas.create_text(width2, height, 
                    text=data.score,
                    anchor=NE, fill="grey", font="Arial 20")
    canvas.create_text(width, height+rowsize, 
                    text="LINES: ",
                    anchor=NW, fill="grey", font="Arial 20")
    canvas.create_text(width2, height+rowsize, 
                    text=data.score,
                    anchor=NE, fill="grey", font="Arial 20")

#draws all buttons on the screen
#currently: pause, reset, end
def drawButtons(canvas, data):
    y=480
    x1=data.gamewidth
    width, height=100, 30
    x2=data.width-data.margin-width
    data.resetpara=(x1,y,x1+width,y+height)
    data.endpara=(x2,y,x2+width,y+height)
    canvas.create_rectangle(data.resetpara,outline="lightgrey")
    canvas.create_rectangle(data.endpara,outline="lightgrey")
    textx1, texty1=(2*x1+width)//2, (2*y+height)//2
    textx2, texty2=(2*x2+width)//2, (2*y+height)//2
    canvas.create_text(textx1, texty1, 
                    text="RESET", fill="grey", font="Arial 15")
    canvas.create_text(textx2, texty2, 
                    text="END", fill="grey", font="Arial 15")
    data.aibutton=(x2,20*10+10,x2+width,20*10+10+height)
    textx3, texty3=textx2, 20*10+10+height//2
    if not data.ai:
        canvas.create_rectangle(data.aibutton,outline="lightgrey")
        canvas.create_text(textx3,texty3,
                    text="AI ON", fill="grey", font="Arial 15")
    if data.ai: 
        canvas.create_rectangle(data.aibutton,outline="lightgrey",fill="lightgrey")
        canvas.create_text(textx3,texty3,
                    text="AI OFF", fill="white", font="Arial 15")
    x3=data.margin+10
    pausewidth=data.cols*data.cellSize-10
    data.pausepara=(x3,y,x3+pausewidth,y+height)
    textx3, texty3=(2*x3+pausewidth)//2, (2*y+height)//2
    if data.paused==False:
        canvas.create_text(textx3, texty3, 
                    text="PAUSE", fill="grey", font="Arial 15")
        canvas.create_rectangle(data.pausepara,outline="lightgrey")
    if data.paused:
        canvas.create_rectangle(data.pausepara,
                    outline="lightgrey", fill="lightgrey")
        canvas.create_text(textx3, texty3, 
                    text="PAUSED", fill="white", font="Arial 15")



#deals with pressing on a button
def buttoneffects(data, x, y):
    if data.screen==1:
        if clickIn(x,y,data.resetpara): reset(data)
        if clickIn(x,y,data.endpara): data.screen=2
        if clickIn(x,y,data.aibutton): activateAI(data)
        if clickIn(x,y,data.pausepara): data.paused=not data.paused
    if data.screen==2:
        return 42
    if data.screen==3:
        return 42
    if data.screen==0:
        return 42

#returns True if the click was inside a certain button 
def clickIn(x, y, button):
    return (x>=button[0] and 
            x<=(button[2])
            and y>=button[1] 
            and y<=(button[3]))

#resets the game, clears board, regenerates next up pieces
#and clears the score and hold
def reset(data):
    data.game=True
    data.board=copy.deepcopy(make2dList(data.rows, data.cols, data.emptyColor))
    data.testboard=copy.deepcopy(data.board)
    data.fallingPieces=[]
    data.fallingColors=[]
    data.score=0
    data.completerows=0
    data.heldpiece=[
    [ False, False, False ],
    [ False, False,  False]
    ]
    newFallingPiece(data)

#turns on AI
def activateAI(data):
    data.ai=not data.ai
    data.newpiece=True

#cite: got this function from lab 6
def drawGrid(canvas, data):
#draws all the cells
    for row in range(2, data.rows):
        for col in range(0, data.cols):
            drawCell(canvas, data, row, col)
    drawGhostPiece(canvas, data)
    drawFallingPiece(canvas, data)

# got half of this from lab 6
def newFallingPiece(data):
#creates a new falling piece
#chooses one at random
    if data.ai==True:
        data.testboard=copy.deepcopy(data.board)
        data.newpiece=True
    if data.fallingPieces==[]:
        for i in range(data.knownpieces):
            piecenum=random.randint(0,6)
            data.fallingPieces.append(data.tetrisPieces[piecenum])
            data.fallingColors.append(data.pieceColors[piecenum])
    else:
        data.fallingPieces.pop(0)
        data.fallingColors.pop(0)
        piecenum=random.randint(0,6)
        data.fallingPieces.append(data.tetrisPieces[piecenum])
        data.fallingColors.append(data.pieceColors[piecenum])
    data.fpr=0
    data.fpc=data.cols//2

#cite: got this function from lab 6, changed 2 lines
def drawFallingPiece(canvas, data):
#draws the falling piece to the board
    for row in range (0,len(data.fallingPieces[0])):
        for col in range(0,len(data.fallingPieces[0][row])):
            if data.fallingPieces[0][row][col]==True:
                drawCell(canvas, data, 
                        data.fpr+row, data.fpc+col, False)

#cite: got this function from lab 6, changed color
def drawCell(canvas, data, row, col, empty=True):
#checks if the box has stuff
    if empty==True: color=data.board[row][col]
    else: color=data.fallingColors[0]
    m=1
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue", width=0)
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color, width=0)

#used to draw cells in next up window and ghost piece
def drawNextUpCell(canvas, data, row, col, color, cover=False):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m=1
    if cover==False:
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue", width=0)
        canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color, width=0)
    else: canvas.create_rectangle(x0, y0, x1, y1, fill="white", width=0)

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

#cite: got this function from lab 6
def fallingPieceIsLegal(data, drow, dcol):
#checks if there is anything in the way 
#of the falling piece
    for row in range (0,len(data.fallingPieces[0])):
        for col in range(0,len(data.fallingPieces[0][row])):
            if data.fallingPieces[0][row][col]==True:
                r=data.fpr+row+drow
                c=data.fpc+col+dcol
                if r>=data.rows: return False
                if r<0: return False
                if c<0: return False
                if c>=data.cols: return False
                if data.board[r][c]!=data.emptyColor:
                    return False
    return True

def testPieceLegal(data, r, c, board=None, piece=None):
#tests if a piece can be placed in a position
    if board==None: 
        for row in range (0,len(data.fallingPieces[0])):
            for col in range(0,len(data.fallingPieces[0][row])):
                if data.fallingPieces[0][row][col]==True:
                    testr=r+row
                    testc=c+col
                    if testr>=data.rows: return False
                    if testr<0: return False
                    if testc<0: return False
                    if testc>=data.cols: return False
                    if data.board[testr][testc]!=data.emptyColor:
                        return False
        return True
    else: 
        for row in range (0,len(piece)):
            for col in range(0,len(piece[row])):
                if piece[row][col]==True:
                    testr=r+row
                    testc=c+col
                    if testr>=len(board): return False
                    if testr<0: return False
                    if testc<0: return False
                    if testc>=len(board[0]): return False
                    if board[testr][testc]!=data.emptyColor:
                        return False
        return True

#cite: got this function from lab 6
def moveFallingPiece(data, drow, dcol):
#moves the falling piece in some direction
    if fallingPieceIsLegal(data, drow, dcol)==True:
        data.fpr+=drow
        data.fpc+=dcol
    elif fallingPieceFell(data, data.fallingPieces[0]):
        placeFallingPiece(data)
        newFallingPiece(data)

#cite: got this function from lab 6
def isRowComplete(data, row):
#checks if a row is all filled
    for col in row:
        if col==data.emptyColor: 
            return False
    return True

#cite: got this function from lab 6
def deleteCompleteRows(data):
#deletes all rows that are completely filled
    for row in range (0,len(data.board)):
        if isRowComplete(data, data.board[row]):
            data.board.pop(row)
            newRow=makeNewRow(data)
            data.board.insert(0, newRow)
            data.score+=1

def deleteCompleteTestRows(data):
#deletes all rows that are completely filled
    data.completerows=0
    for row in range (0,len(data.testboard)):
        if isRowComplete(data, data.testboard[row]):
            data.completerows+=1
            data.testboard.pop(row)
            newRow=makeNewRow(data)
            data.testboard.insert(0, newRow)

#cite: got this function from lab 6
def makeNewRow(data):
#makes a list which is a new row
    result=[]
    for i in range(0, data.cols):
        result.append(data.emptyColor)
    return result

#cite: got this function from lab 6
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

#cite: got this function from lab 6
def rotatePiece(data):
#rotates piece counter clockwise 90 degrees
    rows=len(data.fallingPieces[0][0])
    cols=len(data.fallingPieces[0])
    piece=[]
    for i in range (0,rows):
        piece.append(getCol(data.fallingPieces[0], rows-i-1))
    if rotatePieceIsLegal(data, piece): 
        data.fallingPieces[0]=piece

#rotates a test piece
def rotateTestPiece(data, piece, rotations=1):
    if rotations==0:
        return piece
    rows=len(piece[0])
    cols=len(piece)
    newpiece=[]
    for i in range (0,rows):
        newpiece.append(getCol(piece, rows-i-1))
    return rotateTestPiece(data, newpiece, rotations-1)

#cite: got this function from lab 6
def getCol(list, col):
#gets a column of a 2d list
    result=[]
    for row in list:
        result.append(row[col])
    return result

#cite: got this function from lab 6
def placeFallingPiece(data):
#places the falling piece on to the board
    for row in range(0,len(data.fallingPieces[0])):
        for col in range(0,len(data.fallingPieces[0][0])):
            if data.fallingPieces[0][row][col]==True:
                r=row+data.fpr
                c=col+data.fpc
                data.board[r][c]=data.fallingColors[0]
    deleteCompleteRows(data)
    if(hasLost(data)): data.game=False
    data.held=False
    data.besttestboard=None

def placeFallingTestPiece(data, piece, testr, testc):
#places the falling piece on to the board
    for row in range(0,len(piece)):
        for col in range(0,len(piece[0])):
            if piece[row][col]==True:
                r=row+testr
                c=col+testc
                data.testboard[r][c]=data.fallingColors[0]
    deleteCompleteTestRows(data)

#cite: got this function from lab 6
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

#cite: got this function from lab 6
def hasLost(data):
    for col in data.board[0]:
        if col!=data.emptyColor:
            return True
    return False

####################################
# use the run function as-is
####################################
#cite: got this function from 112 course page, added 4 lines
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
    data.timerDelay = 50 # milliseconds
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

#cite: got this function from lab 6, changed 6 lines
def playTetris():
    rows, cols=22, 10
    cellSize=20
    margin=20
    menuwidth=280
    extraheight=40
    gamewidth=2*margin + cols*cellSize 
    width = gamewidth + menuwidth
    height = 2*margin + rows*cellSize +extraheight
    run(width, height)

playTetris()
