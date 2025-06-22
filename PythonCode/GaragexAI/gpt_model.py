from transformers import pipeline

def generate_response(prompt):
    gpt = pipeline("text-generation", model="gpt2")
    result = gpt(prompt, max_length=50)[0]['generated_text']
    print("🤖 GPT replied:", result)
    return result