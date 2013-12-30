from os.path import dirname, join

DATA_FOLDER = join(dirname(__file__), 'data')


def read_data(filename):
    return file(join(DATA_FOLDER, filename)).read()
