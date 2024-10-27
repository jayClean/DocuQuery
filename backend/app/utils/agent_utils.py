import logging
import autogen
import asyncio
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from app.config import settings
import time

# Set up a logger
logger = logging.getLogger(__name__)

config_list = [
    {
        "api_key": settings.openai_api_key,  # Loaded from environment variables
        "api_rate_limit": 60.0  # Set to allow up to 60 API requests per second
    }
]

# Instantiate AssistantAgent and RetrieveUserProxyAgent as described earlier
assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant that answers questions based on the provided document content. Always consider the user's context.",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,  # Ensure config_list is defined with appropriate models
    },
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",  # Adjust to "ALWAYS" if you want interactive user input for each step
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "question_answering",
        "docs_path": [
            # Add paths or URLs to parsed document contents
        ],
        "chunk_token_size": 2000,  # Adjust based on document length
        "vector_db": "chroma",
        "overwrite": False,
        "get_or_create": True,
    },
    code_execution_config=False,
)

async def rate_limited_request(model, messages):
    """Implement rate limiting for API requests."""
    if model == "gpt-3.5-turbo":
        await asyncio.sleep(20)  # Sleep for 20 seconds to respect RPM
    # Here, implement the logic to send your request to the model
    return await send_request_to_model(model, messages)

async def send_request_to_model(model, messages):
    """Send a request to the model with the required arguments."""
    response = await ragproxyagent.initiate_chat(
        assistant,
        messages=messages,  # Pass messages directly
        model=model  # Specify the model
    )
    return response

async def batch_process_prompts(prompts):
    """Batch process prompts to adhere to API limits."""
    batched_prompts = []
    current_batch = []
    current_tokens = 0
    
    for prompt in prompts:
        token_count = len(prompt.split())  # Estimate token count
        if current_tokens + token_count > 200000:  # Check batch limit
            batched_prompts.append(current_batch)
            current_batch = []
            current_tokens = 0
        current_batch.append({"role": "user", "content": prompt})  # Format as message
        current_tokens += token_count
    
    if current_batch:
        batched_prompts.append(current_batch)
    
    return batched_prompts

async def query_agent(query: str, user_context: str) -> str:
    # Construct prompt combining user context and query
    prompt = f"User context: {user_context}. Query: {query}"
    
    logger.info("Querying agent with prompt: %s", prompt)

    # Create messages list
    messages = [
        {"role": "system", "content": assistant.system_message},
        {"role": "user", "content": prompt}
    ]
    
    try:
        # Process the prompt with rate limiting
        response = await rate_limited_request("gpt-3.5-turbo", messages)
        
        logger.info("Received response from agent: %s", response)
        
    except Exception as e:
        logger.error("Error while querying the agent: %s", str(e))
        response = "An error occurred while processing your request."
    
    return response