"""
Agentic AI Workflow Agents Library

This module contains a comprehensive collection of AI agents designed for building
sophisticated agentic workflows. Each agent serves a specific purpose in the workflow
and can be combined to create complex, intelligent systems.

Author: Agentic AI Project
Date: January 2025
"""

from openai import OpenAI
import numpy as np
import pandas as pd
import re
import csv
import uuid
from datetime import datetime


class DirectPromptAgent:
    """
    A basic agent that provides direct interaction with an LLM without any additional
    context, memory, or specialized tools. This agent simply passes user prompts
    directly to the LLM and returns the response.
    
    Use Case: Simple question-answering scenarios where no additional context is needed.
    """
    
    def __init__(self, openai_api_key):
        """
        Initialize the DirectPromptAgent.
        
        Args:
            openai_api_key (str): OpenAI API key for authentication
        """
        self.openai_api_key = openai_api_key

    def respond(self, prompt):
        """
        Generate a response using direct LLM interaction without system prompts.
        
        Args:
            prompt (str): User input prompt to send to the LLM
            
        Returns:
            str: The LLM's response content as plain text
        """
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}  # Direct user message, no system prompt
            ],
            temperature=0
        )
        return response.choices[0].message.content
        
class AugmentedPromptAgent:
    """
    An agent that responds according to a predefined persona. This agent uses system prompts
    to adopt specific roles or characteristics, leading to more targeted and contextually
    relevant outputs compared to basic prompt-response interactions.
    
    Use Case: When you need responses that follow a specific tone, style, or expertise level.
    """
    
    def __init__(self, openai_api_key, persona):
        """
        Initialize the AugmentedPromptAgent with API key and persona.
        
        Args:
            openai_api_key (str): OpenAI API key for authentication
            persona (str): The persona/role the agent should adopt (e.g., "college professor")
        """
        self.persona = persona
        self.openai_api_key = openai_api_key

    def respond(self, input_text):
        """
        Generate a response using the specified persona via system prompts.
        
        Args:
            input_text (str): User input prompt
            
        Returns:
            str: LLM response following the specified persona
        """
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                # System prompt sets persona and resets context
                {"role": "system", "content": f"You are {self.persona}. Forget all previous context."},
                {"role": "user", "content": input_text}
            ],
            temperature=0
        )

        return response.choices[0].message.content

class KnowledgeAugmentedPromptAgent:
    """
    An agent that incorporates specific, provided knowledge alongside a defined persona
    when responding to prompts. This ensures answers are based on explicit information
    rather than the LLM's inherent knowledge.
    
    Use Case: When you need responses grounded in specific domain knowledge or when
    you want to override the LLM's training data with custom information.
    """
    
    def __init__(self, openai_api_key, persona, knowledge):
        """
        Initialize the KnowledgeAugmentedPromptAgent.
        
        Args:
            openai_api_key (str): OpenAI API key for authentication
            persona (str): The persona/role the agent should adopt
            knowledge (str): Specific knowledge the agent should use exclusively
        """
        self.persona = persona
        self.knowledge = knowledge
        self.openai_api_key = openai_api_key

    def respond(self, input_text):
        """
        Generate a response using only the provided knowledge and persona.
        
        Args:
            input_text (str): User input prompt
            
        Returns:
            str: LLM response based solely on provided knowledge
        """
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        
        # Construct system message with persona and knowledge constraints
        system_message = (
            f"You are {self.persona} knowledge-based assistant. Forget all previous context. "
            f"Use only the following knowledge to answer, do not use your own knowledge: {self.knowledge} "
            f"Answer the prompt based on this knowledge, not your own."
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": input_text}
            ],
            temperature=0
        )
        return response.choices[0].message.content

