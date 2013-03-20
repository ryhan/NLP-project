#!/usr/bin/python

# questionClassifier.py
# process(question) returns the classification of the expected answer.

import os, sys, errno
import re, string
import itertools
import nltk

def process(question):
    if question.startswith("Who "):
        return "PERSON"
    elif question.startswith("When "):
        return "DATE"
    elif question.startswith("Where "):
        return "LOCATION"
    elif question.startswith("What "):
        return "NOUN"
    elif question.startswith(("Why ", "How ")):
        return "PHRASE"
    elif question.startswith("How many "):
        return "NUMERAL"
    elif question.startswith(("Is ", "Was ", "Will ", "Are ", "Were ", "Do ", "Does ", "Did ")):
        return "BOOLEAN"
    else:
        return "UNKOWN"