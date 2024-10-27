from elasticsearch import AsyncElasticsearch
from app.config import settings
from app.utils.nlp_utils import generate_query_embedding
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

es_client = AsyncElasticsearch([settings.elasticsearch_url],
                               verify_certs=False)

async def index_document(doc_id: int, embedding: list, user_id: int):
    try:
        await es_client.index(
            index="documents",
            id=doc_id,
            body={
                "embedding": embedding,
                "user_id": user_id
            }
        )
        logger.info(f"Document {doc_id} indexed successfully.")
    except Exception as e:
        logger.error(f"Error indexing document {doc_id}: {str(e)}")

async def search_documents(query: str, user_id: int):
    try:
        query_embedding = generate_query_embedding(query)
        logger.info("Query embedding generated: %s", query_embedding)

        if not query_embedding:  # Check if embedding is generated
            logger.error("Query embedding is empty, aborting search.")
            return []

        search_query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "script_score": {
                                "query": {"match_all": {}},
                                "script": {
                                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                    "params": {"query_vector": query_embedding}
                                }
                            }
                        },
                        # {"term": {"user_id": user_id}}
                    ]
                }
            }
        }

        logger.info("Executing search query: %s", search_query)

        response = await es_client.search(index="documents", body=search_query)

        logger.info(f"Search returned {len(response['hits']['hits'])} documents.")

        return [
            {
                "doc_id": hit["_id"],
                "score": hit["_score"],
            }
            for hit in response["hits"]["hits"]
        ]
    except Exception as e:
        logger.error("Error querying documents: %s", str(e))
        if hasattr(e, 'info'):
            logger.error("Elasticsearch error details: %s", e.info)
        return []
