import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device: ", device)

print("Načítám embedding model....")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


print("Načítám QA model....")
qa_nazev = "distilbert-base-cased-distilled-squad"
qa_tokenizer = AutoTokenizer.from_pretrained(qa_nazev)
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_nazev).to(device)
qa_model.eval()
print("Hotovo\n")


dokumenty = [
    "The Eiffel Tower is 330 meters tall and located in Paris, France.",
    "The Great Wall of China is over 21,000 kilometers long.",
    "Python is a programming language created by Guido van Rossum in 1991.",
    "The human heart beats about 100,000 times per day.",
    "Mount Everest is the highest mountain on Earth at 8,849 meters.",
    "Photosynthesis is how plants convert sunlight into energy.",
]
doc_embeddings = embedder.encode(dokumenty)

def kosinova_podobnost(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def najdi_nejlepsi(dotaz):
    dotaz_vektor = embedder.encode([dotaz])[0]
    skore = [(kosinova_podobnost(dotaz_vektor, dv),  i)
             for i, dv in enumerate(doc_embeddings)]
    print(f"    DEBUG pred sort:  {[(round(float(s), 3), i) for s, i in skore]}")
    skore.sort(reverse=True)
    print(f"    DEBUG po sort:  {[(round(float(s), 3), i) for s, i in skore]}")
    nej_sim, nej_idx = skore[0]
    print(f"    DEBUG vybrano: idx={nej_idx}, sim={float(nej_sim):.3f}")
    return dokumenty[nej_idx], nej_sim



def odpovez_z_kontextu(otazka, kontext):
    vstup = qa_tokenizer(otazka, kontext, return_tensors="pt").to(device)
    with torch.no_grad():
        vystup = qa_model(**vstup)
    start = torch.argmax(vystup.start_logits)
    end = torch.argmax(vystup.end_logits) + 1
    tokeny = vstup["input_ids"][0][start:end]
    return qa_tokenizer.decode(tokeny)


def rag(otazka):

    kontext, sim = najdi_nejlepsi(otazka)

    odpoved = odpovez_z_kontextu(otazka, kontext)
    return odpoved, kontext, sim

otazky = [
     "How tall is the Eiffel Tower?",
    "Who created Python?",
    "How long is the Great Wall?",
    "What is the highest mountain?",
]

for otazka in otazky:
    odpoved, kontext, sim = rag(otazka)
    print(f"OTÁZKA: {otazka}")
    print(f"    Nalezeny dokument [{sim:.3f}]: {kontext}")
    print(f"    ODPOVĚĎ: {odpoved}\n")
