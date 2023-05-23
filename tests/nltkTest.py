import nltk
from nltk import Tree
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

new_sentences = [
    # "Mas também pelo seu destino, dependente das vicissitudes daqueles tipos contratuais aquele daquele daquela, págs. (Maria Guimarães, ob. cit., pags. 107 / 112).",

#falta adicionar "e" como separador de paginas
# "Tais categorias, no entanto, além de não serem perfeitamente definidas, têm conexões entre si, o que significa que às seis funções apontadas, eventualmente subjacentes à emissão de um \"cartão de plástico\", não correspondem, necessariamente seis cartões distintos, sendo comum a acumulação de várias funções no mesmo cartão (cfr. Maria Raquel Guimarães, As transferências Electrónicas de Fundos e os Cartões de Débito, Almedina, 1999, pags. 55, 58, 63 e 64 ).",

#falta adicionar qualquer digito >99
# "se o cliente decidir contratar, terá de se sujeitar às cláusulas previamente determinadas por outrem, no exercício de um law making power de que este, de facto, desfruta, limitando-se aquele, pois, a aderir a um modelo prefixado\" (cfr. António Pinto Monteiro, Cláusula Penal e Indemnização, pag. 748;",

#talvez seja o anterior e "/" como separador de digitos
# "Segundo outros - e é este o entendimento que reputamos mais acertado -, trata-se de um contrato acessório instrumental, em relação ao contrato de depósito bancário ou ao de abertura de crédito em conta corrente, acessoriedade revelada não apenas pela função do próprio contrato, mas também pelo seu destino, dependente das vicissitudes daqueles tipos contratuais (Maria Raquel Guimarães, ob. cit., pags. 107/112).",

#2 na mesma
# "Os potenciais destinatários deste regime são as companhias de seguros, empresas de transporte, bancos, empresas de fornecimento de água, energia eléctrica ou gás, empresas que se dedicam à transmissão de bens, de maquinaria, de automóveis, de electrodomésticos, etc. (v. António Pinto Monteiro, Contratos de Adesão, pag. 740, e Antunes Varela, Direito das Obrigações, vol. 1, pag. 262 )."

"se o cliente decidir contratar, terá de se sujeitar às cláusulas previamente determinadas por outrem, no exercício de um law making power de que este, de facto, desfruta, limitando-se aquele, pois, a aderir a um modelo prefixado\" (cfr. António Pinto Monteiro, Cláusula Penal e Indemnização, pag. 748;Meneses Cordeiro, Direito das Obrigações, pags. 96 e sgs;Vaz Serra, Obrigações, Ideias Preliminares, pags. 162 e sgs;Antunes Varela, Das Obrigações em Geral;Almeida Costa, Direito das Obrigações, pags. 196 e sgs;Mota Pinto, Contratos de Adesão, Revista de Direito e de Estudos Sociais, pags. 119 e sgs.).",

# "mesmo Autor em BMJ n. 83, pag. 69 e segs. António Pinto Monteiro (\"Cláusulas Limitativas e de Exclusão da Responsabilidade \", pag. 85 nota 164 e \"Clausula Penal e Indemnização, pag. 31, nota 77)."

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
    tagged_sentence = unigram_tagger.tag(nltk.word_tokenize(new_sentence))

    for tuples in word_tag_list:
        for i, tagTuple in enumerate(tagged_sentence):
            if tuples[0] == tagTuple[0] and tuples[1] != tagTuple[1]:
                tagged_sentence[i] = tuples
                continue

    for i, tagTuple in enumerate(tagged_sentence):
        if tagTuple[0].isdigit():
            tagged_sentence[i] = (tagTuple[0], 'NUM')


    print(tagged_sentence)
    lista_sem_none=[]
    for i, tagTuple in enumerate(tagged_sentence):
            if tagTuple[1] is not None:
                lista_sem_none.append(tagTuple)
            else:
                tagTuple = (tagTuple[0], 'N')
                lista_sem_none.append(tagTuple)
                # print(f"Encontrado None em: {tupla[0]}")
    tagged_sentence = lista_sem_none
    #print(tagged_sentence)

    grammar = r"""
        NOME: {(<NPROP>){2,}}
        PAG_DOT: {<PAG><PUNC>?}
        VOL_DOT: {<VOL><PUNC>?}
        VOLS: {<VOL_DOT><NUM>((<PUNC>|<KC>)<NUM>)*}
        PAGS: {<PAG_DOT><NUM>((<PUNC>|<KC>)<NUM>)*(<KC><SGS>)?}
        OB_CIT: {<NOME><PUNC>*<NOME><PUNC>*<PAGS>}
        REF: {<NOME><.*>*?(<PAGS>|<SEP>)} 
    """
    #REF: {<NOME><.*>*<PAGS>}
    #REF: {<NOME><[^PAGS].*>*<PAGS>}
    # LIVRO: {<PUNC><.*>+?<PUNC><PAGS>}
    #         }<PAGS|NOME>{

    # # Criando o objeto RegexpParser com as regras definidas
    parser = nltk.RegexpParser(grammar)
    #print(parser)

    # tagged_sentence = [( "money" ,"NN"),("market", "NN"),("fund", "NN")]
    result = parser.parse(tagged_sentence)
    print(result)

    autor = ""
    pags = []
    vols = []
    for subtree in result.subtrees():
        # if subtree.label() == 'PAGS':
        #     for leaf in subtree.leaves():
        #         if(leaf[1] == "NUM"):
        #             pags.append(leaf[0])
        # if subtree.label() == 'VOLS':
        #     for leaf in subtree.leaves():
        #         if(leaf[1] == "NUM"):
        #             vols.append(leaf[0])
        # if subtree.label() == "NOME":
        #     author_names = []
        #     for leaf in subtree.leaves():
        #         author_names.append(leaf[0])
        #     autor = " ".join(author_names)
        # if subtree.label() == "LIVRO":
        #     print("Found livro!")
        if subtree.label() == "REF":
            # print(subtree)
            autor_flag = False
            for subtree2 in subtree.subtrees():
                if subtree2.label() == "NOME" and not autor_flag:
                    author_names = []
                    for leaf in subtree2.leaves():
                        author_names.append(leaf[0])
                    print("Autor: " + (" ".join(author_names)))
                    autor_flag = True
                    print("Obra: " + getBook(subtree))
                if subtree2.label() == 'VOLS':
                    vols = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            vols.append(leaf[0])
                    print("Volumes: ", vols)
                    vols = []
                if subtree2.label() == 'PAGS':
                    pags = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            vols.append(leaf[0])
                        if (leaf[1] == 'SGS'):
                            vols.append('+')
                    print("Páginas: ", vols)
                    vols = []
            print("-----##------")

def getBook(subtreeOriginal):
    autor_flag = False
    book = ""
    for subtree in subtreeOriginal:
        if not isinstance(subtree, Tree):
            if subtree[1] != 'PUNC' and subtree[1] != 'SEP':
                book = book + subtree[0] + " "
        elif subtree.label() == "NOME" and not autor_flag:
            autor_flag = True #Salta o 1º
        elif subtree.label() == 'VOLS' or subtree.label() == 'VOL_DOT':
            vols = []
        elif subtree.label() == 'PAGS' or subtree.label() == 'PAG_DOT':
            pags = []
        elif subtree.label() == 'PUNC' or subtree.label() == 'REF':
            punc = []
        else:
            book = book + tree_to_str(subtree)
    return book

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