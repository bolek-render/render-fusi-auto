import pickle


def load(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        return data
