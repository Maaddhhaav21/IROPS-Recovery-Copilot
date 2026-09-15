import chromadb
from sentence_transformers import SentenceTransformer

from app.rag.ingest import load_pdfs, split_documents


MODEL_NAME = "BAAI/bge-base-en-v1.5"

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="irops_policies"
)

model = SentenceTransformer(MODEL_NAME)


def build_vectorstore():
    documents = load_pdfs()
    chunks = split_documents(documents)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    metadatas = [
        {
            "source": chunk["source"]
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB")


if __name__ == "__main__":
    build_vectorstore()