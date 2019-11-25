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

    print("Vocabulary size")
    print(len(word2ind))

    # create n-gram corpus

    # create vocab_bracket to add brackets to each word
    vocab_bracket = []

    for word in vocabulary:
        vocab_bracket.append("<" + word + ">")

    print(vocab_bracket)
