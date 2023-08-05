import pickle


def save(data, directory_file):
    outfile = open(directory_file, 'wb')
    pickle.dump(data, outfile)
    outfile.close()
    return None


def load(directory_file):
    outfile = open(directory_file, "rb")
    data = pickle.load(outfile)
    outfile.close()
    return data

