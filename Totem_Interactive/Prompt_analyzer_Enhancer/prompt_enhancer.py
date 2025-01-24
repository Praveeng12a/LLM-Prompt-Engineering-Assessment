# prompt_enhancer.py
from typing import Dict, Any
from dotenv import load_dotenv
from Prompt_analyzer_Enhancer.config import Config
from Prompt_analyzer_Enhancer.templates import create_prompt_enhancer_template
from langchain.chains import LLMChain


class PromptEnhancer:
    def __init__(self, config: Config):
        self.llm = config.llm
        self.prompt_enhancer_template = create_prompt_enhancer_template()

    def enhance_prompt(self, original_prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        # Create LLM Chain for enhancement
        chain = LLMChain(
            llm=self.llm, 
            prompt=self.prompt_enhancer_template
        )

        # Generate enhanced prompt
        try:
            # print("Invoking chain with:")
            # print("Prompt:", original_prompt)
            # print("Task Type:", analysis.get("task_type", "general"))
            # print("Missing Elements:", ", ".join(analysis.get("missing_elements", [])))

            enhanced_result = chain.run(
                prompt=original_prompt,
                task_type=analysis.get("task_type", "general"),
                complexity=analysis.get("complexity", "medium"),
                missing_elements=", ".join(analysis.get("missing_elements", []))
            )

            # print("Raw Enhanced Result:", enhanced_result)

            # Clean and structure the enhanced prompt
            cleaned_text = enhanced_result.strip()
            
            return {
                "enhanced_prompt": {
                    "text": cleaned_text,
                    "technique": "Specification Expansion",
                    "improvement_metrics": {
                        "clarity": round(min(analysis.get("clarity_score", 0.5) + 0.4, 1.0), 2),
                        "context": round(min(analysis.get("context_score", 0.4) + 0.5, 1.0), 2),
                        "specificity": round(0.6, 2)
                    }
                }
            }
        except Exception as e:
            print(f"Error occurred: {e}")
            # Fallback enhancement
            return {
                "enhanced_prompt": {
                    "text": f"{original_prompt}. Please provide more specific details and context.",
                    "technique": "Basic Enhancement",
                    "improvement_metrics": {
                        "clarity": 0.4,
                        "context": 0.5,
                        "specificity": 0.6
                    }
                }
            }

# Example usage
# def main():
#     try:
#         config = Config()
#         enhancer = PromptEnhancer(config)

#         case = {
#             "prompt": "write code for sorting array",
#             "analysis": {
#                 "task_type": "code",
#                 "complexity":"low",
#                 "missing_elements": [
#                     "array type",
#                     "sorting algorithm",
#                     "performance requirements",
#                 ],
#                 "context_score": 0.4,
#                 "clarity_score": 0.5,
#             },
#         }

#         result = enhancer.enhance_prompt(case["prompt"], case["analysis"])
#         print("\nOriginal Prompt:", case["prompt"])
#         print("Enhanced Prompt:", result)
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         import traceback
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()