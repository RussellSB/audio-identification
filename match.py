from collections import Counter, defaultdict
from fingerprint import fingerprintBuilder
from util import load_pickle
from tqdm.auto import tqdm
import numpy as np
import os


def get_offsets(q, db):

    time_offsets = defaultdict(list)  # stores a list of offset values for each hashkey match

    for feature in q:
        if feature in db.data:
            
            data_start_time = db.data[feature][0]
            query_start_time = q[feature]

            identity = db.data[feature][1]
            title = db.identity2title[identity]

            time_offset = data_start_time - query_start_time # compute starting time differences
            time_offsets[title].append(time_offset)  # storing by song title with feature match

    return time_offsets

# Matches query and database features and returns scoring
def match(queryfile, db):

    q = db.fingerprint(queryfile)  # finger print with same database params
    time_offsets = get_offsets(q, db)  # gets offsets between db and query fingerprints
    scoring = Counter() # TODO: change

    for title in time_offsets:
        track_offsets = time_offsets[title]  # List of time offsets
        offset_count = Counter()  # counter dictionary

        for offset in track_offsets:
            offset_count[offset] += 1  # count each offset per track

        counts = sorted(offset_count.values())
        scoring[title] = counts[-1] # add the most popular offset as the score
        
    return scoring.most_common()[:3]  # returns top three most common titles


# Performs query matching for all queries in query set
def audioIdentification(querysetPath, indexfile, outfile):
    db = load_pickle(indexfile)

    open(outfile, 'w').close() # Clears file from any previous runs
    f = open(outfile, 'a')  # Opens file for appending

    for queryfile in tqdm(os.listdir(querysetPath)):
        top_matches = match(querysetPath+'/'+queryfile, db)

        # Consider top three matches for results output
        line = queryfile + '\t'
        for matches in top_matches:
            line += matches[0] + '\t'  # Append song name in order of rank
        f.write(line+'\n')
        
