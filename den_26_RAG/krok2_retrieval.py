from sentence_transformers import SentenceTransformer
import numpy as np

print("Načítám embeddung model....")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Hotovo\n")

dokumenty = [
    "The Eiffel Tower is 330 meters tall and located in Paris, France.",
    "The Great Wall of China is over 21,000 kilometers long.",
    "Python is a programming language created by"
    "Guido van Rossum in 1991.",
    "The human heart beats about 100,000 times per day.",
    "Mount Everest is the highest mountain on Earth at 8,849 meters.",
    "Photosynthesis is how plants convert sunlight into energy.",

]

print("Počítám embeddingy dokkumentů...")
doc_embeddings = model.encode(dokumenty)
print("Tvar:", doc_embeddings.shape, "\n")

def kosinova_podobnost(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def najdi_relevantni(dotaz, k=2):
    dotaz_vektor = model.encode([dotaz])[0]

    skore = []
    for i, doc_vec in enumerate(doc_embeddings):
        sim = kosinova_podobnost(dotaz_vektor, doc_vec)
        skore.append((sim, i))

    skore.sort(reverse=True)
    return skore[:k]

dotazy = [
    "How tall is the Eiffel Tower ?",
    "Who invented Python",
    "What is the tallest mountain?",
]

for dotaz in dotazy:
    print(f"DOTAZ:  {dotaz}")
    vysledky = najdi_relevantni(dotaz, k=2)
    for sim, idx in vysledky:
        print(f"    [{sim:.3f}] {dokumenty[idx]}")
    print()