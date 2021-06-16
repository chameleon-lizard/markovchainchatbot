from typing import Dict, List, Optional, Tuple
import random
from collections import defaultdict

'''
Class for markov chain text generation.
'''

class Markov:
    ''' 
    Generating dictionary of middle-body and end for setnence
    ret - type of what we want to get
    a - only messages larger then window
    b - window slicing. 'abcdef', window=2 -> ['ab', 'bc', 'cd', 'de']
    c - next word after each window slice
    d - end of sentence after each window slice
    '''
    def __combN(self, ret: str) -> None:
        a = list(filter(lambda x: len(x.split()) > self.__window, self.__lines)) 
        b = [[('{} ' * self.__window).format(*ele).strip() 
            for ele in zip(*[iter(words.split()[i:])] * self.__window)][0] 
            for words in a for i in range(len(words.split())-self.__window)]
        if ret == 'all':
            c = [words.split()[i] for words in a 
                for i in range(self.__window,len(words.split()))]
            d = [' '.join(words.split()[i:]) for words in a 
                for i in range(self.__window,len(words.split()))]
            for i in range(len(b)):
                self.__dictionary[b[i]].append(c[i])
                self.__end_dict[b[i]].append(d[i])
        elif ret == 'dictionary':
            c = [words.split()[i] for words in a 
                for i in range(self.__window,len(words.split()))]
            for i in range(len(b)):
                self.__dictionary[b[i]].append(c[i])
        elif ret == 'end_dict':
            d = [' '.join(words.split()[i:]) for words in a 
                for i in range(self.__window,len(words.split()))]
            for i in range(len(b)):
                self.__end_dict[b[i]].append(d[i])

    # Generating prediction for less window size
    def subgenerate(self, last_words: str, ret: str) -> List[str]:
        if ret == 'body': # Генерируем середину
            if last_words in self.__dictionary:
                return self.__dictionary[last_words]
            else:
                if self.__window == 1:
                    return self.__dictionary[random.choice(list(self.__dictionary.keys()))]
                else:
                    last_words = ' '.join(last_words.split()[-self.__window+1:])
                    return Markov('dict/vkmes.txt', self.__window-1).subgenerate(last_words, 'body')
        elif ret == 'end': # Генерируем концовку
            if last_words in self.__end_dict:
                return self.__end_dict[last_words]
            else:
                if self.__window == 1:
                    return self.__end_dict[random.choice(list(self.__end_dict.keys()))]
                else:
                    last_words = ' '.join(last_words.split()[-self.__window+1:])
                    return Markov('dict/vkmes.txt', self.__window-1).subgenerate(last_words, 'end')

    # Generating our sentence
    def generate(self, length: int) -> str:
        self.__set_defaults()
        # Choosing the start of the sentence
        sentence = random.choice(self.__start).capitalize()

        # Generating the base of the sentence
        for i in range(length):
            last_words = (' '.join([str(item)
                                  for item in sentence.split()[-self.__window:]])).lower()
            words = Markov('dict/vkmes.txt', self.__window-1).subgenerate(' '.join(last_words.split()[-self.__window+1:]), 'body') if last_words not in self.__dictionary.keys() else self.__dictionary[last_words]
            sentence += ' ' + random.choice(words)

        last_words = ' '.join([str(item)
                                  for item in sentence.split()[-self.__window:]])
        # Generating the end of the sentence
        if last_words in self.__end_dict:
            sentence += ' ' + random.choice(self.__end_dict[last_words])
        else:
            last_words = ' '.join(last_words.split()[-self.__window+1:])
            words = Markov('dict/vkmes.txt', self.__window-1).subgenerate(last_words, 'end')
            sentence += ' ' + random.choice(words)
        return sentence

    # Setting defaults (start, mid, end)
    def __set_defaults(self) -> None:
        self.__start = list(map(lambda y: ' '.join(y.split()[:self.__window]), list(filter(lambda x: len(x.split()) > self.__window, self.__lines))))
        self.__combN('all')

    def __init__(self, path: str, window: int) -> None:
        self.__window = window
        self.__dictionary = defaultdict(list)
        self.__end_dict = defaultdict(list)
        self.__start = []
        with open(path, 'r') as ds:
            self.__lines = ds.readlines()
        self.__set_defaults()
