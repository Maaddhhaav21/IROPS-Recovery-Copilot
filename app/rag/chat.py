import os

from dotenv import load_dotenv
from groq import Groq
import chromadb
from sentence_transformers import SentenceTransformer


load_dotenv()


MODEL_NAME = "BAAI/bge-base-en-v1.5"
LLM_MODEL = "openai/gpt-oss-20b"


# -----------------------------
# ChromaDB
# -----------------------------

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="irops_policies"
)


# -----------------------------
# Embedding model
# -----------------------------

embedding_model = SentenceTransformer(MODEL_NAME)


# -----------------------------
# Groq
# -----------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# Retrieve policy
# -----------------------------

def retrieve_policy(question, k=3):

    query_embedding = embedding_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    documents = results["documents"][0]
    sources = results["metadatas"][0]

    return documents, sources


# -----------------------------
# Generate answer
# -----------------------------

def ask_irop_assistant(question):

    documents, sources = retrieve_policy(question)

    context = "\n\n".join(documents)

    prompt = f"""
You are the IROPS Recovery Copilot policy assistant.

Answer the user's question using ONLY the policy context
provided below.

Do not invent airline policies.

If the policy context does not contain enough information,
say:

"I don't have enough information in the available policies."

Policy Context:
----------------
{context}
----------------

User Question:
{question}

Give a concise and clear operational answer.
"""

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer, sources


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    question = "What is the priority for passengers with onward connections?"

    answer, sources = ask_irop_assistant(question)

    print("\n==============================")
    print("IROPS ASSISTANT")
    print("==============================")

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")
    for source in sources:
        print("-", source["source"])