# RAGKnowledgePromptAgent class definition
class RAGKnowledgePromptAgent:
    """
    An agent that uses Retrieval-Augmented Generation (RAG) to find knowledge from a large corpus
    and leverages embeddings to respond to prompts based solely on retrieved information.
    """

    def __init__(self, openai_api_key, persona, chunk_size=2000, chunk_overlap=100):
        """
        Initializes the RAGKnowledgePromptAgent with API credentials and configuration settings.

        Parameters:
        openai_api_key (str): API key for accessing OpenAI.
        persona (str): Persona description for the agent.
        chunk_size (int): The size of text chunks for embedding. Defaults to 2000.
        chunk_overlap (int): Overlap between consecutive chunks. Defaults to 100.
        """
        self.persona = persona
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.openai_api_key = openai_api_key
        self.unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.csv"

    def get_embedding(self, text):
        """
        Fetches the embedding vector for given text using OpenAI's embedding API.

        Parameters:
        text (str): Text to embed.

        Returns:
        list: The embedding vector.
        """
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float"
        )
        return response.data[0].embedding

    def calculate_similarity(self, vector_one, vector_two):
        """
        Calculates cosine similarity between two vectors.

        Parameters:
        vector_one (list): First embedding vector.
        vector_two (list): Second embedding vector.

        Returns:
        float: Cosine similarity between vectors.
        """
        vec1, vec2 = np.array(vector_one), np.array(vector_two)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def chunk_text(self, text):
        """
        Splits text into manageable chunks, attempting natural breaks.

        Parameters:
        text (str): Text to split into chunks.

        Returns:
        list: List of dictionaries containing chunk metadata.
        """
        separator = "\n"
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) <= self.chunk_size:
            return [{"chunk_id": 0, "text": text, "chunk_size": len(text)}]

        chunks, start, chunk_id = [], 0, 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            if separator in text[start:end]:
                end = start + text[start:end].rindex(separator) + len(separator)

            chunks.append({
                "chunk_id": chunk_id,
                "text": text[start:end],
                "chunk_size": end - start,
                "start_char": start,
                "end_char": end
            })

            start = end - self.chunk_overlap
            chunk_id += 1

        with open(f"chunks-{self.unique_filename}", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["text", "chunk_size"])
            writer.writeheader()
            for chunk in chunks:
                writer.writerow({k: chunk[k] for k in ["text", "chunk_size"]})

        return chunks

    def calculate_embeddings(self):
        """
        Calculates embeddings for each chunk and stores them in a CSV file.

        Returns:
        DataFrame: DataFrame containing text chunks and their embeddings.
        """
        df = pd.read_csv(f"chunks-{self.unique_filename}", encoding='utf-8')
        df['embeddings'] = df['text'].apply(self.get_embedding)
        df.to_csv(f"embeddings-{self.unique_filename}", encoding='utf-8', index=False)
        return df

    def find_prompt_in_knowledge(self, prompt):
        """
        Finds and responds to a prompt based on similarity with embedded knowledge.

        Parameters:
        prompt (str): User input prompt.

        Returns:
        str: Response derived from the most similar chunk in knowledge.
        """
        prompt_embedding = self.get_embedding(prompt)
        df = pd.read_csv(f"embeddings-{self.unique_filename}", encoding='utf-8')
        df['embeddings'] = df['embeddings'].apply(lambda x: np.array(eval(x)))
        df['similarity'] = df['embeddings'].apply(lambda emb: self.calculate_similarity(prompt_embedding, emb))

        best_chunk = df.loc[df['similarity'].idxmax(), 'text']

        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are {self.persona}, a knowledge-based assistant. Forget previous context."},
                {"role": "user", "content": f"Answer based only on this information: {best_chunk}. Prompt: {prompt}"}
            ],
            temperature=0
        )

        return response.choices[0].message.content

class EvaluationAgent:
    """
    An agent designed to assess responses from another agent (a "worker" agent) against
    a given set of criteria, potentially refining the response through iterative feedback.
    This agent implements a quality assurance loop to improve output quality.
    
    Use Case: Quality control in agentic workflows where responses need to meet specific
    standards or formats before being considered acceptable.
    """
    
    def __init__(self, openai_api_key, persona, evaluation_criteria, worker_agent, max_interactions):
        """
        Initialize the EvaluationAgent.
        
        Args:
            openai_api_key (str): OpenAI API key for authentication
            persona (str): The persona/role for the evaluation agent
            evaluation_criteria (str): Specific criteria to evaluate responses against
            worker_agent: The agent whose responses will be evaluated
            max_interactions (int): Maximum number of evaluation-correction cycles
        """
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.worker_agent = worker_agent
        self.max_interactions = max_interactions

    def evaluate(self, initial_prompt):
        """
        Manage iterative evaluation and improvement of worker agent responses.
        
        This method implements a feedback loop:
        1. Worker agent generates response
        2. Evaluator judges response against criteria
        3. If unsatisfactory, generate correction instructions
        4. Repeat until criteria met or max interactions reached
        
        Args:
            initial_prompt (str): The original prompt to evaluate
            
        Returns:
            dict: Contains 'final_response', 'evaluation', and 'iterations'
        """
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        prompt_to_evaluate = initial_prompt

        for i in range(self.max_interactions):
            print(f"\n--- Interaction {i+1} ---")

            print(" Step 1: Worker agent generates a response to the prompt")
            print(f"Prompt:\n{prompt_to_evaluate}")
            response_from_worker = self.worker_agent.respond(prompt_to_evaluate)  # TODO: 3 - Obtain a response from the worker agent
            print(f"Worker Agent Response:\n{response_from_worker}")

            print(" Step 2: Evaluator agent judges the response")
            eval_prompt = (
                f"Does the following answer: {response_from_worker}\n"
                f"Meet this criteria: {self.evaluation_criteria} "  # TODO: 4 - Insert evaluation criteria here
                f"Respond Yes or No, and the reason why it does or doesn't meet the criteria."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[  # TODO: 5 - Define the message structure sent to the LLM for evaluation (use temperature=0)
                    {"role": "system", "content": self.persona},
                    {"role": "user", "content": eval_prompt}
                ],
                temperature=0
            )
            evaluation = response.choices[0].message.content.strip()
            print(f"Evaluator Agent Evaluation:\n{evaluation}")

            print(" Step 3: Check if evaluation is positive")
            if evaluation.lower().startswith("yes"):
                print("✅ Final solution accepted.")
                return {
                    "final_response": response_from_worker,
                    "evaluation": evaluation,
                    "iterations": i + 1
                }
            else:
                print(" Step 4: Generate instructions to correct the response")
                instruction_prompt = (
                    f"Provide instructions to fix an answer based on these reasons why it is incorrect: {evaluation}"
                )
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[  # TODO: 6 - Define the message structure sent to the LLM to generate correction instructions (use temperature=0)
                        {"role": "system", "content": self.persona},
                        {"role": "user", "content": instruction_prompt}
                    ],
                    temperature=0
                )
                instructions = response.choices[0].message.content.strip()
                print(f"Instructions to fix:\n{instructions}")

                print(" Step 5: Send feedback to worker agent for refinement")
                prompt_to_evaluate = (
                    f"The original prompt was: {initial_prompt}\n"
                    f"The response to that prompt was: {response_from_worker}\n"
                    f"It has been evaluated as incorrect.\n"
                    f"Make only these corrections, do not alter content validity: {instructions}"
                )
        
        # If max interactions reached without success
        return {
            # TODO: 7 - Return a dictionary containing the final response, evaluation, and number of iterations
            "final_response": response_from_worker,
            "evaluation": evaluation,
            "iterations": self.max_interactions
        }

