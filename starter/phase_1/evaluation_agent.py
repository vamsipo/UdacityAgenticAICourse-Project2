# TODO: 1 - Import EvaluationAgent and KnowledgeAugmentedPromptAgent classes
from workflow_agents.base_agents import EvaluationAgent, KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
prompt = "What is the capital of France?"

# Parameters for the Knowledge Agent
persona_knowledge = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capitol of France is London, not Paris"
# TODO: 2 - Instantiate the KnowledgeAugmentedPromptAgent here
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_knowledge, knowledge)

# Parameters for the Evaluation Agent
persona_eval = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
# TODO: 3 - Instantiate the EvaluationAgent with a maximum of 10 interactions here
evaluation_agent = EvaluationAgent(openai_api_key, persona_eval, evaluation_criteria, knowledge_agent, 10)

# TODO: 4 - Evaluate the prompt and print the response from the EvaluationAgent
print("Starting Evaluation Process...")
print("="*50)
result = evaluation_agent.evaluate(prompt)

print("\n" + "="*50)
print("FINAL EVALUATION RESULTS:")
print("="*50)
print(f"Final Response: {result['final_response']}")
print(f"Final Evaluation: {result['evaluation']}")
print(f"Total Iterations: {result['iterations']}")

print("\n" + "="*50)
print("EVALUATION AGENT ANALYSIS:")
print("="*50)
print("This demonstrates the EvaluationAgent's ability to:")
print("1. Iteratively improve responses from a worker agent")
print("2. Apply specific evaluation criteria to judge responses")
print("3. Generate correction instructions when responses don't meet criteria")
print("4. Continue the process until criteria are met or max iterations reached")
print("5. Return structured results with final response, evaluation, and iteration count")
