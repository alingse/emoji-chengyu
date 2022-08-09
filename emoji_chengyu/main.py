import itertools

import click

from emoji_chengyu.data import CommonChengyuManager, DefaultChengyuManager
from emoji_chengyu.puzzle import gen_puzzle


@click.command()
@click.option('-c', '--count', type=int, default=5, help='puzzle count')
@click.option('--game', is_flag=True, default=False, help='enable interactive game')
@click.option('--all', is_flag=True, default=False, help='use all chengyu, default is common chengyu)')
def emoji_chengyu(count, game, all):
    manager = CommonChengyuManager
    if all:
        manager = DefaultChengyuManager

    puzzles = gen_puzzle(manager=manager)
    puzzles = list(itertools.islice(puzzles, count*2))
    puzzles.sort(key=lambda p: sum(p.mask), reverse=True)
    puzzles = puzzles[:count]

    if not game:
        for puzzle in puzzles:
            print(''.join(puzzle.puzzle), puzzle.chengyu_item.word)
        return

    # interactive game
    for i, puzzle in enumerate(puzzles):
        print(''.join(puzzle.puzzle))
        for j in range(3):
            word = input('成语:')
            if word == puzzle.chengyu_item.word:
                print('正确')
                break
            else:
                puzzle.mask
                print('错误')
        print(puzzle.chengyu_item.word)
