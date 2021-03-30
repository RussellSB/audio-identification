import pickle

def save_pickle(obj, path):
    with open(path, 'wb') as fp:
        pickle.dump(obj, fp)

def load_pickle(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)