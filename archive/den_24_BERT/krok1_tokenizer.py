from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

veta = "this movie is great"

tokeny = tokenizer.tokenize(veta)
print("Věta: ", veta)
print("Tokeny: ", tokeny)

ids = tokenizer.convert_tokens_to_ids(tokeny)
print("Tokend ID: ", ids)

encoded = tokenizer(veta)
print("\nKompletni zakodovani: ")
print(" input_ids: ", encoded["input_ids"])
print("     rozkodovano zpet: ", tokenizer.convert_ids_to_tokens(encoded["input_ids"]))

divna_slova = ["unbelievable", "cryptocurrency", "tokenization", "blizzard", 
"antidisestablishmentarianism"]
for slovo in divna_slova:
    print(f" {slovo!r:35} -> {tokenizer.tokenize(slovo)}")
