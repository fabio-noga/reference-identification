import json
import re
import sys
from datetime import datetime

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

abbrev = ['exs', 'exas', 'trf', 'dr', 'dra', 'prof', 'r', 'al', 'als',
          "proc", "procs", "n", "ac", "fls", "art", "arts", "ep", "cfr", "ob", "obs", "cit", "dl",
          "doc", "docs", "ed", "rel", "j", "v.g", "Lx",
          "ver", "vol", "segs",
          "p", "ps", ", p", 'pp', "págs", "pags", "pag", "pág",  # Paginas
          "loc", "op", "ap", "ss", "vs", "cons", "acs",
          'inc', 'e.g', 'i.e', 'etc',

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
    jsonObject = json.loads(jsonString)
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
    title = "doc_" + str(data.get('Processo')[0].replace("/", "__"))
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

]

def getQuotesFromFile(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegral = data["full_text"]
    textoIntegralLimpo = clearText(textoIntegral)
    textoIntegralLimpo = clearReferences(textoIntegralLimpo)
    textoIntegralLimpo = textoIntegralLimpo.replace("–","-")
    textoIntegralLimpo = textoIntegralLimpo.replace(";",".")
    textoIntegralLimpo = textoIntegralLimpo.replace(" -",".")
    textoIntegralLimpo = textoIntegralLimpo.replace(" –",".")
    textoIntegralLimpo = textoIntegralLimpo.replace(":",".")
    textoIntegralLimpo = textoIntegralLimpo.replace("\n"," ")
    # textoIntegralLimpo = frase.replace("#ENTER#", "")
    pattern = r"(?<=[A-Za-z])\.\."
    replacement = ". . "
    textoIntegralLimpo = re.sub(pattern, replacement, textoIntegralLimpo)
    pattern = re.compile(r' \b_+\b')
    textoIntegralLimpo = re.sub(pattern, '. #Referências#.', textoIntegralLimpo)

    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(abbrev)
    punkt_param.sent_end_chars = (';', ':', " -")
    tokenizer = PunktSentenceTokenizer(punkt_param)

    # a = sent_tokenize(textoIntegralLimpo)
    a = tokenizer.tokenize(textoIntegralLimpo)
    data = []
    for i, frase in enumerate(a):
        flag = False
        # print(re.findall("\..[\[[0-9]+]", frase))
        lowerPhrase = frase.lower()
        if (len(frase)<5):
            i=i-1
            continue
        elif("#Referências#" in frase):
            # print("#\t#\t Separação para Referências")
            data.append("#\t#\t Separação para Referências")
            continue
        elif( re.compile(r'[\[[0-9\/]+]').search(frase)):
            # print(str(i) + "\tbra\t.\t" + frase)
            # print("bra\t.\t" + frase)
            data.append("bra\t.\t" + frase)
            continue
        for pattern in patterns:
            if re.search(pattern, lowerPhrase):
                # print("ref\t|" + pattern + "|\t" + frase)
                data.append("ref\t|" + pattern + "|\t" + frase)
                # print(str(i)+"\tref\t|" + pattern + "|\t" + frase)
                flag = True
                break
        if not flag:
            # print("not\t.\t" + frase)
            data.append("not\t.\t" + frase)
            # print(str(i)+"\tnot\t.\t" + frase)
    # print("###" + frase)
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
