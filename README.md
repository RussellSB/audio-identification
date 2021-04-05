# audio-identification
A musical audio retrieval system with fingerprints, following the algorithm presented by [Wang 2003](https://www.researchgate.net/publication/220723446_An_Industrial_Strength_Audio_Search_Algorithm). This is the approach that Shazam took at the time, but has improved on since then.

## Setup
The required packages are enlisted in requirements.txt. It's recommended to use a virtualenv using pip (alternatively conda should also suffice).  From a command line interface with pip, the virtual environment can be created, activated and updated with the required packages as follows:

```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Data

For the data I/O you a folder named "data" must be present from the root directory. The following directories may also need to be included.

```
data
├── database_recordings
├── fingerprints
├── output
├── query_recordings
└── results
```

### Input

Directories for input are:

* database_recordings - This has audio files from a subset of the GTZAN dataset. May be downloaded from [here](https://collect.qmul.ac.uk/down?t=R8SDLMOKUOSCD2VB/6P63FFT4AN0581R7V49FJKO).
* query_recordings - This has some audio files from the same subset, but cropped and with noise added to it for a fairly challenging evaluation. May be downloaded from [here](https://collect.qmul.ac.uk/down?t=450TPH3RDUJNA920/6P4TNTJT7GSTR7NUC226IJ8).

The database set is sampled at 22050Hz, whereas the query set at 44100 Hz. Nonetheless, in this approach they are both sampled at 22050 Hz.

### Output

Directories for output are:

* fingerprints - Stores arrays of audio fingerprints in .pickle format. Each file would correspond to a version of the fingerprint database (with specific parameters)
* output - Stores .txt files with a line per query file. The first word corresponds to the query file, and the following three word correspond to the retrieved match in descending order of similarity. Only the top three are returned for later evaluating up to a rank of three.
* results - Stores .txt files with recall results from tested experiments. This is not automatically outputted to or required. But for transparency purposes, console logged results from the evaluation have been copied and formatted into text files here.

Files from the fingerprint folder were not included due to large file sizes - but output and results files are included as they only store text files with small file sizes.

## Usage

### Main

An example use case of the system may be ran from the main file, as enlisted below. With a call to three different methods, it indexes, queries, and evaluates all the dataset files in that order. The final evaluation results are printed to the command line.

```
python main.py
```

### Experiments

To replicate the performed experiments, you may simply run experiments.py. Here a set of experiments per parameters were tested to investigate the affectiveness of different approaches to indexing. 

```
python experiments.py
```