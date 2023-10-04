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

max_length = 64
file_path = '../output/training_file.txt'
df = pd.DataFrame({'label': int(), 'text': str()}, index=[])
with open(file_path, "r", encoding="utf-8") as f:
    for line in f.readlines():
        split = line.split('\t')
        # df = df.append({'label': 1 if split[0] == 'spam' else 0,
        #                     'text': split[1]},
        #                     ignore_index = True)
        data_frames = [df]
        data_frames.append(pd.DataFrame({'label': [1 if split[0] == 'TP' else 0], 'text': [split[1]]}))
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
    do_lower_case=True
)


def print_rand_sentence():
    '''Displays the tokens and respective IDs of a random text sample'''
    index = random.randint(0, len(text) - 1)
    table = np.array([tokenizer.tokenize(text[index]),
                      tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text[index]))]).T
    print(tabulate(table,
                   headers=['Tokens', 'Token IDs'],
                   tablefmt='fancy_grid'))


print_rand_sentence()
token_id = []
attention_masks = []


def preprocessing(input_text, tokenizer):
    '''
  Returns <class transformers.tokenization_utils_base.BatchEncoding> with the following fields:
    - input_ids: list of token ids
    - token_type_ids: list of token type ids
    - attention_mask: list of indices (0,1) specifying which tokens should considered by the modeldir (return_attention_mask = True).
  '''
    return tokenizer.encode_plus(
        input_text,
        add_special_tokens=True,
        max_length=max_length,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True
    )


for sample in text:
    encoding_dict = preprocessing(sample, tokenizer)
    token_id.append(encoding_dict['input_ids'])
    attention_masks.append(encoding_dict['attention_mask'])
token_id = torch.cat(token_id, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
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
                   headers=['Tokens', 'Token IDs', 'Attention Mask'],
                   tablefmt='fancy_grid'))

# print_rand_sentence_encoding()
# # %%% DATA SPLIT %%%
# val_ratio = 0.2
# # Recommended batch size: 16, 32. See: https://arxiv.org/pdf/1810.04805.pdf
# batch_size = 16
# # Indices of the train and validation splits stratified by labels
# train_idx, val_idx = train_test_split(
#     np.arange(len(labels)),
#     test_size=val_ratio,
#     shuffle=True,
#     stratify=labels)
# # Train and validation sets
# train_set = TensorDataset(token_id[train_idx],
#                           attention_masks[train_idx],
#                           labels[train_idx])
# val_set = TensorDataset(token_id[val_idx],
#                         attention_masks[val_idx],
#                         labels[val_idx])
# # Prepare DataLoader
# train_dataloader = DataLoader(
#     train_set,
#     sampler=RandomSampler(train_set),
#     batch_size=batch_size
# )
# validation_dataloader = DataLoader(
#     val_set,
#     sampler=SequentialSampler(val_set),
#     batch_size=batch_size
# )
#
#
# # %%% TRAIN %%%
# def b_tp(preds, labels):
#     '''Returns True Positives (TP): count of correct predictions of actual class 1'''
#     return sum([preds == labels and preds == 1 for preds, labels in zip(preds, labels)])
#
#
# def b_fp(preds, labels):
#     '''Returns False Positives (FP): count of wrong predictions of actual class 1'''
#     return sum([preds != labels and preds == 1 for preds, labels in zip(preds, labels)])
#
#
# def b_tn(preds, labels):
#     '''Returns True Negatives (TN): count of correct predictions of actual class 0'''
#     return sum([preds == labels and preds == 0 for preds, labels in zip(preds, labels)])
#
#
# def b_fn(preds, labels):
#     '''Returns False Negatives (FN): count of wrong predictions of actual class 0'''
#     return sum([preds != labels and preds == 0 for preds, labels in zip(preds, labels)])
#
#
# def b_metrics(preds, labels):
#     '''
#   Returns the following metrics:
#     - accuracy    = (TP + TN) / N
#     - precision   = TP / (TP + FP)
#     - recall      = TP / (TP + FN)
#     - specificity = TN / (TN + FP)
#   '''
#     preds = np.argmax(preds, axis=1).flatten()
#     labels = labels.flatten()
#     tp = b_tp(preds, labels)
#     tn = b_tn(preds, labels)
#     fp = b_fp(preds, labels)
#     fn = b_fn(preds, labels)
#     b_accuracy = (tp + tn) / len(labels)
#     b_precision = tp / (tp + fp) if (tp + fp) > 0 else 'nan'
#     b_recall = tp / (tp + fn) if (tp + fn) > 0 else 'nan'
#     b_specificity = tn / (tn + fp) if (tn + fp) > 0 else 'nan'
#     return b_accuracy, b_precision, b_recall, b_specificity
#
#
# # Load the BertForSequenceClassification modeldir
# model = BertForSequenceClassification.from_pretrained(
#     model_name,
#     num_labels=2,
#     output_attentions=False,
#     output_hidden_states=False,
# )
# # Recommended learning rates (Adam): 5e-5, 3e-5, 2e-5. See: https://arxiv.org/pdf/1810.04805.pdf
# optimizer = torch.optim.AdamW(model.parameters(),
#                               lr=5e-5,
#                               eps=1e-08
#                               )
# # Run on GPU
# # modeldir.cuda()
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# # Recommended number of epochs: 2, 3, 4. See: https://arxiv.org/pdf/1810.04805.pdf
# def train():
#     epochs = 2
#     for _ in trange(epochs, desc='Epoch'):
#         # ========== Training ==========
#         # Set modeldir to training mode
#         model.train()
#         # Tracking variables
#         tr_loss = 0
#         nb_tr_examples, nb_tr_steps = 0, 0
#         for step, batch in enumerate(train_dataloader):
#             batch = tuple(t.to(device) for t in batch)
#             b_input_ids, b_input_mask, b_labels = batch
#             optimizer.zero_grad()
#             # Forward pass
#             train_output = model(b_input_ids,
#                                  token_type_ids=None,
#                                  attention_mask=b_input_mask,
#                                  labels=b_labels)
#             # Backward pass
#             train_output.loss.backward()
#             optimizer.step()
#             # Update tracking variables
#             tr_loss += train_output.loss.item()
#             nb_tr_examples += b_input_ids.size(0)
#             nb_tr_steps += 1
#         # ========== Validation ==========
#         # Set modeldir to evaluation mode
#         model.eval()
#         # Tracking variables
#         val_accuracy = []
#         val_precision = []
#         val_recall = []
#         val_specificity = []
#         for batch in validation_dataloader:
#             batch = tuple(t.to(device) for t in batch)
#             b_input_ids, b_input_mask, b_labels = batch
#             with torch.no_grad():
#                 # Forward pass
#                 eval_output = model(b_input_ids,
#                                     token_type_ids=None,
#                                     attention_mask=b_input_mask)
#             logits = eval_output.logits.detach().cpu().numpy()
#             label_ids = b_labels.to('cpu').numpy()
#             # Calculate validation metrics
#             b_accuracy, b_precision, b_recall, b_specificity = b_metrics(logits, label_ids)
#             val_accuracy.append(b_accuracy)
#             # Update precision only when (tp + fp) !=0; ignore nan
#             if b_precision != 'nan': val_precision.append(b_precision)
#             # Update recall only when (tp + fn) !=0; ignore nan
#             if b_recall != 'nan': val_recall.append(b_recall)
#             # Update specificity only when (tn + fp) !=0; ignore nan
#             if b_specificity != 'nan': val_specificity.append(b_specificity)
#         print('\n\t - Train loss: {:.4f}'.format(tr_loss / nb_tr_steps))
#         print('\t - Validation Accuracy: {:.4f}'.format(sum(val_accuracy) / len(val_accuracy)))
#         print('\t - Validation Precision: {:.4f}'.format(sum(val_precision) / len(val_precision)) if len(
#             val_precision) > 0 else '\t - Validation Precision: NaN')
#         print('\t - Validation Recall: {:.4f}'.format(sum(val_recall) / len(val_recall)) if len(
#             val_recall) > 0 else '\t - Validation Recall: NaN')
#         print('\t - Validation Specificity: {:.4f}\n'.format(sum(val_specificity) / len(val_specificity)) if len(
#             val_specificity) > 0 else '\t - Validation Specificity: NaN')
#
#
# def saveModel():
#     tokenizer.save_pretrained("./tokenizer/")
#     torch.save(model.state_dict(), "tokenizer/model2")
#
# train()
# saveModel()

