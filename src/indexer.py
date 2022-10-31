import gzip
import os
import sys
import json
import re
# import matplotlib.pyplot as plt

inverted_index = {}
scene_list = {}
play_list = {}

def indexer():
    with gzip.open(inputFile, 'rb') as file:
        obj = json.load(file)
    docs = obj['corpus']
    
    for doc in docs:
        text = re.split('\\s+', doc['text'])
        pos = 0
        term_pos = {}
        for term in text:
            if term not in term_pos:
                term_pos[term] = []
            term_pos[term].append(pos)
            pos += 1
        for term in term_pos:
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append([doc['sceneId'], doc['playId'], term_pos[term]])
            if term not in scene_list:
                scene_list[term] = []
            scene_list[term].append(doc['sceneId'])
            if term not in play_list:
                play_list[term] = []
            if doc['playId'] not in play_list[term]:
                play_list[term].append(doc['playId'])

def query():
    queries = []
    with open (queriesFile) as file:
        for line in file:
            queries.append(line.strip().split())
    file.close()
    for query in queries:
        result = []
        query_name = query[0]
        scene_or_play = query[1]
        and_or = query[2].lower().strip()
        word_phrase_K = query[3:]
        scene_play_list = {}

        if scene_or_play == 'play':
            scene_play_list = play_list
        else:
            scene_play_list = scene_list
        docs = set()
        if and_or == 'and':
            for word in word_phrase_K:
                if word in scene_play_list:
                    result.append(scene_play_list[word])
            if len(result) > 0:
                and_list = set(result[0])
                i = 1
                while i < len(result):
                    and_list = and_list & set(result[i])
                    i += 1
                docs = and_list
        else:
            or_list = set()
            for word in word_phrase_K:
                if word in scene_play_list:
                    for s in scene_play_list[word]:
                        or_list.add(s)
            docs = or_list
        
        output_file = open(outputFolder + "/" + query_name + ".txt", "w")
        for l in list(sorted(docs)):
            output_file.write(l + "\n")
        output_file.close()
        docs = set()

def analyze_data():
    with gzip.open(inputFile, 'rb') as f:
        data = json.load(f)
        
    scenes = data["corpus"]
    shortest_scene_id = ""
    shortest_scene_len = float('inf')
    longest_scene_id = ""
    longest_scene_len = 0
    all_plays_len = {}
    word_count = 0
    you_plot = []
    thee_thy_plot = []
    
    for scene in scenes:
        #Find lenghts of play
        current_play = scene["playId"]
        if current_play not in all_plays_len:
            all_plays_len[current_play] = 0
        text = re.split('\\s+', scene["text"])
        all_plays_len[current_play] += len(text)
        #Get number of you words and thy or thee words
        you = text.count("you")
        thee_thy = text.count("thee") + text.count("thy")
        if (you != 0):
            you_plot.append([scene["sceneNum"], you])
        if (thee_thy != 0):
            thee_thy_plot.append([scene["sceneNum"], thee_thy])
        # Find longest and shortest scenes        
        if (len(text) >= longest_scene_len):
            longest_scene_len = len(text)
            longest_scene_id = scene["sceneId"]
        if (len(text) <= shortest_scene_len):
            shortest_scene_len = len(text)
            shortest_scene_id = scene["sceneId"]
        word_count += len(text)
    shortest_play_id = ""
    shortest_play_len = float('inf')
    longest_play_id = ""
    longest_play_len = 0

    for play in all_plays_len:
        if all_plays_len[play] > longest_play_len:
            longest_play_id = play
            longest_play_len = all_plays_len[play]
        if all_plays_len[play] < shortest_play_len:
            shortest_play_id = play
            shortest_play_len = all_plays_len[play]
    
    x = [x[0] for x in you_plot]
    y = [y[1] for y in you_plot]
    x1 = [x[0] for x in thee_thy_plot]
    y1 = [y[1] for y in thee_thy_plot]
    
    print({
        "Shortest Scene": (shortest_scene_id, shortest_scene_len),
        "Longest Scene": (longest_scene_id, longest_scene_len),
        "Shortest Play": (shortest_play_id, shortest_play_len),
        "Longest Play": (longest_play_id, longest_play_len),
        "Average Word per Scene": word_count / len(scenes),
    }   )
    
    plt.plot(x, y)
    plt.plot(x1, y1)
    plt.xlabel("Scene ID")
    plt.ylabel("Word Count")
    plt.show()
        
    return {
        "Shortest Scene": (shortest_scene_id, shortest_scene_len),
        "Longest Scene": (longest_scene_id, longest_scene_len),
        "Shortest Play": (shortest_play_id, shortest_play_len),
        "Longest Play": (longest_play_id, longest_play_len),
        "Average Word per Scene": word_count / len(scenes),
    }

if __name__ == '__main__':
     # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'shakespeare-scenes.json.gz'
    queriesFile = sys.argv[2] if argv_len >= 3 else 'trainQueries.tsv'
    outputFolder = sys.argv[3] if argv_len >= 4 else 'results/'
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    indexer()
    query()
    # analyze_data()