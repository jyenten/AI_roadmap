from transformers import pipeline

print(" === 1) Zero-shot klasifikace ===")
zero_shot = pipeline("zero-shot-classification")

text = "I just bought a new graphics card for deeep learning."
tridy = ["technology", "cooking", "sport", "politics",]
vysledek = zero_shot(text, candidate_labels=tridy)

print(f"Text: {text!r}")
for label, score in zip(vysledek["labels"], vysledek["scores"]):
    print(f"    {label:12} -> {score:.3f}")


print("\n ===2) Shrnuti textu ===")
summarizer = pipeline("text2text-generation", model="facebook/bart-large-cnn")

dlouhy_text = """
Artificial intelligence has rapidly evolved over the past decade. 
Deep learning models, especially transformers, have revolutionized 
natural language processing. These models can now translate languages, 
answer questions, and even write code. However, they require enormous 
amounts of data and computing power to train effectively.
"""
shrnuti = summarizer(dlouhy_text, max_lenght=40, min_lenght=10)
print("Shrnuti:", shrnuti[0]["summary_text"])

print("\n=== 3) Question answering ===")
qa = pipeline("question-answering")

kontext = """
The Eiffel Tower is located in Paris, France. It was built in 1889 
and is 330 meters tall. It was designed by Gustave Eiffel.
"""

otazka = "How tall is the Eiffel Tower ?"
odpoved = qa(question=otazka, context=kontext)
print(f"Otazka:     {otazka}")
print(f"Odpoved:    {odpoved['answer']} (jistota: {odpoved['score']:.2f})")


