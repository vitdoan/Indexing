# Breakdown
### My indexing and query functions are both in src/indexer.py

# Description
### In my indexer function, I iterated through all documents and built the inverted index with the form of Map(Term, List(Posting)). Posting is a list of [String sceneId, String playId, int[] positions]. I also created 2 dictionaries: scene_list(term, String[] scene_Id) and play_list(term, String[] play_Id) to latter use in my query function. 

# Libraries
### matplotlib is used to graph the plot. The others are used to handle file input output.

# Dependencies
### matplotlib

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