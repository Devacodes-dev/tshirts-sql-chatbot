from groq import Groq
import os

print("API KEY FOUND:", bool(os.getenv("GROQ_API_KEY")))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()
for m in models.data:
    print(m.id)
