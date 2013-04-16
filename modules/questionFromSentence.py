#!/usr/bin/python

# questionFromSentence.py
# Authored by Ryhan Hassan | rhassan@andrew.cmu.edu
# Transforms declarative sentences into questions.

import re
import nltk
import random

# GIVEN string sentence
# RETURNS (question string, success boolean)
def transform_IT_IS(sentence):
  if ("It is" in sentence):
    question = sentence.replace("It is", "What is")
    return (question, True)
  return (sentence, False)

def add_questionmark(sentence):
  if (sentence[len(sentence) - 1] == '.'):
    sentence = sentence[:len(sentence) - 1]
  return sentence + "?"

# GIVEN string representing a declarative sentence,
# RETURNS string representing a question.
def transform(sentence):

  sentence = add_questionmark(sentence)   # '.' -> '?'

  (question, success) = transform_IT_IS(sentence)
  if success: return (question, True)

  # Switch PRP and VBZ Be
  BEING = [ "IS", "ARE", "WAS", "WERE"]
  tokens = nltk.word_tokenize(sentence)
  posTag = nltk.pos_tag([tokens[0]])[0]

  #add_why = (random.randint(0,1) == 1)
  add_why = 0

  #if (tokens[1].upper() in BEING and posTag == 'PRP'):
  if (len(tokens) > 1 and tokens[1].upper() in BEING):
    tokens = [tokens[1].capitalize(), tokens[0].lower()] + tokens[2:]

    if (add_why):
      tokens = ["Why", tokens[0].lower()] + tokens[1:]

    question = " ".join(tokens)
    if ("," in question):
      question = question.split(",")[0] + "?"

    return (question, True)

  if (len(tokens) > 2 and tokens[2].upper() in BEING):
    tokens = [tokens[2].capitalize(), tokens[0].lower(), tokens[1].lower()] + tokens[3:]
    #return (" ".join(tokens), True)

    if (add_why):
      tokens = ["Why", tokens[0].lower()] + tokens[1:]

    question = " ".join(tokens)
    if ("," in question):
      question = question.split(",")[0] + "?"
    return (question, True)

  if (tokens[0].upper() == "IT"):
    tokens = ["What"] + tokens[1:]
    #return (" ",join(tokens), True)
    question = " ".join(tokens)
    if ("," in question):
      question = question.split(",")[0] + "?"
    return (question, True)

  """
  tagged = nltk.pos_tag(tokens)
  entities = nltk.chunk.ne_chunk(tagged)

  (word0, tag0) = tagged[0]
  (word1, tag1) = tagged[1]
  if (tag0 == 'PRP' and tag1 =='VBZ'):
    tokens = [word1.capitalize(), word0.lower()] + tokens[2:]
    return (" ".join(tokens), True)
  """
  #print("FAIL: " + sentence)

  return (sentence, False)

# GIVEN list of sentences,
# RETURNS list of questions.
def process(sentences):
  questions = [ ]
  for sentence in sentences:
    (question, success) = transform(sentence)
    if (success): questions.append( question )
  return questions