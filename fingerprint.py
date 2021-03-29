import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np

import scipy.ndimage as ndimage
import scipy.ndimage.filters as filterss
from skimage.morphology import disk, diamond, square

# Custom implementation for picking peaks
def pick_peaks(D, shape='square', size=10, uniform=True, show=False):

    # The only shapes available are square, diamond and disk.
    assert shape == 'square' or shape == 'diamond' or shape == 'disk',\
    'Parameter shape must be set to \'disk\', \'diamond\' or \'square\''

    # Compute the constellation map
    data = np.log(D)
    footprint = eval(shape + '(' + str(size) + ')')  # formulates kernel from params
    max_blobs = ndimage.maximum_filter(data, footprint=footprint)
    const_map = data == max_blobs

    # Only considers the points within a normal distribution
    if uniform:
        stdev = np.std(max_blobs)
        mean = np.mean(max_blobs)
        distribution = np.multiply(data >= (mean-stdev), data <= (mean+stdev))
        const_map = np.multiply(const_map, distribution)

    if(show):
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
        plt.title('Constillaiton Map')
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
def hash_peaks(peaks, gap=200, size=(200, 200)):
    
    d = {}

    # Iterate through anchor points
    for anchor in peaks:
        
        # Preparing target zone boundaries
        freq_start = anchor[0] - (size[0]//2)
        freq_end = anchor[0] + (size[0]//2)
        time_start = anchor[1] + gap
        time_end = time_start + size[1]
        
        # Hash only points within the target zone
        for target in peaks:
            
            # Validates as a target if within target zone
            if target[0] >= freq_start and target[0] <= freq_end \
                and target[1] >= time_start and target[1] <= time_end:
                
                time_diff = target[1] - anchor[1]
                key = '{}-{}-{}'.format(str(anchor[0]), str(target[0]), str(time_diff))
                
                d[key] = anchor[1]

    return d
