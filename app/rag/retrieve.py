import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-base-en-v1.5"

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="irops_policies"
)

model = SentenceTransformer(MODEL_NAME)


def search_policy(question, k=3):
    query_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results


if __name__ == "__main__":

    question = "What is the priority for passengers with onward connections?"

    results = search_policy(question)

    for i, document in enumerate(results["documents"][0]):
        print("\n--------------------")
        print(f"Result {i + 1}")
        print("Source:", results["metadatas"][0][i])
        print(document)