from cmu_112_graphics import *
from tkinter import *

# GameModes

# 1. Splash screen
class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width//2,mode.height//2,text='SplashScreen',font=font)
    
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
class GameMode(mode, canvas):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width//2,mode.height//2,text='Game',font=font)

    def keyPressed(mode, event):
        if (event.key == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)

# 4. Question mode
class QuestionMode(mode, canvas):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width//2,mode.height//2,text="Question",font=font)

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
        
app = OurApp(width = 500, height = 500)