#!/usr/bin/python

# questionContentSelector.py
# Authored by Ryhan Hassan | rhassan@andrew.cmu.edu
# Identifies declarative sentences in source text
# that are candidates for question generation.

import re
import nltk

# Use part-of-speech tagging to 
# score the usefulness of a sentence.
def entity_score(sentence):
  tokens = nltk.word_tokenize(sentence)
  tokensU = map(lambda (x): x.upper, tokens)
  if (2 < len(tokens) and len(tokens) < 12):
    if ("IS" in tokensU or "WAS" in tokensU or
        "WERE" in tokensU or "BEING" in tokensU or
        "ARE" in tokensU):

      if (nltk.pos_tag([tokens[0]])[0] == "PRP"):
        return 1.0
      else:
        return 0.5 

  #tagged = nltk.pos_tag(tokens)
  # entities = nltk.chunk.ne_chunk(tagged)
  score = 0
  return score

# Temporary naive approach to scoring a sentence
def naive_score(sentence):
  word_count = len(nltk.word_tokenize(sentence))
  weird = not any((c in sentence) for c in "?;:[]()"),

  features = [
    not weird,             # Avoid weird characters
    "It is" in sentence,   # Look for "It is ..."
    " is " in sentence,    # Look for "[foo] is [bar]"
    4 < word_count < 12,  
    5 < word_count < 7
  ]
  return float(sum(features))/len(features)

def sentence_score(sentence):
  return 0.1*naive_score(sentence) + 0.9*entity_score(sentence)

# GIVEN source_text string and
# GIVEN n integer representing number of candidates to return,
# RETURNS list of candidate strings
def process(source_text, n):
  sentences = nltk.sent_tokenize(source_text)
  sentences = sorted(sentences, key = lambda (x): -sentence_score(x))
  return sentences[:int(n)]
