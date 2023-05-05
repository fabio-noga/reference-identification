# import spacy
#
# nlp = spacy.load('pt_core_news_lg')
#
# texts = ["Segundo Silva (2010), o Brasil é o maior produtor de café do mundo.",
#         "O livro 'O Guarani' de José de Alencar foi publicado em 1857.",
#         "Em seu discurso de posse, Kennedy disse 'Não pergunte o que seu país pode fazer por você, pergunte o que você pode fazer por seu país'."]
#
# for text in texts:
#     doc = nlp(text)
#
#     for ent in doc.ents:
#         print(ent.text + " | " + ent.label_)
#         if ent.label_ == 'REF':
#             print(ent.text)








# First, install transformers library via pip install transformers

# from transformers import AutoTokenizer, AutoModelForTokenClassification
#
# tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-large-portuguese-cased")
# model = AutoModelForTokenClassification.from_pretrained("neuralmind/bert-large-portuguese-cased", num_labels=9)
# # tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
# # model = AutoModelForTokenClassification.from_pretrained("neuralmind/bert-base-portuguese-cased", num_labels=2)
#
# # List of phrases to check for references
# phrases = [
#     "De acordo com Santos et al. (2020), o Brasil é um país promissor.",
#     "A pesquisa realizada por Silva (2018) demonstra que...",
#     "Não existem estudos que comprovem essa afirmação."
# ]
#
# # Tokenize phrases
# tokenized_phrases = [tokenizer.encode(phrase, add_special_tokens=False) for phrase in phrases]
#
# # Identify if phrases contain references
# for i, phrase in enumerate(phrases):
#     inputs = tokenizer.encode_plus(phrase, return_tensors="pt")
#     outputs = model(inputs["input_ids"], inputs["attention_mask"])
#     predictions = outputs.logits.argmax(-1).squeeze().tolist()
#
#     # Check if the label for "B-REF" (beginning of a reference) appears in the predictions
#     if 2 in predictions:
#         print(f"Phrase {i + 1} contains a reference.")
#     else:
#         print(f"Phrase {i + 1} does not contain a reference.")


# import bertopic
# import pandas as pd
#
# # Initialize the BERTopic model with the pre-trained BERTimbau embeddings
# model = bertopic.BERTopic(language="portuguese")
#
# # Define the list of phrases to be clustered
# phrases = [
#     "De acordo com Santos et al. (2020), o Brasil é um país promissor.",
#     "A pesquisa realizada por Silva (2018) demonstra que...",
#     "Não existem estudos que comprovem essa afirmação."
# ]
#
# # Cluster the phrases using BERTopic
# topics, probs = model.fit_transform(phrases)
#
# # Convert the clusters to a dataframe
# df = pd.DataFrame({'phrase': phrases, 'topic': topics})
#
#
# # Define a function to create the IEEE-style reference
# def create_reference(phrase, topic):
#     authors = [x.strip() for x in phrase.split("(")[0].split("et al.")[0].split(",")]
#     year = [x.strip() for x in phrase.split("(")[1].split(")")[0].split(",")][0]
#     title = df[df['topic'] == topic]['phrase'].tolist()[0].split(".")[0]
#     return ", ".join(authors) + ", \"" + title + "\", " + year + "."
#
#
# # Create the IEEE-style references for each phrase
# for i, row in df.iterrows():
#     print(create_reference(row['phrase'], row['topic']))






from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch

# tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-large-portuguese-cased")
# model = AutoModelForTokenClassification.from_pretrained("neuralmind/bert-large-portuguese-cased", num_labels=3)
#
# def classify_tokens(text):
#     inputs = tokenizer(text, return_tensors="pt")
#     outputs = model(**inputs)
#     predictions = torch.argmax(outputs.logits, dim=-1)
#     return [model.config.id2label[label_id] for label_id in predictions[0].tolist()]
#
# phrases = [    "De acordo com Santos et al. (2020), o Brasil é um país promissor.",    "A pesquisa realizada por Silva (2018) demonstra que...",    "Não existem estudos que comprovem essa afirmação."]
#
# for phrase in phrases:
#     print(phrase)
#     print(classify_tokens(phrase))
#
#
# nlp = pipeline('ner', model='neuralmind/bert-base-portuguese-cased', tokenizer='neuralmind/bert-base-portuguese-cased')
#
# def has_references_or_quotes(text):
#     entities = nlp(text)
#     for entity in entities:
#         if entity['entity'] == 'I-REF' or entity['entity'] == 'I-Q':
#             return True
#     return False
#
# phrases = [
#     "De acordo com Santos et al. (2020), o Brasil é um país promissor.",
#     "A pesquisa realizada por Silva (2018) demonstra que...",
#     "Não existem estudos que comprovem essa afirmação."
# ]
#
# for phrase in phrases:
#     if has_references_or_quotes(phrase):
#         print(f"The phrase '{phrase}' contains references or quotes.")
#     else:
#         print(f"The phrase '{phrase}' does not contain references or quotes.")



# from transformers import AutoTokenizer, AutoModelForTokenClassification
#
# # Load BERTimbau tokenizer and model for token classification
# tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-large-portuguese-cased")
# model = AutoModelForTokenClassification.from_pretrained("neuralmind/bert-large-portuguese-cased", num_labels=3)
#
# # Define labels for the token classification task
# label_list = ["O", "B-REF", "I-REF", "B-QUOTE", "I-QUOTE"]
#
# # Example phrases
# phrases = [
#     "De acordo com Santos et al. (2020), o Brasil é um país promissor.",
#     "A pesquisa realizada por Silva (2018) demonstra que...",
#     "Não existem estudos que comprovem essa afirmação.",
#     "Olá, como estás?"
# ]
#
# # Tokenize and prepare input data for BERTimbau model
# inputs = tokenizer(phrases, return_tensors="pt", padding=True, truncation=True)
#
# # Run input data through BERTimbau model
# outputs = model(**inputs)
#
# # Get predicted labels from BERTimbau model
# predicted_labels = []
# for logits in outputs.logits:
#     label_id = logits.argmax(dim=1).tolist()
#     labels = [label_list[i] for i in label_id]
#     predicted_labels.append(labels)
#
# # Print predicted labels for each phrase
# for i, phrase in enumerate(phrases):
#     print(f"Phrase {i+1}: {phrase}")
#     print(f"Predicted labels: {predicted_labels[i]}")
#     print()


# import torch
# from transformers import AutoTokenizer, AutoModelForTokenClassification
#
# tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
# model = AutoModelForTokenClassification.from_pretrained("neuralmind/bert-base-portuguese-cased", num_labels=3)
#
# labels = ["O", "B-REF", "B-QUO", "I-REF", "I-QUO"]
#
#
# def identify_references_and_quotes(text):
#     tokens = tokenizer.encode(text, add_special_tokens=True)
#     with torch.no_grad():
#         outputs = model(torch.tensor([tokens]))
#         predictions = torch.argmax(outputs.logits, dim=-1)[0]
#
#     token_labels = [(tokenizer.decode([token]), labels[prediction]) for token, prediction in zip(tokens, predictions)]
#
#     references = []
#     quotes = []
#     for i, (token, label) in enumerate(token_labels):
#         if label == "B-REF":
#             reference = token
#             j = i + 1
#             while j < len(token_labels) and token_labels[j][1].startswith("I-"):
#                 reference += token_labels[j][0]
#                 j += 1
#             references.append(reference)
#         elif label == "B-QUO":
#             quote = token
#             j = i + 1
#             while j < len(token_labels) and token_labels[j][1].startswith("I-"):
#                 quote += token_labels[j][0]
#                 j += 1
#             quotes.append(quote)
#
#     return references, quotes
#
#
# text = "Segundo João, 'A vida é bela' é um filme inspirador."
# references, quotes = identify_references_and_quotes(text)
# print("References:", references)
# print("Quotes:", quotes)



