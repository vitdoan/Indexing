# Breakdown
My indexing and query functions are both in src/indexer.py

# Description
### indexer()
Documents are parsed and iterated to build the inverted index with the form of Map(Term, List(Posting)). 

Posting is a list of [String sceneId, String playId, int[] positions]. 

2 dictionaries are also created: scene_list(term, String[] scene_Id) and play_list(term, String[] play_Id) to latter use in my query function. 

### query()
* Handling And: 
- Iterate through the scene or play list and store all the documents ID that contains the words in word_phrase_K in an array. Iterate through that 2D and find the intersection of each its array elements by using & operator for 2 sets.

* Handling Or:
- Iterate through the scene or play list and add all of the documents ID that contains one of the words in word_phrase_K. Add each element into a set and duplicates are prevented since set does not contain duplicate.

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
### To enable graph
Uncomment ```import matplotlib.pyplot as plt``` and ```analyze_data()``` in main function.

