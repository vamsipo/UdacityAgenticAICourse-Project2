# TODO: 1 - Import the KnowledgeAugmentedPromptAgent class from workflow_agents
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"

# TODO: 2 - Instantiate a KnowledgeAugmentedPromptAgent with:
#           - Persona: "You are a college professor, your answer always starts with: Dear students,"
#           - Knowledge: "The capital of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

# Get the response from the agent
response = knowledge_agent.respond(prompt)
print("Agent Response:")
print(response)

# TODO: 3 - Write a print statement that demonstrates the agent using the provided knowledge rather than its own inherent knowledge.
print("\n" + "="*70)
print("DEMONSTRATION OF KNOWLEDGE-BASED RESPONSE:")
print("="*70)
print("This response demonstrates that the KnowledgeAugmentedPromptAgent is using")
print("the PROVIDED KNOWLEDGE rather than its inherent LLM knowledge.")
print()
print("Expected behavior:")
print("- The agent should respond that the capital of France is London (incorrect but as provided)")
print("- This contradicts the LLM's inherent knowledge that Paris is the capital")
print("- The response should start with 'Dear students,' due to the persona")
print("- This proves the agent is following the explicit knowledge instructions")
print("  rather than relying on its pre-trained knowledge")
