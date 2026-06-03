import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

# model natrénovaný přímo na question answering (SQuAD dataset)
nazev = "distilbert-base-cased-distilled-squad"
tokenizer = AutoTokenizer.from_pretrained(nazev)
model = AutoModelForQuestionAnswering.from_pretrained(nazev).to(device)
model.eval()

kontext = """
The Eiffel Tower is located in Paris, France. It was built in 1889 
and is 330 meters tall. It was designed by Gustave Eiffel.
"""

def odpovez(otazka):
    # zakóduj otázku + kontext dohromady
    vstup = tokenizer(otazka, kontext, return_tensors="pt").to(device)
    with torch.no_grad():
        vystup = model(**vstup)
    # model vrací skóre pro ZAČÁTEK a KONEC odpovědi v textu
    start = torch.argmax(vystup.start_logits)
    end = torch.argmax(vystup.end_logits) + 1
    # vytáhni tokeny mezi start a end a převeď zpět na text
    tokeny = vstup["input_ids"][0][start:end]
    return tokenizer.decode(tokeny)

otazky = [
    "How tall is the Eiffel Tower?",
    "Who designed it?",
    "When was it built?",
    "Where is it located?",
]

print()
for otazka in otazky:
    print(f"  Q: {otazka}")
    print(f"  A: {odpovez(otazka)}\n")