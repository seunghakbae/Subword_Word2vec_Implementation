from Config import config

def main():
    args = config()
    ns = args.ns # value for ns
    part = args.part # part or full
    ng_small = args.ng_small # ngram_smallest_value
    ng_big = args.big # ngram_biggest_value
    use_subsample = args.subsample # use_subsample or not

    word_corpus,subword_corpus = get_corpus(part, ng_small, ng_big,use_subsample)
    emb_, _ = word2vec_trainer(word_corpus, subword_corpus, ns=ns, dimension=64, learning_rate=0.05, iteration=50000)
    test(emb)

main()