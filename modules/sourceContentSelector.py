#!/usr/bin/python

# sourceContentSelector.py
# Given a question, returns relevant parts of an article

import sys, os, string, re
import nltk
from nltk.stem import PorterStemmer

# parts of speech of any "important" word
key_POS = set(["CD","FW","NN","NNS","NNP","NPS","VB","VBD","VBG","VBN","VBP","VBZ"])

# auxiliary verbs we should ignore
aux = set(["is", "was", "did", "does", "do", "were", "are"])

# we should probably change this to the WordNet lemmatizer, but this is ok for now
ps = PorterStemmer()

# Given a question, returns a list of keywords
def getKeywords(question):
  tagged = nltk.tag.pos_tag(question)
  #nltk.ne_chunk(tagged)
  tagged = [pair for pair in tagged if pair[1] in key_POS and pair[0].lower() not in aux]
  result = []
  for tag in tagged:
    if tag[1] == "NNP":
      # named entities aren't that helpful until we implement coreference resolution
      result.append(tag[0])
    else:
      result.append(ps.stem(tag[0]))
  return set(result)

# Given a question, returns relevant parts of an article
def getRelevantSentences(question, article):
  relevant = []
  sentences = nltk.tokenize.sent_tokenize(article)
  for sent in sentences:
      sentence = nltk.tokenize.word_tokenize(sent)
      sentence = map(ps.stem, sentence)
      s = score(question, sentence)
      relevant.append((sent, s))
  return relevant

def score(question, sentence):
    score = 0
    score += ngramWeight(question, sentence)
    keywords = getKeywords(question)
    score += proximity(keywords, sentence)
    return score

# measures the proximity of the keywords from the original query to each other
def proximity(keywords, sentence):
    length = len(sentence)
    for i in range(len(keywords), length+1):
        for j in range(length+1-i):
            words = set(sentence[j:i+j])
            if keywords <= words:
                return 10-i
    return 0

# compare two sentences using ngrams (upto trigram)
def ngramWeight(question, sentence):
  #stem and take set intersections for unigrams
  uniQ = map(ps.stem, question)
  uniS = sentence
  unigram = set(uniQ).intersection(set(uniS))

  #get all bigram overlaps, rolls around end of sentence
  bigramQ = {uniQ[i-1]+uniQ[i] for i,word in enumerate(uniQ)}
  bigramS = {uniS[i-1]+uniS[i] for i,word in enumerate(uniS)}
  bigram = bigramQ.intersection(bigramS)

  trigramQ = {uniQ[i-2]+uniQ[i-1]+uniQ[i] for i,word in enumerate(uniQ)}
  trigramS = {uniS[i-2]+uniS[i-1]+uniS[i] for i,word in enumerate(uniS)}
  trigram = trigramQ.intersection(trigramS)

  lam1 = 0.2
  lam2 = 0.3
  lam3 = 0.5

  return lam1*len(unigram) + lam2*len(bigram) + lam3*len(trigram)

if __name__ == '__main__':
    print proximity(set(["the", "moon", "stroke"]), ["I",  "want", "to", "see", "the", "moon", "stroke"])
