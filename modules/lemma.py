# takes in a word list and returns a list of lists
# each nested list is a list of lemmas for each word

import nltk
from nltk.corpus import wordnet as wn

def lem(words):
  pos_tagged = nltk.pos_tag(words)
  lemmaList = []

  for word, tag in pos_tagged:
    temp = set({word})

    if tag[0] == 'N':
      for ss in wn.synsets(word, pos=wn.NOUN):
        temp.update(set(lemma.name for lemma in ss.lemmas))
    elif tag[0] == 'V':
      for ss in wn.synsets(word, pos=wn.VERB):
        temp.update(set(lemma.name for lemma in ss.lemmas))

    lemmaList.append(temp)

  return lemmaList