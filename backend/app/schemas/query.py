from pydantic import BaseModel

class QueryResult(BaseModel):
    # doc_id: str  # Document ID (as a string)
    content: str  # The content of the document
    # score: float  # Relevance score of the document (optional)

class QueryRequest(BaseModel):
    query: str