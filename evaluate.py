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

