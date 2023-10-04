import spacy
import pandas as pd
from spacy.matcher import Matcher
from spacy.lang.pt.examples import sentences

# https://towardsdatascience.com/how-to-extract-structured-information-from-a-text-through-python-spacy-749b311161e



# text = "This statement is true, according to Charles Darwin in \"The Evolution of the World\""

with open('../unmarkedTestFiles/examples.txt', 'r', encoding='utf-8') as f:
    text = [line for line in f.readlines()]

df = pd.DataFrame(text,columns=['text'])
df.head()

text = df['text'][0]

nlp = spacy.load("pt_core_news_sm")
doc = nlp(text)

features = []
for token in doc:
    features.append({'token' : token.text, 'pos' : token.pos_})

fdf = pd.DataFrame(features)
fdf.head(len(fdf))

# Definir pattern
first_tokens_author = ['segundo', '(']
last_tokens_author = ['em', ',']
pattern_father = [[{'LOWER' : {'IN' : first_tokens_author}},
           {'POS':'PROPN', 'OP' : '+'},
           {'LOWER': {'IN' : last_tokens_author}} ]]


def get_author(x):
    doc = nlp(x)
    matcher = Matcher(nlp.vocab)
    matcher.add("matching_father", pattern_father)
    matches = matcher(doc)
    sub_text = ''
    if (len(matches) > 0):
        span = doc[matches[0][1]:matches[0][2]]
        sub_text = span.text
    tokens = sub_text.split(' ')

    name, surname = tokens[1:-1]
    return name, surname

new_columns = ['name','surname']
# for n,col in enumerate(new_columns):
    # df[col] = df['text'].apply(lambda x: get_author(x)).apply(lambda x: x[n])

print(get_author(df['text'][0]))
print(get_author(df['text'][1]))

# fdf = pd.DataFrame(features)
# fdf.head(len(fdf))
#
# print(fdf)

# print(doc.text)
# for token in doc:
#     print(token.text, token.pos_, token.dep_)
#
# nlp = spacy.load("pt_core_news_lg")
#
# doc = nlp(text)
# sentences = list(doc.sents)
# sentence = (sentences[0])
#
# print(doc)
# chunks = list(doc.noun_chunks)
# for chunk in chunks:
#     print(chunk)
# for token in sentence:
#     print(str(token) + " " + str(token.pos_))