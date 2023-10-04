import os
import re

phrases = [
    "This is page pp.200 of the book.",
    "Please refer to pag.38 for more information.",
    "Chapter ch.12 covers advanced topics.",
    "aaa.aaa aaa.aaa",
    "20.20"
]

pattern = r"[A-Za-z]\.\d"

for phrase in phrases:
    match = re.search(pattern, phrase)
    if match:
        print(f"Pattern found in phrase: '{phrase}'")
    else:
        print(f"Pattern not found in phrase: '{phrase}'")
# verifiedFiles = []
# i = 0
# for file in os.listdir("doc_json"):
#     print(str(i) +": "+file)
#     i += 1
#     verifiedFiles.append(file)
# fileIndex = input()
# data = Utils.getQuotesFromFileByNameFromListFinal(os.path.join("", "doc_json", verifiedFiles[int(fileIndex)]))
# print(data)
#
# for entry in data:
#     if entry.startswith("TP"):
#         line = entry.split("\t")[4]
#         nltkTest.grammaering(line)
# for line in data:
#     print(line)

# def generateBertDataset():
#     full_data = []
#     i = 0
#     for file in os.listdir("../quotes_verificadas"):
#         # data = Utils.getQuotesFromFileByPattern(os.path.join("doc_json", file))
#         # data = Utils.getQuotesFromFileByNameFromListFinal(os.path.join("doc_json", file))
#         i +=1
#         try:
#             folder = "quotes_verificadas"
#             title = file
#             print(title)
#             with open("../" + folder + "/" + title, "r", encoding='utf-8') as outfile:
#                 for line in outfile:
#                     lineParts = line.split('\t')
#                     if lineParts[0] == "-" or lineParts[0] == "#": # Frases com brackets [2] têm uma possivel referencia nao identificavel por nao seguir exatamente um padrão, apenas referenciarem-se a alguma informação extra textual.
#                         continue
#                     lineParts[0] = lineParts[0].replace("?", "")
#                     try:
#                         full_data.append(lineParts[0] + "\t" + lineParts[4])
#                     except:
#                         print(line)
#         except:
#             # print(data)
#             print("Error creating " + title, file=sys.stderr)
#             exit()
#     # print(full_data)
#     with open("quote_collection.txt", "w", encoding='utf-8') as outfile:
#         for line in full_data:
#             outfile.write(line)


# names = ["Maria Raquel Guimarães", "Maria Ribeira Grande da Silva Pereira Amandio Sottomayor", "Jose Almeida Coutinho"]
#
# def contains_name(phrase, names):
#     translator = str.maketrans("", "", string.punctuation)
#
#     # Remove punctuation using the translation table
#     text_without_punctuation = phrase.translate(translator)
#     phrase_words = text_without_punctuation.split()
#     for name in names:
#         name_words = name.split()
#         if all(word in phrase_words for word in name_words):
#             return True
#     return False

# def contains_name(phrase, names):
#     phrase_words = phrase.split()
#     for full_name in names:
#         name_words = full_name.split()
#         flag = True
#         for name in name_words:
#             if name not in phrase_words:
#                 flag = False
#         if flag:
#             return True
#     return False
#



# phrase = "Tais categorias, no entanto, além de não serem perfeitamente definidas, têm conexões entre si, o que significa que às seis funções apontadas, eventualmente subjacentes à emissão de um \"cartão de plástico\", não correspondem, necessariamente seis cartões distintos, sendo comum a acumulação de várias funções no mesmo cartão (cfr. Maria Raquel Guimarães, As transferências Electrónicas de Fundos e os Cartões de Débito, Almedina, 1999, pags. 55, 58, 63 e 64 )."
# if contains_name(phrase, names):
#     print("The phrase contains a name from the list.")
# else:
#     print("The phrase does not contain a name from the list.")

# with open("./autores_fdup.txt", "r", encoding='utf-8') as f:
#     lines = f.readlines()
#     nameList = []
#     for line in lines:
#         # 384-322 a.C. Aristóteles
#         line = re.sub(r'a.C\.?', '', line, flags=re.IGNORECASE)
#         line = re.sub(r'\d+(-\d+)?', '', line)
#         line = line.replace("a.C.", "").replace("º", "").replace("ª", "").replace("?", "")
#         members = line.split("$$")[1:]
#         #1º Visconde de Carnaxide
#         #1255-1307? Tiago de Viterbo
#         apelido = members[0][1:].strip('\n').strip("|").strip(" ").replace(",", "")
#         try:
#             nomes = members[1][1:].strip('\n').strip("|").strip(" ").replace(",", "")
#         except:
#             nomes = ""
#         fullname = str(nomes) + " " + str(apelido)
#         #Alves Sandra Mara Campos; Delduque Maria Célia; Neto Nicolau Dino
#         if ";" in fullname:
#             nomes = fullname.split(";")
#             for nome in nomes:
#                 nameList.append(nome.strip(" "))
#         else:
#             nameList.append(fullname.strip(" "))
#     nameList = sorted(nameList)
#     nameList = list(set(nameList))
#     nameList = sorted(nameList)
#     with open("../assets/investigadores_completo.txt", "w", encoding='utf-8') as outfile:
#         for line in nameList:
#             outfile.write(line + "\n")


