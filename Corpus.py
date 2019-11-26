from collections import Counter


def get_corpus(part="part", ng_small=3, ng_big=6, use_subsample=True):

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
    processed = []

    #Discard rare words
    for word in corpus:
        if frequency[word]>4:
            processed.append(word)

    vocabulary = set(processed)

    # Assignan index number to a word

    # create word2ind dict
    word2ind = {}
    word2ind[' '] = 0
    i = 1
    for word in vocabulary:
        word2ind[word] = i
        i += 1

    # create ind2word dict
    ind2word = {}
    for word,index in word2ind.items():
        ind2word[index] = word

    print("Vocabulary size : " +str(len(word2ind)))

    # create n-gram corpus

    print("splitting into n-grams...")
    # create vocab_bracket to add brackets to each word

    # create dictionary with all n-grams
    subword_corpus = {}

    for word in vocabulary:
        subword_corpus[word] = create_subword(word, ng_small, ng_big)




    return None, None

def hash(sub_word, k = 2.10 * (10 ** 6)):

    fnv_offset_basis = 0xcbf29ce484222325
    fnv_prime = 0x100000001b3

    for char in sub_word:
        print(ord(char))


def create_subword(word,ng_small, ng_big):

    wrapped = "<" + word + ">"

    subword_corpus = []

    for ng in range(ng_small, ng_big+1): # from ng_small to ng_big
            for i in range(len(wrapped)-ng+1):
                subword_corpus.append(wrapped[i:i+ng])

    return subword_corpus