# test_oai_key.py explainer

"""
This script determines what OpenAI models the API key set in the .env file has access to use.
It is helpful when encountering model-specific errors such as: 
- "Model not found" or "Access denied for the specified model".

By running this script, you can verify which models are available for your API key, allowing you to adjust your application accordingly.
"""

# Example of setting the model_name in individual agent files:
"""
In each agent file (e.g., chat_wizard.py), it is necessary to set the model_name to ensure that the agent uses a model that the API key has access to.
This prevents conflicts and errors related to model access. 

For instance, in chat_wizard.py, you would do the following:

from agency_swarm import Agent
import os
from dotenv import load_dotenv

class ChatWizardAgent(Agent):
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get model name from environment variable
        model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini-2024-07-18')
        
        super().__init__(
            name="ChatWizard",
            description="Manages user interaction and orchestrates the brand building process by engaging users, collecting inputs, and coordinating with specialized agents.",
            instructions="chat_wizard/instructions.md",
            tools_folder="chat_wizard/tools",
            temperature=0.5,
            max_prompt_tokens=25000,
            model=model_name  # Set model from environment variable
        )
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# You can set the model name in your .env file like so:
"""
OPENAI_MODEL_NAME=gpt-4o-mini-2024-07-18
"""

def list_models():
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: API key is missing! Please set OPENAI_API_KEY in your environment variables.")
        return
    
    try:
        # Initialize the client
        client = OpenAI(api_key=api_key)
        
        # List available models
        models = client.models.list()
        
        print("\nAvailable models for your API key:")
        print("----------------------------------")
        for model in models.data:
            print(f"- {model.id}")
            
    except Exception as e:
        print(f"\nError accessing OpenAI API: {str(e)}")
        print("\nThis could be due to:")
        print("1. Invalid API key")
        print("2. Network connectivity issues")
        print("3. API access restrictions")
        print("\nPlease verify your API key and permissions in your OpenAI account.")

if __name__ == "__main__":
    list_models()
