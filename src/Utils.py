import json
import re
import sys
from datetime import datetime

from nltk.tokenize import sent_tokenize


def fileToArray(filePath):
    file = open(filePath, "r", encoding="utf-8")
    fileArray = []
    for line in file.read().split('\n'):
        fileArray.append(line)
    return fileArray[:-1]


def clearRomanNumerals(phrase):
    pattern = r'\b([IVXLCDM]+)\.\b'

    # Find all occurrences of Roman numerals with trailing dot in the phrase
    matches = re.findall(pattern, phrase)

    # Iterate over the matches and replace the "." with ")"
    for match in matches:
        replacement = match + ")"
        phrase = re.sub(r'\b' + match + r'\.\b', replacement, phrase)

    return phrase


def clearSpecialCharacters(text):
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
    text = text.replace("] / [", "/")
    return text


def clearEnters(text):
    return re.sub("(\\n){2,}", "\n", text)


def clearReferences(text):
    text = text.replace("“", "\"")
    text = text.replace("”", "\"")

    # '. [2]\n'
    occurrences = re.findall("\. [\[[0-9\/]+]\\n", text)
    for ocorrence in occurrences:
        value = ocorrence.split(". [")[1].split("]")[0]
        text = text.replace(ocorrence, " [" + value + "]. ")

        occurrences = re.findall("\. [\[[0-9\/]+] [A-Z0-9]", text)
    # '. [7] Multiple'
    for ocorrence in occurrences:
        value = ocorrence.split(". [")[1].split("]")[0]
        character = ocorrence.split(". [")[1].split("]")[1].split(" ")[1]
        text = text.replace(ocorrence, " [" + value + "]. " + character)

    return text


def createJsonSchemaFromRawSchema(jsonString):
    jsonObject = json.loads(json.dumps(jsonString))
    newJson = {}
    for key in jsonObject:
        value = jsonObject[key]
        newJson = documentJsonMapper(key, value, newJson)
    newJson["type"] = "Acordao"
    return newJson


def documentJsonMapper(key, value, json):
    if key == "Link":
        json["link"] = value[0]
    elif key == "Processo":
        json["_id"] = value[0]
    elif key == "Tribunal":
        json["court"] = value[0].replace("Acórdão do ", "")
    elif key == "Data do Acordão":
        json["date"] = value[0]
        datetime_object = datetime.strptime(json["date"], '%m/%d/%Y')
        json["year"] = value[0] = datetime_object.year
    elif key == "Descritores":
        json["descriptors"] = value
    elif key == "Relator":
        json["author"] = value
    elif key == "Sumário ":
        json["summary"] = value[0]
    elif key == "Decisão Texto Integral":
        json["full_text"] = value[0]

    return json

    # This are the types that were ignored
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


def removeFakeNewLines(phrases):
    for i, phrase in enumerate(phrases):
        charCounter = 0
        for char in phrase:
            if char == '(':
                charCounter = charCounter + 1
            if char == ')':
                if charCounter != 0:
                    charCounter = charCounter - 1
        if charCounter != 0 and i + 1 < len(phrases):
            return removeFakeNewLines(mergeArray(phrases, i, i + 1))
    return phrases


def mergeArray(array, index1, index2):
    item1 = str(array[index1])
    item2 = str(array[index2])

    merged_item = str(item1 + item2)
    array[index1] = merged_item
    array.pop(index2)

    return array


def getQuotesArray(filePath):
    fileData = open(filePath, mode='r', encoding='utf8', buffering=1)
    data = json.load(fileData)
    textoIntegral = data["full_text"]
    textoIntegralLimpo = clearSpecialCharacters(textoIntegral)
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


def getOnlyReferencesFromExtractedData(data):
    references = []
    for line in data:
        if line.startswith('TP'):
            lineParts = line.split("\t")
            references.append(lineParts[4])
    return references

def logInfo(message):
    print("[INFO] " + message)