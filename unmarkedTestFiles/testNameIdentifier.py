from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

model_name='dslim/bert-large-NER'
# model_name = "neuralmind/bert-large-portuguese-cased"
bert_tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModelForTokenClassification.from_pretrained(model_name)

nlp = pipeline('ner', model=bert_model, tokenizer=bert_tokenizer)
# names_string = "Hi there Jon Jones Jon Jones Jr. Jon Paul Jones John D. Jones"
names_string = "Olá, tudo bem Jão Joanes João Joanes Jr. e fundo de Clero da Justiça, Jacinto Paulo Joanes Miguel D. João"

ner_list = nlp(names_string)
print(ner_list)

this_name = []
all_names_list_tmp = []

for ner_dict in ner_list:
    if ner_dict['entity'] == 'B-PER':
        if len(this_name) == 0:
            this_name.append(ner_dict['word'])
        else:
            all_names_list_tmp.append([this_name])
            this_name = []
            this_name.append(ner_dict['word'])
    elif ner_dict['entity'] == 'I-PER':
        this_name.append(ner_dict['word'])

all_names_list_tmp.append([this_name])

print(all_names_list_tmp)

final_name_list = []
for name_list in all_names_list_tmp:
    full_name = ' '.join(name_list[0]).replace(' ##', '').replace(' .', '.')
    final_name_list.append([full_name])

print(final_name_list)