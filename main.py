from fingerprint import fingerprintBuilder
from match import audioIdentification
from evaluate import evaluate


# Runs final evaluation, indexing from best parameters deduced from experiments
def run_final():
    #fingerprintBuilder('data/database_recordings', 'data/fingerprints/final.pickle', spectype='stft', shape='disk', uniform=False, gap=0, targetsize=(400,200))
    #audioIdentification('data/query_recordings', 'data/fingerprints/final.pickle', 'data/output/final.txt')
    evaluate('data/output/final.txt', 'avg')
    evaluate('data/output/final.txt', 'classical')
    evaluate('data/output/final.txt', 'pop')

if __name__ == '__main__':
    run_final()