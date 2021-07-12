from emoji_chengyu.chengyu import gen_one_pair


def emoji_chengyu():
    N = 100

    pairs = [gen_one_pair() for i in range(N)]
    pairs = list(filter(None, pairs))
    pairs.sort(key=lambda pair: pair['emojis'].count(None))

    for pair in pairs[:20]:
        print(pair['word'], pair['emoji'])
