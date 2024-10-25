from fastapi import FastAPI
from app.database import engine, Base
from app.routes.auth import router as user_router
from app.routes.document import router as document_router

# Create the database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

# Include user-related routes
app.include_router(user_router, prefix="/users", tags=["users"])

# Include document upload routes
app.include_router(document_router, prefix="/documents", tags=["Documents"])

# @app.on_event("startup")
# async def startup_event():
#     await create_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to DocuQuery!"}