# %%% PREDICT %%%


# saved_model = torch.load("./tokenizer/modelstate")
new_sentence = 'Como afirma João Costa, em A Responsabilidade Civil do Médico-Reflexões Sobre a Noção da Perda de Chance e a Tutela do Doente Lesado, publicado em 2008 pela Coimbra Editora pp. 93-96, destaca que, em geral, se o objetivo almejado for alcançado'
new_sentence = 'Como afirma (cfr. João Costa, in A Responsabilidade Civil do Médico-Reflexões Sobre a Noção da Perda de Chance e a Tutela do Doente Lesado, 2008, Coimbra Editora pp. 93-96) destaca que, em geral, se o objetivo almejado for alcançado'
# new_sentence = 'Exemplo de Texto.'

# tokenizer = BertTokenizer.from_pretrained(
#     "./tokenizer/vocab.txt",
#     do_lower_case=True,
#     local_files_only=True,
# )

# modeldir = BertForSequenceClassification.from_pretrained(
#         saved_model,
#         local_files_only=True,
#         num_labels=2,
#         output_attentions=False,
#         output_hidden_states=False,
#     )

# for num in range(1, 11):
#     modeldir = BertForSequenceClassification.from_pretrained(
#         saved_model,
#         local_files_only=True,
#         num_labels=2,
#         output_attentions=False,
#         output_hidden_states=False,
#     )
#
#     # We need Token IDs and Attention Mask for inference on the new sentence
#     test_ids = []
#     test_attention_mask = []
#     # Apply the tokenizer
#     encoding = preprocessing(new_sentence, tokenizer)
#
#     # Extract IDs and Attention Mask
#     test_ids.append(encoding['input_ids'])
#     test_attention_mask.append(encoding['attention_mask'])
#     test_ids = torch.cat(test_ids, dim=0)
#     test_attention_mask = torch.cat(test_attention_mask, dim=0)
#
#     index = random.randint(0, len(text) - 1)
#     tokens = tokenizer.tokenize(tokenizer.decode(test_ids[0]))
#     token_ids = [i.numpy() for i in test_ids[0]]
#     attention = [i.numpy() for i in test_attention_mask[0]]
#     # table = np.array([tokens, token_ids, attention]).T
#     # print(tabulate(table,
#     #                headers=['Tokens', 'Token IDs', 'Attention Mask'],
#     #                tablefmt='fancy_grid'))
#
#     # Forward pass, calculate logit predictions
#     with torch.no_grad():
#         output = modeldir(test_ids.to(device), token_type_ids=None, attention_mask=test_attention_mask.to(device))
#
#     prediction = 'Referencia' if np.argmax(output.logits.cpu().numpy()).flatten().item() == 1 else 'Normal'
#
#     print('Input Sentence: ', new_sentence)
#     print('Predicted Class: ', prediction)