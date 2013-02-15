import sys
import os
import string
import re

def classifyQuestions(question):
    if question.startswith("Who "):
        return "PERSON"
    elif question.startswith("When "):
        return "TIME"
    elif question.startswith("Where "):
        return "LOCATION"
    elif question.startswith("What "):
        return "NOUN"
    elif question.startswith("Why ", "How "):
        return "PHRASE"
    elif question.startswith("Is ", "Was ", "Will ", "Are ", "Were ", "DO ", "Does ", "Did "):
        return "BOOLEAN"
    else:
        return "UNKOWN"

def questionsToDeclaration(question):
    pass 
