import csv
import json
import re
import sys
from datetime import datetime

import nltk
from nltk.corpus import mac_morpho
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktTrainer, PunktLanguageVars

abbrev = ['exs', 'exas', 'trf', 'dr', 'dra', 'prof', 'r', 'al', 'als',
          "proc", "procs", "n", "ac", "fls", "art", "arts", "ep", "cfr", "ob", "obs", "cit", "dl",
          "doc", "docs", "ed", "rel", "j", "v.g", "Lx",
          "ver", "vol", "segs",
          "p", "ps", ", p", 'pp', "págs", "pags", "pag", "pág",  # Paginas
          "loc", "op", "ap", "ss", "vs", "cons", "acs",
          'inc', 'e.g', 'i.e', 'etc', 'sgs', 'vg', 'Lx', 'J',

          # "º ", "ª ", "º", "ª", "º",
          # "I", "V", "X", "D", "L", "C", "M",
          "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def fileToArray(filePath):
    file = open(filePath, "r", encoding="utf-8")
    fileArray = []
    for line in file.read().split('\n'):
        fileArray.append(line)
    return fileArray[:-1]


def clearText(text):  # https://duvidas.dicio.com.br/abreviaturas-lista-de-abreviacoes/
    # cleanNumbers = ["0.", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."]
    cleanInitials = ["I.", "V.", "X.", "D.", "L.", "C.", "M.",
                     "º.", "ª.", ]
    cleanWords = ["proc.", "procs.", "n.", "ac.", "fls.", "art.", "arts.", "ep.", "cfr.", "ob.", "obs.", "cit.", "dl.",
                  "ver.", "vol.", "segs.",
                  "págs.", "pags.", "pag.", "pág.", "loc.", "op.", "ap." "ss.", "cons.", "acs."]
    # for word in cleanNumbers:
    #     text.replace(word, word.replace(".", "-"))

    text = text.replace("[[", "[")
    text = text.replace("]]", "]")
    text = text.replace("[ [", "[")
    text = text.replace("] ]", "]")
    text = text.replace(" .", " ")
    text = text.replace(". – ", " - ")
    text = text.replace(". - ", " - ")
    text = text.replace(".- ", "- ")
    text = text.replace("). ", ") ")
    text = text.replace(". []", "[].")
    text = text.replace(".\"", "\"")

    for word in cleanInitials:
        text = text.replace(word, word.replace(".", ")"))

    # for word in cleanWords:
    #     text = text.replace(word, word.replace(".", ""))
    #     text = text.replace(word.capitalize(), word.capitalize().replace(".", ""))
    return text


def clearEnters(text):
    # text = text.replace('\n', ' ')
    # text = re.sub("[^\\n]\\n?", " ")
    # text = re.sub("(\\n){2,}", "\n")
    text = re.sub("(\\n){2,}", "////TempString", text)
    # text = text.replace("\n", " ")
    text = text.replace("////TempString", "\n")
    # text = text.replace("\n", "#ENTER#")
    # text = text.replace(".\n", ".")
    # text = text.replace("\n", " ")
    # text = text.replace(". [", "[")
    # text = text.replace(".[", "[")
    return text


def clearReferences(text):
    textoIntegralLimpo = text.replace("] / [", "/")

    # textoIntegralLimpo = textoIntegralLimpo.replace("\n", "#ENTER#")
    textoIntegralLimpo = textoIntegralLimpo.replace("“", "\"")
    textoIntegralLimpo = textoIntegralLimpo.replace("”", "\"")

    # '. [2]\n'
    ocorrencias = re.findall("\. [\[[0-9\/]+]\\n", textoIntegralLimpo)
    for ocorrencia in ocorrencias:
        valor = ocorrencia.split(". [")[1].split("]")[0]
        textoIntegralLimpo = textoIntegralLimpo.replace(ocorrencia, " [" + valor + "]. ")

    ocorrencias = re.findall("\. [\[[0-9\/]+] [A-Z0-9]", textoIntegralLimpo)
    # '. [7] Recorrencia'
    for ocorrencia in ocorrencias:
        valor = ocorrencia.split(". [")[1].split("]")[0]
        character = ocorrencia.split(". [")[1].split("]")[1].split(" ")[1]
        textoIntegralLimpo = textoIntegralLimpo.replace(ocorrencia, " [" + valor + "]. " + character)

    # ocorrencias = re.findall("\. [\[[0-9]+]\s(/\s\[[0-9]+]\s){1,}[A-Z0-9]", textoIntegralLimpo)
    # ocorrencias1 = re.findall("\/ [\[0-9]+] ", textoIntegralLimpo)
    # ocorrencias = re.findall("\. [\[[0-9\/]+]\\n", textoIntegralLimpo)
    # print(ocorrencias)
    # # '. [4] / [5] Recorrencia'
    # for ocorrencia in ocorrencias:
    #     valor = ocorrencia.split(". [")[1].split("]")[0]
    #     textoIntegralLimpo = textoIntegralLimpo.replace(ocorrencia, " ["+valor+"]. ")

    return textoIntegralLimpo


def makeSchema(jsonString):
    jsonObject = json.loads(json.dumps(jsonString))
    newJson = {}
    for key in jsonObject:
        value = jsonObject[key]
        # print("The key and value are ({}) = ({})".format(key, value))
        newJson = switch(key, value, newJson)
    newJson["type"] = "Acordao"
    return newJson


def switch(key, value, jsonObject):
    if key == "Link":
        jsonObject["link"] = value[0]
        return jsonObject
    elif key == "Processo":
        # jsonObject["n_process"] = value[0]
        jsonObject["_id"] = value[0]
        return jsonObject
    elif key == "Tribunal":
        jsonObject["court"] = value[0].replace("Acórdão do ", "")
        return jsonObject
    elif key == "Data do Acordão":
        jsonObject["date"] = value[0]
        datetime_object = datetime.strptime(jsonObject["date"], '%m/%d/%Y')
        jsonObject["year"] = value[0] = datetime_object.year
        return jsonObject
    elif key == "Descritores":
        jsonObject["descriptors"] = value
        return jsonObject
    # Votação e Decisão estão juntos
    # elif key == "Votação" or key == "Decisão":
    #     if "vote" in jsonObject:
    #         jsonObject["vote"].append(value[0])
    #     else:
    #         jsonObject["vote"] = [value[0]]
    #     return jsonObject

    elif key == "Relator":
        jsonObject["author"] = value
        return jsonObject
    elif key == "Sumário ":
        jsonObject["summary"] = value[0]
        return jsonObject
    elif key == "Decisão Texto Integral":
        # textoIntegralLimpo = clearText(value[0])
        # textoIntegralLimpo = clearReferences(textoIntegralLimpo)
        # textoIntegralLimpo = textoIntegralLimpo.replace("\n", " ")
        # jsonObject["full_text"] = textoIntegralLimpo
        jsonObject["full_text"] = value[0]
        return jsonObject

    # jsonObject[key] = value
    return jsonObject

    # elif key == "Nº Convencional":
    # elif key == "Nº do Documento":
    # elif key == "Referência de Publicação":
    # elif key == "Tribunal Recurso":
    # elif key == "Processo no Tribunal Recurso":
    # elif key == "Data":
    # elif key == "Texto Integral":
    # elif key == "Privacidade":
    # elif key == "Meio Processual":
    # elif key == "Área Temática":
    # elif key == "Legislação Nacional":
    # elif key == "Legislação Comunitária":
    # elif key == "Jurisprudência Nacional":


def saveData(folder, data):
    title = "doc_" + str(data.get('_id').replace("/", "__"))
    _saveData(folder, title, data)


def _saveData(folder, title, data):
    jsonObject = json.dumps(data, indent=4, ensure_ascii=False)
    # jsonObject = json.dumps(makeSchema(jsonObject), indent=4, ensure_ascii=False)
    try:
        with open(folder + "/" + title + ".json", "w", encoding='utf-8') as outfile:
            outfile.write(jsonObject)
    except:
        print(jsonObject)
        print("Error creating " + title, file=sys.stderr)
        exit()
    print("File " + title + " created successfully")
    return jsonObject

patterns = [
    r" in ",
    r" by ",
    r" pag\. ",
    r" pág\. ",
    r" pags\. ",
    r" págs\. ",
    r" cfr\. ",
    r" citando ",
    r"afirma que",
    r"a expressão é de",
    r"como .+ sublinha",
    r"como dá conta",
    r"como ensina",
    r"como nos dá conta",
    r"como sublinha",
    r"como sugerido por",
    r"como sustenta",
    r"conforme alerta",
    r"conforme discorre",
    r"conforme explicam",
    r"conforme explica",
    r"do mesmo modo,",
    r"em sentido próximo .+ se pronuncia",
    r" escreve ",
    r"explica o autor:",
    r"na doutrina",
    r"na síntese de",
    r"nas palavras de",
    r"neste sentido",
    # r"neste sentido, afirma",
    r"no mesmo sentido aponta",
    # r"no mesmo sentido aponta também o prof.",
    # r"No mesmo sentido, refere .+ in artigo publicado",
    # r"Para ...",
    # r"Por todos, cfr.",
    # r"Refere, a este propósito, ... in...",
    r"seguindo .+ a obra de",
    r"segundo",
    r"sobre .+ vide",
    # r"sobre este ponto, .+ vide ainda",
    # r"neste sentido, vide",
    # r"em sentido oposto, vide",
    r"sobre o tema pode ver-se ainda",
    r" vide ",
    # r"vide, por todos,",
    r"como acentua a ",
    r"como acentua o ",
    # r"por Acórdão do ",
    # r"por Acórdão da ",
    # r"mencionado acórdão do",
    # r"mencionado acórdão da",
    # r" cfr. ",

]

class CustomLanguageVars(PunktLanguageVars):
    sent_end_chars = ('.', ';')  # Add ";" as a sentence-ending character

def getQuotesFromFileByPattern(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(abbrev)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    # a = sent_tokenize(textoIntegralLimpo)
    a = tokenizer.tokenize(textoIntegralLimpo)
    return tokenizeByPatterns(a)

def getQuotesFromFileByName(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(abbrev)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    # a = sent_tokenize(textoIntegralLimpo)
    a = tokenizer.tokenize(textoIntegralLimpo)
    return tokenizeByName(a)

def getQuotesFromFileByNameGrammar(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(abbrev)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    # a = sent_tokenize(textoIntegralLimpo)
    a = tokenizer.tokenize(textoIntegralLimpo)
    return tokenizeByNameGrammar(a)

def getQuotesFromFileByNameInvestigadores(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(abbrev)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    # a = sent_tokenize(textoIntegralLimpo)
    a = tokenizer.tokenize(textoIntegralLimpo)
    return tokenizeByNameInvestigadores(a)

def getQuotesFromFileByNameFromList(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(abbrev)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    # a = sent_tokenize(textoIntegralLimpo)
    a = tokenizer.tokenize(textoIntegralLimpo)
    return tokenizeByNameFromList(a)

def getQuotesFromFileByNameFromListFinal(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegralLimpo = cleanTokenizer(data)
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(abbrev)
    tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=CustomLanguageVars())
    # a = sent_tokenize(textoIntegralLimpo)
    a = tokenizer.tokenize(textoIntegralLimpo)
    a = removeFakeNewLines(a)
    return tokenizeByNameFromListFinal(a)

def cleanTokenizer(data):
    textoIntegral = data["full_text"]
    textoIntegralLimpo = clearText(textoIntegral)
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

    # pattern = r'(\d+)\.'
    # result = re.sub(pattern, r'\1', string)
    # textoIntegralLimpo = frase.replace("#ENTER#", "")
    pattern = r"(?<=[A-Za-z])\.\."
    replacement = ". . "
    textoIntegralLimpo = re.sub(pattern, replacement, textoIntegralLimpo)
    pattern = re.compile(r' \b_+\b')
    textoIntegralLimpo = re.sub(pattern, '. #Referências#.', textoIntegralLimpo)

    return textoIntegralLimpo

def removeFakeNewLines(phrases):
    for i, phrase in enumerate(phrases):
        charCounter=0
        for char in phrase:
            if char == '(':
                charCounter = charCounter + 1
            if char == ')':
                if charCounter != 0:
                    charCounter = charCounter - 1
        if charCounter != 0 and i+1 < len(phrases):
            return removeFakeNewLines(merge_items(phrases, i, i+1))
    return phrases

def merge_items(array, index1, index2):
    item1 = str(array[index1])
    item2 = str(array[index2])

    merged_item = str(item1 + item2)
    array[index1] = merged_item
    array.pop(index2)

    return array

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
        for pattern in patterns:
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
    input_file = "./assets/investigadores.txt"

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
            data.append("-\tbra\t.\t.\t" + phrase)
            continue

        for name in names:
            if name in phrase:
                lowerPhrase = phrase.lower()
                for pattern in patterns:
                    if re.search(pattern, lowerPhrase):
                        flag = True
                        data.append("TP?\tref\t|" + name + "|\t|" + pattern + "|\t" + phrase)
                        break
            if flag:
                break

        if not flag:
            data.append("TN?\tnot\t.\t.\t" + phrase)
    return data

def tokenizeByNameInvestigadores(tokenizer):
    input_file = "./assets/investigadores.txt"

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
    input_file = "./tests/mac_morpho_custom.txt"

    custom_words = [("/", "PUNC")]

    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
        word_tag_list = [(line.split()[0], line.split()[1]) for line in lines]

    custom_words = custom_words + word_tag_list
    custom_words = [custom_words]

    sentences = mac_morpho.tagged_sents() + custom_words
    unigram_tagger = nltk.UnigramTagger(sentences)

    data = []
    for i, phrase in enumerate(tokenizer):
        tagged_sentence = unigram_tagger.tag(nltk.word_tokenize(phrase))

        lista_sem_none = []
        for tupla in tagged_sentence:
            if tupla[1] is not None:
                lista_sem_none.append(tupla)

        tagged_sentence = lista_sem_none

        for tuples in word_tag_list:
            for i, tagTuple in enumerate(tagged_sentence):
                if tuples[0] == tagTuple[0] and tuples[1] != tagTuple[1]:
                    tagged_sentence[i] = tuples

        grammar = r"""
            NOME: {(<NPROP>){2,}}
            PAG_DOT: {<PAG><PUNC>?}
            PAGS: {<PAG_DOT><NUM>(<PUNC><NUM>)*}
        """

        parser = nltk.RegexpParser(grammar)
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
            if subtree.label() == "PAGS":
                for subtree in result.subtrees():
                    if subtree.label() == "NOME":
                        flag = True
                        data.append("TP?\tref\t|" + subtree.leaves()[0][0] + " " + subtree.leaves()[1][0] + "|\t" + phrase)
                        continue

        if not flag:
            data.append("TN?\tnot\t.\t" + phrase)
    return data

def getQuotesArray(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegral = data["full_text"]
    textoIntegralLimpo = clearText(textoIntegral)
    textoIntegralLimpo = clearReferences(textoIntegralLimpo)
    textoIntegralLimpo = textoIntegralLimpo.replace("\n", " ")

    a = sent_tokenize(textoIntegralLimpo)
    data = []
    for frase in a:
        data1 = [frase]
        if (" in " in frase
                or " by " in frase
                or " pag " in frase
                or " pags " in frase
                or " cfr " in frase
                or re.compile(r'[\[[0-9\/]+]').search(frase)):
            data1.append(True)
            data1.append(frase)
        else:
            data1.append(False)
            data1.append("")
        data.append(data1)

    return data
