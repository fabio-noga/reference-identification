import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

from tabulate import tabulate
from tqdm import trange
import random


val_ratio = 0.2
# Recommended batch size: 16, 32. See: https://arxiv.org/pdf/1810.04805.pdf
batch_size = 16
# Recommended number of epochs: 2, 3, 4. See: https://arxiv.org/pdf/1810.04805.pdf
epochs = 2

# %%% DATASET %%%

file_path = '../output/SMSSpamCollection'  #Testing file
df = pd.DataFrame({'label': int(), 'text': str()}, index=[])
with open(file_path) as f:
    for line in f.readlines():
        split = line.split('\t')
        data_frames = [df]
        data_frames.append(pd.DataFrame({'label': [1 if split[0] == 'spam' else 0], 'text': [split[1]]}))
        df = pd.concat(data_frames, ignore_index=True)

df.head()
text = df.text.values
labels = df.label.values
model_name = "neuralmind/bert-large-portuguese-cased"

# %%% PREPROCESSING %%%

tokenizer = BertTokenizer.from_pretrained(
    model_name,
    do_lower_case=True
)


def printRandSentence():
    index = random.randint(0, len(text) - 1)
    table = np.array([tokenizer.tokenize(text[index]),
                      tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text[index]))]).T
    print(tabulate(table,
                   headers=['Tokens', 'Token IDs'],
                   tablefmt='fancy_grid'))


printRandSentence()

tokenId = []
attentionMasks = []


def preprocessing(inputText, tokenizer):
    return tokenizer.encode_plus(
        inputText,
        add_special_tokens=True,
        max_length=64,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True
    )


for sample in text:
    encodingDict = preprocessing(sample, tokenizer)
    tokenId.append(encodingDict['input_ids'])
    attentionMasks.append(encodingDict['attention_mask'])

tokenId = torch.cat(tokenId, dim=0)
attentionMasks = torch.cat(attentionMasks, dim=0)
labels = torch.tensor(labels)
print(labels)


def printRandSentenceEncoding():
    '''Displays tokens, token IDs and attention mask of a random text sample'''
    index = random.randint(0, len(text) - 1)
    tokens = tokenizer.tokenize(tokenizer.decode(tokenId[index]))
    token_ids = [i.numpy() for i in tokenId[index]]
    attention = [i.numpy() for i in attentionMasks[index]]

    table = np.array([tokens, token_ids, attention]).T
    print(tabulate(table,
                   headers=['Tokens', 'Token IDs', 'Attention Mask'],
                   tablefmt='fancy_grid'))


printRandSentenceEncoding()

# %%% DATA SPLIT %%%

# Indices of the train and validation splits stratified by labels
train_idx, val_idx = train_test_split(
    np.arange(len(labels)),
    test_size=val_ratio,
    shuffle=True,
    stratify=labels)

# Train and validation sets
train_set = TensorDataset(tokenId[train_idx],
                          attentionMasks[train_idx],
                          labels[train_idx])

val_set = TensorDataset(tokenId[val_idx],
                        attentionMasks[val_idx],
                        labels[val_idx])

# Prepare DataLoader
train_dataloader = DataLoader(
    train_set,
    sampler=RandomSampler(train_set),
    batch_size=batch_size
)

validation_dataloader = DataLoader(
    val_set,
    sampler=SequentialSampler(val_set),
    batch_size=batch_size
)


# %%% TRAIN %%%

def getTP(preds, labels):
    return sum([preds == labels and preds == 1 for preds, labels in zip(preds, labels)])


def getFP(preds, labels):
    return sum([preds != labels and preds == 1 for preds, labels in zip(preds, labels)])


def getTN(preds, labels):
    return sum([preds == labels and preds == 0 for preds, labels in zip(preds, labels)])


def getFN(preds, labels):
    return sum([preds != labels and preds == 0 for preds, labels in zip(preds, labels)])


# accuracy    = (TP + TN) / N
# precision   = TP / (TP + FP)
# recall      = TP / (TP + FN)
# specificity = TN / (TN + FP)
def getMetrics(preds, labels):
    preds = np.argmax(preds, axis=1).flatten()
    labels = labels.flatten()
    tp = getTP(preds, labels)
    tn = getTN(preds, labels)
    fp = getFP(preds, labels)
    fn = getFN(preds, labels)
    accuracy = (tp + tn) / len(labels)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 'nan'
    recall = tp / (tp + fn) if (tp + fn) > 0 else 'nan'
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 'nan'
    return accuracy, precision, recall, specificity


# Load the BertForSequenceClassification modeldir
model = BertForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2,
    output_attentions=False,
    output_hidden_states=False,
)

# Recommended learning rates (Adam): 5e-5, 3e-5, 2e-5. See: https://arxiv.org/pdf/1810.04805.pdf
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5, eps=1e-08)


# modeldir.cuda() # Run on GPU

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

for _ in trange(epochs, desc='Epoch'):

    # ========== Training ==========

    # Set modeldir to training mode
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

    # Set modeldir to evaluation mode
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
        b_accuracy, b_precision, b_recall, b_specificity = getMetrics(logits, label_ids)
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
test_ids = torch.cat(test_ids, dim=0)
test_attention_mask = torch.cat(test_attention_mask, dim=0)

# Forward pass, calculate logit predictions
with torch.no_grad():
    output = model(test_ids.to(device), token_type_ids=None, attention_mask=test_attention_mask.to(device))

prediction = 'Spam' if np.argmax(output.logits.cpu().numpy()).flatten().item() == 1 else 'Ham'

print('Input Sentence: ', new_sentence)
print('Predicted Class: ', prediction)
