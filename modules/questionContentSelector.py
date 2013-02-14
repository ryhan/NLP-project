#!/usr/bin/python

# questionContentSelector.py
# Authored by Ryhan Hassan | rhassan@andrew.cmu.edu
# Identifies declarative sentences in source text
# that are candidates for question generation.

import re
import nltk

# Use part-of-speech tagging and entity chunking to 
# score the usefulness of a sentence.
def entity_score(sentence):
  # tokens = nltk.word_tokenize(sentence)
  # tagged = nltk.pos_tag(tokens)
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

# GIVEN source_text string
# RETURNS list of candidate strings
def process(source_text, n):
  if (n < 1): n = 10
  print(n)
  # Should probably apply co-reference resolution first.
  sentences = nltk.sent_tokenize(source_text)
  sentences = sorted(sentences, key = lambda (x): -1* sentence_score(x))
  return sentences[:int(n)]