# BERT (Bidirectional Encoder Representations from Transformers) is a powerful language model that can be used for a variety of natural language processing tasks, including citation/reference identification.
#
# Here are the general steps to use BERT for citation/reference identification:
#
# Collect the data: Gather a large set of documents that include citations and references. These documents can be in any format (e.g., PDF, plain text), as long as the citations and references are clearly marked.
#
# Preprocess the data: Before training the BERT model, you need to preprocess the data. This includes tokenization (breaking the text into individual words), creating input sequences, and labeling the citations and references.
#
# Fine-tune the BERT model: Fine-tuning involves training the BERT model on your specific task. In this case, you would train the model to identify citations and references in text. You would use a labeled dataset for this, where each citation and reference is labeled with a tag indicating whether it is a citation or a reference.
#
# Test the model: Once the model is trained, you need to test it on a separate dataset to evaluate its performance. You can calculate metrics such as precision, recall, and F1-score to measure the accuracy of the model.
#
# Deploy the model: Once the model is trained and tested, you can deploy it to identify citations and references in new documents.
#
# There are many open-source libraries and tools available that can help you implement BERT for citation/reference identification, such as Hugging Face's Transformers library and AllenNLP.




# THIS WORKS FINE

# from transformers import AutoModelForMaskedLM, AutoTokenizer
# model_checkpoint = "neuralmind/bert-base-portuguese-cased"
# model_mlm = AutoModelForMaskedLM.from_pretrained(model_checkpoint)
# # model_mlm = AutoModelForTokenClassification.from_pretrained("neuralmind/bert-base-portuguese-cased")
# tokenizer_mlm = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
#
#
# from transformers import pipeline
# nlp = pipeline("fill-mask", model=model_mlm, tokenizer=tokenizer_mlm)
#
# text = "O panteísmo sustenta que [MASK] é o universo e o universo é Deus."
# result = nlp(text)
# print(f"Best option for [MASK] will be: {result[0]['token_str']}")
# print("Final texts:")
# for option in result:
#     final_result = text.replace("[MASK]", option['token_str'])
#     print(f"Final text: \"{final_result}\"")



import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

from tabulate import tabulate
from tqdm import trange
import random

# %%% DATASET %%%

file_path = './content/SMSSpamCollection'
df = pd.DataFrame({'label':int(), 'text':str()}, index = [])
with open(file_path) as f:
  for line in f.readlines():
    split = line.split('\t')
    # df = df.append({'label': 1 if split[0] == 'spam' else 0,
    #                     'text': split[1]},
    #                     ignore_index = True)

    data_frames = [df]
    data_frames.append(pd.DataFrame({'label': [1 if split[0] == 'spam' else 0], 'text': [split[1]]}))
    df = pd.concat(data_frames, ignore_index=True)

    # data_frames = [pd.DataFrame({'label': [int(split[0] == 'spam')], 'text': [split[1]]})]
    # df = pd.concat(data_frames, ignore_index=True)

df.head()

# df = pd.DataFrame({'label':0, 'text':'I like cats.'}, index = [])
# split = "ham\tI like cats.".split("\t")
# df = pd.DataFrame({'label':int(), 'text':str()}, index = [])
# df = df.append({'label': 1 if split[0] == 'spam' else 0,'text': split[1]}, ignore_index = True)

text = df.text.values
labels = df.label.values
model_name = "neuralmind/bert-large-portuguese-cased"
# model_name = 'bert-base-uncased'

# %%% PREPROCESSING %%%

tokenizer = BertTokenizer.from_pretrained(
    model_name,
    do_lower_case = True
    )

def print_rand_sentence():
  '''Displays the tokens and respective IDs of a random text sample'''
  index = random.randint(0, len(text)-1)
  table = np.array([tokenizer.tokenize(text[index]),
                    tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text[index]))]).T
  print(tabulate(table,
                 headers = ['Tokens', 'Token IDs'],
                 tablefmt = 'fancy_grid'))

print_rand_sentence()


token_id = []
attention_masks = []

def preprocessing(input_text, tokenizer):
  '''
  Returns <class transformers.tokenization_utils_base.BatchEncoding> with the following fields:
    - input_ids: list of token ids
    - token_type_ids: list of token type ids
    - attention_mask: list of indices (0,1) specifying which tokens should considered by the model (return_attention_mask = True).
  '''
  return tokenizer.encode_plus(
                        input_text,
                        add_special_tokens = True,
                        max_length = 32,
                        padding='max_length',
                        return_attention_mask = True,
                        return_tensors = 'pt',
                        truncation=True
                   )


