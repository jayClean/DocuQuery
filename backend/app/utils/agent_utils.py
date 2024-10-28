import os
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import openai
from app.config import settings
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Load assistant ID from environment variables
assistant_id = os.environ.get("ASSISTANT_ID", None)

# Define the configuration list with model and API key
config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": settings.openai_api_key,
        "api_rate_limit": 60.0
    }
]

# Define assistant configuration with tools and no human input mode
assistant_config = {
    "tools": [
        {"type": "file_search"}
    ],
    "human_input_mode": "NEVER"  # Disables manual input prompts
}

# Instantiate the OpenAI agent
oai_agent = GPTAssistantAgent(
    name="oai_agent",
    instructions="I'm an OpenAI assistant running in autogen",
    llm_config={
        "config_list": config_list,
    },
    assistant_config=assistant_config,
)

# Instantiate the User Proxy Agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config=False,
    human_input_mode="ALWAYS"  # Ensures no human input prompts
)

# Function to query the agent via user_proxy
async def query_agent(query: str):
    try:
        # user_proxy initiates chat with oai_agent on behalf of the user
        response = await user_proxy.initiate_chat(
            recipient=oai_agent,
            messages=[
                {"role": "user", "content": query}
            ],
            model="gpt-3.5-turbo",  # Specify the model if needed
        )
        return response
    # except openai.error.RateLimitError:
    #     logger.error("Rate limit exceeded, try again later.")
    #     return "Service is temporarily unavailable due to rate limits. Please try again later."
    except Exception as e:
        logger.error("Error while querying the agent: %s", str(e))
        return "An error occurred while processing your request."
