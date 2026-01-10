from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY").strip(),
    model="llama-3.1-8b-instant"
)

response = llm.invoke("Say OK")
print(response.content)
