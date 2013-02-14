NLP Term Project
===========
11411 Group 6 Project. See [NLP Project Page](https://www.ark.cs.cmu.edu/NLP/S13/project.php)

### Contributors

- [Daniel Sedra](https://github.com/dsedra "github.com/dsedra")
- [Stephen Bly](https://github.com/gardenhead "github.com/gardenhead")
- [Ryhan Hassan](https://github.com/ryhan "github.com/ryhan")

### Timeline

- Thursday February 7, Stub Program (Ryhan)  & Initial Plan (Daniel)
- Tuesday February 26, Progress Report 1 (Stephen)
- Thursday March 21, Progress Report 2 (Ryhan)
- Tuesday April 9, Dry run system
- Tuesday April 16, Project code due
- Tuesday April 30, Demos at Google
- Thursday May 2, Final Report

## Asking Program
```
./ask article.txt nquestions
```
The asking program takes an 
- `article.txt` containing a Wikipedia article and 
-  an integer `nquestions`.

## Answering Program
```
./answer article.txt questions.txt
```
The answering program takes an 
- `article.txt` containing a Wikipedia article and 
- a textfile `questions.txt` containing one question per line.

## Getting Started
### Permissions
```
chmod +x ask
chmod +x answer
```

### Installing NLTK
See [NLTK installation guide](http://nltk.org/install.html)

First download `setuptools`, http://pypi.python.org/pypi/setuptools
```
sudo sh Downloads/setuptools-...egg
sudo easy_install pip 
sudo pip install -U numpy
sudo pip install -U pyyaml nltk
```
### Download NLTK datasets

```
python
>>> import nltk
>>> nltk.download()
```
Once the NLTK Downloader GUI pops up, download all to `/Users/USERNAME/nltk_data`