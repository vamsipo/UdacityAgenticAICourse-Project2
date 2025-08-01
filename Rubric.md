Rubric
Use this project rubric to understand and assess the project criteria.

The Agentic Toolkit - Agent Implementation
Criteria	Submission Requirements
Implement required agent classes with correct structure and initialization.

| All six student-implemented agent classes (DirectPromptAgent, AugmentedPromptAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent, ActionPlanningAgent) are defined in workflow_agents/base_agents.py. Each agent class includes an __init__ method that correctly initializes necessary attributes as specified in the project instructions (e.g., API key, persona, knowledge, evaluation criteria, worker agent, max interactions, agent details for routing).Each agent class implements a primary public method for its core functionality (e.g., respond for prompt-based agents, evaluate for EvaluationAgent, route for RoutingAgent, extract_steps_from_prompt for ActionPlanningAgent). Each primary method is designed to return the output in the format specified by the project instructions (e.g., string content, dictionary, list of steps). |

Configure agents for correct LLM interaction and API key management.

All implemented agents that directly interact with an LLM are configured to use the gpt-3.5-turbo model, unless otherwise specified for a particular agent class (e.g., text-embedding-3-large for RoutingAgent embeddings).
The OpenAI API key is passed to agent instances during initialization, not hardcoded within the agent classes.
The EvaluationAgent uses temperature=0 for its OpenAI API calls related to generating evaluations and correction instructions.
Implement agent-specific prompt engineering and core logic as per requirements.

Each implemented agent class correctly constructs and utilizes prompts (system and user messages) and/or logic according to requirements:

DirectPromptAgent: Passes the user prompt directly as a user message to the LLM without a system prompt; returns only text content.
AugmentedPromptAgent: Uses a system prompt to set its persona and instruct the LLM to forget previous context; returns only text content.
KnowledgeAugmentedPromptAgent: Uses a system prompt to set persona, provide specific knowledge, and instruct the LLM to use only that knowledge and forget other context; returns only text content.
EvaluationAgent: Implements an iterative loop (up to max_interactions) to get a response from a worker agent, evaluate it against criteria, and (if needed) generate correction instructions to refine the worker's response; returns a dictionary with final response, evaluation, and iteration count.
RoutingAgent: Implements a method to get text embeddings (using text-embedding-3-large), computes cosine similarity between prompt embedding and agent description embeddings, selects the best agent, and calls its function, returning the selected agent's response.
ActionPlanningAgent: Uses a system prompt defining its role to extract and list actionable steps from a user prompt, processing the LLM response into a clean list.
The Agentic Toolkit - Agent Testing
Criteria	
Provide functional test scripts for each implemented agent.
Submission Requirements
A separate Python test script is provided for each of the six implemented agents (DirectPromptAgent, AugmentedPromptAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent, ActionPlanningAgent).
Each test script:
imports the corresponding agent class from workflow_agents.base_agents.
instantiates the agent with necessary parameters (API key, persona, knowledge, criteria, etc., as per agent type and instructions in project_instructions_doc).
calls the agent's primary method with a sample prompt as specified in the project instructions.
prints the agent's response or the relevant part of the agent's output.
Submit evidence of successful test script execution.

Outputs (screenshots or text files of terminal output) are provided for the execution of all seven test scripts (including the one for the provided RAGKnowledgePromptAgent).
The outputs clearly show the prompt used (if printed by the script) and the agent's response for each test.
For DirectPromptAgent, output includes the print statement explaining its knowledge source.
For AugmentedPromptAgent, output includes comments discussing knowledge source and persona impact.
For KnowledgeAugmentedPromptAgent, output includes a print statement confirming use of provided knowledge.
Project Management Workflow - Setup and Agent Instantiation
Criteria	Submission Requirements
Implement initial workflow setup in agentic_workflow.py.

The agentic_workflow.py script correctly imports ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, and RoutingAgent from workflow_agents.base_agents.
The OpenAI API key is loaded from an environment variable.
The content of Product-Spec-Email-Router.txt is loaded into the product_spec variable.
Instantiate core workflow agents and specialized knowledge agents correctly.

