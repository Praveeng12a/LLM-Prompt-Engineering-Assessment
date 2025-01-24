# llm_selector.py
from typing import Dict, Any, List
import random

class LLMSelector:
    # Extensible LLM model mapping
    LLM_MODELS = {
        "code": {
            "Low": ["claude-haiku", "mistral-small"],
            "Medium": ["claude-opus", "gpt-3.5-turbo"],
            "High": ["claude-3-5-sonnet", "gpt-4"]
        },
        "writing": {
            "Low": ["claude-haiku", "gpt-3.5-turbo"],
            "Medium": ["claude-opus", "anthropic-claude"],
            "High": ["claude-3-5-sonnet", "gpt-4"]
        },
        "analysis": {
            "Low": ["claude-haiku", "mistral-small"],
            "Medium": ["claude-opus", "gpt-3.5-turbo"],
            "High": ["claude-3-5-sonnet", "gpt-4-turbo"]
        },
        "general": {
            "Low": ["claude-haiku"],
            "Medium": ["claude-opus"],
            "High": ["claude-3-5-sonnet"]
        }
    }

    @classmethod
    def select_model(cls, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dynamically select the most suitable LLM based on prompt analysis
        """
        # Extract task type and complexity, with defaults
        task_type = analysis.get('task_type', 'general').lower()
        complexity = analysis.get('complexity', 'Medium')

        # Normalize inputs
        task_type = task_type if task_type in cls.LLM_MODELS else 'general'
        complexity = complexity if complexity in ['Low', 'Medium', 'High'] else 'Medium'

        # Select models for the task type and complexity
        available_models = cls.LLM_MODELS.get(task_type, cls.LLM_MODELS['general'])[complexity]
        primary_model = random.choice(available_models)

        reasoning = cls._generate_reasoning(task_type, complexity)

        return {
             "recommended_llm": {
                "model": primary_model,
                "reasoning": reasoning
        }
    }

    @classmethod
    def _generate_reasoning(cls, task_type: str, complexity: str) -> str:
        """
        Generate model selection reasoning based on task and complexity
        """
        if task_type == "code":
            if complexity == "Low":
               return "Simple coding task or basic implementation."
            elif complexity == "Medium":
                return "Coding task requiring intermediate level of implementation details."
            else: # High complexity
                return "Technical task requiring code generation and understanding of implementation details."
        elif task_type == "writing":
             if complexity == "Low":
               return "Basic writing task or simple text generation."
             elif complexity == "Medium":
                return "Writing task that may require creative writing or some level of complexity."
             else: # High complexity
                 return "Complex writing task that may require creativity, structure, and detailed outputs."
        elif task_type == "analysis":
            if complexity == "Low":
               return "Simple analytical task with straightforward data."
            elif complexity == "Medium":
                return "Analytical task that may involve data examination."
            else: # High complexity
                 return "Complex analysis of datasets requiring thorough examination and reasoning."
        else: # General
            if complexity == "Low":
               return "General low-level task."
            elif complexity == "Medium":
                 return "General task at the medium level"
            else:
                return "General task at the high level"



# Example usage
# def main():
#     analysis = {
#         "task_type": "code",
#         "complexity": "Medium",
#         "context_score": 0.7,
#         "clarity_score": 0.8
#     }

#     selector = LLMSelector()
    
#     result = selector.select_model(analysis)
#     # print("Analysis:")
#     # print(analysis)
#     print("\nLLM Selection:")
#     print(result)

# if __name__ == "__main__":
#     main()