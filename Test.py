import torch

def get_word_embeddings(corpus, subword_embeddings):
    D = subword_embeddings.size(1)
    word_embeddings = torch.zeros(len(corpus.word2ind), D)

    for word_index in range(1, len(corpus.word2ind)):
        subword_indices = corpus.sw_hash[corpus.ind2word[word_index]]
        subword_indices = [corpus.hash2ind[subword_index] for subword_index in subword_indices]
        word_embeddings[word_index] = torch.sum(subword_embeddings[subword_indices], 0)

    return word_embeddings # torch.tensor(V, D)


def sim(testwords, corpus, matrix):

    word_embeddings = get_word_embeddings(corpus, matrix)

    def get_testword_embedding(testword):
        subwords = corpus.create_subword(testword)

        subword_indices = []
        for subword in subwords:
            try:
                subword_index = corpus.sw2ind[subword]
                subword_indices.append(subword_index)
            except:
                continue

        return torch.sum(matrix[subword_indices], 0) # torch.tensor(D)

    for testword in testwords:

        testword_emb = get_testword_embedding(testword)

        similarities = [(torch.cosine_similarity(testword_emb, word_emb, 0), index) for index, word_emb in enumerate(word_embeddings)]

        similarities.sort(key=lambda elem: elem[0], reverse=True)
        print()
        print("===============================================")
        print("The most similar words to \"" + testword + "\"")
        count = 0
        i = 0
        while count < 5:
            similarity, word_index = similarities[i]
            i += 1
            if corpus.ind2word[word_index] == testword:
                continue
            print(corpus.ind2word[word_index] + ":%.3f" % (similarity))
            count += 1
        print("===============================================")
        print()