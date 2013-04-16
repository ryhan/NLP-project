#!/usr/bin/python

# sourceContentSelector.py
# Given a question, returns relevant parts of an article

import sys, os, string, re
import nltk
from nltk.stem import PorterStemmer
import collections
import numpy as np

# Ignore words that don't have these parts of speech when computing keywords
key_POS = set(["CD","FW","NN","NNS","NNP","NPS","VB","VBD","VBG","VBN","VBP","VBZ"])
# auxiliary verbs we should ignore
aux = set(["is", "was", "did", "does", "do", "were", "are"])

# the porter stemmer! yay!
ps = PorterStemmer()

# check up to 5-grams for the bleu score
MAX_NGRAMS = 5

# Given a question, returns a list of keywords
def getKeywords(question):
  tagged = nltk.tag.pos_tag(question)
  tagged = [pair for pair in tagged if pair[1] in key_POS and pair[0].lower() not in aux]
  return {ps.stem(tag[0]) for tag in tagged}

# Given a question, return a list of each sentence in the article
# with a score attached to it
def getScoredSentences(question, article):
  scored_sentences = []
  sentences = nltk.tokenize.sent_tokenize(article)
  for sentence in sentences:
      if sentence.strip() == "": continue
      tokenized = nltk.word_tokenize(sentence.lower())
      s = score(question, tokenized)
      scored_sentences.append((sentence, s))
  return scored_sentences

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

  # compute the geometric mean of the ngrams precision/recall
  precision = np.mean(np.log(ngram_score / len(pred_ngrams)))
  recall = np.mean(np.log(ngram_score / len(ref_ngrams)))

  # apply the brevity penalty
  if pred_len <= ref_len: precision += 1.0 - (float(ref_len) / pred_len)
  if ref_len <= pred_len: recall += 1.0 - (float(pred_len) / ref_len)

  precision = np.exp(precision)
  recall = np.exp(recall)

  return precision, recall
