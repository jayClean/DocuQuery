# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from app.models.users import DocumentMetadata  # Import your DocumentMetadata model
# from app.schemas.query import QueryRequest, QueryResult  # Import your request and response schemas
# from app.schemas.user import UserResponse
# from app.dependencies.user import get_current_user, get_db  # Import your dependencies
# from app.utils.agent_utils import query_agent  # Assuming you have a query agent function
# import logging
# from typing import List

# router = APIRouter()
# logger = logging.getLogger(__name__)

# @router.get("/", response_model=List[QueryResult])
# async def search_user_documents(
#     query: QueryRequest,
#     current_user: UserResponse = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     try:
#         # Step 1: Construct the SQL query
#         stmt = (
#             select(DocumentMetadata)
#             .where(DocumentMetadata.user_id == current_user.id)
#             .where(DocumentMetadata.parsed_data.ilike(f"%{query.query}%"))  # Assuming you're searching in parsed_data
#         )

#         # Step 2: Execute the query
#         result = await db.execute(stmt)
#         documents = result.scalars().all()  # Retrieve the documents

#         # Prepare the response list
#         query_results = []

#         # If there are results, use the agent to formulate a response
#         if documents:
#             user_context = f"User ID: {current_user.id}. Documents: {', '.join([str(doc.id) for doc in documents])}."
#             agent_response = await query_agent(query.query, user_context)

#             # Build the list of QueryResult
#             for doc in documents:
#                 query_results.append(QueryResult(
#                     doc_id=doc.id,
#                     content=doc.parsed_data,  # Assuming parsed_data contains the relevant content
#                     # Add any other necessary fields based on your QueryResult schema
#                 ))

#             return query_results  # Return the list of QueryResult objects
#         else:
#             # If no documents are found, return an empty list
#             return []

#     except Exception as e:
#         logger.error(f"Error querying documents: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error querying documents: {str(e)}")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.users import DocumentMetadata
from app.schemas.query import QueryRequest, QueryResult
from app.schemas.user import UserResponse
from app.dependencies.user import get_current_user, get_db
from app.utils.agent_utils import query_agent
import logging
from typing import List
from sqlalchemy import func

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=QueryResult)
async def search_user_documents(
    query: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"User {current_user.id} initiated a search with query: {query}")

    try:
        # Construct the SQL query for PostgreSQL
        stmt = (
            select(DocumentMetadata)
            .where(DocumentMetadata.user_id == current_user.id)
            .where(
                func.to_tsvector('english', DocumentMetadata.parsed_data).op('@@')(
                    func.plainto_tsquery('english', query)
                )
            )
        )

        # Execute the query
        result = await db.execute(stmt)
        documents = result.scalars().all()

        logger.info(f"Found {len(documents)} documents for user {current_user.id}")

        query_results = []
        for doc in documents:
            # Assuming score is calculated somehow, if not, you can set a default value
            score = 0  # Replace this with the actual score calculation if applicable

            query_results.append(QueryResult(
                doc_id=str(doc.id),  # Convert doc_id to string
                content=doc.parsed_data,
                score=score  # Include the score in the response
            ))

        # Use the agent to generate a response based on the query and results
        # Combine user context and query into a single prompt
        combined_prompt = f"User context: User ID - {current_user.id}. Found documents: {', '.join([res.content for res in query_results])}. Query: {query}"

        # Send the combined prompt to the agent
        agent_response = await query_agent(combined_prompt)

        print(agent_response)

        return {
            "content": agent_response  # Include agent's response in the output
        }

    except Exception as e:
        logger.error(f"Error querying documents for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying documents: {str(e)}")


