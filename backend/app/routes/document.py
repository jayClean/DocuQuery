from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.s3 import upload_to_s3
from app.services.parsing import parse_document
from app.models.users import DocumentMetadata
from app.schemas.document import DocumentMetadataResponse
from app.dependencies.user import get_current_user
from app.database import get_db
from app.schemas.user import UserResponse
from app.utils.elasticsearch_utils import index_document

router = APIRouter()

@router.post("/upload", response_model=DocumentMetadataResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Step 1: Read file contents into memory
        file_bytes = await file.read()

        # Step 2: Reset the file pointer to the beginning for uploading
        file.file.seek(0)

        # Step 3: Upload file to S3
        s3_url = await upload_to_s3(file.file, file.filename)

        # Step 4: Parse the document
        parsed_data = await parse_document(s3_url)

        # Step 5: Save metadata and parsed data to DB
        new_document = DocumentMetadata(
            filename=file.filename,
            s3_url=s3_url,
            user_id=current_user.id,
            parsed_data=parsed_data  # This assumes parsed_data can be serialized
        )
        db.add(new_document)
        await db.commit()
        await db.refresh(new_document)

        # await index_document(new_document.id, parsed_data, current_user.id)
        
        return new_document
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.get("/documents", response_model=List[DocumentMetadataResponse])
async def get_documents(current_user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DocumentMetadata).filter(DocumentMetadata.user_id == current_user.id)
    )
    documents = result.scalars().all()
    return documents

@router.get("/{document_id}", response_model=DocumentMetadataResponse)
async def get_document(document_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DocumentMetadata).filter(DocumentMetadata.id == document_id)
    )
    document = result.scalars().first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
