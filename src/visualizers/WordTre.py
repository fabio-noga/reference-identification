import os
import re

import nltk
from nltk import Tree
from nltk.corpus import mac_morpho

sentences = mac_morpho.tagged_sents()
unigram_tagger = nltk.UnigramTagger(sentences)

phrase="Expressões como \"dinheiro de plástico\", \"moeda electrónica\", \"telemática\", \"caixas automáticas\", \"porta-moedas electrónico\" são exemplos de termos que passaram a fazer parte do léxico corrente dos dias de hoje (  Com mais desenvolvimento, cfr. Maria Raquel Guimarães, \"As Transferências Electrónicas de Fundos e os Cartões de Débito\", Almeida, 1999, pp. 11 e 12.).)"
tagged_sentence = unigram_tagger.tag(nltk.word_tokenize(phrase))

grammar = r"""
        NOME: {<NPROP2>((<NPROP>|<PREP>)?<NPROP2>)+}
        PAG_DOT: {<PAG><PONT>?}
        VOL_DOT: {<VOL><PONT>?}
        NOT_DOT: {<NOT><PONT>?}
        VOLS: {<VOL_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*}
        PAGS: {<PAG_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*(<KC><SGS>)?}
        NOTS: {<NOT_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*(<KC><SGS>)?}
        REF: {(<NOME><.*>+?(<PAGS>(<PUNC><NOTS>)?)(<SEP>|<PONT>|<PUNC>|<KC>))|(<NOME><.*>{,2}?<IN><.*>+?(<SEP>|<PONT>|<PAGS>)<KC>?)} 
    """

parser = nltk.RegexpParser(grammar)
# print(parser)

# tagged_sentence = [( "money" ,"NN"),("market", "NN"),("fund", "NN")]
result = parser.parse(tagged_sentence)


result.draw()