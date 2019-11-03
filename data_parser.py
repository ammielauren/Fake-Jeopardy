import json
import random

#Selects a random jeopardy game
def selectRandomJeopardyGame(files):
    with open(files, 'r') as f:
        jeopardy_dict = json.load(f)
    randomChoice = random.choice(list(jeopardy_dict))
    randomShow = randomChoice['show_number']
    randomJeopardy = []
    for jeopardyQuestion in jeopardy_dict:
        if randomShow == jeopardyQuestion['show_number']:
            randomJeopardy.append(jeopardyQuestion)
    return randomJeopardy


#Returns a list of 12-13 categories
#Get only the 6 categories for the board
def selectCategories(l):
    categories = set()
    for question in l:
        categories.add(question['category'])
    return list(categories)
