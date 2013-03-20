# takes in a word list and returns a list of lists
# each nested list is a list of lemmas for each word

import nltk
from nltk.corpus import wordnet as wn

def lem(list):

  pos = nltk.pos_tag(list)

  lemmaList = []

  for word,tag in pos:
    temp = set({word})

    if tag[0] == 'N':
      for ss in wn.synsets(word, pos=wn.NOUN):
        temp.update(set(lemma.name for lemma in ss.lemmas))
      lemmaList.append(temp)
    elif tag[0] == 'V':
      for ss in wn.synsets(word, pos=wn.VERB):
        temp.update(set(lemma.name for lemma in ss.lemmas))
      lemmaList.append(temp)
    else:
      lemmaList.append({word})

  return lemmaList
