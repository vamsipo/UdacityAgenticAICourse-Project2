# TODO: 1 - Import all required libraries, including the ActionPlanningAgent
from workflow_agents.base_agents import ActionPlanningAgent
import os
from dotenv import load_dotenv

# TODO: 2 - Load environment variables and define the openai_api_key variable with your OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

knowledge = """
# Fried Egg
1. Heat pan with oil or butter
2. Crack egg into pan
3. Cook until white is set (2-3 minutes)
4. Season with salt and pepper
5. Serve

# Scrambled Eggs
1. Crack eggs into a bowl
2. Beat eggs with a fork until mixed
3. Heat pan with butter or oil over medium heat
4. Pour egg mixture into pan
5. Stir gently as eggs cook
6. Remove from heat when eggs are just set but still moist
7. Season with salt and pepper
8. Serve immediately

# Boiled Eggs
1. Place eggs in a pot
2. Cover with cold water (about 1 inch above eggs)
3. Bring water to a boil
4. Remove from heat and cover pot
5. Let sit: 4-6 minutes for soft-boiled or 10-12 minutes for hard-boiled
6. Transfer eggs to ice water to stop cooking
7. Peel and serve
"""

# TODO: 3 - Instantiate the ActionPlanningAgent, passing the openai_api_key and the knowledge variable
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge)

# TODO: 4 - Print the agent's response to the following prompt: "One morning I wanted to have scrambled eggs"
prompt = "One morning I wanted to have scrambled eggs"
print("ACTION PLANNING AGENT TEST:")
print("="*50)
print(f"Prompt: {prompt}")
print("\nExtracted Action Steps:")
print("-" * 30)

steps = action_planning_agent.extract_steps_from_prompt(prompt)
for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")

print("\n" + "="*50)
print("ACTION PLANNING AGENT ANALYSIS:")
print("="*50)
print("This demonstrates the ActionPlanningAgent's ability to:")
print("1. Use provided knowledge to extract relevant action steps")
print("2. Parse user prompts to identify the requested task (scrambled eggs)")
print("3. Return a clean, structured list of actionable steps")
print("4. Focus only on steps from the provided knowledge base")
print("5. Ignore irrelevant information and extract only pertinent steps")
