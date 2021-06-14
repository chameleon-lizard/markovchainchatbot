import numpy as np
import random


def endCombN(line, n, dictionary):
	if len(line)>=n:
		for i in range(len(line)):
			precomb = ''
			if len(line) >= i+n:
				for j in range(n):
					precomb += line[i+j] + ' '
				precomb = precomb.strip()
				if len(line) > i+n:
					if precomb != None:
						if precomb in dictionary:
							nex = dictionary[precomb]
							nex.append(' '.join(line[i+n:]))
							dictionary[precomb] = nex
						else:
							dictionary[precomb] = [' '.join(line[i+n:])]
	return dictionary


def combN(line, n, dictionary):
	comb = []
	precomb = ''
	if len(line)>=n:
		for i in range(len(line)):
			precomb = ''
			if len(line) >= i+n:
				for j in range(n):
					precomb += line[i+j] + ' '
				precomb = precomb.strip()
				if len(line) > i+n:
					if precomb != None:
						if precomb in dictionary:
							nex = dictionary[precomb]
							nex.append(line[i+n])
							dictionary[precomb] = nex
						else:
							dictionary[precomb] = [line[i+n]]
				comb.append(precomb)
		return [comb, dictionary]
	return [None, dictionary]

def subgenerate(lw, n, lines):
	dictionary = {}
	for i in lines:
		words = i.split()
		combination, dictionary = combN(words, n, dictionary)
	lastWords = ' '.join([str(item) for item in lw.split()[-n:]])
	#print(lastWords)
	if lastWords in dictionary:
		return dictionary[lastWords]
	else:
		return subgenerate(lastWords, n-1, lines)

	text.close()

def generate(start, dictionary, end, n, lines):
	sentence = start[random.randint(0,len(start)-1)]
	sentence = sentence.capitalize() 
	for i in range(5):
		print(sentence.split()[-n:])
		lastWords =  ' '.join([str(item) for item in sentence.split()[-n:]])
		if lastWords in dictionary:
			words = dictionary[lastWords]
		else:
			words = subgenerate(lastWords, n-1, lines)
		sentence += ' ' + words[random.randint(0,len(words)-1)]
	lastWords =  ' '.join([str(item) for item in sentence.split()[-n:]]) # Формируем концовку
	if lastWords in end:
		words = end[lastWords]
		sentence += ' ' + words[random.randint(0,len(words)-1)]
		return sentence
	else:
		while n > 0:
			n -= 1
			lastWords =  ' '.join([str(item) for item in sentence.split()[-n:]])
			end = {}
			for i in lines:
				words = i.split()
				end = endCombN(words,n, end)
			if lastWords in end:
				sentence += ' ' + words[random.randint(0,len(words)-1)]
				return sentence

def markovN(n):
	text = open('dict/vkmes.txt', 'r')
	lines = text.readlines()
	corpus = []
	start = [] # Мы можем создать словарь, но легче будет создать лист и вносить любое начало предложений туда, а потом просто выбирать случайным числом (вероятность останется той же)
	end = []
	dictionary = {}
	endDict = {}


	for i in lines:
		words = i.split()
		if len(words) >= n:
			start.append(' '.join([str(item) for item in words[:n]]))
			end.append(' '.join([str(item) for item in words[-n:]]))

		#for j in range(len(words)-1):
		#	s.append(words[j]+' '+words[j+1])
		combination, dictionary = combN(words, n, dictionary)
		endDict = endCombN(words,n, endDict)
		if combination != None:
			corpus.append(combination)

	corpus = [item for sublist in corpus for item in sublist] # Делаем плоский список
	text.close()
	answer = generate(start, dictionary, endDict, n, lines)
	return answer