# def check_name_presence(phrase, name):
#     # Split the phrase into individual words
#     phrase_words = phrase.split()
#
#     # Iterate over the phrase words to find the starting index of the name
#     for i in range(len(phrase_words) - len(name) + 1):
#         # Get the sublist of words starting from the current index
#         subphrase = phrase_words[i:i + len(name)]
#
#         # Check if the subphrase matches the name words in any order
#         if set(subphrase) == set(name):
#             return True
#
#     return False
# # Example usage
# phrase = "I Maria like to play with Ines in Aguas"
# phrase = "I  like to play with Maria Ines Aguas in "
# name = "Ines Maria Aguas"
#
# if check_name_presence(phrase, name):
#     print("The name is present in the phrase.")
# else:
#     print("The name is not present in the phrase.")
#
#
#
#
#
#
# def binary_search(names, target):
#     left = 0
#     right = len(names) - 1
#
#     while left <= right:
#         mid = (left + right) // 2
#         mid_name = names[mid]
#
#         if mid_name == target:
#             return mid  # Found the target, return the index
#
#         if mid_name < target:
#             left = mid + 1  # Target is in the right half
#         else:
#             right = mid - 1  # Target is in the left half
#
#     return -1  # Target not found
#
# # Example usage:
# names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"]
# target_name = "Eve"
#
# # Sort the list before performing binary search
# names.sort()
#
# # Call the binary search function
# index = binary_search(names, target_name)
#
# if index != -1:
#     print(f"Found {target_name} at index {index}")
# else:
#     print(f"{target_name} not found in the list.")
#
#
#
#
# start_time = time.time()
# time_after_block_prev = start_time
#
# file = "doc_5261__20.6T8BRG.G1.S1.json"
#
# fileData = open(os.path.join("../doc_json", file), mode='r', encoding='utf8', buffering=1)
# data = json.load(fileData)
# textoIntegralLimpo = Utils.cleanTokenizer(data)
# punkt_param = PunktParameters()
# punkt_param.abbrev_types = set(Utils.abbrev)
# tokenizer = PunktSentenceTokenizer(punkt_param, lang_vars=Utils.CustomLanguageVars())
# # a = sent_tokenize(textoIntegralLimpo)
# a = tokenizer.tokenize(textoIntegralLimpo)
# a = Utils.removeFakeNewLines(a)
#
#
# input_file = "../assets/investigadores_completo.txt"
#
# names = []
# with open(input_file, "r", encoding='utf-8') as f:
#     lines = f.readlines()
#     for line in lines:
#         line = line.strip('\n')
#         names.append(line)
#
# data = []
# for i, phrase in enumerate(a):
#
#     flag = False
#     if (len(phrase) < 5):
#         i = i - 1
#         continue
#     elif ("#Referências#" in phrase):
#         # print("#\t#\t Separação para Referências")
#         data.append("#\t#\t#\t Separação para Referências")
#         continue
#     elif (re.compile(r'[\[[0-9\/]+]').search(phrase)):
#         # print(str(i) + "\tbra\t.\t" + frase)
#         # print("bra\t.\t" + frase)
#         data.append("-\tbra\t.\t.\t" + phrase)
#         continue
#
#     for name in names:
#         name_words = name.split()
#         translator = str.maketrans("", "", string.punctuation)
#         text_without_punctuation = phrase.translate(translator)
#         phrase_words = text_without_punctuation.split()
#         if all(word in phrase_words for word in name_words):
#         # if name in phrase:
#             lowerPhrase = phrase.lower()
#             for pattern in Utils.patterns:
#                 if re.search(pattern, lowerPhrase):
#                     flag = True
#                     data.append("TP?\tref\t|" + name + "|\t|" + pattern + "|\t" + phrase)
#                     break
#         if flag:
#             break
#
#     if not flag:
#         data.append("TN?\tnot\t.\t.\t" + phrase)
# # print(data)
#
# end_time = time.time()
# # Total elapsed time
# total_elapsed_time = end_time - start_time
# print(f"Overall elapsed time: {total_elapsed_time} seconds")
