import pickle


def load_model(fname):
    """Load pickled trained model for deployment use

    :param fname: filepath of the pkl file
    :return: loaded model object
    """
    file = open(fname, "rb")
    data = pickle.load(file)
    file.close()

    return data
