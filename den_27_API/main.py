from fastapi import FastAPI
from pydantic import BaseModel
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

app = FastAPI()


print("Načítám modely... (chvili to potrva)")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

qa_nazev = "distilbert-base-cased-distilled-squad"
qa_tokenizer = AutoTokenizer.from_pretrained(qa_nazev)
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_nazev).to(device)
qa_model.eval()

dokumenty = [
    "The Eiffel Tower is 330 meters tall and located in Paris, France.",
    "The Great Wall of China is over 21,000 kilometers long.",
    "Python is a programming language created by Guido van Rossum in 1991.",
    "The human heart beats about 100,000 times per day.",
    "Mount Everest is the highest mountain on Earth at 8,849 meters.",
    "Photosynthesis is how plants convert sunlight into energy.",
]

doc_embeddings = embedder.encode(dokumenty)
print("Modely nacteny, API je pripraveno!")


def kosinova_podobnost(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def najdi_nejlepsi(dotaz):
    dotaz_vektor = embedder.encode([dotaz])[0]
    skore = np.array([kosinova_podobnost(dotaz_vektor, dv) for dv in doc_embeddings])
    nej_idx = int(np.argmax(skore))
    return dokumenty[nej_idx], float(skore[nej_idx])

def odpovez_z_kontextu(otazka, kontext):
    vstup = qa_tokenizer(otazka, kontext, return_tensors="pt").to(device)
    with torch.no_grad():
        vystup = qa_model(**vstup)
    start = torch.argmax(vystup.start_logits)
    end = torch.argmax(vystup.end_logits) + 1
    tokeny = vstup["input_ids"][0][start:end]
    return qa_tokenizer.decode(tokeny)

@app.get("/")
def domovska_stranka():
    return{"zprava": "RAG API bezi! Jdi na /docs to vyzkouset."}

class Dotaz(BaseModel):
    otazka: str

@app.post("/zeptej-se")
def zeptej_se(dotaz: Dotaz):

    kontext, sim = najdi_nejlepsi(dotaz.otazka)

    odpoved = odpovez_z_kontextu(dotaz.otazka, kontext)
    return{
        "otazka": dotaz.otazka,
        "odpoved": odpoved,
        "zdroj": kontext,
        "podobnost": round(sim, 3)

    }

