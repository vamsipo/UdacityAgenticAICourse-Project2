#!/usr/bin/env python3
"""
Simple test script to verify all agents are working and capture outputs
"""

import sys
import os
sys.path.append('starter/phase_1')

from workflow_agents.base_agents import DirectPromptAgent, AugmentedPromptAgent, KnowledgeAugmentedPromptAgent, ActionPlanningAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv('starter/phase_1/.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

def test_direct_prompt_agent():
    print("="*60)
    print("TESTING DIRECT PROMPT AGENT")
    print("="*60)
    
    agent = DirectPromptAgent(openai_api_key)
    response = agent.respond("What is the capital of France?")
    print(f"Response: {response}")
    print("✅ DirectPromptAgent test completed successfully")
    return response

def test_augmented_prompt_agent():
    print("\n" + "="*60)
    print("TESTING AUGMENTED PROMPT AGENT")
    print("="*60)
    
    persona = "You are a college professor; your answers always start with: 'Dear students,'"
    agent = AugmentedPromptAgent(openai_api_key, persona)
    response = agent.respond("What is the capital of France?")
    print(f"Response: {response}")
    print("✅ AugmentedPromptAgent test completed successfully")
    return response

def test_knowledge_augmented_prompt_agent():
    print("\n" + "="*60)
    print("TESTING KNOWLEDGE AUGMENTED PROMPT AGENT")
    print("="*60)
    
    persona = "You are a college professor, your answer always starts with: Dear students,"
    knowledge = "The capital of France is London, not Paris"
    agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)
    response = agent.respond("What is the capital of France?")
    print(f"Response: {response}")
    print("✅ KnowledgeAugmentedPromptAgent test completed successfully")
    return response

def test_action_planning_agent():
    print("\n" + "="*60)
    print("TESTING ACTION PLANNING AGENT")
    print("="*60)
    
    knowledge = """
# Scrambled Eggs
1. Crack eggs into a bowl
2. Beat eggs with a fork until mixed
3. Heat pan with butter or oil over medium heat
4. Pour egg mixture into pan
5. Stir gently as eggs cook
6. Remove from heat when eggs are just set but still moist
7. Season with salt and pepper
8. Serve immediately
"""
    
    agent = ActionPlanningAgent(openai_api_key, knowledge)
    steps = agent.extract_steps_from_prompt("One morning I wanted to have scrambled eggs")
    print("Extracted steps:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    print("✅ ActionPlanningAgent test completed successfully")
    return steps

def main():
    print("AGENTIC AI PROJECT - AGENT TESTING")
    print("="*60)
    
    try:
        # Test all agents
        direct_response = test_direct_prompt_agent()
        augmented_response = test_augmented_prompt_agent()
        knowledge_response = test_knowledge_augmented_prompt_agent()
        action_steps = test_action_planning_agent()
        
        print("\n" + "="*60)
        print("ALL AGENT TESTS COMPLETED SUCCESSFULLY! ✅")
        print("="*60)
        
        # Save results to file
        with open("agent_test_results.txt", "w") as f:
            f.write("AGENTIC AI PROJECT - AGENT TEST RESULTS\n")
            f.write("="*60 + "\n\n")
            f.write("1. DirectPromptAgent Response:\n")
            f.write(f"{direct_response}\n\n")
            f.write("2. AugmentedPromptAgent Response:\n")
            f.write(f"{augmented_response}\n\n")
            f.write("3. KnowledgeAugmentedPromptAgent Response:\n")
            f.write(f"{knowledge_response}\n\n")
            f.write("4. ActionPlanningAgent Steps:\n")
            for i, step in enumerate(action_steps, 1):
                f.write(f"  {i}. {step}\n")
            f.write("\nAll tests completed successfully!")
        
        print("Results saved to 'agent_test_results.txt'")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
