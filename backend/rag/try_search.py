"""See chunk size, overlap and characters per chunk (run from backend/):
uv run python -m rag.try_chunks
"""
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from rag.data_ingestion import CHUNK_SIZE, CHUNK_OVERLAP, split_into_chunks

PDF = Path(__file__).resolve().parents[2] / "sample_docs" / "aldermoor_procurement_policy.pdf"


def shared_overlap(a: str, b: str) -> int:
    """Length of the longest ending of `a` that is also the start of `b`."""
    for n in range(min(len(a), len(b)), 0, -1):
        if a.endswith(b[:n]):
            return n
    return 0


pages = PyPDFLoader(str(PDF)).load()
chunks = split_into_chunks(pages)

print(f"File:          {PDF.name}")
print(f"chunk_size:    {CHUNK_SIZE}  (maximum characters per chunk)")
print(f"chunk_overlap: {CHUNK_OVERLAP}  (maximum characters shared with the next chunk)")
print(f"Pages: {len(pages)}   Chunks: {len(chunks)}")
print(f"Total characters in all pages: {sum(len(p.page_content) for p in pages)}")
print("-" * 70)

for i, chunk in enumerate(chunks):
    text = chunk.page_content
    print(f"Chunk {i + 1} | page {chunk.metadata.get('page')} | characters: {len(text)}")
    print(f"  starts: {text[:60]!r}")
    print(f"  ends:   {text[-60:]!r}")
    if i > 0:
        overlap = shared_overlap(chunks[i - 1].page_content, text)
        print(f"  overlap with previous chunk: {overlap} characters")
    print()