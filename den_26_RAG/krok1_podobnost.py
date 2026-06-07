from sentence_transformers import SentenceTransformer
import numpy as np

print("Načítám embedding mode...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Hotovo!\n")

vety = [
    "The cat sleeps on the sofa.",
    "A kitten is resting on the couch.",
    "Python is a great programming language."

]

emb = model.encode(vety)
print("Tvar embeddingů:", emb.shape)


def kosinova_podobnost(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("\n Podbnosti")
print(f"Věta 0 vs 1 (kočka vs kotě):   {kosinova_podobnost(emb[0], emb[1]):.3f}")
print(f"Věta 0 vs 2 (kočka vs Python):  {kosinova_podobnost(emb[0], emb[2]):.3f}")
print(f"Věta 1 vs 2 (kotě vs Python):   {kosinova_podobnost(emb[1], emb[2]):.3f}")

