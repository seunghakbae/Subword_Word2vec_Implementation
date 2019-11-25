import argparse

def config():

    parser =argparse.ArgumentParser(description='Subword_Word2vec')
    parser.add_argument('ns', metavar="negative_sampling", type=int, help="Negative Sampling value")
    parser.add_argument('part', metavar='part', type=str, help='"part" if you want to train on a part of corpus, "full" if you want to train on full corpus')
    parser.add_argument('ng_small', metavar='ngram_smallest', type=int, help='ngram smallest value')
    parser.add_argument('ng_big', metavar='ngram_biggest', type=int, help="ngram biggest value")
    parser.add_argument('subsample', metavar="use_subsample", type=str, help="0 for not using subsampling, 1 for using subsampling")

    return parser.parse_args()