class RoutingAgent:
    """
    An agent capable of directing user prompts to the most appropriate specialized agent
    from a collection, based on semantic similarity between the prompt and descriptions
    of what each agent handles.
    
    Use Case: Intelligent task distribution in multi-agent systems where different
    agents have different specializations or capabilities.
    """

    def __init__(self, openai_api_key, agents):
        """
        Initialize the RoutingAgent.
        
        Args:
            openai_api_key (str): OpenAI API key for authentication
            agents (list): List of agent dictionaries with 'name', 'description', and 'func'
        """
        self.openai_api_key = openai_api_key
        self.agents = agents

    def get_embedding(self, text):
        """
        Calculate text embeddings using OpenAI's embedding model.
        
        Args:
            text (str): Text to embed
            
        Returns:
            list: Embedding vector for the input text
        """
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float"
        )
        embedding = response.data[0].embedding
        return embedding 

    def route(self, user_input):
        """
        Route user prompts to the most appropriate agent based on semantic similarity.
        
        This method:
        1. Computes embedding for user input
        2. Computes embeddings for all agent descriptions
        3. Calculates cosine similarity between input and each agent
        4. Selects agent with highest similarity score
        5. Calls the selected agent's function
        
        Args:
            user_input (str): User prompt to route
            
        Returns:
            str: Response from the selected agent
        """
        input_emb = self.get_embedding(user_input)
        best_agent = None
        best_score = -1

        for agent in self.agents:
            agent_emb = self.get_embedding(agent["description"])
            if agent_emb is None:
                continue

            # Calculate cosine similarity
            similarity = np.dot(input_emb, agent_emb) / (np.linalg.norm(input_emb) * np.linalg.norm(agent_emb))
            print(f"Agent: {agent['name']}, Similarity: {similarity}")

            if similarity > best_score:
                best_score = similarity
                best_agent = agent

        if best_agent is None:
            return "Sorry, no suitable agent could be selected."

        print(f"[Router] Best agent: {best_agent['name']} (score={best_score:.3f})")
        return best_agent["func"](user_input)


class ActionPlanningAgent:
    """
    An agent crucial for constructing agentic workflows. This agent uses its provided
    knowledge to dynamically extract and list the steps required to execute a task
    described in a user's prompt.
    
    Use Case: Breaking down complex tasks into actionable steps, workflow orchestration,
    and task decomposition in agentic systems.
    """

    def __init__(self, openai_api_key, knowledge):
        """
        Initialize the ActionPlanningAgent.
        
        Args:
            openai_api_key (str): OpenAI API key for authentication
            knowledge (str): Domain-specific knowledge for step extraction
        """
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge

    def extract_steps_from_prompt(self, prompt):
        """
        Extract actionable steps from a user prompt using provided knowledge.
        
        This method:
        1. Uses system prompt to define agent role and knowledge constraints
        2. Processes user prompt to identify required actions
        3. Returns clean, structured list of steps
        4. Filters out empty or irrelevant content
        
        Args:
            prompt (str): User prompt describing a task or goal
            
        Returns:
            list: Clean list of actionable steps extracted from the prompt
        """
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        
        # Define system prompt with role and knowledge constraints
        system_prompt = (
            f"You are an action planning agent. Using your knowledge, you extract from the user prompt "
            f"the steps requested to complete the action the user is asking for. You return the steps as a list. "
            f"Only return the steps in your knowledge. Forget any previous context. "
            f"This is your knowledge: {self.knowledge}"
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        response_text = response.choices[0].message.content

        # Clean and format the extracted steps
        steps = response_text.split("\n")
        cleaned_steps = [step.strip() for step in steps if step.strip()]

        return cleaned_steps
