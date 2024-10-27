from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.auth import router as user_router
from app.routes.document import router as document_router
from app.routes.query import router as query_router

# Create the database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

# Set CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Include user-related routes
app.include_router(user_router, prefix="/users", tags=["users"])

# Include document upload routes
app.include_router(document_router, prefix="/documents", tags=["Documents"])

app.include_router(query_router, prefix="/search", tags=["Document Search"])

# @app.on_event("startup")
# async def startup_event():
#     await create_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to DocuQuery!"}
