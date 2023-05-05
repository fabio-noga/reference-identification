import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

#https://github.com/nunorc/qaptnet
#https://huggingface.co/Luciano/bert-base-portuguese-cased-finetuned-peticoes

# model_checkpoint = "neuralmind/bert-base-portuguese-cased"
# model_mlm = AutoModelForMaskedLM.from_pretrained(model_checkpoint)
# # model_mlm = AutoModelForTokenClassification.from_pretrained("neuralmind/bert-base-portuguese-cased")
# tokenizer_mlm = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")

# Load the pre-trained BERT model and tokenizer
# model_name = 'dbmdz/bert-large-cased-finetuned-conll03-english'
# # model_name = 'neuralmind/bert-large-portuguese-cased'
# # # model_name = 'Luciano/bert-base-portuguese-cased-finetuned-peticoes'
# tokenizer = AutoTokenizer.from_pretrained(model_name, do_lower_case=False)
# model = AutoModelForTokenClassification.from_pretrained(model_name)
#
# # Define the sentence to be processed
# # sentence = "This quote was by Charles Dickens in 'The Book'."
# sentence = "In his renowned literary work known as 'The Book', the celebrated British author and social critic Charles Dickens uttered the following statement, which has since been widely cited and revered for its profundity and eloquence."
# # sentence = "Está é uma frase em português escrita por Joaquim de Almeida"
#
# # Tokenize the sentence
# tokens = tokenizer.encode(sentence, add_special_tokens=False)
#
# # Convert token IDs to a PyTorch tensor
# tokens_tensor = torch.tensor([tokens])
#
# # Get the model's predictions for the token classifications
# outputs = model(tokens_tensor)
#
# # Get the predicted labels and convert them to strings
# predicted_labels = torch.argmax(outputs.logits, axis=-1)
# predicted_labels = [model.config.id2label[label_id] for label_id in predicted_labels[0].tolist()]
#
# # Map the predicted labels back to the original tokens
# predicted_tokens = tokenizer.convert_ids_to_tokens(tokens)
# predicted_entities = []
#
# # Extract the named entities from the predictions
# current_entity = None
# for token, label in zip(predicted_tokens, predicted_labels):
#     if label.startswith('B-'):
#         if current_entity:
#             predicted_entities.append(current_entity)
#         current_entity = {'entity': label[2:], 'tokens': [token]}
#     elif label.startswith('I-'):
#         if not current_entity:
#             current_entity = {'entity': label[2:], 'tokens': [token]}
#         else:
#             current_entity['tokens'].append(token)
#     else:
#         if current_entity:
#             predicted_entities.append(current_entity)
#             current_entity = None
#
# # Print the identified author and book title
# for entity in predicted_entities:
#     if entity['entity'] == 'PER':
#         author = tokenizer.convert_tokens_to_string(entity['tokens'])
#         print('Author:', author)
#     elif entity['entity'] == 'MISC':
#         book_title = tokenizer.convert_tokens_to_string(entity['tokens'])
#         print('Book Title:', book_title)