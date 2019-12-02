import torch as torch
import random

def getRandomContext(corpus, C=5):
    wordID = random.randint(0, len(corpus) - 1)

    context = corpus[max(0, wordID - C):wordID]
    if wordID + 1 < len(corpus):
        context += corpus[wordID + 1:min(len(corpus), wordID + C + 1)]

    centerword = corpus[wordID]
    context = [w for w in context if w != centerword]

    if len(context) > 0:
        return centerword, context
    else:
        return getRandomContext(corpus, C)


def NS_Skipgram(center_hash, inputMatrix, outputMatrix):

    V, D = inputMatrix.size()

    inputVector = torch.sum(inputMatrix[center_hash], 0)
    # print(V,D)
    # print(inputMatrix.shape)
    # print(outputMatrix.shape)
    # print(inputVector.shape)
    # print(inputVector.view(D,1).shape)
    # exit()
    out = outputMatrix.mm(inputVector.view(D, 1))

    target = out[0]
    NS_samples = out[1:]

    loss = -torch.log(torch.sigmoid(target)) - torch.sum(torch.log(torch.sigmoid(-NS_samples)))

    sigmoid_value = torch.sigmoid(out)
    grad = sigmoid_value

    grad[0][0] -= 1.0

    grad_emb = grad.view(1, -1).mm(outputMatrix)  # /len(contextWords)
    grad_out = grad.mm(inputVector.view(1, -1))

    return loss, grad_emb, grad_out


def word2vec_trainer(corpus, ns=20, dimension=64, learning_rate=0.05, iteration=50000):
    # Xavier initialization of weight matrices
    W_emb = torch.randn(len(corpus.total_hash), dimension) / (dimension ** 0.5)
    W_out = torch.randn(len(corpus.word2ind), dimension) / (dimension ** 0.5)

    centerword, contexts = getRandomContext(corpus.processed)
    contextInds = [corpus.word2ind[word] for word in contexts]

    losses=[]

    for i in range(iteration):
        for contextInd in contextInds:
            selected = random.sample(corpus.freqtable, ns)
        if contextInd in selected:
            selected.remove(contextInd)

        activated = [contextInd] + selected
        center_hash_ind = [corpus.hash2ind[hash] for hash in corpus.sw_hash[centerword]]

        L, G_emb, G_out = NS_Skipgram(center_hash_ind, W_emb, W_out[activated])
        W_emb[center_hash_ind] -= learning_rate * G_emb.squeeze()
        W_out[activated] -= learning_rate * G_out
        losses.append(L.item())

        if i % 10000 == 0:
            avg_loss = sum(losses) / len(losses)
            print("Loss : %f" % (avg_loss,))
            losses = []

    return W_emb, W_out
