from os.path import dirname, join

# TODO: Move this helper function into a ployst-testing library that all
# providers can import from.

DATA_FOLDER = join(dirname(__file__), 'data')


def read_data(filename):
    return file(join(DATA_FOLDER, filename)).read()
