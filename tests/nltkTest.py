import re

import nltk
from nltk import Tree
from nltk.corpus import mac_morpho
from nltk.tokenize import word_tokenize

# Train the tagger on the tagged sentences in the corpus
input_file = "./mac_morpho_custom.txt"

custom_words = [("/", "PUNC")]



with open("../assets/apelidos.txt", "r", encoding='utf-8') as f:
    lines = f.readlines()
    # print(lines)
    word_tag_list = [(line.split()[0].lower().split("\n")[0], "NPROP2") for line in lines]

custom_words = custom_words + word_tag_list
word_tag_list = []
with open("../assets/proprios.txt", "r", encoding='utf-8') as f:
    lines = f.readlines()
    word_tag_list = [(line.split()[0].lower().split("\n")[0], "NPROP2") for line in lines]

custom_words = custom_words + word_tag_list
word_tag_list = []

with open(input_file, "r", encoding='utf-8') as f:
    lines = f.readlines()
    word_tag_list = [(line.split()[0], line.split()[1]) for line in lines]

word_tag_list = custom_words + word_tag_list
custom_words = [word_tag_list]

# mac_morpho_tagged_words = mac_morpho.tagged_words() + custom_words
# sentences = mac_morpho.tagged_sents()
# sentences.append(custom_words)
sentences = mac_morpho.tagged_sents() + custom_words
unigram_tagger = nltk.UnigramTagger(sentences)
print("Passou 1")
#
# # Tag a new sentence
# new_sentence = "Eu amo comer pizza"

new_sentences = [
    # "Mas também pelo seu destino, dependente das vicissitudes daqueles tipos contratuais aquele daquele daquela, págs. (Maria Guimarães, ob. cit., pags. 107 / 112).",

    # falta adicionar "e" como separador de paginas
    # "Tais categorias, no entanto, além de não serem perfeitamente definidas, têm conexões entre si, o que significa que às seis funções apontadas, eventualmente subjacentes à emissão de um \"cartão de plástico\", não correspondem, necessariamente seis cartões distintos, sendo comum a acumulação de várias funções no mesmo cartão (cfr. Maria Raquel Guimarães, As transferências Electrónicas de Fundos e os Cartões de Débito, Almedina, 1999, pags. 55, 58, 63 e 64 ).",

    # falta adicionar qualquer digito >99
    # "se o cliente decidir contratar, terá de se sujeitar às cláusulas previamente determinadas por outrem, no exercício de um law making power de que este, de facto, desfruta, limitando-se aquele, pois, a aderir a um modelo prefixado\" (cfr. António Pinto Monteiro, Cláusula Penal e Indemnização, pag. 748;",

    # talvez seja o anterior e "/" como separador de digitos
    # "Segundo outros - e é este o entendimento que reputamos mais acertado -, trata-se de um contrato acessório instrumental, em relação ao contrato de depósito bancário ou ao de abertura de crédito em conta corrente, acessoriedade revelada não apenas pela função do próprio contrato, mas também pelo seu destino, dependente das vicissitudes daqueles tipos contratuais (Maria Raquel Guimarães, ob. cit., pags. 107/112).",

    # 2 na mesma
    # "Os potenciais destinatários deste regime são as companhias de seguros, empresas de transporte, bancos, empresas de fornecimento de água, energia eléctrica ou gás, empresas que se dedicam à transmissão de bens, de maquinaria, de automóveis, de electrodomésticos, etc. (v. António Pinto Monteiro, Contratos de Adesão, pag. 740, e Antunes Varela, Direito das Obrigações, vol. 1, pag. 262 )."

    # "se o cliente decidir contratar, terá de se sujeitar às cláusulas previamente determinadas por outrem, no exercício de um law making power de que este, de facto, desfruta, limitando-se aquele, pois, a aderir a um modelo prefixado\" (cfr. António Pinto Monteiro, Cláusula Penal e Indemnização, pag. 748;Meneses Cordeiro, Direito das Obrigações, pags. 96 e sgs;Vaz Serra, Obrigações, Ideias Preliminares, pags. 162 e sgs;Antunes Varela, Das Obrigações em Geral;Almeida Costa, Direito das Obrigações, pags. 196 e sgs;Mota Pinto, Contratos de Adesão, Revista de Direito e de Estudos Sociais, pags. 119 e sgs.).",

    # "mesmo Autor em BMJ n. 83, pag. 69 e segs. António Pinto Monteiro (\"Cláusulas Limitativas e de Exclusão da Responsabilidade \", pag. 85 nota 164 e \"Clausula Penal e Indemnização, pag. 31, nota 77)."

    #Weird
    "Fernando Andrade Ires de Lima/João de Matos Antunes Varela, Código Civil Anotado , Vol. III, Coimbra, Coimbra Editora, 1987, pp.378 e ss. Mais recentemente, a propósito da legitimidade do alienante, demandado numa ação de preferência, para recorrer de acórdão que julgou procedente a ação, conforme o acórdão do Supremo Tribunal de Justiça de 19 de junho de 2019 (Abrantes Geraldes), proc. n.º 1274/15.8T8FAR.E1.S1"
]


