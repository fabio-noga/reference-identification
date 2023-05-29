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
    # "Fernando Andrade Ires de Lima/João de Matos Antunes Varela, Código Civil Anotado , Vol. III, Coimbra, Coimbra Editora, 1987, pp.378 e ss. Mais recentemente, a propósito da legitimidade do alienante, demandado numa ação de preferência, para recorrer de acórdão que julgou procedente a ação, conforme o acórdão do Supremo Tribunal de Justiça de 19 de junho de 2019 (Abrantes Geraldes), proc. n.º 1274/15.8T8FAR.E1.S1"
    #
    # "O phishing (do inglês fishing «pesca») pressupõe uma fraude electrónica caracterizada por tentativas de adquirir dados pessoais, através do envio de e-mails com uma pretensa proveniência da entidade bancária do receptor, por exemplo, a pedir determinados elementos confidenciais (número de conta, número de contrato, número de cartão de contribuinte ou qualquer outra informação pessoal), por forma a que este ao abri-los e ao fornecer as informações solicitadas e/ou ao clicar em links para outras páginas ou imagens, ou ao descarregar eventuais arquivos ali contidos, poderá estar a proporcionar o furto de informações bancárias e a sua utilização subsequente, cfr Pedro Verdelho, in Phishing e outras formas de defraudação nas redes de comunicação, in Direito da Sociedade De Informação, Volume VIII, 407/419: Maria Raquel Guimarães, in Cadernos de Direito Privado, nº41, Janeiro/Março de 2013;"
    #
    # "Tal como a posse relevante para usucapião (a par de outros requisitos, deve ser pública), também a oposição exercida pelo detentor precário tem de ser ostensiva em relação àquele em nome de quem possuía, sendo que, como observa Orlando de Carvalho, in \"Introdução à Posse\", RLJ, Ano 123°, nº3792 (1990-1991), a respeito da posse pública, esta não deixa de ser pública quando não é propriamente conhecida de toda a gente, é-o acima de tudo, quando é conhecida do interessado directo ou indirecto - \"trata-se de uma relação mais com o próprio interessado do que com o público em geral\"».",

    #João Calvão da Silva in \"Sinal de Contrato Promessa\" , Almedina, 2007, 12ª edição, a páginas 79 a 80
    # "(Neste sentido, vide João Calvão da Silva in \"Sinal de Contrato Promessa\" , Almedina, 2007, 12ª edição, a páginas 79 a 80, onde refere: \"A admitir-se a validade da cláusula pela qual o promitente comprador renuncia antecipadamente ao direito de arguir a nulidade estaria aberta a porta para com a maior das facilidades os promitentes vendedores incluirem nas promessas uma cláusula do estilo em que as partes declarariam prescindir das formalidades impostas pelo artigo 410º, nº 3, renunciando à invocação da respectiva omissão, e assim sabotar o sentido e fim de uma norma de protecção da parte mais fraca, o consumidor.",

    # "Perfilhando o mesmo entendimento, vide o acórdão do Supremo Tribunal de Justiça de 5 de Julho de 2007 (relator Oliveira Rocha), proferido no processo nº 07B2027, publicado in www.dgsi.pt. Em sentido oposto, vide Fernando Gravato de Morais, in \"Contratos-Promessa em Geral.Contratos-Promessa em Especial\" , Almedina, Abril de 2009, a páginas 278 a 279, quando refere: \"Quanto ao facto de os promitentes prescindirem do reconhecimento presencial das assinaturas, renunciando assim à invocação da nulidade do contrato promessa, cremos que nada obsta a que tal aconteça.",
]


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
    # phrase = ". ".join([part.strip() for part in phrase.split(".")])
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
        NOME: {<NPROP2>+(<NPROP>?<PREP>?<NPROP2>)+}
        PAG_DOT: {<PAG><PONT>?}
        VOL_DOT: {<VOL><PONT>?}
        NOT_DOT: {<NOT><PONT>?}
        VOLS: {<VOL_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*}
        PAGS: {<PAG_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*(<KC><SGS>)?}
        NOTS: {<NOT_DOT><NUM>((<PUNC>|<KC>|<ART>)<NUM>)*(<KC><SGS>)?}
        REF: {<NOME><IN>?<.*>+?(<PAGS>(<PUNC><NOTS>)?)(<SEP>|<PONT>|<PUNC>|<KC>)} 
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
            reference = {}
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
                            if "autor" in reference:
                                reference["autor"].append(name)
                            else:
                                reference["autor"] = [name]
                            autor_flag = 1
                            break
                    if autor_flag == 0: #Nome não encontrado na base de dados
                        autor_flag = 2
                        bad_author_counter += 1
                        continue
                elif subtree2.label() == 'VOLS':
                    vols = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            vol = leaf[0]
                            if not leaf[0].isdigit():
                                vol = leaf[0].upper()
                            vols.append(vol)
                    # reference.append("Volumes: [" + ', '.join(vols) + "]")
                    reference["vol"] = vols
                elif subtree2.label() == 'PAGS':
                    pags = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            pags.append(leaf[0])
                        if (leaf[1] == 'SGS'):
                            pags.append('+')
                    # reference.append("Páginas: [" + ', '.join(pags) + "]")
                    reference["pag"] = pags
                elif subtree2.label() == 'NOTS':
                    notes = []
                    for leaf in subtree2.leaves():
                        if (leaf[1] == "NUM"):
                            notes.append(leaf[0])
                        if (leaf[1] == 'SGS'):
                            notes.append('+')
                    # reference.append("Notas: [" + ', '.join(notes) + "]")
                    reference["notes"] = notes
            if autor_flag == 2:  # Author not in DB
                continue
            reference = extractOtherReferenceParts(subtree, reference, bad_author_counter)
            if reference != {}:
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
            if subtree[1] == 'PUNC' and subtree[0] == "," and book != "":  # End of part
                book = capitalizePhrase(book).strip(" ")
                if bad_author_counter != 0:
                    bad_author_counter -= 1
                    book = ""
                elif len(book) <= 1:
                    book = ""
                else:
                    if not flag: # Titu
                        flag = True
                        reference["obra"] = book
                        # book = "Obra: " + book
                    elif book.isdigit() and  1800 < int(book) < 2100:
                        reference["ano"] = book
                        # book = "Ano: " + book
                    elif "Editor" in book or "Editora" in book:
                        reference["editora"] = book
                        # book = "Editora: " + book
                    elif "Edição" in book:
                        reference["edicao"] = book
                        # book = "Edição: " + book
                    else:
                        if "outro" in reference:
                            reference["outro"].append(book)
                        else:
                            reference["outro"] = [book]
                        # book = "Outro: " + book
                    # reference.append(book)
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

    # try:
    #     print("Autor: ", autor)
    #     print("Volumes: ", vols)
    #     print("Páginas: ", pags)
    # except NameError:
    #     print("Não foi possível extrair as informações da frase.")
    # result.draw()

