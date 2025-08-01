"""
Alternative Workflow Examples - Demonstrating Agentic Workflow Adaptability

This file demonstrates how the agentic workflow adapts to different types of project
planning requests by modifying the workflow_prompt. Each example shows how the same
workflow system can handle different facets of project planning.

Author: Agentic AI Project
Date: January 2025
"""

# Import required agents from the workflow_agents library
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load the product spec
with open("Product-Spec-Email-Router.txt", "r", encoding="utf-8") as file:
    product_spec = file.read()

def setup_agents():
    """Setup all the agents needed for the workflow"""
    
    # Action Planning Agent
    knowledge_action_planning = (
        "Stories are defined from a product spec by identifying a "
        "persona, an action, and a desired outcome for each story. "
        "Each story represents a specific functionality of the product "
        "described in the specification. \n"
        "Features are defined by grouping related user stories. \n"
        "Tasks are defined for each story and represent the engineering "
        "work required to develop the product. \n"
        "A development Plan for a product contains all these components"
    )
    action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)
    
    # Product Manager Agent
    persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
    knowledge_product_manager = (
        "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
        "The sentences always start with: As a "
        "Write several stories for the product spec below, where the personas are the different users of the product. "
        + product_spec
    )
    product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)
    
    # Program Manager Agent
    persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
    knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
    program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)
    
    # Development Engineer Agent
    persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
    knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
    development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)
    
    # Support Functions
    def product_manager_support_function(query):
        return product_manager_knowledge_agent.respond(query)
    
    def program_manager_support_function(query):
        return program_manager_knowledge_agent.respond(query)
    
    def development_engineer_support_function(query):
        return development_engineer_knowledge_agent.respond(query)
    
    # Routing Agent
    routing_agent = RoutingAgent(openai_api_key, [])
    routes = [
        {
            "name": "Product Manager",
            "description": "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories",
            "func": product_manager_support_function
        },
        {
            "name": "Program Manager", 
            "description": "Responsible for defining product features by organizing and grouping related user stories into cohesive capabilities",
            "func": program_manager_support_function
        },
        {
            "name": "Development Engineer",
            "description": "Responsible for defining detailed development tasks and technical implementation work required for user stories and features",
            "func": development_engineer_support_function
        }
    ]
    routing_agent.agents = routes
    
    return action_planning_agent, routing_agent

def run_workflow_example(workflow_prompt, example_name):
    """Run a workflow example with the given prompt"""
    
    print(f"\n{'='*80}")
    print(f"WORKFLOW EXAMPLE: {example_name}")
    print(f"{'='*80}")
    print(f"Workflow Prompt: {workflow_prompt}")
    print("-" * 80)
    
    try:
        action_planning_agent, routing_agent = setup_agents()
        
        # Extract workflow steps
        workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
        print(f"\nExtracted {len(workflow_steps)} workflow steps:")
        for i, step in enumerate(workflow_steps, 1):
            print(f"  {i}. {step}")
        
        # Execute workflow
        completed_steps = []
        for i, step in enumerate(workflow_steps, 1):
            print(f"\n--- STEP {i}/{len(workflow_steps)} ---")
            print(f"Executing: {step}")
            
            try:
                result = routing_agent.route(step)
                completed_steps.append(result)
                print(f"✅ Step {i} completed")
                print(f"Result preview: {result[:150]}..." if len(result) > 150 else f"Result: {result}")
            except Exception as e:
                print(f"❌ Error in step {i}: {str(e)}")
                completed_steps.append(f"Error: {str(e)}")
        
        # Final output
        if completed_steps:
            print(f"\n🎯 FINAL OUTPUT for {example_name}:")
            print("-" * 40)
            final_output = completed_steps[-1]
            print(final_output)
        
        print(f"\n✅ {example_name} workflow completed successfully!")
        
    except Exception as e:
        print(f"❌ Workflow failed: {str(e)}")

def main():
    """Run multiple workflow examples to demonstrate adaptability"""
    
    print("AGENTIC WORKFLOW ADAPTABILITY DEMONSTRATION")
    print("="*80)
    print("This demonstration shows how the same agentic workflow system")
    print("adapts to different types of project planning requests.")
    
    # Example 1: Feature-focused workflow
    run_workflow_example(
        "Define only the key features for the Email Router product",
        "FEATURE-FOCUSED PLANNING"
    )
    
    # Example 2: Risk assessment workflow
    run_workflow_example(
        "Generate a risk assessment plan for the Email Router based on its specification",
        "RISK ASSESSMENT PLANNING"
    )
    
    # Example 3: User story focused workflow
    run_workflow_example(
        "What are the essential user stories for the Email Router system?",
        "USER STORY PLANNING"
    )
    
    # Example 4: Technical architecture workflow
    run_workflow_example(
        "What are the technical architecture requirements for implementing the Email Router?",
        "TECHNICAL ARCHITECTURE PLANNING"
    )
    
    print(f"\n{'='*80}")
    print("ADAPTABILITY ANALYSIS")
    print(f"{'='*80}")
    print("Key observations about workflow adaptability:")
    print("1. 🔄 Action Planning: Extracts different types of steps based on prompt focus")
    print("2. 🎯 Intelligent Routing: Routes to appropriate specialists based on step content")
    print("3. 📋 Contextual Responses: Each agent provides responses relevant to the specific request")
    print("4. 🔧 Flexible Output: Same system generates features, risks, stories, or architecture")
    print("5. 🚀 Scalable Approach: Framework adapts without code changes")
    
    print(f"\n✅ All workflow adaptability examples completed successfully!")

if __name__ == "__main__":
    main()
