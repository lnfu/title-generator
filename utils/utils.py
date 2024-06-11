import os


def ensureDirectoryExists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
