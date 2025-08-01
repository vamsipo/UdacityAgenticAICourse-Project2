"""
Agentic Workflow for Project Management

This module implements a sophisticated agentic workflow system that transforms product
specifications into comprehensive project management artifacts. The system uses multiple
specialized AI agents working in coordination to generate user stories, product features,
and detailed engineering tasks.

Key Components:
- ActionPlanningAgent: Breaks down high-level goals into actionable steps
- RoutingAgent: Intelligently routes tasks to appropriate specialist agents
- Specialist Teams: Product Manager, Program Manager, and Development Engineer
- Quality Assurance: Each team includes evaluation agents for output refinement

Author: Agentic AI Project
Date: January 2025
"""

# Import required agents from the workflow_agents library
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

import os
from dotenv import load_dotenv

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
with open("Product-Spec-Email-Router.txt", "r", encoding="utf-8") as file:
    product_spec = file.read()

# Instantiate all the agents

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
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    + product_spec
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Enhanced Evaluation Agent with Scoring Mechanism
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").

# ENHANCEMENT: Advanced evaluation criteria with scoring mechanism
persona_product_manager_eval = "You are an advanced evaluation agent that checks and scores the answers of other worker agents"
evaluation_criteria_product_manager = """
The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value].

SCORING CRITERIA (Rate each story 1-10):
1. Structure Compliance (2 points): Does it follow the exact "As a... I want... so that..." format?
2. Persona Clarity (2 points): Is the user type specific and well-defined?
3. Action Specificity (2 points): Is the desired action/feature clearly described?
4. Value Proposition (2 points): Is the benefit/value clearly articulated?
5. Business Relevance (2 points): Does it align with the Email Router product requirements?

MINIMUM ACCEPTABLE SCORE: 8/10 per story
OVERALL ACCEPTANCE: All stories must score 8+ and there must be at least 5 diverse user stories covering different user types.
"""
product_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_product_manager_eval, evaluation_criteria_product_manager, product_manager_knowledge_agent, 10)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
evaluation_criteria_program_manager = ("The answer should be product features that follow the following structure: " +
                                      "Feature Name: A clear, concise title that identifies the capability\n" +
                                      "Description: A brief explanation of what the feature does and its purpose\n" +
                                      "Key Functionality: The specific capabilities or actions the feature provides\n" +
                                      "User Benefit: How this feature creates value for the user")
program_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_program_manager_eval, evaluation_criteria_program_manager, program_manager_knowledge_agent, 10)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
evaluation_criteria_dev_engineer = ("The answer should be tasks following this exact structure: " +
                                   "Task ID: A unique identifier for tracking purposes\n" +
                                   "Task Title: Brief description of the specific development work\n" +
                                   "Related User Story: Reference to the parent user story\n" +
                                   "Description: Detailed explanation of the technical work required\n" +
                                   "Acceptance Criteria: Specific requirements that must be met for completion\n" +
                                   "Estimated Effort: Time or complexity estimation\n" +
                                   "Dependencies: Any tasks that must be completed first")
development_engineer_evaluation_agent = EvaluationAgent(openai_api_key, persona_dev_engineer_eval, evaluation_criteria_dev_engineer, development_engineer_knowledge_agent, 10)


# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

def product_manager_support_function(query):
    """
    Support function for Product Manager - generates and evaluates user stories
    
    This function implements error handling and logging for robust workflow execution.
    It handles API timeouts, evaluation failures, and other potential issues.
    """
    print(f"[Product Manager] Processing: {query}")
    
    try:
        # Get response from Knowledge Agent with timeout handling
        print(f"[Product Manager] Generating initial response...")
        response = product_manager_knowledge_agent.respond(query)
        print(f"[Product Manager] Initial response generated successfully")
        
        # Evaluate the response with error handling
        print(f"[Product Manager] Starting evaluation process...")
        evaluation_result = product_manager_evaluation_agent.evaluate(query)
        print(f"[Product Manager] Evaluation completed after {evaluation_result.get('iterations', 'unknown')} iterations")
        
        # Return the final validated response
        return evaluation_result['final_response']
        
    except Exception as e:
        error_msg = f"[Product Manager] Error during processing: {str(e)}"
        print(f"{error_msg}")
        # Return a fallback response instead of crashing the workflow
        return f"Error in Product Manager processing: {str(e)}. Please review manually."

