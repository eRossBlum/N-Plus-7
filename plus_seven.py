#!/usr/bin/env python3

import json
import re
from typing import Tuple
import nltk
from nltk.tokenize import word_tokenize
import sys


def make_list_of_english_nouns() -> list[str]:
    with open("WebstersDictionary-Use/dictionary.json", encoding='utf8') as read_file:
        webster = json.load(read_file)
    list_of_english_nouns = list()
    for entry in webster:
        if entry['pos'] == 'n.':
            list_of_english_nouns.append(entry['word'].lower().split(';', 1)[0])
    return sorted(list_of_english_nouns)


def gen_sentences(path: str) -> Tuple[str, str]:
    with open(path, encoding='utf8') as file:
        for line in file:
            yield word_tokenize(re.sub(r"—", ' — ', line)), line


def replace_keep_case(word, replacement, text):
    def func(match):
        g = match.group()
        if g.islower(): return replacement.lower()
        if g.istitle(): return replacement.title()
        if g.isupper(): return replacement.upper()
        return replacement
    return re.sub(word, func, text, flags=re.I)


def seven_nouns_after(noun_in: str, wordlist: list[str]) -> str:
    noun_in = noun_in.lower()
    try:
        index_in = wordlist.index(noun_in)
    except ValueError:
        return noun_in
    return wordlist[index_in + 7 % len(wordlist)]


def main():
    english_wordlist = make_list_of_english_nouns()
    edited_version = list()
    for tokenized_line, line_untokenized in gen_sentences(sys.argv[1]):
        pos_tagged = nltk.pos_tag(tokenized_line)
        noun_list_in_line = list()
        replacement_dict = dict()
        for word, tag in pos_tagged:
            if tag in {'NN', 'NNS', 'NNP', 'NNPS'}:
                noun_list_in_line.append(word)
        for noun in noun_list_in_line:
            new_noun = seven_nouns_after(noun, english_wordlist)
            if new_noun != noun:
                replacement_dict[noun] = new_noun
        for key, val in replacement_dict.items():
            line_untokenized = replace_keep_case(key, val, line_untokenized)
        edited_version.append(line_untokenized)
        print(replacement_dict)
        noun_list_in_line = list()
        replacement_dict = dict()

    print(' '.join(edited_version))


if __name__ == '__main__':
    main()
    