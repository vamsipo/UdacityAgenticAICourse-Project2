# TODO: 1 - Import the KnowledgeAugmentedPromptAgent and RoutingAgent
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, RoutingAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

persona = "You are a college professor"

knowledge_texas = "You know everything about Texas"
# TODO: 2 - Define the Texas Knowledge Augmented Prompt Agent
texas_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge_texas)

knowledge_europe = "You know everything about Europe"
# TODO: 3 - Define the Europe Knowledge Augmented Prompt Agent
europe_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge_europe)

persona_math = "You are a college math professor"
knowledge_math = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"
# TODO: 4 - Define the Math Knowledge Augmented Prompt Agent
math_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_math, knowledge_math)

routing_agent = RoutingAgent(openai_api_key, {})
agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas",
        "func": lambda x: texas_agent.respond(x)  # TODO: 5 - Call the Texas Agent to respond to prompts
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe",
        "func": lambda x: europe_agent.respond(x)  # TODO: 6 - Define a function to call the Europe Agent
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        "func": lambda x: math_agent.respond(x)  # TODO: 7 - Define a function to call the Math Agent
    }
]

routing_agent.agents = agents

# TODO: 8 - Print the RoutingAgent responses to the following prompts:
#           - "Tell me about the history of Rome, Texas"
#           - "Tell me about the history of Rome, Italy"
#           - "One story takes 2 days, and there are 20 stories"

print("ROUTING AGENT TEST RESULTS:")
print("="*60)

test_prompts = [
    "Tell me about the history of Rome, Texas",
    "Tell me about the history of Rome, Italy", 
    "One story takes 2 days, and there are 20 stories"
]

for i, prompt in enumerate(test_prompts, 1):
    print(f"\nTest {i}: {prompt}")
    print("-" * 50)
    response = routing_agent.route(prompt)
    print(f"Response: {response}")
    print()

print("="*60)
print("ROUTING AGENT ANALYSIS:")
print("="*60)
print("This demonstrates the RoutingAgent's ability to:")
print("1. Calculate embeddings for user prompts and agent descriptions")
print("2. Use cosine similarity to find the best matching agent")
print("3. Route different types of queries to appropriate specialized agents")
print("4. Handle geographic queries (Texas vs Europe)")
print("5. Identify mathematical content and route to math specialist")
