#!/usr/bin/python

# sourceContentSelector.py
# Given a question, returns relevant parts of an article

import sys, os, string, re
import nltk
from nltk.stem import PorterStemmer
import collections
import numpy as np
sys.path.append("modules")
import lemma

# Any keywords in the sentence will be these parts of speech
key_POS = set(["CD","FW","NN","NNS","NNP","NPS","VB","VBD","VBG","VBN","VBP","VBZ"])
# auxiliary verbs we should ignore
aux = set(["is", "was", "did", "does", "do", "were", "are"])

# we should probably change this to the WordNet lemmatizer, but this is ok for now
ps = PorterStemmer()

MAX_NGRAMS = 5

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
      if sent.strip() == "": continue
      sentence = nltk.tokenize.word_tokenize(sent)
      s = score(question, sentence)
      scored_sent.append((sent, s))
  return scored_sent

# Scores a sentence based on how well we think it answers the question
def score(question, sentence):
    score = 0
    sentence = map(ps.stem, sentence)
    keywords = getKeywords(question)
    question = map(ps.stem, question)
    score += proximity(keywords, sentence)
    question_ngrams = count_ngrams(question, MAX_NGRAMS, True)
    sentence_ngrams = count_ngrams(sentence, MAX_NGRAMS, True)
    precision, recall = bleu_score(question_ngrams, len(question), sentence_ngrams, len(sentence), 5)
    f1 = (2*precision*recall)/(precision+recall)
    score += 2*f1
    return score

# Finds the shortest window in the targest sentence
# in which all keywords appear, and assigns a score.
def proximity(keywords, sentence):
    length = len(sentence)
    for i in range(len(keywords), length+1):
        for j in range(length+1-i):
            words = set(sentence[j:i+j])
            if keywords <= words:
                return 1 - i/length
    return 0

# From YC
def count_ngrams(tokens, n, all_smaller=False):
  """Counts the frequency of n-grams in the given list of tokens.

  :param tokens: list of tokens to compute ngrams for.
  :param n: number of grams to count.
  :param all_smaller: set to True to include all n-grams from n=1 to n.
  """

  counts = collections.Counter()
  for k in xrange(1 if all_smaller else n, n+1):
    for i in xrange(len(tokens)-k+1):
      counts[tuple(tokens[i:i+k])] += 1

  return counts
#end def

def bleu_score(ref_ngrams, ref_len, pred_ngrams, pred_len, n):
  """Calculate the BLEU precision and recall from ngram counts.

  :param ref_ngrams: reference sentence ngrams.
  :param ref_len: reference sentence length.
  :param pred_ngrams: predicted sentence ngrams.
  :param pred_len: predicted sentence length.
  :param n: the maximum number of ngrams to consider.
  """

  if not ref_len or not pred_len: return 0.0, 0.0
  if not len(ref_ngrams) or not len(pred_ngrams): return 0.0, 0.0

  ngram_score = np.zeros(n, dtype=np.float32) + 0.1

  # compute the ngram intersections
  for ngram, c in ref_ngrams.iteritems():
    if len(ngram) > n: continue

    k = min(c, pred_ngrams[ngram])
    ngram_score[len(ngram) - 1] += k
  #end for

  # compute the geometric mean of the ngrams precision/recall
  precision = np.mean(np.log(ngram_score / len(pred_ngrams)))
  recall = np.mean(np.log(ngram_score / len(ref_ngrams)))

  # apply the brevity penalty
  if pred_len <= ref_len: precision += 1.0 - (float(ref_len) / pred_len)
  if ref_len <= pred_len: recall += 1.0 - (float(pred_len) / ref_len)

  precision = np.exp(precision)
  recall = np.exp(recall)

  return precision, recall
#end def


# Compare the overlap of two sentences using ngrams
# (up to trigrams). This is similar to the BLEU score.
#def ngramWeight(question, sentence):
#  #stem and take set intersections for unigrams
#  uniQ = map(ps.stem, question)
#  uniS = sentence
#  unigram = set(uniQ).intersection(set(uniS))
#
#
#  #get all bigram overlaps, rolls around end of sentence
#  if len(uniQ) > 1 and len(uniS) > 1:
#    bigramQ = set([uniQ[i-1]+uniQ[i] for i,word in enumerate(uniQ)])
#    bigramS = set([uniS[i-1]+uniS[i] for i,word in enumerate(uniS)])
#    bigram = bigramQ.intersection(bigramS)
#  else:
#      bigram = {}
#
#  if len(uniQ) > 2 and len(uniS) > 2:
#    trigramQ = set([uniQ[i-2]+uniQ[i-1]+uniQ[i] for i,word in enumerate(uniQ)])
#    trigramS = set([uniS[i-2]+uniS[i-1]+uniS[i] for i,word in enumerate(uniS)])
#    trigram = trigramQ.intersection(trigramS)
#  else:
#      trigram = {}
#
#
#  lam1 = 0.2
#  lam2 = 0.3
#  lam3 = 0.5
#
#  return lam1*len(unigram) + lam2*len(bigram) + lam3*len(trigram)

# for testing
if __name__ == '__main__':
    print proximity(set(["the", "moon", "stroke"]), ["I",  "want", "to", "see", "the", "moon", "stroke"])
