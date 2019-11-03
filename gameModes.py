from cmu_112_graphics import *
from tkinter import *

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
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width//2,mode.height//2,text='Game',font=font)

    def keyPressed(mode, event):
        if (event.key == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)

    def mousePressed(mode, event):
        # If player clicks inside of a question box
        # Then mode turns into QuestionMode
        x0, y0 = event.x, event.y
        # Input the question
        category, value = getCell(x0, y0)
        question, answer = getQuestionAnswer(category, value)

    def getQuestionAnswer(category, value):
#        jeopardyQs[category, value] => question, answer
#        app.setActiveMode(QuestionMode(question, answer))
        return 42

    # From http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBounds(app, row, col):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = app.width - 2*app.margin
        gridHeight = app.height - 2*app.margin
        columnWidth = gridWidth / app.cols
        rowHeight = gridHeight / app.rows
        x0 = app.margin + col * columnWidth
        x1 = app.margin + (col+1) * columnWidth
        y0 = app.margin + row * rowHeight
        y1 = app.margin + (row+1) * rowHeight
        return (x0, y0, x1, y1)

    # From http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCell(app, x, y):
        # returns (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not pointInGrid(app, x, y)):
            return (-1, -1)
        gridWidth  = app.width - 2*app.margin
        gridHeight = app.height - 2*app.margin
        cellWidth  = gridWidth / app.cols
        cellHeight = gridHeight / app.rows
        row = int((y - app.margin) / cellHeight)
        col = int((x - app.margin) / cellWidth)

        return (row, col)

# 4. Question mode
class QuestionMode(GameMode):
    def __init__(mode, question, answer):
        mode.question = question
        mode.answer = answer
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        txt = f'Question Mode\nQuestion={mode.question}\nAnswer={mode.answer}'
        canvas.create_text(mode.width//2,mode.height//2,text=txt,font=font)

###############################
# Making app
###############################

class OurApp(ModalApp):
    def appStarted(app):
        # New game => selectRandomGame

        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.questionMode = QuestionMode(app.gameMode,'','')
        app.setActiveMode(app.splashScreenMode)
        
app = OurApp(width = 500, height = 500)