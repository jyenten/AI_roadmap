import torch

texty = [
    "this movie is grat",
    "i love this film",
    "terrible boring movie",
    "i hate this film",
]

slovnik = {"<pad>": 0, "<unk>": 1}
for veta in texty:
    for token in veta.split():
        if token not in slovnik:
            slovnik[token] = len(slovnik)

def veta_na_cisla(veta):
    cisla = []
    for token in veta.split():

        cisla.append(slovnik.get(token, 1))

    return cisla

sekvence = [veta_na_cisla(veta) for veta in texty]

print("Sekvence (ruzne delky):")
for veta, seq in zip(texty, sekvence):
    print(f"    {veta!r} -> {seq}")

max_delka = max(len(seq) for seq in sekvence)
print("\nNejdels veta ma delku:", max_delka)

sekvence_padded = []
for seq in sekvence:

    padding = [0] * (max_delka - len(seq))
    sekvence_padded.append(seq + padding)

print("\nSekvence po paddingu(stejne delky):")
for seq in sekvence_padded:
    print("", seq)

X = torch.tensor(sekvence_padded)
print("\nTvar tensoru X:", X.shape)