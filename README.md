NLP Term Project
===========
11411 Group 6 Project
Final Demo Tuesday, April 30 at Google Pittsburgh
See [NLP Project Page](https://www.ark.cs.cmu.edu/NLP/S13/project.php)

## Getting Started
The objective of this project is to build two programs which can generate and answer questions related to a Wikipedia article.

### Asking Program
```
sh ask.sh article.txt nquestions
```
The asking program takes an `article.txt` containing a Wikipedia article and an integer `nquestions`.

To generate questions from a real article, try
```
sh ask.sh data/set1/a6.txt 3
```


### Answering Program
```
sh answer.sh article.txt questions.txt
```
The answering program takes an `article.txt` containing a Wikipedia article and a textfile `questions.txt` containing one question per line.

To answer questions from a real article, try
```
sh answer.sh data/set1/a6.txt fake_questions.txt
```

## About

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