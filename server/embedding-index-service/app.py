from fastapi import FastAPI
import chromadb
from pydantic import BaseModel
from typing import Optional, Dict, List

chroma_client = chromadb.Client()


app = FastAPI()

class CollectionCreateRequest(BaseModel):
    collection_name: str
    metadata: Optional[Dict[str, str]] = None

class CollectionAddItemRequest(BaseModel):
    id: str
    content: str
    metadata: Optional[Dict[str, str]] = None

class CollectionAddItemsRequest(BaseModel):
    items: List[CollectionAddItemRequest]


@app.post("/collections/create",summary = "creates a new collection")
def create_collection(collection_create_req: CollectionCreateRequest):
    
    try:
        collection = chroma_client.create_collection(
            name = collection_create_req.collection_name,
            metadata=collection_create_req.metadata
        )
        return {"message": "successfully created collection"}
    except:
        raise HTTPException(status_code=404, detail="Error occurred while attempting to create collection")


@app.post("/collections/add", summary="Add items with ids and metadata to a collection")
def add_items_to_collection(req: CollectionAddItemsRequest):
    try:
            collection = chroma_client.get_collection(collection_name)
            for item in req.items:
                collection.add(
                    ids=[item.id],
                    documents=[item.content],
                    metadatas=[item.metadata] if item.metadata else None
                )
            return {"message": f"Added {len(req.items)} items to collection '{collection_name}'."}
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))



@app.post("/collections", summary = "List all collections")
def get_collections():
    
    return [collection.name for collection in chroma_client.list_collections()]