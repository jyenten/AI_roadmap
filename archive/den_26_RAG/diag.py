import numpy as np
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

dokumenty = [
    "The Eiffel Tower is 330 meters tall and located in Paris, France.",
    "The Great Wall of China is over 21,000 kilometers long.",
    "Python is a programming language created by Guido van Rossum in 1991.",
    "The human heart beats about 100,000 times per day.",
    "Mount Everest is the highest mountain on Earth at 8,849 meters.",
    "Photosynthesis is how plants convert sunlight into energy.",
]

doc_embeddings = embedder.encode(dokumenty)
print("Tvar doc_embeddings: ", doc_embeddings.shape)

def kosinova_podobnost(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

dotaz = "Who created Python?"
dv = embedder.encode([dotaz])[0]
print(f"\nDotaz:  {dotaz}")
for i, doc_vec in enumerate(doc_embeddings):
    sim = kosinova_podobnost(dv, doc_vec)
    print(f"    [{sim:.3f}] {dokumenty[i]}")