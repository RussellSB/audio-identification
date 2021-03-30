import librosa
from matplotlib import pyplot as plt
import numpy as np

import scipy.ndimage as ndimage
from skimage.morphology import disk, diamond, square

import os
from tqdm.auto import tqdm
from util import save_pickle

# Making a class so that parameter information can be stored alongside data in an object
class fingerprintBuilder:
    def __init__(self, dataPath, indexfile,
                spectype='stft', n_fft=1024, window='hann', win_length=1024, hop_length=512,
                shape='disk', neighbourhood=10, uniform=True, show=False,
                gap=50, targetsize=(200, 200)):

        # Parameters for spectrogram
        self.spectype = spectype
        self.n_fft = n_fft
        self.window = window
        self.win_length = win_length
        self.hop_length = hop_length

        # Parameters for peak picking
        self.shape = shape
        self.neighbourhood = neighbourhood
        self.uniform = uniform
        self.show = show

        # Parameters for combinatorial hashing
        self.gap = gap
        self.targetsize = targetsize

        # Stores hashed data for matching
        self.data = {}
        self.identity2title = []

        # Looping through all data and saving (assumes the whole directory is full of wavs to index)
        for identity, filename in enumerate(tqdm(os.listdir(dataPath))):
            self.identity2title.append(filename)  # Keeping track of id and title with .wav at end
            hash_dict = self.fingerprint(dataPath+'/'+filename, identity)
            self.data.update(hash_dict)

        save_pickle(self, indexfile)  # saves itself as an object with data and parameter info

    # Finger prints an audio file with a number of adjustable parameters
    def fingerprint(self, audio_file, identity=None):
        
        x, sr = librosa.load(os.path.join(audio_file))
        
        # Loading spectrogram 
        if self.spectype == 'stft':
            D = np.abs(librosa.stft(x, self.n_fft, self.hop_length, self.win_length, self.window))
        elif self.spectype == 'mel':
            D = librosa.feature.melspectrogram(x, sr, n_fft=self.n_fft, hop_length=self.hop_length, win_length=self.win_length, window=self.window)
        elif self.spectype == 'cqt':
            D = np.abs(librosa.cqt(x, sr, self.hop_length, window=self.window))
        else: 
            raise Exception('Parameter spectype must be set to \'stft\', \'mel\' or \'cqt\'')
        
        peaks = self.pick_peaks(D)
        hash_dict = self.hash_peaks(peaks, identity)
        
        return hash_dict


    # Custom implementation for picking peaks, accepts spectrogram as input
    def pick_peaks(self, D):

        # The only shapes available are square, diamond and disk.
        assert self.shape == 'square' or self.shape == 'diamond' or self.shape == 'disk',\
        'Parameter shape must be set to \'disk\', \'diamond\' or \'square\''

        # Compute the constellation map
        data = np.log(D)
        footprint = eval(self.shape + '(' + str(self.neighbourhood) + ')')  # formulates kernel from params
        max_blobs = ndimage.maximum_filter(data, footprint=footprint)
        const_map = data == max_blobs

        # Only considers the points within a normal distribution
        if self.uniform:
            stdev = np.std(max_blobs)
            mean = np.mean(max_blobs)
            distribution = np.multiply(data >= (mean-stdev), data <= (mean+stdev))
            const_map = np.multiply(const_map, distribution)

        if self.show:
            plt.figure(figsize=(20, 5))
            plt.title('Spectrogram')
            plt.xlabel('Frames')
            plt.ylabel('Frequency bins')
            plt.imshow(librosa.amplitude_to_db(D,ref=np.max), origin='lower', cmap='gray_r')

            plt.figure(figsize=(20, 5))
            plt.title('Max Blobs')
            plt.xlabel('Frames')
            plt.ylabel('Frequency bins')
            plt.imshow(max_blobs, origin='lower', cmap='gray_r')

            plt.figure(figsize=(20, 5))
            plt.title('Constellaiton Map')
            plt.xlabel('Frames')
            plt.ylabel('Frequency bins')
            plt.imshow(const_map, origin='lower', cmap='gray_r')

        # Gets coordinate information
        freq_y, time_x = np.nonzero(const_map)
        coordinates = list(zip(freq_y, time_x))

        # Sorts with respect to time then frequency
        coordinates = sorted(coordinates , key=lambda p: [p[1], p[0]])

        return coordinates


    # Note that size is in terms of (frequency bins, time frames)
    def hash_peaks(self, peaks, identity=None):
        
        d = {}

        # Iterate through anchor points
        for anchor in peaks:
            
            # Preparing target zone boundaries
            freq_start = anchor[0] - (self.targetsize[0]//2)
            freq_end = anchor[0] + (self.targetsize[0]//2)
            time_start = anchor[1] + self.gap
            time_end = time_start + self.targetsize[1]
            
            # Hash only points within the target zone
            for target in peaks:
                
                # Validates as a target if within target zone
                if target[0] >= freq_start and target[0] <= freq_end \
                    and target[1] >= time_start and target[1] <= time_end:
                    
                    # Generates key-value pair with information
                    time_diff = target[1] - anchor[1]
                    key = str(anchor[0]) + str(target[0]) + str(time_diff)
                    if identity is not None: d[key] = (anchor[1], identity)
                    else: d[key] = anchor[1]

        return d


# A wide variety of example cases, performed in order to evaluate parameters for each step of the pipeline
def index_experiments():

    # # Investigating spectrogram type
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/stft.pickle', spectype='stft')
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/mel.pickle', spectype='mel')
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/cqt.pickle', spectype='cqt')

    # # Investigating shape (const map)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/disk.pickle', shape='disk')
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/diamond.pickle', shape='diamond')
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/square.pickle', shape='square')
    # # Investigating uniformity (const map)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/uniform-true.pickle', uniform=True)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/uniform-false.pickle', uniform=False)
    # Investigating neighbourhood (const map)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/neigh-5.pickle', neighbourhood=5)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/neigh-10.pickle', neighbourhood=10)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/neigh-20.pickle', neighbourhood=20)
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/neigh-50.pickle', neighbourhood=50)

    # # Investigating targetsize (hashing)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/gap-0.pickle', gap=0)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/gap-50.pickle', gap=50)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/gap-100.pickle', gap=100)
    # # Investigating targetsize (hashing)
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/t-200-400.pickle', targetsize=(200,400))
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/t-200-200.pickle', targetsize=(200,200))
    # fingerprintBuilder('data/database_recordings', 'data/fingerprints/t-400-200.pickle', targetsize=(400,200))


if __name__ == '__main__':
    index_experiments()
    
