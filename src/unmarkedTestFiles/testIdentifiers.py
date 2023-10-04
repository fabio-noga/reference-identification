import os
import re
import time

import nltk

from src import TextExtraction, Config

# from unmarkedTestFiles import usingBertToQuotes

input_file = "../assets/investigadores_completo.txt"

names = []
with open(input_file, "r", encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        names.append(line)


def identiftByGrammar(phrase):

    # data = []
    # for i, phrase in enumerate(tokenizer):

    bad_author_counter = 0
    phrase = " / ".join([part.strip() for part in phrase.split("/")])
    phrase = ". ".join([part.strip() for part in phrase.split(".")])
    phrase = " - ".join([part.strip() for part in phrase.split("-")])
    originalPhrase = phrase
    phrase = phrase.lower()

    tagged_sentence = TextExtraction.unigram_tagger.tag(nltk.word_tokenize(phrase))

    # Replace tags for custom ones
    for tuples in TextExtraction.word_tag_list:
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
        print("first")
        return False
    elif ("#Referências#" in phrase):
        print("second")
        return False
    elif (re.compile(r"\[\d+\]").search(phrase)):
        print(phrase)
        return False

    for subtree in result.subtrees():
        if subtree.label() == "REF":
            return "TP"
    return "TN"

def identifyBy2Efforts(phrase):

    # data = []
    # for i, phrase in enumerate(tokenizer):

    bad_author_counter = 0
    phrase = " / ".join([part.strip() for part in phrase.split("/")])
    phrase = ". ".join([part.strip() for part in phrase.split(".")])
    phrase = " - ".join([part.strip() for part in phrase.split("-")])
    originalPhrase = phrase
    phrase = phrase.lower()

    tagged_sentence = TextExtraction.unigram_tagger.tag(nltk.word_tokenize(phrase))

    # Replace tags for custom ones
    for tuples in TextExtraction.word_tag_list:
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
        print("first")
        return False
    elif ("#Referências#" in phrase):
        print("second")
        return False
    elif (re.compile(r"\[\d+\]").search(phrase)):
        print(phrase)
        return False

    for subtree in result.subtrees():
        if subtree.label() == "REF":

            lowerPhrase = phrase.lower()
            # characters_to_replace = [".", ";", ")", "(", ":", "-", "\"", ",", "'", "/"]
            clean_phrase = lowerPhrase.replace(".", "").replace(".", "").replace(",", "").replace(";", "").replace("(",
                                                                                                                   "").replace(
                ")", "").replace(":", "").replace("\"", "").replace("'", "")
            clean_phrase = clean_phrase.replace("/", " ").replace("-", " ")
            words = clean_phrase.split(" ")
            for name in names:
                name_words = name.split()
                if all(word.lower() in words for word in name_words):
                    # if name in phrase:
                    return "TP"
    return "TN"

def identifyByPatternThenName(phrase):

    data = []


    flag = False
    if (len(phrase) < 5):
        print(phrase)
        return False
    elif ("#Referências#" in phrase):
        print(phrase)
        return False

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
            for name in names:
                name_words = name.split()
                if all(word.lower() in words for word in name_words):
                    # if name in phrase:
                    return "TP"
    return "TN"

# saved_model1 = torch.load("tokenizer/model.bin")
# saved_model = "./tokenizer/model.bin"
# saved_model2 = "./tokenizer/"
# config_file = "./tokenizer/tokenizer_config.json"
# model = torch.nn.Linear(5, 2)
# model.load_state_dict(torch.load(saved_model))
#
# tokenizer = BertTokenizer.from_pretrained(
#     saved_model2,
#     local_files_only=True,
#     do_lower_case=True,
# )
#
# print("first")
#
# class Model(nn.Module):
#     def __init__(self, n_input_features):
#         super(Model, self).__init__()
#         self.linear = nn.Linear(n_input_features, 1)
#
#     def forward(self, x):
#         y_pred = torch.sigmoid(self.linear(x))
#         return y_pred
#
# model = Model(n_input_features=6)
#
# learning_rate = 0.01
# optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
#
# checkpoint = {
# "epoch": 90,
# "model_state": model.state_dict(),
# "optim_state": optimizer.state_dict()
# }
# print(optimizer.state_dict())
# FILE = "tokenizer/model.bin"
# torch.save(checkpoint, FILE)
#
# model = Model(n_input_features=6)
# optimizer = torch.optim.SGD(model.parameters(), lr=0)
#
# checkpoint = torch.load(FILE)
# model.load_state_dict(checkpoint['model_state'])
# optimizer.load_state_dict(checkpoint['optim_state'])
# epoch = checkpoint['epoch']
#
# model = BertForSequenceClassification.from_pretrained(
#     torch.load(FILE),
#     config=config_file,
#     local_files_only=True,
#     num_labels=2,
#     output_attentions=False,
#     output_hidden_states=False,
#     ignore_mismatched_sizes=True,
# )
# model = BertForSequenceClassification.from_pretrained(
#     f'{dirname(__file__)}/tokenizer/model.bin/',
#     config=config_file,
#     local_files_only=True,
#     num_labels=2,
#     output_attentions=False,
#     output_hidden_states=False,
#     ignore_mismatched_sizes=True,
# )
# print("second")

# def identifyByBERT(phrase):
    #
    #
    # # We need Token IDs and Attention Mask for inference on the new sentence
    # test_ids = []
    # test_attention_mask = []
    # # Apply the tokenizer
    # encoding = usingBertToQuotes.preprocessing(phrase, usingBertToQuotes.tokenizer)
    #
    # # Extract IDs and Attention Mask
    # test_ids.append(encoding['input_ids'])
    # test_attention_mask.append(encoding['attention_mask'])
    # test_ids = torch.cat(test_ids, dim=0)
    # test_attention_mask = torch.cat(test_attention_mask, dim=0)
    #
    # # Forward pass, calculate logit predictions
    # with torch.no_grad():
    #     output = usingBertToQuotes.model(test_ids.to(usingBertToQuotes.device),
    #                                      token_type_ids=None, attention_mask=test_attention_mask.to(usingBertToQuotes.device))
    #
    # prediction = "TP" \
    #     if np.argmax(output.logits.cpu().numpy()).flatten().item() == 1 \
    #     else "TN"
    #
    # # print('Input Sentence: ', phrase)
    # # print('Predicted Class: ', prediction)
    # return prediction


def verifyAll():
    start_time = time.time()
    time_after_block_prev = start_time
    prevTime = time.time()
    # os.listdir("doc_json")
    folder = os.path.join("../..", "assets", "validated_quotes")
    files = os.listdir(folder)
    files.sort()
    for file in files:
        TN = 0
        TP = 0
        FN = 0
        FP = 0
        # try:
        title = file
        valid_data = []
        with open(os.path.join(folder, file), "r", encoding='utf-8') as validated_file:
            for line in validated_file:
                if not line.startswith("TN") and not line.startswith("TP") and \
                        not line.startswith("FN") and not line.startswith("FP"): continue
                lineArray = line.split("\t")
                lineLength = len(lineArray)-1
                a = identifyByPatternThenName(lineArray[lineLength])
                # a = identiftByGrammar(lineArray[lineLength])
                # a = identifyByBERT(lineArray[lineLength])
                a = identifyBy2Efforts(lineArray[lineLength])
                if (lineArray[0] == "TN" or lineArray[0] == "FP") and a == "TN": TN += 1
                elif (lineArray[0] == "TN" or lineArray[0] == "FP") and a == "TP":
                    # print(f"{lineArray[0]} {lineArray[lineLength]}")
                    FP += 1
                elif (lineArray[0] == "TP" or lineArray[0] == "FN") and a == "TN":
                    # print(f"{lineArray[0]} {a} {lineArray[lineLength]}")
                    FN += 1
                elif (lineArray[0] == "TP" or lineArray[0] == "FN") and a == "TP": TP += 1
                else: print(f"{lineArray[0]} {a}")
        time_after_block_cur = time.time()
        elapsed_time_block_cur = time_after_block_cur - prevTime
        prevTime = time_after_block_cur
        # print(f"Time after code block {title}: {elapsed_time_block_cur} seconds | TN {TN} | TP {TP} | FN {FN} | FP {FP}")
        print(f"{title} {elapsed_time_block_cur} :\t{TN}\t{TP}\t{FN}\t{FP}")


        #     for i,line in enumerate(data):
        #         if i == len(valid_data) or len(valid_data[i].split("")): break
        #         if valid_data[i].strip().split("\t")[4] != line.strip().split("\t")[4]:
        #             print(valid_data[i].strip().split("\t")[4])
        #             print(line.strip().split("\t")[4])
        #             continue
        #         validated_line = valid_data[i].split("\t")[0]
        #         this_line = line.split("\t")[0]
        #         validated_line = validated_line.replace("?","")
        #         this_line = this_line.replace("?","")
        #         if not this_line.startswith("T") or not validated_line.startswith("T"): break
        #         if (validated_line == "TN" or validated_line == "FP") and this_line == "TN": TN+=1
        #         if (validated_line == "TN" or validated_line == "FP") and this_line == "TP": FP+=1
        #         if (validated_line == "TP" or validated_line == "FN") and this_line == "TN": FN+=1
        #         if (validated_line == "TP" or validated_line == "FN") and this_line == "TP": TP+=1
        # time_after_block_cur = time.time()
        # elapsed_time_block_cur = time_after_block_cur - time_after_block_prev
        # print(f"Time after code block {i+1}: {elapsed_time_block_cur} seconds | TN {TN} | TP {TP} | FN {FN} | FP {FP}")
        # time_after_block_prev = time_after_block_cur
        # # except:
        # #     print(data)
        # #     print("Error creating " + title, file=sys.stderr)
        # #     exit()
        # # print("File " + title + " created successfully")
        # # return data
        # # Utils._saveData2("quotes_verificadas", file, data)

    end_time = time.time()
    # Total elapsed time
    total_elapsed_time = end_time - start_time
    print(f"Overall elapsed time: {total_elapsed_time} seconds")


# print(identiftByGrammar("TP	ref	|Guilherme de Oliveira|	| p\. |	(Código Civil Anotado, Livro IV, Direito da Família, Coordenação de Clara Sottomayor, Almedina, 2020, pp. 444/445) A norma constante do artigo 1730.º, n.º 1, do Código Civil consagra uma regra imperativa cuja \"ratio\" reside na proteção de cada um dos cônjuges contra o risco de aproveitamento do ascendente psicológico eventualmente adquirido sobre o outro para lograr uma distribuição mais vantajosa do património [cf. Guilherme de Oliveira, \"Sobre o contrato-promessa de partilha de bens comuns (Anotação ao Acórdão da Relação de Coimbra, de 28/11/95)\", Revista de Legislação e de Jurisprudência , ano 129, 1996/7, Coimbra, Coimbra Editora, p. 286]."))
# print(identiftByGrammar("TP	ref	|Guilherme de Oliveira|	| p\. |	No entanto, como Guilherme de Oliveira também sublinha (\"Sobre o contrato-promessa de partilha..., cit., p. 286), a regra da metade visa igualmente tutelar o interesse de terceiros - os credores pessoais de cada cônjuge -, que adquiriram a legítima expectativa de que a quota de cada um dos cônjuges apresentaria um valor igualitário e, por outro lado, de que o regime de bens convencionado ou fixado por lei permaneceria inalterado."))
# print(identiftByGrammar("TP	ref	|Guilherme de Oliveira|	| p\. |	Por outra banda, tal acordo desigual poderia servir para esconder doações que o cônjuge prejudicado faz ao outro, contra o estatuído no art. 1764.º/1 do Código Civil (cfr. Guilherme de Oliveira, Manual de Direito da Família , 2.ª edição, Coimbra, Almedina, 2021, p. 219)."))
# print(identiftByGrammar("TP	ref	|Helena Mota|	| p\. |	Do mesmo modo, Rute Teixeira Pedro, \"Do exercício da autonomia privada na partilha do património comum do casal\", Autonomia e heteronomia no Direito da Família e no Direito das Sucessões , coordenação de Helena Mota e Maria Raquel Guimarães, Coimbra, Almedina, 2016, p. 354-555, dá conta que, de acordo com o entendimento formal estrito da regra da metade que tem vindo a ser seguido, resultam interditos todos os acordos que se desviem de tal regra, ainda que firmados com o objetivo \"da prossecução de um cumprimento material da igualdade entre os cônjuges no que respeita à repartição, ex post facto , das vantagens e desvantagens patrimoniais associadas à relação matrimonial dissolvida\"."))
# print(identiftByGrammar("Designa-se por contrato de conta bancária (ou abertura de conta) o acordo havido entre uma instituição bancária e um cliente « através do qual se constitui, disciplina e baliza a respectiva relação jurídica bancária », cfr Engrácia Antunes, Direito dos Contratos Comerciais, 483."))
# print(identiftByGrammar("Esta complexa figura contratual, tem sido subsumida a nível jurisprudencial e pela maior parte da doutrina na espécie negocial de depósito, tal como a mesma nos é definida pelos artigos 1185º e 1187º do CCivil, através do qual a Autora colocou à disposição do Réu o seu dinheiro e para que este o guardasse e o restituísse quando fosse exigido, constituindo esta figura um depósito irregular ao qual se aplicam as regras do mútuo, com as necessárias adaptações, cf Calvão da Silva, Direito Bancário, 2001, 347/351;"))

verifyAll()