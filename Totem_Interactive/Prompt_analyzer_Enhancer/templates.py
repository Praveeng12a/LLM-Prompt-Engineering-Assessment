# templates.py
from langchain.prompts import PromptTemplate

def create_analysis_prompt_template() -> PromptTemplate:
    """Create comprehensive analysis prompt template"""
    analysis_template = """Perform an in-depth prompt analysis with these guidelines:

    Analysis Criteria:
    1. Identify primary task type
    2. Assess prompt complexity
    3. Determine missing contextual elements
    4. Evaluate context and clarity scores

    Provide output in JSON format with:
    - task_type (string)
    - complexity (Low/Medium/High)
    - missing_elements (list)
    - context_score (0-1)
    - clarity_score (0-1)

    Prompt: {prompt}
    """
    return PromptTemplate(input_variables=["prompt"], template=analysis_template)


def create_prompt_enhancer_template() -> PromptTemplate:
    """Enhance prompt by addressing missing elements and improving clarity"""
    prompt_enhancer_template = """Enhance the given prompt to be concise and clear, addressing any missing elements.
    Ensure the prompt is specific and includes detailed instructions.

    Original Prompt: {prompt}
    Task Type: {task_type}
    Complexity: {complexity}
    Missing Elements: {missing_elements}

    Provide a concise, clear enhancement of the original prompt that addresses any missing elements.
    Focus on adding specificity and clarity without unnecessary details.

    Enhanced Prompt: Write a {task_type} to {prompt}. 
    Include detailed steps, {missing_elements}, and any necessary context for clarity.
    """
    return PromptTemplate(
        input_variables=["prompt","task_type","complexity","missing_elements"],
        template=prompt_enhancer_template,
    )
