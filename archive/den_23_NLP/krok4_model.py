import torch
import torch.nn as nn

class SentimentModel(nn.Module):
    def __init__(self, velikot_slovniku, embedding_dim=8):
        super().__init__()

        self.embedding = nn.Embedding(velikot_slovniku, embedding_dim, padding_idx=0)

        self.fc = nn.Linear(embedding_dim, 1)

    def forward(self, x):
        embedded = self.embedding(x)
        veta_vekotr = embedded.mean(dim=1)
        skore = self.fc(veta_vekotr)
        return skore.squeeze(1)

velikost_slovniku = 12
model = SentimentModel(velikost_slovniku)

testovaci_x = torch.tensor([[9, 10, 3, 0], [2, 3, 4, 5]])
vystup = model(testovaci_x)

print("Vstup (Čísla slov):")
print(testovaci_x)
print("Tvar vstupu:", testovaci_x.shape)
print("\nVýstup modelu (syrové skóre):", vystup)
print("Tvar vystupu", vystup.shape)

