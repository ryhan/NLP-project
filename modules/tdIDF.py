import nltk, math, operator
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

  largest = 0
  for x in vec:
    if x > largest:
      largest = x

  print largest
  print map(lambda y: y/largest,vec)

def files():  
  for i in xrange(8,11):
      for j in xrange(1,5):
          for k in xrange(1,10):
            partic = {}
            if i < 10:
              path = '../Question_Answer_Dataset_v1.1/S0'+str(i)+'/data/set'+str(j)+'/a'+str(k)+'.txt'
            else:
              path = '../Question_Answer_Dataset_v1.1/S'+str(i)+'/data/set'+str(j)+'/a'+str(k)+'.txt'
            cfile = open(path,'r')

            for tok in nltk.word_tokenize(cfile.read()):
              partic[tok] = partic.get(tok,0) + 1
            dicts.append(partic)
            cfile.close()






main('and kangaroo','and and kangaroo')


