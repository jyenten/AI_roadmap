import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

script_dir = os.path.dirname(os.path.abspath(__file__))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)


texty = [
    "this movie is great",
    "i love this film",
    "terrible boring movie",
    "i hate this film",
]
labely = [1, 1, 0, 0]

slovnik = {"<pad>": 0, "<unk>": 1}
for veta in texty:
    for token in veta.split():
        if token not in slovnik:
            slovnik[token] = len(slovnik)

def veta_na_cisla(veta):
    return [slovnik.get(token, 1) for token in veta.split()]

sekvence = [veta_na_cisla(v)for v in texty]
max_delka = max(len(s) for s in sekvence)
sekvence_padded = [s + [0] * (max_delka - len(s)) for s in sekvence]

class SentimentDataset(Dataset):
    def __init__(self, sekvence, labely):
        self.sekvence = torch.tensor(sekvence)
        self.labely = torch.tensor(labely, dtype=torch.float32)
    def __len__(self):
        return len(self.labely)
        
    def __getitem__(self, idx):
        return self.sekvence[idx], self.labely[idx]
    
dataset = SentimentDataset(sekvence_padded, labely)
loader = DataLoader(dataset, batch_size=2, shuffle=True)


class SentimentModel(nn.Module):
    def __init__(self, velikost_slovniku, embedding_dim=8):
        super().__init__()
        self.embedding = nn.Embedding(velikost_slovniku, embedding_dim, padding_idx=0)
        self.fc = nn.Linear(embedding_dim, 1)

    def forward(self, x):
        embedded = self.embedding(x)
        veta_vektor = embedded.mean(dim=1)
        skore = self.fc(veta_vektor)
        return skore.squeeze(1)
    
model = SentimentModel(len(slovnik)).to(device)


loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

epochy = 100
for epoch in range(epochy):
    model.train()
    celkova_loss = 0.0
    for batch_x, batch_y in loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()
        vystup = model(batch_x)
        loss = loss_fn(vystup, batch_y)
        loss.backward()
        optimizer.step()

        celkova_loss += loss.item()
        
if(epoch + 1) % 20 == 0:
    print(f"Epoch {epoch + 1}/{epochy} - Loss: {celkova_loss:.4f}")

print("\nTrénink hotový!")

def predpovez_sentiment(veta):
    model.eval()
    with torch.no_grad():
        cisla = veta_na_cisla(veta)

        cisla = cisla + [0] * (max_delka - len(cisla))

        cisla = cisla[:max_delka]
        x = torch.tensor([cisla]).to(device)
        skore = model(x)
        prst = torch.sigmoid(skore).item()
    sentiment = "POZITIVNÍ" if prst >= 0.5 else "negativní"
    return sentiment, prst

testovaci_vety = [
    "i love this movie",
    "terrible film",
    "this is great",
    "love and terrible",
    "love love and terrible",
    "love nad terrible",
    "terrible and love",
]

print("\n ---- Test na nových větách ---")
for veta in testovaci_vety:
    sentiment, prst = predpovez_sentiment(veta)
    print(f" {veta!r:30} -> {sentiment} (jistota: {prst:.2f})")


