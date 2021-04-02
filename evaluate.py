# Test match of wavfile title with ground_truth title 
from numpy.lib.function_base import append


def strmatch(ground_truth, wavfile):
    if wavfile[:-4] == ground_truth:
        return True
    else:
        return False


def get_recalls(f, lines, genre='classical'):

    results_genre = []  # stores the results specific to specified genre

    # Filters lines with respect to genre
    for line in lines:
        line = line.strip().split('\t')
        retrieved = line[1:]
        ground_truth = line[0].split('-')[0]

        # Skips if query file is not of the desired genre
        if not genre in ground_truth: continue
        results_genre.append({'ground_truth': ground_truth, 'retrieved': retrieved} )

    total = len(results_genre)
    recall_rank = [0, 0, 0]  # Initialising average recall seperately for ranks 1, 2 and 3

    # evaluates with respect to genre
    for result in results_genre:
        retrieved = result['retrieved']
        ground_truth = result['ground_truth']

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
# scope is either 'classical', 'pop' or 'avg'
def evaluate(outfile, scope):

    f = open(outfile, 'r')
    lines = f.readlines()

    recalls_classical = get_recalls(f, lines, genre='classical')
    recalls_pop = get_recalls(f, lines, genre='pop')
    recalls_avg = [(i + j)/2 for i, j in zip(recalls_classical, recalls_pop)]

    # Prints the overall results for the current experiment/outfile
    if(scope=='classical'): print(outfile, recalls_classical)
    if(scope=='pop'): print(outfile, recalls_pop)
    if(scope=='avg'): print(outfile, recalls_avg)

