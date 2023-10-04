import csv
import json
import os
import re

import nltk
from nltk import PunktSentenceTokenizer
from nltk.corpus import mac_morpho
from nltk.tokenize.punkt import PunktParameters, PunktLanguageVars

from src import Config
from src.Utils import removeFakeNewLines, clearSpecialCharacters, clearReferences

unigram_tagger = nltk.UnigramTagger(mac_morpho.tagged_sents())
custom_words = [("/", "PUNC")]
relative_path = os.path.join(Config.ROOT_FOLDER, "assets")

with open(os.path.join(relative_path, "names.txt"), "r", encoding='utf-8') as f:
    lines = f.readlines()
    word_tag_list = [(line.split()[0].lower().split("\n")[0], "NPROP2") for line in lines]

custom_words = custom_words + word_tag_list
relative_path = os.path.join(Config.ROOT_FOLDER, "unmarkedTestFiles")
with open(os.path.join(relative_path, Config.MAC_MORPHO_FILE), "r", encoding='utf-8') as f:
    lines = f.readlines()
    word_tag_list = [(line.split()[0], line.split()[1]) for line in lines]

word_tag_list = custom_words + word_tag_list
custom_words = [word_tag_list]

# TODO: this can be connected to DB by DbUtils
def getInvestigators():
    relative_path = os.path.join(Config.ROOT_FOLDER, "assets")
    investigators = []
    with open(os.path.join(relative_path, "investigadores_completo.txt"), "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            investigators.append(line)
    return investigators

class CustomLanguageVars(PunktLanguageVars):
    sent_end_chars = ('.', ';', '\n')  # Add ";" as a sentence-ending character

def prepareTokenizer(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(Config.ABBREV)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    return tokenizer.tokenize(textoIntegralLimpo)

def getQuotesFromFileByPattern(filePath):
    return tokenizeByPatterns(prepareTokenizer(filePath))

def getQuotesFromFileByName(filePath):
    return tokenizeByName(prepareTokenizer(filePath))

def getQuotesFromFileByNameGrammar(filePath):
    return tokenizeByNameGrammar(prepareTokenizer(filePath))

def getQuotesFromFileByNameInvestigadores(filePath):
    return tokenizeByNameInvestigadores(prepareTokenizer(filePath))

def getQuotesFromFileByNameFromList(filePath):
    return tokenizeByNameFromList(prepareTokenizer(filePath))

def getQuotesFromFileByNameFromListFinal(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    return getQuotesFromDataByName(data)


def getQuotesFromDataByName(data):
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(Config.ABBREV)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    tokenized = tokenizer.tokenize(textoIntegralLimpo)
    return tokenizeByNameFromListFinal(removeFakeNewLines(tokenized))

def cleanTokenizer(data):
    textoIntegral = data["full_text"]
    textoIntegralLimpo = clearSpecialCharacters(textoIntegral)
    textoIntegralLimpo = clearReferences(textoIntegralLimpo)
    textoIntegralLimpo = textoIntegralLimpo.replace("\n", " ")
    textoIntegralLimpo = textoIntegralLimpo.replace(" ", "")
    textoIntegralLimpo = textoIntegralLimpo.replace("–", "-")
    # textoIntegralLimpo = textoIntegralLimpo.replace(";",".")  #Para agora dá, mas é importante perceber que isto serve para quando ha mais do que 1 referencia na mesma linha
    textoIntegralLimpo = textoIntegralLimpo.replace(" ;", ";")
    # textoIntegralLimpo = textoIntegralLimpo.replace(" -",",") #Nao justifica trocar por ".", mas é importante ter em conta
    # textoIntegralLimpo = textoIntegralLimpo.replace(" –",",")
    # textoIntegralLimpo = textoIntegralLimpo.replace(":",".") #Melhor  retirar porque vários livros têm ":" como pontuação no titulo
    textoIntegralLimpo = textoIntegralLimpo.replace(" .", ".")
    textoIntegralLimpo = textoIntegralLimpo.replace("( )", "( ")

    pattern = r"(?<=[A-Za-z])\.\."
    replacement = ". . "
    textoIntegralLimpo = re.sub(pattern, replacement, textoIntegralLimpo)
    pattern = re.compile(r' \b_+\b')
    textoIntegralLimpo = re.sub(pattern, '. #Referências#.', textoIntegralLimpo)

    return textoIntegralLimpo

def tokenizeByPatterns(tokenizer):
    data = []
    for i, frase in enumerate(tokenizer):
        flag = False
        # print(re.findall("\..[\[[0-9]+]", frase))
        lowerPhrase = frase.lower()
        if (len(frase) < 5):
            i = i - 1
            continue
        elif ("#Referências#" in frase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t#\t Separação para Referências")
            continue
        elif (re.compile(r'[\[[0-9\/]+]').search(frase)):
            # print(str(i) + "\tbra\t.\t" + frase)
            # print("bra\t.\t" + frase)
            data.append("-\tbra\t.\t" + frase)
            continue
        for pattern in Config.PATTERNS:
            if re.search(pattern, lowerPhrase):
                # print("ref\t|" + pattern + "|\t" + frase)
                data.append("TP?\tref\t|" + pattern + "|\t" + frase)
                # print(str(i)+"\tref\t|" + pattern + "|\t" + frase)
                flag = True
                break
        if not flag:
            # print("not\t.\t" + frase)
            data.append("TN?\tnot\t.\t" + frase)
            # print(str(i)+"\tnot\t.\t" + frase)
    # print("###" + frase)
    return data

def tokenizeByName(tokenizer):
    names = []
    with open("assets/surnames.csv", 'r', newline='', encoding='utf-8') as csvfile:  # 4200-072 e 44 e 3060-123 ??
        lines = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in lines:
            name = ', '.join(row).split(',')[0]
            names.append(name)

    names.sort()

    data = []
    for i, phrase in enumerate(tokenizer):
        characters_to_replace = [".", ";", ")", "(", ":", "-", "\"", ",", "'", "/"]
        for char in characters_to_replace:
            phrase = phrase.replace(char, "")
        words = phrase.split(" ")

        flag = False
        lowerPhrase = phrase.lower()
        if (len(phrase) < 5):
            i = i - 1
            continue
        elif ("#Referências#" in phrase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t#\t Separação para Referências")
            continue
        elif (re.compile(r'[\[[0-9\/]+]').search(phrase)):
            # print(str(i) + "\tbra\t.\t" + frase)
            # print("bra\t.\t" + frase)
            data.append("-\tbra\t.\t" + phrase)
            continue

        for i, word in enumerate(words):
            if word in names:
                if i != len(words) - 1 and words[i + 1] in names:
                    flag = True
                    data.append("TP?\tref\t|" + word + " " + words[i+1] + "|\t" + phrase)
                    continue
        if not flag:
            data.append("TN?\tnot\t.\t" + phrase)
    return data

def tokenizeByNameFromList(tokenizer):
    proprios = []
    apelidos = []
    with open("assets/proprios.txt", 'r', newline='', encoding='utf-8') as outfile:
        lines = outfile.readlines()
        for line in lines:
            line = line.strip('\n')
            line = line.strip('\r')
            proprios.append(line)

    with open("assets/apelidos.txt", 'r', newline='', encoding='utf-8') as outfile:
        lines = outfile.readlines()
        for line in lines:
            line = line.strip('\n')
            line = line.strip('\r')
            apelidos.append(line)

    data = []
    for i, phrase in enumerate(tokenizer):
        characters_to_replace = [".", ";", ")", "(", ":", "-", "\"", ",", "'", "/"]
        clean_phrase = phrase
        for char in characters_to_replace:
            clean_phrase = clean_phrase.replace(char, "")
        words = clean_phrase.split(" ")

        flag = False
        # lowerPhrase = phrase.lower()
        if (len(phrase) < 5):
            i = i - 1
            continue
        elif ("#Referências#" in phrase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t#\t Separação para Referências")
            continue
        elif (re.compile(r'[\[[0-9\/]+]').search(phrase)):
            # print(str(i) + "\tbra\t.\t" + frase)
            # print("bra\t.\t" + frase)
            data.append("-\tbra\t.\t" + phrase)
            continue

        for i, word in enumerate(words):
            if word in proprios:
                if i != len(words) - 1 and words[i + 1] in apelidos:
                    flag = True
                    data.append("TP?\tref\t|" + word + " " + words[i+1] + "|\t" + phrase)
                    break
            if word in apelidos:
                if i != len(words) - 1 and (words[i + 1] in proprios or words[i + 1] in apelidos):
                    flag = True
                    data.append("TP?\tref\t|" + word + " " + words[i+1] + "|\t" + phrase)
                    break
        if not flag:
            data.append("TN?\tnot\t.\t" + phrase)
    return data

def tokenizeByNameFromListFinal(tokenizer):
    input_file = os.path.join(Config.ROOT_FOLDER, "assets", "investigadores_completo.txt")

    names = []
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            names.append(line)

    data = []
    for i, phrase in enumerate(tokenizer):

        flag = False
        if (len(phrase) < 5):
            i = i - 1
            continue
        elif ("#Referências#" in phrase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t#\t Separação para Referências")
            continue

        lowerPhrase = phrase.lower()
        # characters_to_replace = [".", ";", ")", "(", ":", "-", "\"", ",", "'", "/"]
        clean_phrase = lowerPhrase.replace(".", "").replace(".", "").replace(",", "").replace(";", "").replace("(", "").replace(")", "").replace(":", "").replace("\"", "").replace("'", "")
        clean_phrase = clean_phrase.replace("/", " ").replace("-", " ")
        words = clean_phrase.split(" ")

        for pattern in Config.PATTERNS:
            if re.search(pattern, lowerPhrase):
                for name in names:
                    name_words = name.split()
                    if all(word.lower() in words for word in name_words):
                        # if name in phrase:
                        flag = True
                        data.append("TP?\tref\t|" + name + "|\t|" + pattern + "|\t" + phrase)
                        break
            if flag:
                break

        if not flag:
            if (re.compile(r'[\[[0-9\/]+]').search(phrase)):
                # print(str(i) + "\tbra\t.\t" + frase)
                # print("bra\t.\t" + frase)
                data.append("-\tbra\t.\t.\t" + phrase)
            else:
                data.append("TN?\tnot\t.\t.\t" + phrase)
    return data

def tokenizeByNameFromListFinal2(tokenizer):
    input_file = "assets/names.txt"

    names = []
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            names.append(line)

    data = []
    for i, phrase in enumerate(tokenizer):

        flag = False
        if (len(phrase) < 5):
            i = i - 1
            continue
        elif ("#Referências#" in phrase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t#\t Separação para Referências")
            continue

        lowerPhrase = phrase.lower()
        # characters_to_replace = [".", ";", ")", "(", ":", "-", "\"", ",", "'", "/"]
        clean_phrase = lowerPhrase.replace(".", "").replace(".", "").replace(",", "").replace(";", "").replace("(", "").replace(")", "").replace(":", "").replace("\"", "").replace("'", "")
        clean_phrase = clean_phrase.replace("/", " ").replace("-", " ")
        words = clean_phrase.split(" ")

        # for name in names:
        #     name_words = name.split()
        #     if all(word.lower() in words for word in name_words):
        #     # if name in phrase:
        #         for pattern in patterns:
        #             if re.search(pattern, lowerPhrase):
        #                 flag = True
        #                 data.append("TP?\tref\t|" + name + "|\t|" + pattern + "|\t" + phrase)
        #                 break
        #     if flag:
        #         break

        for pattern in Config.PATTERNS:
            if re.search(pattern, lowerPhrase):
                for i, word in enumerate(lowerPhrase):
                    if word in names and lowerPhrase[i+1] in names:
                        # if name in phrase:
                        flag = True
                        data.append("TP?\tref\t|" + word + "|\t|" + pattern + "|\t" + phrase)
                        break
            if flag:
                break

        if not flag:
            if (re.compile(r'[\[[0-9\/]+]').search(phrase)):
                # print(str(i) + "\tbra\t.\t" + frase)
                # print("bra\t.\t" + frase)
                data.append("-\tbra\t.\t.\t" + phrase)
            else:
                data.append("TN?\tnot\t.\t.\t" + phrase)
    return data

def tokenizeByNameInvestigadores(tokenizer):
    input_file = "assets/investigadores.txt"

    names = []
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            names.append(line)

    data = []
    for i, phrase in enumerate(tokenizer):

        flag = False
        if (len(phrase) < 5):
            i = i - 1
            continue
        elif ("#Referências#" in phrase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t#\t Separação para Referências")
            continue
        elif (re.compile(r'[\[[0-9\/]+]').search(phrase)):
            # print(str(i) + "\tbra\t.\t" + frase)
            # print("bra\t.\t" + frase)
            data.append("-\tbra\t.\t" + phrase)
            continue

        for name in names:
            if name in phrase:
                flag = True
                data.append("TP?\tref\t|" + name + "|\t" + phrase)
                continue

        if not flag:
            data.append("TN?\tnot\t.\t" + phrase)
    return data

def tokenizeByNameGrammar(tokenizer):

    data = []
    for i, phrase in enumerate(tokenizer):

        bad_author_counter = 0
        # new_sentence = new_sentence.replace('á', 'a')
        # new_sentence = new_sentence.replace('é', 'e')
        # new_sentence = new_sentence.replace('í', 'i')
        # new_sentence = new_sentence.replace('ó', 'o')
        # new_sentence = new_sentence.replace('ú', 'u')
        # new_sentence = new_sentence.replace('ã', 'a')
        # new_sentence = new_sentence.replace('à', 'a')
        # new_sentence = new_sentence.replace('ê', 'e')
        phrase = " / ".join([part.strip() for part in phrase.split("/")])
        phrase = ". ".join([part.strip() for part in phrase.split(".")])
        originalPhrase = phrase
        phrase = phrase.lower()

        tagged_sentence = unigram_tagger.tag(nltk.word_tokenize(phrase))

        # Replace tags for custom ones
        for tuples in word_tag_list:
            for i, tagTuple in enumerate(tagged_sentence):
                if tuples[0] == tagTuple[0] and tuples[1] != tagTuple[1]:
                    tagged_sentence[i] = tuples
                    continue

        # Add tags to numbers
        for i, tagTuple in enumerate(tagged_sentence):
            if tagTuple[0].isdigit():
                tagged_sentence[i] = (tagTuple[0], 'NUM')
            else:
                pattern = r"^(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"  # Roman Numbers
                if re.match(pattern, tagTuple[0], re.IGNORECASE) is not None:
                    tagged_sentence[i] = (tagTuple[0], 'NUM')

        # print(tagged_sentence)

        for i, tagTuple in enumerate(tagged_sentence):
            if tagTuple[1] is None:
                tagTuple = (tagTuple[0], 'N')
            tagged_sentence[i] = tagTuple

        grammar = r"""
                NAME: {<NPROP2>((<NPROP>|<PREP>)?<NPROP2>)+}
                PAG_DOT: {<PAG><PONT>?}
                PAGS: {<PAG_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*(<KC><SGS>)?}
                REF: {<NAME><.*>+?<PAGS>}
            """
        # NAME: {<NPROP>+(<PREP>?<NPROP>)+}
        # REF: {<NAME><.*>*<PAGS>}
        # REF: {<NAME><[^PAGS].*>*<PAGS>}
        # LIVRO: {<PUNC><.*>+?<PUNC><PAGS>}
        #         }<PAGS|NAME>{
        # OB_CIT: {<NAME><PUNC>*<NAME><PUNC>*<PAGS>}

        # REF: {(<NAME><.*>+?(<PAGS>(<PUNC><NOTS>)?)(<SEP>|<PONT>|<PUNC>|<KC>))|(<NAME><.*>{,2}?<IN><.*>+?(<SEP>|<PONT>|<PAGS>)<KC>?)}

        # # Criando o objeto RegexpParser com as regras definidas
        parser = nltk.RegexpParser(grammar)
        # print(parser)

        # tagged_sentence = [( "money" ,"NN"),("market", "NN"),("fund", "NN")]
        result = parser.parse(tagged_sentence)

        flag = False
        if (len(phrase) < 5):
            i = i - 1
            continue
        elif ("#Referências#" in phrase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t#\t Separação para Referências")
            continue
        elif (re.compile(r'[\[[0-9\/]+]').search(phrase)):
            # print(str(i) + "\tbra\t.\t" + frase)
            # print("bra\t.\t" + frase)
            data.append("-\tbra\t.\t" + phrase)
            continue

        for subtree in result.subtrees():
            if subtree.label() == "REF":
                flag = True
                data.append("TP?\tref\t|" + subtree.leaves()[0][0] + "\t.\t" + subtree.leaves()[1][0] + "|\t" + originalPhrase)
                continue

        if not flag:
            data.append("TN?\tnot\t.\t.\t" + originalPhrase)
    return data