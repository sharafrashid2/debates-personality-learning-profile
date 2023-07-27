# Importing the libraries needed
import torch
from distilbert_nn_class import DistilBERTClass
from transformers import DistilBertTokenizer
import translators as ts

# loading fine tuned tribe identifier model and tokenizer
saved_model_weights = torch.load('./distilbert_torch_spotify_antbeeleech_model/abl_saved_model_weights.pth')
saved_vocab_file = './distilbert_torch_spotify_antbeeleech_model/vocab_distilbert_antbeeleech_work_personalities.bin'

model = DistilBERTClass(3)
model.load_state_dict(saved_model_weights)
tokenizer = DistilBertTokenizer.from_pretrained(saved_vocab_file)
model.eval()

"""
if the text is in Spanish, returns the translated text in English; otherwise, returns
the same text that is inputted
"""
def translate_to_english(text: str) -> str:
    return ts.translate_text(text)

"""
Function that makes an inference about the input_text about which Happimetrics tribe the text belongs to
using the finetuned Reddit DistilBERT model.
"""
def identify_work_personality(input_text):
    input_text = translate_to_english(input_text)
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    # Get the input IDs and attention mask
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Pass the input to the model for inference
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    # Get the predicted class
    predicted_class = torch.argmax(outputs, dim=1).item()
    number_to_label = {0: 'ant', 1: 'bee', 2: 'leech'}

    return number_to_label[predicted_class]
