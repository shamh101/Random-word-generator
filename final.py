

import pickle
import requests
from graph import Graph
from enum import Enum

class Tokenization(Enum):
   
    word = 1
    character = 2
    byte = 3
    none = 4


class RandomWriter(object):
   

    def __init__(self, level, tokenization=None):
       

        self.level = level
        self.tokenization = tokenization or Tokenization.none
        self.graph = Graph()

    def generate(self):
        
        yield from self.graph.random_selection()

    def generate_file(self, filename, amount):
       
        mode = 'wb' if self.tokenization is Tokenization.byte else 'w'
        with open(filename, mode) as f:
            for token in self.generate():
                if amount == 0:
                    break
                if self.tokenization is not Tokenization.byte:
                    token = str(token)
                if self.tokenization is Tokenization.byte and isinstance(token, int):
                    token = bytes([token])
                f.write(token)
                if(self.tokenization is Tokenization.word or self.tokenization is Tokenization.none):
                    f.write(' ')
                amount -= 1

    def save_pickle(self, filename_or_file_object):
       
        if isinstance(filename_or_file_object, str):
            with open(filename_or_file_object, 'wb') as f:
                pickle.dump(self, f)
        else:
            pickle.dump(self, filename_or_file_object)

    @classmethod
    def load_pickle(cls, filename_or_file_object):
      
        if isinstance(filename_or_file_object, str):
            with open(filename_or_file_object, 'rb') as f:
                return pickle.load(f)
        else:
            return pickle.load(filename_or_file_object)


    def train_url(self, url):
      
        if self.tokenization is Tokenization.none:
            raise ValueError('Tokenization may not be None')

        data = requests.get(url)
        if self.tokenization is Tokenization.byte:
            self.train_iterable(data.content)
        else:
            self.train_iterable(data.text)

    def train_iterable(self, data):
        

        if self.tokenization is Tokenization.none:
            try:
                data = iter(data)
            except TypeError:
                raise TypeError('Expected iterable')
        elif self.tokenization is Tokenization.character or self.tokenization is Tokenization.word:
            if not isinstance(data, str):
                raise TypeError('Expected String')
            if self.tokenization is Tokenization.word:
                data = data.split()
        elif self.tokenization is Tokenization.byte:
            if not isinstance(data, bytes):
                raise TypeError('Expected bytes')
        else:
            raise TypeError('Expected String, iterable, or bytes')

        self.create_graph(data)

    def create_graph(self, data):
        """
        create the markov chain based on the provided data
        
        all preconditions should have been checked at this point
        """
        prev = None
        for token in windowed(data, self.level):
            if prev is not None:
                self.graph.link(prev, token)
            prev = token


def windowed(iterable, size):
    """Convert an iterable to an iterable over a "windows" of the input.

     All credit to Arthur Peters

    The windows are produced by sliding a window over the input iterable.
    """
    window = list()
    for v in iterable:
        if len(window) < size:
            window.append(v)
        else:
            window.pop(0)
            window.append(v)
        if len(window) == size:
            yield tuple(window)