for sample in text:
  encoding_dict = preprocessing(sample, tokenizer)
  token_id.append(encoding_dict['input_ids'])
  attention_masks.append(encoding_dict['attention_mask'])

token_id = torch.cat(token_id, dim = 0)
attention_masks = torch.cat(attention_masks, dim = 0)
labels = torch.tensor(labels)
print(labels)

def print_rand_sentence_encoding():
  '''Displays tokens, token IDs and attention mask of a random text sample'''
  index = random.randint(0, len(text) - 1)
  tokens = tokenizer.tokenize(tokenizer.decode(token_id[index]))
  token_ids = [i.numpy() for i in token_id[index]]
  attention = [i.numpy() for i in attention_masks[index]]

  table = np.array([tokens, token_ids, attention]).T
  print(tabulate(table,
                 headers = ['Tokens', 'Token IDs', 'Attention Mask'],
                 tablefmt = 'fancy_grid'))

print_rand_sentence_encoding()

# %%% DATA SPLIT %%%

val_ratio = 0.2
# Recommended batch size: 16, 32. See: https://arxiv.org/pdf/1810.04805.pdf
batch_size = 16

# Indices of the train and validation splits stratified by labels
train_idx, val_idx = train_test_split(
    np.arange(len(labels)),
    test_size = val_ratio,
    shuffle = True,
    stratify = labels)

# Train and validation sets
train_set = TensorDataset(token_id[train_idx],
                          attention_masks[train_idx],
                          labels[train_idx])

val_set = TensorDataset(token_id[val_idx],
                        attention_masks[val_idx],
                        labels[val_idx])

# Prepare DataLoader
train_dataloader = DataLoader(
            train_set,
            sampler = RandomSampler(train_set),
            batch_size = batch_size
        )

validation_dataloader = DataLoader(
            val_set,
            sampler = SequentialSampler(val_set),
            batch_size = batch_size
        )

# %%% TRAIN %%%

def b_tp(preds, labels):
  '''Returns True Positives (TP): count of correct predictions of actual class 1'''
  return sum([preds == labels and preds == 1 for preds, labels in zip(preds, labels)])

def b_fp(preds, labels):
  '''Returns False Positives (FP): count of wrong predictions of actual class 1'''
  return sum([preds != labels and preds == 1 for preds, labels in zip(preds, labels)])

def b_tn(preds, labels):
  '''Returns True Negatives (TN): count of correct predictions of actual class 0'''
  return sum([preds == labels and preds == 0 for preds, labels in zip(preds, labels)])

def b_fn(preds, labels):
  '''Returns False Negatives (FN): count of wrong predictions of actual class 0'''
  return sum([preds != labels and preds == 0 for preds, labels in zip(preds, labels)])

def b_metrics(preds, labels):
  '''
  Returns the following metrics:
    - accuracy    = (TP + TN) / N
    - precision   = TP / (TP + FP)
    - recall      = TP / (TP + FN)
    - specificity = TN / (TN + FP)
  '''
  preds = np.argmax(preds, axis = 1).flatten()
  labels = labels.flatten()
  tp = b_tp(preds, labels)
  tn = b_tn(preds, labels)
  fp = b_fp(preds, labels)
  fn = b_fn(preds, labels)
  b_accuracy = (tp + tn) / len(labels)
  b_precision = tp / (tp + fp) if (tp + fp) > 0 else 'nan'
  b_recall = tp / (tp + fn) if (tp + fn) > 0 else 'nan'
  b_specificity = tn / (tn + fp) if (tn + fp) > 0 else 'nan'
  return b_accuracy, b_precision, b_recall, b_specificity

# Load the BertForSequenceClassification model
model = BertForSequenceClassification.from_pretrained(
    model_name,
    num_labels = 2,
    output_attentions = False,
    output_hidden_states = False,
)

