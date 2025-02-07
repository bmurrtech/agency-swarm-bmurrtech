import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

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
