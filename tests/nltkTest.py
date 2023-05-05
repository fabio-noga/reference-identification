import nltk
from nltk.corpus import mac_morpho
from nltk.tokenize import word_tokenize

# Train the tagger on the tagged sentences in the corpus
input_file = "./mac_morpho_custom.txt"

custom_words = [("/", "PUNC")]

with open(input_file, "r", encoding='utf-8') as f:
    lines = f.readlines()
    word_tag_list = [(line.split()[0], line.split()[1]) for line in lines]

custom_words = custom_words + word_tag_list
custom_words = [custom_words]


# mac_morpho_tagged_words = mac_morpho.tagged_words() + custom_words
# sentences = mac_morpho.tagged_sents()
# sentences.append(custom_words)
sentences = mac_morpho.tagged_sents() + custom_words
unigram_tagger = nltk.UnigramTagger(sentences)
print("Passou 1")
#
# # Tag a new sentence
# new_sentence = "Eu amo comer pizza"
new_sentence = "Mas também pelo seu destino, dependente das vicissitudes daqueles tipos contratuais aquele daquele daquela, págs. (Maria Guimarães, ob. cit., pags. 107 / 112)."
new_sentence = "Tais categorias, no entanto, além de não serem perfeitamente definidas, têm conexões entre si, o que significa que às seis funções apontadas, eventualmente subjacentes à emissão de um \"cartão de plástico\", não correspondem, necessariamente seis cartões distintos, sendo comum a acumulação de várias funções no mesmo cartão (cfr. Maria Raquel Guimarães, As transferências Electrónicas de Fundos e os Cartões de Débito, Almedina, 1999, pags. 55, 58, 63 e 64 )."
# new_sentence = "Maria Guimarães, ob. cit., págs. 107 / 112)."

tagged_sentence = unigram_tagger.tag(nltk.word_tokenize(new_sentence))

for tuples in word_tag_list:
    for i, tagTuple in enumerate(tagged_sentence):
        if tuples[0] == tagTuple[0] and tuples[1] != tagTuple[1]:
            tagged_sentence[i] = tuples


print(tagged_sentence)
lista_sem_none=[]
for tupla in tagged_sentence:
        if tupla[1] is not None:
            lista_sem_none.append(tupla)
        else:
            print(f"Encontrado None em: {tupla[0]}")
tagged_sentence = lista_sem_none
#print(tagged_sentence)

grammar = r"""
    NOME: {(<NPROP>){2,}}
    PAG_DOT: {<PAG><PUNC>?}
    PAGS: {<PAG_DOT><NUM>(<PUNC><NUM>)*}
    OB_CIT: {<NOME><PUNC>*<NOME><PUNC>*<PAGS>}
"""

# # Criando o objeto RegexpParser com as regras definidas
parser = nltk.RegexpParser(grammar)
#print(parser)

# tagged_sentence = [( "money" ,"NN"),("market", "NN"),("fund", "NN")]
result = parser.parse(tagged_sentence)
print(result)

autor = ""
pags = []
for subtree in result.subtrees():
    if subtree.label() == 'PAGS':
        for leaf in subtree.leaves():
            if(leaf[1] == "NUM"):
                pags.append(leaf[0])
    if subtree.label() == "NOME":
        author_names = []
        for leaf in subtree.leaves():
            author_names.append(leaf[0])
        autor = " ".join(author_names)

try:
    print("Autor: ", autor)
    print("Páginas: ", pags)
except NameError:
    print("Não foi possível extrair as informações da frase.")
# result.draw()





# tokens = word_tokenize(new_sentence, language='portuguese')
#
# # Realizando o POS tagging
# pos_tagged = nltk.pos_tag(tokens, lang='por')
#
# # Aplicando o RegexpParser na lista de tuplas com as tags POS
# tree = parser.parse(pos_tagged)
#
# # Percorrendo as subárvores para encontrar os grupos que correspondem à gramática definida
# for subtree in tree.subtrees():
#     if subtree.label() == 'OB_CIT':
#         for leaf in subtree.leaves():
#             if leaf[1].startswith('NPROP'):
#                 autor = leaf[0]
#             elif leaf[1].startswith('NUM'):
#                 pags = leaf[0]
#
# print("Autor: ", autor)
# print("Páginas: ", pags)