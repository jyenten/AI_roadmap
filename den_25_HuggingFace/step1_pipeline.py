from transformers import pipeline

klasifikator = pipeline("sentiment-analysis")

vysledek = klasifikator("I love this movie, it was fanstastic!")
print(vysledek)


vety = [
    "This film is amazing!",
    "Worst movie I have ever seen.",
    "It was okay, nothing special.",
]
vysledky = klasifikator(vety)

print("\n--- Vice vet ---")
for veta, v in zip(vety, vysledky):
    print(f"    {veta!r:40} -> {v['label']} ({v['score']:.2f})")




