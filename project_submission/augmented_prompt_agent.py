# TODO: 1 - Import the AugmentedPromptAgent class
from workflow_agents.base_agents import AugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# TODO: 2 - Instantiate an object of AugmentedPromptAgent with the required parameters
augmented_agent = AugmentedPromptAgent(openai_api_key, persona)

# TODO: 3 - Send the 'prompt' to the agent and store the response in a variable named 'augmented_agent_response'
augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# TODO: 4 - Add a comment explaining:
# - What knowledge the agent likely used to answer the prompt.
# - How the system prompt specifying the persona affected the agent's response.

print("\n" + "="*60)
print("ANALYSIS OF AUGMENTED PROMPT AGENT RESPONSE:")
print("="*60)

print("\nKnowledge Source:")
print("- The agent used the same general knowledge from GPT-3.5-turbo's training data")
print("- This includes factual information about world geography and capital cities")
print("- No additional external knowledge sources were provided to the agent")

print("\nPersona Impact:")
print("- The system prompt instructed the agent to adopt a 'college professor' persona")
print("- This caused the response to start with 'Dear students,' as specified")
print("- The persona likely influenced the tone to be more educational and formal")
print("- The response structure became more pedagogical, suitable for a classroom setting")
print("- The agent 'forgot all previous context' as instructed in the system prompt")
