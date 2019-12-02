from collections import Counter
import math
import numpy as np

class Corpus:

    def __init__(self, part="part", ng_small=3, ng_big=6, use_subsample=True):

        # getting corpus
        print("loading...")
        if part == "part":
            text = open('text8', mode='r').readlines()[0][:1000000]  # Load a part of corpus for debugging
        elif part == "full":
            text = open('text8', mode='r').readlines()[0]  # Load full corpus for submission
        else:
            print("Unknown argument : " + part)
            exit()

        print("tokenizing...")
        corpus = text.split()
        frequency = Counter(corpus)
        self.processed = []

        #Discard rare words
        for word in corpus:
            if frequency[word]>4:
                self.processed.append(word)

        self.vocabulary = set(self.processed)

        # Assignan index number to a word

        # create word2ind dict
        self.word2ind = {}
        self.word2ind[' '] = 0
        i = 1
        for word in self.vocabulary:
            self.word2ind[word] = i
            i += 1

        # create ind2word dict
        self.ind2word = {}
        for word,index in self.word2ind.items():
            self.ind2word[index] = word

        total_freq = 0

        for word in self.vocabulary:
            total_freq += frequency[word]

        # subsampling
        if use_subsample == "1":

            freq_subsampling = {}
            for word in self.vocabulary:
                freq_subsampling[word] = frequency[word] / total_freq

            # calculate subsampling_probability
            prob_subsampling = {}

            for word in self.vocabulary:
                prob_subsampling[word] = max(0, 1 - math.sqrt(0.001 / freq_subsampling[word]))

            subsampled_corpus = []
            discard = 0

            for word in self.processed:
                prob = prob_subsampling[word]
                random_prob = np.random.rand()
                if random_prob > prob:
                    subsampled_corpus.append(word)
                else:
                    discard += 1

            print(len(self.processed))
            print("Discard : " + str(discard))
            print("Vocabulary size : " + str(len(self.word2ind)))

            self.processed = subsampled_corpus
            self.vocabulary = set(self.processed)
        else:
            print("Vocabulary size : " + str(len(self.word2ind)))

        # negative sampling
        self.freqtable = [0, 0, 0]
        for k, v in frequency.items():
            f = int(v ** 0.75)
            for _ in range(f):
                if k in self.word2ind.keys():
                    self.freqtable.append(self.word2ind[k])

        # create n-gram corpus

        print("splitting into n-grams...")
        # create vocab_bracket to add brackets to each word

        # create dictionary with all n-grams
        self.subword_corpus = {}

        # create subwords for each word
        for word in self.vocabulary:
            self.subword_corpus[word] = self.create_subword(word, ng_small, ng_big)

        # create dictionary with subwords to words
        self.subword2word = {}

        for (word, subwords) in self.subword_corpus.items():
            for subword in subwords:
                self.subword2word[subword] = word

        self.sw_hash = {} # dictionary between word and hash of its subwords
        self.total_hash = set() # set that contains all hash
        self.sw2hash = {}

        for word, subwords in self.subword_corpus.items():
            self.sw_hash[word] = []

            for subword in subwords:
                hash = self.fnv_hash(subword)
                self.sw_hash[word].append(hash)
                self.total_hash.add(hash)
                self.sw2hash[subword] = hash

        self.hash2ind = {}
        for (index, hash_val) in enumerate(self.total_hash):
            self.hash2ind[hash_val] = index

        self.sw2ind = {}
        for (subword, hash_val) in self.sw2hash.items():
           self.sw2ind[subword] = self.hash2ind[hash_val]

        self.ind2sw = {}
        for (subword, index) in self.ind2sw.items():
            self.ind2sw[index] = subword

        print("hash size : " + str(len(self.total_hash)))

    def fnv_hash(self, sub_word, k = 2100000):

        fnv_offset_basis = 0xcbf29ce484222325 # fnv offset basis
        # fnv_offset_basis = 0x811c9dc5
        fnv_prime = 0x100000001b3 # fnv_prime

        hash = fnv_offset_basis
        for s in sub_word: # for each character
            hash = hash ^ ord(s) # XOR
            hash *= fnv_prime # multiply by fnv_prime
            hash = hash % k

        return hash


    def create_subword(self, word=None, ng_small=3, ng_big=6):

        wrapped = "<" + word + ">"

        subword_corpus = []

        for ng in range(ng_small, ng_big+1): # from ng_small to ng_big
                for i in range(len(wrapped)-ng+1):
                    subword_corpus.append(wrapped[i:i+ng])

        return subword_corpus