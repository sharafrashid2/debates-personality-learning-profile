# Importing the libraries needed
import torch
from transformers import DistilBertModel, DistilBertTokenizer

# Creating the customized model, by adding a drop out and a dense layer on top of distil bert to get the final output for the model.
class DistillBERTClass(torch.nn.Module):
    def __init__(self):
        super(DistillBERTClass, self).__init__()
        self.l1 = DistilBertModel.from_pretrained("distilbert-base-multilingual-cased")
        self.pre_classifier = torch.nn.Linear(768, 768)
        self.dropout = torch.nn.Dropout(0.3)
        self.classifier = torch.nn.Linear(768, 4)

    def forward(self, input_ids, attention_mask):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output

# loading fine tuned tribe identifier model and tokenizer
saved_model_weights = torch.load('./tribes_model/reddit_saved_model_weights.pth')
saved_vocab_file = './tribes_model/vocab_distilbert_reddit_personalities.bin'

model = DistillBERTClass()
model.load_state_dict(saved_model_weights)
tokenizer = DistilBertTokenizer.from_pretrained(saved_vocab_file)
model.eval()

"""
Function that makes an inference about the input_text about which Happimetrics tribe the text belongs to
using the finetuned Reddit DistilBERT model.
"""
def identify_tribe(input_text):
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    # Get the input IDs and attention mask
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Pass the input to the model for inference
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    # Get the predicted class
    predicted_class = torch.argmax(outputs, dim=1).item()
    number_to_label = {0: 'treehugger', 1: 'spiritualist', 2: 'nerd', 3: 'fatherlander'}

    return number_to_label[predicted_class]

print(identify_tribe("That gadget of yours looks so cool"))