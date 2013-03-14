# takes in a word list and returns a list of lists
# each nested list is a list of lemmas for each word

# TODO
# can be refined by POS tagging

from nltk.corpus import wordnet as wn

def lem(list):
  lemmaList = []

  for word in list:
    temp = []
    for ss in wn.synsets(word):
      temp += [lemma.name for lemma in ss.lemmas]
    lemmaList.append(temp)
  
  print lemmaList

lem(['hello','world'])