# Breakdown
### My indexing and query functions are both in src/indexer.py

# Description
### Indexer function, 
Documents are parsed and iterated to build the inverted index with the form of Map(Term, List(Posting)). 

Posting is a list of [String sceneId, String playId, int[] positions]. 

2 dictionaries are also created: scene_list(term, String[] scene_Id) and play_list(term, String[] play_Id) to latter use in my query function. 

# Libraries
### matplotlib 
- Used to graph the plot. 
- The others are used to handle file input output.

# Dependencies
* matplotlib
* json
* gzip
* os
* sys
* re

# Building
### In your local environment, execute: 
``` 
python3 -m pip install -U pip
python3 -m pip install -U matplotlib
```

# Running
### In your local environment, execute: 
```
python3 indexer.py
```