#!/usr/bin/python

# sourceContentSelector.py
# Given a question, returns relevant parts of an article

import sys, os, string, re
import nltk
from nltk.stem import PorterStemmer
sys.path.append("modules")
import lemma

# Any keywords in the sentence will be these parts of speech
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

# Given a question, return a list of each sentence in the article
# with a score attached to it
def getScoredSentences(question, article):
  scored_sent = []
  sentences = nltk.tokenize.sent_tokenize(article)
  for sent in sentences:
      sentence = nltk.tokenize.word_tokenize(sent)
      sentence = map(ps.stem, sentence)
      s = score(question, sentence)
      scored_sent.append((sent, s))
  return scored_sent

# Scores a sentence based on how well we think it answers the question
def score(question, sentence):
    score = 0
    score += ngramWeight(question, sentence)
    keywords = getKeywords(question)
    score += proximity(keywords, sentence)
    return score

# Finds the shortest window in the targest sentence
# in which all keywords appear, and assigns a score.
def proximity(keywords, sentence):
    length = len(sentence)
    for i in range(len(keywords), length+1):
        for j in range(length+1-i):
            words = set(sentence[j:i+j])
            if keywords <= words:
                return max(20-i, 0)
    return 0

# Compare the overlap of two sentences using ngrams
# (up to trigrams). This is similar to the BLEU score.
def ngramWeight(question, sentence):
  #stem and take set intersections for unigrams
  uniQ = map(ps.stem, question)
  uniS = sentence
  unigram = set(uniQ).intersection(set(uniS))


  #get all bigram overlaps, rolls around end of sentence
  if len(uniQ > 1):
    bigramQ = {uniQ[i-1]+uniQ[i] for i,word in enumerate(uniQ)}
    bigramS = {uniS[i-1]+uniS[i] for i,word in enumerate(uniS)}
    bigram = bigramQ.intersection(bigramS)
  else:
      bigram = 0

  if len(uniQ > 2):
    trigramQ = {uniQ[i-2]+uniQ[i-1]+uniQ[i] for i,word in enumerate(uniQ)}
    trigramS = {uniS[i-2]+uniS[i-1]+uniS[i] for i,word in enumerate(uniS)}
    trigram = trigramQ.intersection(trigramS)
  else:
      trigram = 0

      
  lam1 = 0.2
  lam2 = 0.3
  lam3 = 0.5

  return lam1*len(unigram) + lam2*len(bigram) + lam3*len(trigram)

# for testing
if __name__ == '__main__':
    print proximity(set(["the", "moon", "stroke"]), ["I",  "want", "to", "see", "the", "moon", "stroke"])
