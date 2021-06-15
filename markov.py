from typing import Dict, List, Optional, Tuple
import numpy as np
import random


class Markov:
    '''
    Class for markov chain text generation.
    '''

    def __combN(self, line: List[str], dictionary: Dict[str, List[str]], end_dict: Dict[str, List[str]], window: int) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        if len(line) >= window:
            for i in range(len(line)):
                if len(line) > i + window:
                    precomb = ' '.join(line[i:i+window])

                    dictionary[precomb] = [line[i+window]] if precomb not in dictionary else dictionary[precomb] + [line[i+window]]
                    end_dict[precomb] = [' '.join(line[i+window:])] if precomb not in end_dict else end_dict[precomb] + [' '.join(line[i+window:])]
            return (dictionary, end_dict)

        return (dictionary, end_dict)

    # TODO: If custom is not found
    def __subgenerate(self, last_words: str, window: int) -> List[str]:
        dictionary = {}
        for line in self.__lines:
            dictionary, _ = self.__combN(line.split(), dictionary, {}, window)

        last_words = ' '.join([str(item)
                              for item in last_words.split()[-window:]])

        if last_words in dictionary:
            return dictionary[last_words]
        else:
            return self.__subgenerate(last_words, window - 1)

    def generate(self, length: int) -> str:
        self.__set_defaults()
        # Choosing the start of the sentence
        sentence = random.choice(self.__start).capitalize()

        # Generating the base of the sentence
        for i in range(length):
            last_words = ' '.join([str(item)
                                  for item in sentence.split()[-self.__window:]])
            words = self.__subgenerate(last_words, self.__window -
                                       1) if last_words not in self.__dictionary.keys() else self.__dictionary[last_words]
            sentence += ' ' + random.choice(words)

        # Generating the end of the sentence
        if last_words in self.__end_dict:
            sentence += ' ' + random.choice(self.__end_dict[last_words])
            return sentence
        else:
            for n in range(self.__window, 0, -1):
                last_words = ' '.join([str(item)
                                      for item in sentence.split()[-n:]])
                end_dict = {}
                for line in self.__lines:
                    _, end_dict = self.__combN(line.split(), {}, end_dict, self.__window)

                if last_words in self.__end_dict:
                    sentence += ' ' + random.choice(self.__end_dict[last_words])
                    return sentence

    def __set_defaults(self) -> None:
        for line in self.__lines:
            self.__start = [
                ' '.join([i for i in words[:self.__window]])
                for words in filter(lambda x: len(x) >= self.__window, line.split())
            ]

            self.__dictionary, self.__end_dict = self.__combN(
                line.split(), {}, {}, self.__window)


    def __init__(self, path: str, window: int) -> None:
        self.__window = window
        self.__dictionary = {}
        self.__end_dict = {}
        with open(path, 'r') as ds:
            self.__lines = ds.readlines()

        self.__set_defaults()


moysha = Markov('dict/vkmes.txt', 2)
print(moysha.generate(5))
print(moysha.generate(5))
print(moysha.generate(5))
print(moysha.generate(5))