# new_sentence = "Maria Guimarães, ob. cit., págs. 107 / 112)."


def grammaering(new_sentence):
    # new_sentence = new_sentence.replace('á', 'a')
    # new_sentence = new_sentence.replace('é', 'e')
    # new_sentence = new_sentence.replace('í', 'i')
    # new_sentence = new_sentence.replace('ó', 'o')
    # new_sentence = new_sentence.replace('ú', 'u')
    # new_sentence = new_sentence.replace('ã', 'a')
    # new_sentence = new_sentence.replace('à', 'a')
    # new_sentence = new_sentence.replace('ê', 'e')
    new_sentence = " / ".join([part.strip() for part in new_sentence.split("/")])
    new_sentence = ". ".join([part.strip() for part in new_sentence.split(".")])
    new_sentence = new_sentence.lower()

    tagged_sentence = unigram_tagger.tag(nltk.word_tokenize(new_sentence))

# TODO: Add Year and Editor as Other

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

    print(tagged_sentence)
    lista_sem_none = []

    for i, tagTuple in enumerate(tagged_sentence):
        if tagTuple[1] is None:
            tagTuple = (tagTuple[0], 'N')
        tagged_sentence[i] = tagTuple

    grammar = r"""
        NOME: {<NPROP2>+(<PREP>?<NPROP2>)+}
        PAG_DOT: {<PAG><PONT>?}
        VOL_DOT: {<VOL><PONT>?}
        NOT_DOT: {<NOT><PONT>?}
        VOLS: {<VOL_DOT><NUM>((<PUNC>|<KC>)<NUM>)*}
        PAGS: {<PAG_DOT><NUM>((<PUNC>|<KC>)<NUM>)*(<KC><SGS>)?}
        NOTS: {<NOT_DOT><NUM>((<PUNC>|<KC>)<NUM>)*(<KC><SGS>)?}
        REF: {<NOME><.*>{3,}?((<PAGS><PUNC><NOTS>)|<SEP>|(<PAGS>(<SEP>|<PONT>|<PUNC>?<KC>)))} 
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
    print(result)
    reference = []

    for subtree in result.subtrees():
        if subtree.label() == "REF":
            # print(subtree)
            # autor_flag = False
            for subtree2 in subtree.subtrees():
                if subtree2.label() == "NOME":
                    author_names = []
                    for leaf in subtree2.leaves():
                        author_names.append(leaf[0])
                    reference.append("Autor: " + capitalizePhrase(" ".join(author_names)))
                    # autor_flag = True
                elif subtree2.label() == 'VOLS':
                    vols = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            vol = leaf[0]
                            if not leaf[0].isdigit():
                                vol = leaf[0].upper()
                            vols.append(vol)
                    reference.append("Volumes: [" + ', '.join(vols) + "]")
                elif subtree2.label() == 'PAGS':
                    pags = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            pags.append(leaf[0])
                        if (leaf[1] == 'SGS'):
                            pags.append('+')
                    reference.append("Páginas: [" + ', '.join(pags) + "]")
                elif subtree2.label() == 'NOTS':
                    notes = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            notes.append(leaf[0])
                        if (leaf[1] == 'SGS'):
                            notes.append('+')
                    reference.append("Notas: [" + ', '.join(notes) + "]")
            reference = otherReferenceParts(subtree, reference)
            reference.append("-----##------")

    for piece in reference:
        print(piece)


def otherReferenceParts(subtreeOriginal, reference):
    flag = False
    book = ""
    for subtree in subtreeOriginal:
        if not isinstance(subtree, Tree):
            if subtree[1] == 'PUNC' and subtree[0] == "," and book != "":  # End of part
                book = capitalizePhrase(book).strip(" ")
                if not flag: # Titu
                    flag = True
                    book = "Obra: " + book
                elif book.isdigit() and  1800 < int(book) < 2100:
                    book = "Ano: " + book
                elif "Editor" in book or "Editora" in book:
                    book = "Editora: " + book
                else:
                    book = "Outro: " + book
                reference.append(book)
                book = ""
            elif subtree[1] != 'SEP' and subtree[1] != 'PUNC' and subtree[1] != 'PONT':
                book = book + subtree[0] + " "
        # elif subtree.label() == "NOME":
            # autor_flag = True  # Salta o 1º
        elif (subtree.label() == 'VOLS' or subtree.label() == 'VOL_DOT' or
              subtree.label() == 'PAGS' or subtree.label() == 'PAG_DOT' or
              subtree.label() == 'NOTS' or subtree.label() == 'NOT_DOT' or
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

    # try:
    #     print("Autor: ", autor)
    #     print("Volumes: ", vols)
    #     print("Páginas: ", pags)
    # except NameError:
    #     print("Não foi possível extrair as informações da frase.")
    # result.draw()

for sentence in new_sentences:
    grammaering(sentence)