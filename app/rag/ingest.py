from pathlib import Path
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter


KNOWLEDGE_DIR = Path("knowledge")


def load_pdfs():
    documents = []

    for pdf_file in KNOWLEDGE_DIR.glob("*.pdf"):
        pdf = fitz.open(pdf_file)

        text = ""

        for page in pdf:
            text += page.get_text()

        documents.append({
            "source": pdf_file.name,
            "text": text
        })

        pdf.close()

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for document in documents:
        text_chunks = splitter.split_text(document["text"])

        for chunk in text_chunks:
            chunks.append({
                "source": document["source"],
                "text": chunk
            })

    return chunks


if __name__ == "__main__":
    documents = load_pdfs()

    print(f"Loaded {len(documents)} PDF files")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    for i, chunk in enumerate(chunks[:5]):
        print("\n--------------------")
        print(f"Chunk {i + 1}")
        print("Source:", chunk["source"])
        print(chunk["text"])