import os
import re

import nltk
from nltk import Tree
from nltk.corpus import mac_morpho
from nltk.tokenize import word_tokenize

# Train the tagger on the tagged sentences in the corpus
input_file = "mac_morpho_custom.txt"

custom_words = [("/", "PUNC")]



# with open("../assets/apelidos.txt", "r", encoding='utf-8') as f:
#     lines = f.readlines()
#     # print(lines)
#     word_tag_list = [(line.split()[0].lower().split("\n")[0], "NPROP2") for line in lines]
#
# custom_words = custom_words + word_tag_list
# word_tag_list = []

current_dir = os.path.dirname(os.path.abspath(__file__))

# Find the root folder by going up in the directory structure
root_folder = current_dir
while not os.path.isfile(os.path.join(root_folder, 'README.md')):
    root_folder = os.path.dirname(root_folder)
relative_path = os.path.join(root_folder, "assets")

investigadores = []
with open(os.path.join(relative_path, "investigadores_completo.txt"), "r", encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        investigadores.append(line)

with open(os.path.join(relative_path, "names.txt"), "r", encoding='utf-8') as f:
    lines = f.readlines()
    # print(lines)
    word_tag_list = [(line.split()[0].lower().split("\n")[0], "NPROP2") for line in lines]

custom_words = custom_words + word_tag_list
word_tag_list = []
# with open("../assets/proprios.txt", "r", encoding='utf-8') as f:
#     lines = f.readlines()
#     word_tag_list = [(line.split()[0].lower().split("\n")[0], "NPROP2") for line in lines]
#
# custom_words = custom_words + word_tag_list
# word_tag_list = []
relative_path = os.path.join(root_folder, "unmarkedTestFiles")
with open(os.path.join(relative_path, input_file), "r", encoding='utf-8') as f:
    lines = f.readlines()
    word_tag_list = [(line.split()[0], line.split()[1]) for line in lines]

word_tag_list = custom_words + word_tag_list
custom_words = [word_tag_list]

# mac_morpho_tagged_words = mac_morpho.tagged_words() + custom_words
# sentences = mac_morpho.tagged_sents()
# sentences.append(custom_words)
sentences = mac_morpho.tagged_sents() + custom_words
unigram_tagger = nltk.UnigramTagger(sentences)
#
# # Tag a new sentence
# new_sentence = "Eu amo comer pizza"




# new_sentence = "Maria Guimarães, ob. cit., págs. 107 / 112)."

def extractQuoteDataFromPhrase(phrase):
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
        NOME: {(<NPROP2>((<NPROP>|<PREP>)<NPROP2>)?)*}
        PAG_DOT: {<PAG><PONT>?}
        VOL_DOT: {<VOL><PONT>?}
        NOT_DOT: {<NOT><PONT>?}
        VOLS: {<VOL_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*}
        PAGS: {<PAG_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*(<KC><SGS>)?}
        NOTS: {<NOT_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*(<KC><SGS>)?}
        REF: {(<NOME><.*>+?(<PAGS>(<PUNC><NOTS>)?)(<SEP>|<PONT>|<PUNC>|<KC>))|(<NOME><.*>{,2}?<IN><.*>+?(<SEP>|<PONT>|<PAGS>)<KC>?)} 
    """
    # NOME: {<NPROP>+(<PREP>?<NPROP>)+}
    # REF: {<NOME><.*>*<PAGS>}
    # REF: {<NOME><[^PAGS].*>*<PAGS>}
    # LIVRO: {<PUNC><.*>+?<PUNC><PAGS>}
    #         }<PAGS|NOME>{
    # OB_CIT: {<NOME><PUNC>*<NOME><PUNC>*<PAGS>}

    # # Criando o objeto RegexpParser com as regras definidas
    parser = nltk.RegexpParser(grammar)
    # print(parser)

    # tagged_sentence = [( "money" ,"NN"),("market", "NN"),("fund", "NN")]
    result = parser.parse(tagged_sentence)
    # print(result)
    referenceList = []

    for subtree in result.subtrees():
        if subtree.label() == "REF":
            # print(subtree)
            # autor_flag = False
            reference = []
            autor_flag = 0
            for subtree2 in subtree.subtrees():
                if autor_flag == 2 and subtree2.label() != "NOME": # Author not in DB
                    continue
                if subtree2.label() == "NOME":
                    author_names = []
                    for leaf in subtree2.leaves():
                        author_names.append(leaf[0])
                    for name in investigadores:
                        if all(word.lower() in author_names for word in name.split()):
                            name = name.replace("\n", "")
                            reference.append("author: " + name)
                            autor_flag = 1
                            break
                    if autor_flag == 0: #Nome não encontrado na base de dados
                        autor_flag = 2
                        bad_author_counter += 1
                        continue
                elif subtree2.label() == 'PAGS':
                    pags = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            pags.append(leaf[0])
                        if (leaf[1] == 'SGS'):
                            pags.append('+')
                    reference.append("pags: " + "[" + ", ".join(pags) +"]")
                elif subtree2.label() == 'VOLS':
                    vols = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            vol = leaf[0]
                            if not leaf[0].isdigit():
                                vol = leaf[0].upper()
                            vols.append(vol)
                    reference.append("vols: [" + ', '.join(vols) + "]")
                elif subtree2.label() == 'NOTS':
                    notes = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            notes.append(leaf[0])
                        if (leaf[1] == 'SGS'):
                            notes.append('+')
                    reference.append("notes: [" + ', '.join(notes) + "]")
            if autor_flag == 2:  # Author not in DB
                continue
            reference = extractOtherReferenceParts(subtree, reference, bad_author_counter)
            referenceList.append(reference)

    return referenceList


def extractOtherReferenceParts(subtree_original, reference, bad_author_counter):
    flag = False
    book = ""
    tupleIn = ('in', 'IN')
    if tupleIn in subtree_original:
        indice_in = subtree_original.index(tupleIn)
        subtree_original = subtree_original[indice_in:]
    for subtree in subtree_original:
        if not isinstance(subtree, Tree):
            if ((subtree[1] == 'PUNC' and subtree[0] == ",") or subtree[1] == 'SEP') and book != "":  # End of part
                book = capitalizePhrase(book).strip(" ")
                if bad_author_counter != 0:
                    bad_author_counter -= 1
                    book = ""
                elif len(book) <= 1:
                    book = ""
                else:
                    if not flag: # Titu
                        flag = True
                        # reference["obra"] = book
                        book = "obra: " + book
                    elif book.isdigit() and  1800 < int(book) < 2100:
                        # reference["ano"] = book
                        book = "ano: " + book
                    elif "Editor" in book or "Editora" in book:
                        # reference["editora"] = book
                        book = "editora: " + book
                    elif "Edição" in book:
                        # reference["edicao"] = book
                        book = "edicao: " + book
                    else:
                        book = "outro: " + book
                    reference.append(book)
                    book = ""
            elif subtree[1] != 'SEP' and subtree[1] != 'PUNC' and subtree[1] != 'PONT' and subtree[1] != 'IN':
                book = book + subtree[0] + " "
        # elif subtree.label() == "NOME":
            # autor_flag = True  # Salta o 1º
        elif (subtree.label() == 'VOLS' or subtree.label() == 'VOL_DOT' or
              subtree.label() == 'PAGS' or subtree.label() == 'PAG_DOT' or
              subtree.label() == 'NOTS' or subtree.label() == 'NOT_DOT' or
              subtree.label() == 'IN' or
              subtree.label() == 'NOME' or
              subtree.label() == 'PUNC' or subtree.label() == 'REF'):
            punc = []
        else:
            book = book + tree_to_str(subtree)
    return reference

def capitalizePhrase(phrase):
    list = phrase.split(" ")
    new_list = []
    for item in list:
        new_list.append(item.capitalize())
    return " ".join(new_list)

def tree_to_str(tree):
    if isinstance(tree, tuple):
        return tree[0]
    string = ""
    for subtree in tree:
        string = string + tree_to_str(subtree) + " "
    return string

def getQuoteJsonAsIEEE(quote):
    author = ""
    obra = ""
    pags = ""
    vols = ""
    notes = ""
    editor = ""
    edicao = ""
    ano = ""
    outro = ""
    for line in quote:
        if line.startswith("author:"):
            line = line[len("author:"):].strip()
            names = line.split()
            name = names[len(names) - 1] + ", " + " ".join(names[:-1])
            if author != "":
                author += " and "
            author += name

        if line.startswith("obra:"):
            line = line[len("obra:"):].strip()
            if obra != "":
                obra += "\" and \""
            obra += line

        if line.startswith("pags:"):
            line = line[len("pags:"):].strip()
            if pags != "":
                pags += "; "
            pags += line

        if line.startswith("vols:"):
            line = line[len("vols:"):].strip()
            if vols != "":
                vols += "; "
            vols += line

        if line.startswith("notes:"):
            line = line[len("notes:"):].strip()
            if notes != "":
                notes += "; "
            notes += line

        if line.startswith("editora:"):
            line = line[len("editora:"):].strip()
            if editor != "":
                editor += "; "
            editor += line

        if line.startswith("edicao:"):
            line = line[len("edicao:"):].strip()
            if edicao != "":
                edicao += "; "
            edicao += line

        if line.startswith("ano:"):
            line = line[len("ano:"):].strip()
            if ano != "":
                ano += "; "
            ano += line

        if line.startswith("outro:"):
            line = line[len("outro:"):].strip()
            if outro != "":
                outro += ", "
            outro += line

    reference = author
    if ano != "": reference += " (" + ano + ")"
    reference += ". \"" + obra + "\""

    if edicao != "": reference +=  ", " + edicao
    if editor != "": reference +=  ", " + editor
    if pags != "": reference +=  ", págs. " + pags
    if vols != "": reference +=  ", vols. " + vols
    if notes != "": reference +=  ", notes " + notes
    if outro != "": reference +=  ", " + outro
    reference += ";"
    return reference


# quotes = [{'autor': ['João Calvão da Silva'], 'pag': ['79', '80'], 'obra': "`` Sinal De Contrato Promessa ''", 'outro': ['Almedina'], 'ano': '2007', 'edicao': '12ª Edição'}, {'autor': ['Fernando de Gravato Morais'], 'pag': ['278', '279'], 'obra': "`` Contratos-promessa Em Geral.contratos-promessa Em Especial ''", 'outro': ['Almedina', 'Abril De 2009']}]
#
# for quote in quotes:
#     getQuoteJsonAsIEEE(quote)



# try:
#     print("Autor: ", autor)
#     print("Volumes: ", vols)
#     print("Páginas: ", pags)
# except NameError:
#     print("Não foi possível extrair as informações da frase.")
# result.draw()

new_sentences = [
]


for sentence in new_sentences:
    print(extractQuoteDataFromPhrase(sentence))
