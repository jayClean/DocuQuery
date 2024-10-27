# import logging
# from langchain.embeddings import OpenAIEmbeddings  # Replace with the actual embedding model
# from app.config import settings

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Initialize the embeddings model (e.g., OpenAI Embeddings)
# embedding_model = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

# def generate_query_embedding(query: str):
#     """
#     Generate an embedding for the given query string.

#     Args:
#         query (str): The query string to be embedded.

#     Returns:
#         list: The embedding of the query as a list of floats.
#     """
#     try:
#         logger.info("Generating embedding for query: %s", query)
        
#         # Generate the embedding for the query
#         embedding = embedding_model.embed_query(query)
        
#         # Log the embedding for debugging purposes (limit log length to avoid excessive output)
#         if embedding:
#             logger.info("Embedding generated successfully. Sample values: %s", str(embedding[0][:5]) + "...")
#         else:
#             logger.warning("Embedding generation returned an empty result.")
        
#         # Return the first (and only) embedding as a list
#         return embedding[0] if embedding else []
        
#     except Exception as e:
#         logger.error("Error generating query embedding: %s", str(e))
#         return []

import logging
from sentence_transformers import SentenceTransformer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the sentence transformer model (e.g., 'all-MiniLM-L6-v2')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_query_embedding(query: str):
    """
    Generate an embedding for the given query string.

    Args:
        query (str): The query string to be embedded.

    Returns:
        list: The embedding of the query as a list of floats.
    """
    try:
        logger.info("Generating embedding for query: %s", query)

        # Generate the embedding for the query
        embedding = embedding_model.encode(query, convert_to_tensor=True)

        # Log the embedding for debugging purposes (limit log length to avoid excessive output)
        if embedding is not None:
            logger.info("Embedding generated successfully. Sample values: %s", str(embedding[:5]) + "...")
        else:
            logger.warning("Embedding generation returned an empty result.")
        
        # Return the embedding as a list
        return embedding.tolist()  # Convert tensor to list

    except Exception as e:
        logger.error("Error generating query embedding: %s", str(e))
        return []
