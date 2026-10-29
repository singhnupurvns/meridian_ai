"""Compare meanings with real embeddings (run from backend/): uv run python -m rag.try_embeddings"""
import math
from rag.embeddings import get_embeddings

embeddings = get_embeddings()

question = "When do we pay servo motor suppliers?"
texts = [
    "Servo motor are paid Net-45 terms.",
    "Filling line equipment in depreciated over 10 years.",
    "Revenue in FY2024 was EUR2.84 billion",
]

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

question_vector = embeddings.embed_query(question)
text_vectors = embeddings.embed_documents(texts)

print("numbers per question:", len(question_vector))
print(question_vector)
print("first four numbers:", [round(x, 3) for x in question_vector[:4]])
print()
print("Question:", question)


for text, vector in zip(texts, text_vectors):
    print(f"{cosine(question_vector, vector):.2f}  | numbers per text: {len(vector)}  | {text}")
