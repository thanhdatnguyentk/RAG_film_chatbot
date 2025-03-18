import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it").to("cuda")
def generate_answer(question, retrieved_text):
    inputs = f"Query: {question}\n : \n{retrieved_text}"
    print(inputs)
    inputs = tokenizer(inputs, return_tensors="pt").to("cuda")
    with torch.no_grad():
        respone = model.generate(**inputs, max_new_tokens=200)
    outputs = tokenizer.batch_decode(respone, skip_special_tokens=True)[0]
    return outputs
