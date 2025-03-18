import torch
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration


def generate_answer(question, retrieved_text):
    model_name = "facebook/rag-sequence-nq"
    tokenizer = RagTokenizer.from_pretrained(model_name)
    generator = RagSequenceForGeneration.from_pretrained(model_name).to("cuda")
    inputs = f"Query: {question}\n : \n{retrieved_text}"
    inputs.to("cuda")
    
    with torch.no_grad():
        generated = generator.generate(**inputs)
    
    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