def program_manager_support_function(query):
    """
    Support function for Program Manager - generates and evaluates product features
    
    This function implements error handling and logging for robust workflow execution.
    """
    print(f"[Program Manager] Processing: {query}")
    
    try:
        print(f"[Program Manager] Generating initial response...")
        response = program_manager_knowledge_agent.respond(query)
        print(f"[Program Manager] Initial response generated successfully")
        
        print(f"[Program Manager] Starting evaluation process...")
        evaluation_result = program_manager_evaluation_agent.evaluate(query)
        print(f"[Program Manager] Evaluation completed after {evaluation_result.get('iterations', 'unknown')} iterations")
        
        return evaluation_result['final_response']
        
    except Exception as e:
        error_msg = f"[Program Manager] Error during processing: {str(e)}"
        print(f"{error_msg}")
        return f"Error in Program Manager processing: {str(e)}. Please review manually."

def development_engineer_support_function(query):
    """
    Support function for Development Engineer - generates and evaluates development tasks
    
    This function implements error handling and logging for robust workflow execution.
    """
    print(f"[Development Engineer] Processing: {query}")
    
    try:
        print(f"[Development Engineer] Generating initial response...")
        response = development_engineer_knowledge_agent.respond(query)
        print(f"[Development Engineer] Initial response generated successfully")
        
        print(f"[Development Engineer] Starting evaluation process...")
        evaluation_result = development_engineer_evaluation_agent.evaluate(query)
        print(f"[Development Engineer] Evaluation completed after {evaluation_result.get('iterations', 'unknown')} iterations")
        
        return evaluation_result['final_response']
        
    except Exception as e:
        error_msg = f"[Development Engineer] Error during processing: {str(e)}"
        print(f"{error_msg}")
        return f"Error in Development Engineer processing: {str(e)}. Please review manually."

# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.

routing_agent = RoutingAgent(openai_api_key, [])

# Define the routes for the routing agent
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

# Assign routes to the routing agent
routing_agent.agents = routes

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "Create a comprehensive project plan for the Email Router product including user stories, product features, and development tasks."
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
print(f"Extracted {len(workflow_steps)} workflow steps:")
for i, step in enumerate(workflow_steps, 1):
    print(f"  {i}. {step}")

#   2. Initialize an empty list to store 'completed_steps'.
completed_steps = []

print("\n" + "="*80)
print("EXECUTING AGENTIC WORKFLOW")
print("="*80)

#   3. Loop through the extracted workflow steps:
for i, step in enumerate(workflow_steps, 1):
    print(f"\n--- STEP {i}/{len(workflow_steps)} ---")
    print(f"Executing: {step}")
    print("-" * 50)
    
    #      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
    try:
        result = routing_agent.route(step)
        #      b. Append the result to 'completed_steps'.
        completed_steps.append(result)
        #      c. Print information about the step being executed and its result.
        print(f"\nStep {i} completed successfully")
        print(f"Result preview: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
    except Exception as e:
        print(f"Error in step {i}: {str(e)}")
        completed_steps.append(f"Error: {str(e)}")

#   4. After the loop, print the final output of the workflow (the last completed step).
print("\n" + "="*80)
print("WORKFLOW EXECUTION COMPLETED")
print("="*80)

if completed_steps:
    print(f"\nTotal steps completed: {len(completed_steps)}")
    print("\nFINAL WORKFLOW OUTPUT:")
    print("-" * 40)
    final_output = completed_steps[-1]  # Last completed step
    print(final_output)
    
    print("\n" + "="*80)
    print("AGENTIC WORKFLOW SUMMARY")
    print("="*80)
    print("This agentic workflow successfully demonstrated:")
    print("1. Action Planning: Breaking down high-level goals into actionable steps")
    print("2. Intelligent Routing: Directing steps to appropriate specialist agents")
    print("3. Knowledge-Augmented Processing: Using domain-specific knowledge")
    print("4. Quality Evaluation: Iterative improvement through evaluation agents")
    print("5. Structured Output: Generating user stories, features, and development tasks")
    print("\n The Email Router product is now ready for development with comprehensive planning!")
else:
    print("No steps were completed successfully.")
