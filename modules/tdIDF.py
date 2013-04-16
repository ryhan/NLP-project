import nltk
import math

dicts = []

def main(question, article):
  ddict = get_counts()
  for tok in nltk.word_tokenize(article):
    ddict[tok] = ddict.get(tok, 0) + 1

  vec = []
  for tok in nltk.word_tokenize(question):
    tf = ddict.get(tok, 0)
    idf = math.log(float(108)/len(filter(lambda x:tok in x.keys(),dicts)) + 1)
    vec.append(tf*idf)

  largest = max(vec)
  normalized = map(lambda y: y/largest, vec)
  return normalized

articles_per_set = 9

def get_counts():
  counts = {}
  sets_per_year = 4
  for year in ("S08", "S09", "S10"):
    for i in xrange(1, num_sets):
      for j in xrange(1, articles_per_set+1):
        path = "../Question_Answer_Dataset_v1.1/"+year+"/data/set"+str(i)+"/a"+str(j)+".txt"
        cfile = open(path).read()
        partic = {}
        for tok in nltk.word_tokenize(cfile):
          partic[tok] = partic.get(tok, 0) + 1
        counts.append(partic)
    sets_per_year += 1
  return counts