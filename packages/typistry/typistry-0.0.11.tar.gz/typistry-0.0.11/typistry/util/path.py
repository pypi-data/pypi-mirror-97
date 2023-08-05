from os import path

def root():
    d = path.dirname(path.dirname(path.abspath(__file__)))
    return d

def from_root(path: str):
    return root() + path