# Recommended learning rates (Adam): 5e-5, 3e-5, 2e-5. See: https://arxiv.org/pdf/1810.04805.pdf
optimizer = torch.optim.AdamW(model.parameters(),
                              lr = 5e-5,
                              eps = 1e-08
                              )

# Run on GPU
# model.cuda()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Recommended number of epochs: 2, 3, 4. See: https://arxiv.org/pdf/1810.04805.pdf
epochs = 2

for _ in trange(epochs, desc='Epoch'):

    # ========== Training ==========

    # Set model to training mode
    model.train()

    # Tracking variables
    tr_loss = 0
    nb_tr_examples, nb_tr_steps = 0, 0

    for step, batch in enumerate(train_dataloader):
        batch = tuple(t.to(device) for t in batch)
        b_input_ids, b_input_mask, b_labels = batch
        optimizer.zero_grad()
        # Forward pass
        train_output = model(b_input_ids,
                             token_type_ids=None,
                             attention_mask=b_input_mask,
                             labels=b_labels)
        # Backward pass
        train_output.loss.backward()
        optimizer.step()
        # Update tracking variables
        tr_loss += train_output.loss.item()
        nb_tr_examples += b_input_ids.size(0)
        nb_tr_steps += 1

    # ========== Validation ==========

    # Set model to evaluation mode
    model.eval()

    # Tracking variables
    val_accuracy = []
    val_precision = []
    val_recall = []
    val_specificity = []

    for batch in validation_dataloader:
        batch = tuple(t.to(device) for t in batch)
        b_input_ids, b_input_mask, b_labels = batch
        with torch.no_grad():
            # Forward pass
            eval_output = model(b_input_ids,
                                token_type_ids=None,
                                attention_mask=b_input_mask)
        logits = eval_output.logits.detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()
        # Calculate validation metrics
        b_accuracy, b_precision, b_recall, b_specificity = b_metrics(logits, label_ids)
        val_accuracy.append(b_accuracy)
        # Update precision only when (tp + fp) !=0; ignore nan
        if b_precision != 'nan': val_precision.append(b_precision)
        # Update recall only when (tp + fn) !=0; ignore nan
        if b_recall != 'nan': val_recall.append(b_recall)
        # Update specificity only when (tn + fp) !=0; ignore nan
        if b_specificity != 'nan': val_specificity.append(b_specificity)

    print('\n\t - Train loss: {:.4f}'.format(tr_loss / nb_tr_steps))
    print('\t - Validation Accuracy: {:.4f}'.format(sum(val_accuracy) / len(val_accuracy)))
    print('\t - Validation Precision: {:.4f}'.format(sum(val_precision) / len(val_precision)) if len(
        val_precision) > 0 else '\t - Validation Precision: NaN')
    print('\t - Validation Recall: {:.4f}'.format(sum(val_recall) / len(val_recall)) if len(
        val_recall) > 0 else '\t - Validation Recall: NaN')
    print('\t - Validation Specificity: {:.4f}\n'.format(sum(val_specificity) / len(val_specificity)) if len(
        val_specificity) > 0 else '\t - Validation Specificity: NaN')


# %%% PREDICT %%%

new_sentence = 'WINNER!! As a valued network customer you have been selected to receivea £900 prize reward! To claim call 09061701461. Claim code KL341. Valid 12 hours only.'

# We need Token IDs and Attention Mask for inference on the new sentence
test_ids = []
test_attention_mask = []

# Apply the tokenizer
encoding = preprocessing(new_sentence, tokenizer)

# Extract IDs and Attention Mask
test_ids.append(encoding['input_ids'])
test_attention_mask.append(encoding['attention_mask'])
test_ids = torch.cat(test_ids, dim = 0)
test_attention_mask = torch.cat(test_attention_mask, dim = 0)

# Forward pass, calculate logit predictions
with torch.no_grad():
  output = model(test_ids.to(device), token_type_ids = None, attention_mask = test_attention_mask.to(device))

prediction = 'Spam' if np.argmax(output.logits.cpu().numpy()).flatten().item() == 1 else 'Ham'

print('Input Sentence: ', new_sentence)
print('Predicted Class: ', prediction)




