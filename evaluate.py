# Test match of wavfile title with ground_truth title 
def strmatch(ground_truth, wavfile):
    if wavfile[:-4] == ground_truth:
        return True
    else:
        return False


def get_recalls(f, lines, total, genre='classical'):

    # Initialising average recall seperately for ranks 1, 2 and 3
    recall_rank = [0, 0, 0]

    for line in lines:
        result = line.strip().split('\t')
        retrieved = result[1:]
        ground_truth = result[0].split('-')[0]

        # Skips if query file is not of the desired genre
        if not genre in ground_truth: continue
        
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

    return recall_rank

# Evaluates results file and prints results
def evaluate(outfile):

    f = open(outfile, 'r')
    lines = f.readlines()
    total = len(lines)

    recalls_classical = get_recalls(f, lines, total, genre='classical')
    recalls_pop = get_recalls(f, lines, total, genre='pop')
    recalls_avg = [(i + j)/2 for i, j in zip(recalls_classical, recalls_pop)]

    # Prints the overall results for the current experiment/outfile
    print(outfile, recalls_classical)
    print(outfile, recalls_pop)
    print(outfile, recalls_avg)
    print()

