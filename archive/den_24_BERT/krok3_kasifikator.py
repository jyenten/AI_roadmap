import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
).to(device)

texty = [

    "this movie is great",
    "i love this film",
    "terrible boring movie",
    "i hate this film",
]

labely = [1, 1, 0, 0]

vstup = tokenizer(texty, padding=True, truncation=True, return_tensors="pt").to(device)
labels_tensor = torch.tensor(labely).to(device)

print("\nTvar input_ids:", vstup["input_ids"].shape)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

model.train()
epochy = 30
for epoch in range(epochy):
    optimizer.zero_grad()

    vystup = model(**vstup, labels=labels_tensor)
    loss = vystup.loss
    loss.backward()
    optimizer.step()

    if(epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/{epochy} - Loss: {loss.item():.4f}")

print("\nTrenink hotovy")

import torch.nn.functional as F

def predpovez(veta):
    model.eval()
    with torch.no_grad():
        v = tokenizer(veta, return_tensors="pt").to(device)
        logits = model(**v).logits
        pravdep = F.softmax(logits, dim=1)
        trida = torch.argmax(pravdep, dim=1)
    sentiment = "POZITIVNI" if trida == 1 else "NEGATIVNI"
    jistota = pravdep[0, trida].item()
    return sentiment, jistota

testovaci_vety = [
    "i love this movie",
    "terrible film",
    "love and terrible",
    "terrible and scary and beautiful film",
    "this movie is not bad",
]

print("\nBERT")
for veta in testovaci_vety:
    sentiment, jistota = predpovez(veta)
    print(f" {veta!r:28} -> {sentiment} (jistota: {jistota:.2f})")

