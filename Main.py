from Config import config
from Corpus import Corpus
from Train import word2vec_trainer
from Test import sim

def main():
    args = config()
    ns = args.ns # value for ns
    part = args.part # part or full
    ng_small = args.ng_small # ngram_smallest_value
    ng_big = args.ng_big # ngram_biggest_value
    use_subsample = args.subsample # use_subsample or not

    corpus = Corpus(part, ng_small, ng_big,use_subsample)
    emb, _ = word2vec_trainer(corpus, ns=ns, dimension=64, learning_rate=0.05, iteration=50000)
    # Print similar words
    testwords = ["narrow-mindedness", "department", "campfires", "knowing", "urbanize", "imperfection", "principality", "abnormal", "secondary", "ungraceful"]
    sim(testwords, corpus, emb)

main()