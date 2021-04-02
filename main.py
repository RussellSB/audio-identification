from fingerprint import fingerprintBuilder
from match import audioIdentification
from evaluate import evaluate


# A wide variety of example cases, performed in order to later evaluate parameters for each step of the pipeline
def index_experiments():

    # Investigating spectrogram type
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/stft.pickle', spectype='stft')
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/mel.pickle', spectype='mel')
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/cqt.pickle', spectype='cqt')

    # Investigating shape (const map)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/disk.pickle', shape='disk')
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/diamond.pickle', shape='diamond')
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/square.pickle', shape='square')
    # Investigating uniformity (const map)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/uniform-true.pickle', uniform=True)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/uniform-false.pickle', uniform=False)
    # Investigating neighbourhood (const map)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/neigh-5.pickle', neighbourhood=5)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/neigh-10.pickle', neighbourhood=10)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/neigh-20.pickle', neighbourhood=20)

    # Investigating targetsize (hashing)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/gap-0.pickle', gap=0)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/gap-50.pickle', gap=50)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/gap-100.pickle', gap=100)
    # Investigating targetsize (hashing)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/t-200-400.pickle', targetsize=(200,400))
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/t-200-200.pickle', targetsize=(200,200))
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/t-400-200.pickle', targetsize=(400,200))


def match_and_evaluate():

    data = ['stft', 'mel', 'cqt',
            'disk', 'diamond', 'square',
            'uniform-true', 'uniform-false',
            'neigh-5', 'neigh-10', 'neigh-20',
            'gap-0', 'gap-50', 'gap-100',
            't-200-400', 't-200-200', 't-400-200']

    #for d in data:
    d='stft'
    audioIdentification('data/query_recordings', 'data/fingerprints/'+d+'.pickle', 'data/output/'+d+'.txt')
    evaluate('data/output/'+d+'.txt')


def run_experiments():
    # index_experiments()
    match_and_evaluate()
    

if __name__ == '__main__':
    run_experiments()