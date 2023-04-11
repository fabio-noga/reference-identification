from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# Load a pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Define a text variable
text = "This is a sample text. It contains multiple sentences. Some sentences may end with an abbreviation, like Dr. or Mr. Doe."

# Tokenize the text into individual tokens
tokens = tokenizer.tokenize(text)

# Run the tokens through the BERT model to get sentence boundaries
input_ids = tokenizer.encode(text, return_tensors='pt')
with torch.no_grad():
    outputs = model(input_ids)
predictions = torch.argmax(outputs.logits, dim=-1)[0]

# Use the sentence boundaries to extract sentences from the text
sentences = []
sentence = ""
for i in range(len(tokens)):
    if predictions[i+1] == 1: # If token is the start of a new sentence
        sentences.append(sentence.strip()) # Add the current sentence to the list
        sentence = "" # Start a new sentence
    sentence += tokens[i].replace("##", "") + " " # Add the current token to the current sentence

sentences.append(sentence.strip()) # Add the last sentence to the list

print(sentences)