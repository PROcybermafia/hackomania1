from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
import shutil
import uuid

app = FastAPI()

# Schema for indexing
schema = Schema(id=ID(stored=True, unique=True), content=TEXT(stored=True))

# Create index directory
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
else:
    ix = open_dir("indexdir")

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8")  # assumes plain text files
    doc_id = str(uuid.uuid4())

    # Index the content
    writer = ix.writer()
    writer.add_document(id=doc_id, content=text)
    writer.commit()

    return {"message": "Document uploaded", "id": doc_id}

@app.get("/search/")
async def search(query: str):
    results_list = []
    with ix.searcher() as searcher:
        parser = QueryParser("content", schema=ix.schema)
        myquery = parser.parse(query)
        results = searcher.search(myquery, limit=10)
        for r in results:
            results_list.append({"id": r['id'], "snippet": r.highlights("content")})
    return JSONResponse(content={"results": results_list})
