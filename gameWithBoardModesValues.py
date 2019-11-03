from cmu_112_graphics import *
from tkinter import *
from data_parser import *

# GameModes

# 1. Splash screen
class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_rectangle(0,0,mode.width,mode.height,fill='darkblue')
        canvas.create_text(mode.width//2,mode.height//2,text='SplashScreen',font=font,fill='yellow')
    
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

# 2. Help screen
class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width//2,mode.height//2,text='Help',font=font)

    def keyPressed(mode, event):
        if (event.key != 'q'):
            mode.app.setActiveMode(mode.app.gameMode)

# 3. Game mode
class GameMode(Mode):

    @staticmethod
    def gameDimensions():
        rows = 6
        cols = 6
        cellSize = 450/6
        margin = 25
        return(rows, cols, cellSize, margin)    

    def appStarted(mode):
        mode.rows, mode.cols, mode.cellSize, mode.margin = GameMode.gameDimensions()
        mode.width  = mode.cellSize * mode.cols + mode.margin*2
        mode.height = mode.cellSize * mode.rows + mode.margin*2
        mode.emptyColor = "light blue"
        mode.board  = [[mode.emptyColor]*mode.cols for rows in range(mode.rows)]
        mode.values = [[0]*mode.cols for rows in range(mode.rows)]

        mode.jeopardyQs = selectRandomJeopardyGame("JEOPARDY_QUESTIONS1.json")
        mode.categories = selectCategories(mode.jeopardyQs)
        (mode.question, mode.answer) = (None, None)

        for row in range(mode.rows):
            for col in range(mode.cols):
                mode.values[row][col] = (row)*200

    #from the notes with minor changes
    def drawCell(mode, row, col):
        gridWidth  = mode.width - 2*mode.margin
        gridHeight = mode.height - 2*mode.margin
        x0 = mode.margin + gridWidth * col / mode.cols
        x1 = mode.margin + gridWidth * (col+1) / mode.cols
        y0 = mode.margin + gridHeight * row / mode.rows
        y1 = mode.margin + gridHeight * (row+1) / mode.rows
        return (x0, y0, x1, y1)

    def drawBackground(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='pink')

    def findMaxLength(mode):
        maxLength = 1
        for i in range(len(mode.categories)):
            length = len(mode.categories[i])
            if length >= maxLength:
                length = maxLength
        return maxLength

    def drawBoard(mode, canvas):
        maxLen = mode.findMaxLength()
        for row in range(mode.rows):
            for col in range(mode.cols):
                (x0, y0, x1, y1) = GameMode.drawCell(mode, row, col)
                canvas.create_rectangle(x0,y0,x1,y1)
                if row == 0:
                    canvas.create_text((x0+x1)/2,(y0+y1)/2, text = mode.categories[col],
                                        width = x1-x0)
                else:
                    canvas.create_text((x0+x1)/2,(y0+y1)/2, text = mode.values[row][col])

    def redrawAll(mode, canvas):
        GameMode.drawBackground(mode, canvas)
        GameMode.drawBoard(mode, canvas)
        font = 'Arial 26 bold'
        canvas.create_text(mode.width//2,mode.height//2,text='Game',font=font)

    def keyPressed(mode, event):
        if (event.key == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)

    def mousePressed(mode, event):
        # If player clicks inside of a question box
        # Then mode turns into QuestionMode
        x0, y0 = event.x, event.y
        row, col = GameMode.getCell(mode, x0, y0)
        print(row, col)
        if (row > 0 and col >= 0):
            category = mode.categories[col]
            value = mode.values[row][col]
            print(f'{category}, {value}')
            GameMode.getQuestionAnswer(mode, category, value)
            mode.app.setActiveMode(mode.app.questionMode)

    def getQuestionAnswer(mode, category, value):
        for questions in mode.jeopardyQs:
            if (questions['category'] == category 
                    and questions['value'] == "$" + str(value)):
                    (mode.question, mode.answer) = (questions['question'], questions['answer'])
        if mode.question == None:
            print("WHAATTT?????")
        elif mode.answer == None:
            print("HUH?")
        else:
            print(f'{mode.question}, {mode.answer}')
        return (4,2)

    # From http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBounds(mode, row, col):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = mode.width - 2*mode.margin
        gridHeight = mode.height - 2*mode.margin
        columnWidth = gridWidth / mode.cols
        rowHeight = gridHeight / mode.rows
        x0 = mode.margin + col * columnWidth
        x1 = mode.margin + (col+1) * columnWidth
        y0 = mode.margin + row * rowHeight
        y1 = mode.margin + (row+1) * rowHeight
        return (x0, y0, x1, y1)

    # From http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCell(mode, x, y):
        # returns (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not GameMode.pointInGrid(mode, x, y)):
            return (-1, -1)
        gridWidth  = mode.width - 2*mode.margin
        gridHeight = mode.height - 2*mode.margin
        cellWidth  = gridWidth / mode.cols
        cellHeight = gridHeight / mode.rows
        row = int((y - mode.margin) / cellHeight)
        col = int((x - mode.margin) / cellWidth)

        return (row, col)

    def pointInGrid(mode, x, y):
        # return True if (x, y) is inside the grid defined by mode.
        return ((mode.margin <= x <= mode.width-mode.margin) and
                (mode.margin <= y <= mode.height-mode.margin))

#Question Class
class Question(object):
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

        

# 4. Question mode
class QuestionMode(Mode):

    def appStarted(mode):
        print("WHWIEWKEWE")
        mode.question = mode.app.gameMode.question
        mode.answer = mode.app.gameMode.answer
        """mode.url = mode.isImage(mode.question)
        print(mode.url)
        if mode.url != "":
            mode.image = mode.loadImage(mode.url)"""

        mode.showAnswer = False

    """def isImage(mode, question):
        url = ""
        if question == None:
            return None
        split = question.split()
        for word in split:
            if word.startswith("href"):
                url = word[4:]
                split.remove(word)
                " ".join(mode.question)
        return url
        #return mode.loadImage(url)"""

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0, mode.width, mode.height, fill = "blue")
        canvas.create_text(mode.width/2, mode.height/3, 
                            text = mode.app.gameMode.question, width = mode.width,
                            font = 'Arial 30 bold')
        """
        if mode.url != "":
            canvas.create_image(mode.width/2, 2 * mode.height/3,
                            image=ImageTk.PhotoImage(mode.image))"""

        if mode.showAnswer:
            canvas.create_text(mode.width/2, 2 * mode.height/3, text =
                                mode.app.gameMode.answer)
        """font = 'Arial 26 bold'
        txt = f'Question Mode\nQuestion={mode.question}\nAnswer={mode.answer}'
        canvas.create_text(mode.width//2,mode.height//2,text=txt,font=font)"""

    def keyPressed(mode, event):
        if event.key == "p":
            mode.app.setActiveMode(mode.app.gameMode)
        elif event.key == "a":
            mode.showAnswer = True

###############################
# Making app
###############################

class OurApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.questionMode = QuestionMode()
        app.setActiveMode(app.splashScreenMode)
        
jeopardyApp = OurApp(width = 500, height = 500)