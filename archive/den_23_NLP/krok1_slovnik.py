import os

texty = [
    "this movie is great",
    "i love this film",
    "terrible boring movie",
    "i hate this film"
]

veta = texty[0]
tokeny = veta.split()
print("Veta:", veta)
print("Tokeny:", tokeny)

slovnik = {"<pad>": 0, "<unk>": 1}

for veta in texty:
    for token in veta.split():
        if token not in slovnik:
            slovnik[token] = len(slovnik)

print("\nSlovnik (slovo -> index):")
for slovo, index in slovnik.items():
    print(f"    {slovo!r}: {index}")

print("\nVelikost sloviku:", len(slovnik))