import torch
from torch.utils.data import Dataset, DataLoader

texty = [
    "this movie is great",
    "i love this film",
    "terrible boring movie",
    "i hate this film",
]

labely = [1, 1, 0, 0, ]


slovnik = {"<pad>": 0, "<unk>": 1}
for veta in texty:
    for token in veta.split():
        if token not in slovnik:
            slovnik[token] = len(slovnik)

def veta_na_cisla(veta):
    return [slovnik.get(token, 1) for token in veta.split()]

sekvence = [veta_na_cisla(veta) for veta in texty]
max_delka = max(len(seq) for seq in sekvence)
sekvence_padded = [seq + [0] * (max_delka - len(seq)) for seq in sekvence]

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

print("Počet vzorků:", len(dataset))
print("Velikost slovíků:", len(slovnik))

for batch_x, batch_y in loader:
    print("\nDávka X (text jako čísla):")
    print(batch_x)
    print("Tvar X:", batch_x.shape)
    print("Dávka Y (labely):", batch_y)
    break