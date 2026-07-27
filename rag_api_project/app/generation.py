import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.config import Settings

class AnswerGenerator:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.generation_model_name
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            settings.generation_model_name
        ).to(self.device)

        self.model.eval()
        
    def build_prompt(self, question: str, context: str) -> str:
        return f"""
Use the context to answer the question.
Give one short, direct answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    def generate(self, question: str, context: str) -> str:
        prompt = self.build_prompt(
            question=question,
            context=context,
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.settings.generation_max_new_tokens,
                do_sample=False,
            )
        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        )
        return answer.strip()
            


    