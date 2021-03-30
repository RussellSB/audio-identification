from collections import Counter
from fingerprint import fingerprintBuilder
from util import load_pickle
from tqdm import tqdm
import os


# Matches query and database features and returns scoring
def match(queryfile, db):
    q = db.fingerprint(queryfile)
    
    scoring = Counter()

    for feature in q:
        if feature in db.data:

            identity = db.data[feature][1]
            title = db.identity2title[identity]
            scoring[title] += 1

    return scoring.most_common()[:3]  # returns top three most common


# Performs query matching for all queries in query set
def audioIdentification(querysetPath, indexfile, outfile):
    db = load_pickle(indexfile)

    f = open(outfile, 'a')

    for queryfile in tqdm(os.listdir(querysetPath)):
        top_matches = match(querysetPath+'/'+queryfile, db)

        # Consider top three matches for results output
        line = queryfile + '\t'
        for matches in top_matches:
            line += matches[0] + '\t'  # Append song name in order of rank
        f.write(line+'\n')
        

# Query all the database versions indexed in different ways and save results
def query_experiments():

    data = ['stft', 'mel', 'cqt',
            'disk', 'diamond', 'square',
            'uniform-true', 'uniform-false',
            'neigh-5', 'neigh-10', 'neigh-20',
            'gap-0', 'gap-50', 'gap-100',
            't-200-400', 't-200-200', 't-400-200']

    for d in data:
        audioIdentification('data/query_recordings', 'data/fingerprints/'+d+'.pickle', 'data/output/'+d+'.txt')


if __name__ == '__main__':
    query_experiments()