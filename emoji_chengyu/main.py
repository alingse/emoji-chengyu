import itertools
from typing import List

import click

from emoji_chengyu.data import CommonChengyuManager, DefaultChengyuManager
from emoji_chengyu.puzzle import PuzzleItem, gen_puzzle


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

    if game:
        run_emoji_chengyu_game(puzzles)

    for puzzle in puzzles:
        click.echo(f'{puzzle.puzzle_str}\t{puzzle.chengyu_item.word}')


# interactive game
def run_emoji_chengyu_game(puzzles: List[PuzzleItem], retry: int = 4):
    for i, puzzle in enumerate(puzzles):
        click.echo('\n-------------')
        for j in range(retry):
            click.echo(puzzle.puzzle_str)
            word = input('成语:')
            if word == puzzle.chengyu_item.word:
                click.echo('正确')
                break
            else:
                click.echo('错误')
                puzzle = puzzle.clone(1)

            if not puzzle.mask_num:
                break

        click.echo(puzzle.chengyu_item.word)
        click.echo('-------------\n')
