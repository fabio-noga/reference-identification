# -*- coding: utf-8 -*-
import json
import os
import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from string import punctuation

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import spacy
    # nlp = spacy.load('en_core_web_sm')


import DbUtils
import Grabber
import Utils
import sys
import csv

def processQuote(file):
    # texto2 = file['full_text']
    # texto2 = Utils.clearText(texto2)

    data = []
    for item in file:
        if(item[1] == True):
            data.append(sent_tokenize(item[0].lower())[0])
    # for frase in file:
    #     data1 = [sent_tokenize(frase.lower())]
    #     if (" in " in frase
    #         or " by " in frase
    #         or " pag " in frase
    #         or " pags " in frase
    #         or " cfr " in frase
    #         or re.compile(r'[\[[0-9\/]+]').search(frase)):
    #         data1.append(True)
    #         data1.append(frase)
    #     else:
    #         data1.append(False)
    #         data1.append("")
    #     data.append(data1)

    # texto2 = texto2.encode(encoding = 'UTF-8', errors = 'strict')
    # a = sent_tokenize(texto2)
    # for frase in a:
        # print("###" + frase)


    # stopwordsFromFile = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`']+ fileChanger()
    stopwordsFromFile = []
    stopwordsFromFile = list(dict.fromkeys(stopwordsFromFile))
    # stopwords = []
    # with open("assets\\stopwords.txt", 'r', newline='', encoding='utf-8') as stopwordFile:
    #     for row in stopwordFile:
    #         stopwords.append(row)
    stopwords1 = list(stopwords.words('portuguese') + list(punctuation)) + stopwordsFromFile

    stopwords1 = sorted(list(dict.fromkeys(stopwords1)))

    # texto2 = texto2.lower()

    for line in data:
        cleaned_text = line.translate(str.maketrans('', '', string.punctuation))  # remove pontuation
        tokenized_words = cleaned_text.split()
        final_words = []
        doc = nlp(line)
        named_entities = [ent.text for ent in doc.ents if ent.label_ == 'PER']

        # Extract publication year using regex
        year_match = re.search(r'\b\d{4}\b', line)
        year = year_match.group(0) if year_match else None

        # Extract article/book title using heuristics
        title = None
        title_match = re.search(r'\'(.+?)\'', line)
        if title_match:
            title = title_match.group(1)
        else:
            for token in doc:
                if token.is_title and not token.is_stop and token.pos_ != 'DET':
                    title = token.text + ' ' + ' '.join(
                        [t.text for t in token.rights if t.pos_ not in ['PUNCT', 'SYM']])
                    break
        reference = ''
        if title is not None:
            reference += '"' + title + '", '
        if year is not None:
            reference += year + '.'
        print(reference)
        # stop_words = set(stopwords.words('portuguese'))
        # tokens = word_tokenize(line, language='portuguese')
        # tagged = nltk.pos_tag(tokens, lang='por')
        # ne_tagged = ne_chunk(tagged, binary=False)
        # for chunk in ne_tagged:
        #     if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
        #         final_words.append(' '.join(c[0] for c in chunk.leaves()))
        # for word in tokenized_words:
        #     if word not in stopwords1:
        #         final_words.append(word)
        # print(final_words)
        # print(nltk.pos_tag(final_words))