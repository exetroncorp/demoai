from smolagents import CodeAgent, tool
from smolagents.models import OpenAIServerModel

# Define the whalator tool
@tool
def whalator(text: str) -> str:
    """
    Adds whale emojis around the input string.
    
    Args:
        text: The text to add whale emojis around
        
    Returns:
        The input text surrounded by whale emojis
    """
    return f"🐋 {text} 🐋"

def main():
    print("🐋 Hello World SmoLAgent with Whalator Tool! 🐋")
    print("=" * 50)
    
    # Initialize the OpenAI-compatible model
    model = OpenAIServerModel(
        base_url="tôt",
        api_key="robert",
        model_name="gpt-3.5-turbo"  # or whatever model you're using
    )
    
    # Create the agent with the whalator tool
    agent = CodeAgent(
        tools=[whalator],
        model=model,
        verbose=True
    )
    
    # Test the agent
    print("Testing the whalator tool...")
    print()
    
    # Example 1: Direct request to use the tool
    result1 = agent.run("Use the whalator tool on the text 'Hello World'")
    print(f"Result 1: {result1}")
    print()
    
    # Example 2: More natural request
    result2 = agent.run("Can you add whale emojis around 'Python is awesome'?")
    print(f"Result 2: {result2}")
    print()
    
    # Example 3: Interactive conversation
    print("Interactive mode (type 'quit' to exit):")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("🐋 Goodbye! 🐋")
            break
        
        if user_input:
            try:
                response = agent.run(user_input)
                print(f"Agent: {response}")
                print()
            except Exception as e:
                print(f"Error: {e}")
                print()

if __name__ == "__main__":
    # You might need to install smolagents first:
    # pip install smolagents
    main()