An ActionPlanningAgent is instantiated with the provided knowledge_action_planning. The knowledge_product_manager string is correctly completed by appending the product_spec.
A KnowledgeAugmentedPromptAgent for the Product Manager is instantiated with persona_product_manager and the completed knowledge_product_manager.
A KnowledgeAugmentedPromptAgent for the Program Manager is instantiated with persona_program_manager and knowledge_program_manager.
A KnowledgeAugmentedPromptAgent for the Development Engineer is instantiated with persona_dev_engineer and knowledge_dev_engineer.
Instantiate Evaluation Agents for each specialized role.

An EvaluationAgent for the Product Manager is instantiated with:
persona: "You are an evaluation agent that checks the answers of other worker agents”
evaluation_criteria: "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
The product_manager_knowledge_agent as agent_to_evaluate.
An EvaluationAgent for the Program Manager is instantiated with persona_program_manager_eval and the specified multi-line structure for product features as evaluation_criteria.
An EvaluationAgent for the Development Engineer is instantiated with persona_dev_engineer_eval and the specified multi-line structure for tasks as evaluation_criteria.
Instantiate and configure the Routing Agent.

A RoutingAgent is instantiated.
Its agents attribute is assigned a list of dictionaries, with each dictionary representing a route for Product Manager, Program Manager, and Development Engineer.
Each route dictionary contains name (e.g., "Product Manager"), description (e.g., "Responsible for defining product personas and user stories only..."), and func (a lambda or reference to a support function).
Project Management Workflow - Workflow Logic and Execution
Criteria	Submission Requirements
Implement support functions for routed tasks.

Support functions (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function) are defined.Each support function:

Accepts an input query (a step from the action plan).
Calls the respond() method of its corresponding KnowledgeAugmentedPromptAgent.
Passes the response from the Knowledge Agent to the evaluate() method of its corresponding EvaluationAgent.
Returns the final, validated response (e.g., from the 'final_response' key of the evaluation result).

Implement the main agentic workflow orchestration.

| The workflow uses the action_planning_agent to get a list of workflow_steps from the workflow_prompt.The workflow iterates through the workflow_steps.In each iteration:The current step is printed.The routing_agent.route() method is called with the current step.The result from the routing_agent is appended to a list of completed_steps.The result of the current step is printed.The final output of the workflow (e.g., the last item in completed_steps or a consolidated summary) is printed after all steps are processed. |

Produce a final, structured output for the Email Router project.

The agentic_workflow.py script, when run with the Product-Spec-Email-Router.txt and a suitable high-level prompt (e.g., workflow_prompt from starter code, or similar, focusing on generating a full project plan), produces a final output.
This output represents a comprehensively planned project for the Email Router, including user stories, product features, and detailed engineering tasks.
The generated user stories follow the structure: "As a [type of user], I want [an action or feature] so that [benefit/value]."
The generated product features follow the structure: "Feature Name:...", "Description:...", "Key Functionality:...", "User Benefit:..."
The generated engineering tasks follow the structure: "Task ID:...", "Task Title:...", "Related User Story:...", "Description:...", "Acceptance Criteria:...", "Estimated Effort:...", "Dependencies:..."
Industry Best Practices
Criteria	Submission Requirements
Write code that is readable, well-commented, and modular.

Variable and function names in the Python code are descriptive and generally follow Python conventions (e.g., snake_case for functions/variables, PascalCase for classes).
The Python code (base_agents.py and agentic_workflow.py) includes comments or docstrings explaining complex logic or the purpose of functions/classes.
Code within base_agents.py is organized into distinct agent classes.
Code within agentic_workflow.py is organized logically (e.g., setup, agent instantiation, support functions, main workflow logic).
Suggestions to Make Your Project Stand Out
Modify the workflow_prompt in agentic_workflow.py to explore different facets of project planning (e.g., "Define only the key features for the Email Router product," or "Generate a risk assessment plan for the Email Router based on its specification") and document how the agentic workflow adapts.

Extend the EvaluationAgent for one of the roles (e.g., Product Manager) to include more sophisticated criteria or a scoring mechanism for the generated artifacts.

Add basic error handling or logging within the agentic_workflow.py to make the workflow more robust (e.g., what happens if an agent fails to respond or an API call times out?).

Write a brief reflection (in a separate reflection.md file) on the strengths and limitations of the implemented agentic workflow, and suggest one specific improvement to the agent design or workflow orchestration.


