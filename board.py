#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:54:50 2019

@author: maya
"""


from cmu_112_graphics import *
from tkinter import *

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#######################################################################
def playGame():
    '''
    Setup the window for the game
    '''
    (rows, cols, cellSize, margin) = gameDimensions() #get dimensions
    #Calculate width and height
    width  = cellSize * cols + margin*2
    height = cellSize * rows + margin*2 
    runApp(width=width, height=height) 

def gameDimensions():
    '''
    Send default values for window setup. 
    '''
    rows = 6
    cols = 6
    cellSize = 150
    margin = 25
    return(rows, cols, cellSize, margin)    
    
def appStarted(app):
    '''
    Sets up game state
    '''
    (rows, cols, cellSize, margin) = gameDimensions()
    app.rows   = rows
    app.cols   = cols
    app.margin = margin # margin around grid
    app.cellSize = cellSize
    app.width  = cellSize * cols + margin*2
    app.height = cellSize * rows + margin*2
    app.emptyColor = "light blue"
    app.board  = [[app.emptyColor]*app.cols for rows in range(app.rows)]    

#from the notes with minor changes
def drawCell(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='pink')

#from the notes with edits
def drawBoard(app, canvas):
    #Back ground to orange
    #canvas.create_rectangle(0, 0, app.width, app.height, fill='orange')
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = drawCell(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1,
                                    fill= app.board[row][col], width=5)

    


# __________________Main_functions____________        
def redrawAll(app, canvas):
    '''
    main draw function
    '''
    drawBackground(app, canvas)
    drawBoard(app, canvas)
        
def main():
    playGame()

if __name__ == '__main__':
    main()
