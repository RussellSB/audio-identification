from collections import Counter
from fingerprint import fingerprintBuilder
from util import load_pickle
from tqdm import tqdm
import os

# Test match of wavfile title with ground_truth title 
def strmatch(ground_truth, wavfile):
    if wavfile[:-4] == ground_truth:
        return True
    else:
        return False

# Evaluates results file and prints results
def evaluate(outfile):
    f = open(outfile, 'r')
    lines = f.readlines()
    total = len(lines)

    # Initialising average recall seperately for ranks 1, 2 and 3
    recall_rank = [0, 0, 0]

    for line in lines:
        result = line.strip().split('\t')
        retrieved = result[1:]
        ground_truth = result[0].split('-')[0]
        
        # Update ranks up to a cut off of three accordingly
        if strmatch(ground_truth, retrieved[0]):
            recall_rank[0] += 1/total
            recall_rank[1] += 1/(total*2)
            recall_rank[2] += 1/(total*3)

        if strmatch(ground_truth, retrieved[1]):
            recall_rank[1] += 1/(total*2)
            recall_rank[2] += 1/(total*3)
        
        if strmatch(ground_truth, retrieved[2]):
            recall_rank[2] += 1/(total*3)

    print(outfile, recall_rank) 


# Evaluate recall of results of paramater varied experiments
def evaluate_experiments():

    # data = ['stft', 'mel', 'cqt',
    #         'disk', 'diamond', 'square',
    #         'uniform-true', 'uniform-false',
    #         'neigh-5', 'neigh-10', 'neigh-20', 'neigh-50',
    #         'gap-0', 'gap-50', 'gap-100',
    #         't-200-400', 't-200-200', 't-400-200']

    # for d in data:
    #     evaluate('data/output/'+d+'.txt')

    evaluate('data/output/neigh-50.txt')

if __name__ == '__main__':
    evaluate_experiments()

