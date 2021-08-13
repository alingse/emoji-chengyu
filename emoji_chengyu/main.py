import itertools

from emoji_chengyu.puzzle import gen_puzzle


def emoji_chengyu():
    N = 100
    pg = gen_puzzle()
    puzzles = list(itertools.islice(pg, N))
    puzzles.sort(key=lambda p: sum(p.mask), reverse=True)

    M = 20
    for puzzle in puzzles[:M]:
        print(''.join(puzzle.puzzle), puzzle.chengyu_item.word)
