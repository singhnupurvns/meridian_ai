from rag.vector_store import get_vector_store
from rag.data_ingestion import ingest_pdf

PDF = "../sample_docs/aldermoor_procurement_policy.pdf"
Source = "local://aldermoor_procurement_policy.pdf"

def ids_for_source():
    # Only the chunks that came from this PDF
    return get_vector_store().get(where={"source": Source})["ids"]

print("first run: ", ingest_pdf(PDF, Source))
ids_1 = ids_for_source()
print("ids after first run :", ids_1)

print("second run:", ingest_pdf(PDF, Source))
ids_2 = ids_for_source()
print("ids after second run:", ids_2)

print("same IDs?      ", sorted(ids_1) == sorted(ids_2))
print("same count?    ", len(ids_1) == len(ids_2))