from pydantic import BaseModel

class DocumentMetadataResponse(BaseModel):
    id: int
    filename: str
    s3_url: str
    parsed_data: str

    class Config:
        from_attributes = True