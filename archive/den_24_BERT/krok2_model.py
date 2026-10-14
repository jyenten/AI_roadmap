import torch
from transformers import AutoTokenizer, AutoModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased").to(device)
model.eval()

veta = "this movice is great"

vstup = tokenizer(veta, return_tensors="pt").to(device)
print("\ninput_ids:", vstup["input_ids"])
print("Tvar input input_ids:", vstup["input_ids"].shape)

with torch.no_grad():
    vystup = model(**vstup)

embeddingy = vystup.last_hidden_state
print("\nTvar embeddingu", embeddingy.shape)

cls_vektor = embeddingy[:, 0, :]
print("Tvar [CLS] vektoru", cls_vektor.shape)
print("Prvnich 5 cisel [CLS] vekotru: ", cls_vektor[0, :5])

