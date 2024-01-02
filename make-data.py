import json
import os
import sys
from collections import defaultdict

marked_emoji_filepath = './emoji_chengyu/data/emoji.cn.json'
chengyu_filepath = './emoji_chengyu/data/chengyu.json'
chengyu_count_filepath = './emoji_chengyu/data/chengyu.count.json'

temp_idiom_filepath = 'temp.idiom.json'
temp_word_filepath = 'temp.word.json'
temp_emoji_filepath = 'temp.emoji.json'
temp_chengyu_use_filepath = 'temp.chengyu.use.txt'


def make_idiom():
    with open(temp_idiom_filepath) as f:
        raw_content = f.read()

    idioms = json.loads(raw_content)

    with open(chengyu_filepath, 'w') as f:
        for x in idioms:
            idiom = {}
            idiom['word'] = x['word']
            idiom['pinyin'] = x['pinyin']
            f.write(json.dumps(idiom, ensure_ascii=False))
            f.write('\n')


def load_word_map():
    with open(temp_word_filepath) as f:
        words = json.load(f)

    word_map = defaultdict(list)
    for x in words:
        word_map[x['word']] = x['pinyin']
    return word_map


def load_emoji_map():
    with open(temp_emoji_filepath) as f:
        emojis = json.load(f)

    emoji_map = {}
    for key, value in emojis.items():
        emoji = {}
        emoji['name'] = key
        emoji['keywords'] = value['keywords']
        emoji['category'] = value['category']
        emoji_map[value['char']] = emoji
    return emoji_map


def mark_one_emoji(emoji, emoji_map, word_map):
    print(f'this emoji is {emoji}')
    print(f'category: {emoji_map[emoji]["category"]}')
    print(f'keywords: {emoji_map[emoji]["keywords"]}')

    flag = None
    words = []

    while True:
        word = input('input cn word:')
        if word == '':
            print('will try next emoji')
            flag = 'next'
            break
        if word == 'exit':
            print('will exit.')
            flag = 'exit'
            break

        if word not in word_map:
            print(f'word {word} have no data')
            continue

        pinyin = word_map[word]
        one_word = {}
        one_word['word'] = word
        one_word['pinyin'] = pinyin
        words.append(one_word)
    return flag, words


def mark_emoji():
    marked_emoji_map = {}
    marks = []

    if os.path.exists(marked_emoji_filepath):
        with open(marked_emoji_filepath) as f:
            for line in f:
                mark = json.loads(line)
                marks.append(mark)
                marked_emoji_map[mark['emoji']] = True

    word_map = load_word_map()
    emoji_map = load_emoji_map()

    for emoji in emoji_map:
        # 只标记新的
        if emoji in marked_emoji_map:
            continue
        try:
            flag, words = mark_one_emoji(
                emoji=emoji,
                emoji_map=emoji_map,
                word_map=word_map)
        except Exception as e:
            print(e)
            break

        if flag == 'exit':
            break
        mark = {}
        mark['emoji'] = emoji
        mark['words'] = words
        marks.append(mark)
        marked_emoji_map[emoji] = True

    with open(marked_emoji_filepath, 'w') as f:
        for mark in marks:
            f.write(json.dumps(mark, ensure_ascii=False))
            f.write('\n')


def edit_emoji():
    pass


def count_chengyu_use():
    try:
        with open(chengyu_count_filepath) as f:
            word_count_map = json.load(f)
    except Exception:
        word_count_map = {}

    with open(temp_chengyu_use_filepath) as f:
        temp_chengyu_use_txt = f.read()

    with open(chengyu_filepath) as f:
        for line in f:
            item = json.loads(line)
            word = item['word']
            count = temp_chengyu_use_txt.count(word)
            count += word_count_map.get(word, 0)
            if count > 0:
                word_count_map[word] = count

    with open(chengyu_count_filepath, 'w') as f:
        json.dump(word_count_map, f, indent=4, ensure_ascii=False)


def main():
    if len(sys.argv) == 1:
        print('python3 make-data.py [idiom|emoji|word]')
        print('python3 make-data.py emoji [mark|edit]')
        return
    elif sys.argv[1] == 'idiom':
        make_idiom()
        return
    elif sys.argv[1] == 'word':
        word_map = load_word_map()
        print(len(word_map))
        return
    elif sys.argv[1] == 'emoji':
        if len(sys.argv) == 2:
            emoji_map = load_emoji_map()
            print(len(emoji_map))
            return
        elif sys.argv[2] == 'mark':
            mark_emoji()
            return
        elif sys.argv[2] == 'edit':
            edit_emoji()
            return
    elif sys.argv[1] == 'count':
        count_chengyu_use()


if __name__ == '__main__':
    main()