for sentence in new_sentences:
    print(extractQuoteDataFromPhrase(sentence))


def getQuoteJsonAsIEEE(quote):
    reference = ""
    for i, author in enumerate(quote["autor"]):
        names = author.split()
        name = names[len(names)-1] + ", " + " ".join(names[:-1])
        reference += name
        if i != len(quote["autor"])-1:
            reference += "; "
    if "ano" in quote:
        reference += ' (' + quote["ano"] + ')'
    reference += '. "' + quote["obra"] + '"'
    if "edicao" in quote:
        reference += ", " + quote["edicao"]
    if "pag" in quote:
        reference += ", "
        if len(quote["pag"]) == 1:
            reference += "pág. " + quote["pag"][0]
        else:
            reference += "págs. "
            for i, pag in enumerate(quote["pag"]):
                if pag == "+":
                    reference += "sgs"
                else:
                    reference += pag
                if i < len(quote["pag"])-2:
                    reference += ", "
                elif i == len(quote["pag"])-2:
                    reference += " e "
    if "vol" in quote:
        reference += ", "
        if len(quote["vol"]) == 1:
            reference += "vol. " + quote["vol"][0]
        else:
            reference += "vols. "
            for i, pag in enumerate(quote["vol"]):
                if pag == "+":
                    reference += "sgs"
                else:
                    reference += pag
                if i < len(quote["vol"])-2:
                    reference += ", "
                elif i == len(quote["vol"])-2:
                    reference += " e "
    if "notes" in quote:
        reference += ", "
        if len(quote["notes"]) == 1:
            reference += "note " + quote["notes"][0]
        else:
            reference += "notes "
            for i, pag in enumerate(quote["notes"]):
                if pag == "+":
                    reference += "sgs"
                else:
                    reference += pag
                if i < len(quote["notes"])-2:
                    reference += ", "
                elif i == len(quote["notes"])-2:
                    reference += " e "
    return reference


quotes = [{'autor': ['João Calvão da Silva'], 'pag': ['79', '80'], 'obra': "`` Sinal De Contrato Promessa ''", 'outro': ['Almedina'], 'ano': '2007', 'edicao': '12ª Edição'}, {'autor': ['Fernando de Gravato Morais'], 'pag': ['278', '279'], 'obra': "`` Contratos-promessa Em Geral.contratos-promessa Em Especial ''", 'outro': ['Almedina', 'Abril De 2009']}]

for quote in quotes:
    getQuoteJsonAsIEEE(quote)