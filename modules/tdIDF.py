import nltk
import math
from nltk.tokenize import word_tokenize

dicts = []

def main(question,article):
  files()
  ddict = {}
  vec = []
  for tok in nltk.word_tokenize(article):
    ddict[tok] = ddict.get(tok,0) + 1

  for tok in nltk.word_tokenize(question):
    tf = ddict.get(tok,0)
    idf = math.log(float(108)/len(filter(lambda x:tok in x.keys(),dicts)) + 1)
    vec.append(tf*idf)

  largest = max(vec)
  print map(lambda y: y/largest,vec)

def files():
  for year in ("S08", "S09", "S10"):
      for i in xrange(1,5):
          for j in xrange(1,10):
            partic = {}
            path = "../Question_Answer_Dataset_v1.1/"+year+"/data/set'+str(i)+'/a'+str(j)+'.txt"
            cfile = open(path).read()

            for tok in nltk.word_tokenize(cfile):
              partic[tok] = partic.get(tok,0) + 1
            dicts.append(partic)

main('and kangaroo','and and kangaroo')
