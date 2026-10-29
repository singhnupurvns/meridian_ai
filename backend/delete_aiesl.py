from rag.vector_store import get_vector_store

SOURCE = "local://Aiesl Employees service regulation.pdf"

store = get_vector_store()
ids = store.get(where={"source": SOURCE})["ids"]
print("chunks found for this source:", len(ids))

if ids:
    store.delete(ids=ids)

print("total chunks now:", len(store.get()["ids"]))