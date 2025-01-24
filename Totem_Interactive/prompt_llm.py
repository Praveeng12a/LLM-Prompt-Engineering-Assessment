# prompt_llm.py

import json
from Prompt_analyzer_Enhancer.analyzer import PromptAnalyzer
from Prompt_analyzer_Enhancer.config import Config
from Prompt_analyzer_Enhancer.llm_selector import LLMSelector
from Prompt_analyzer_Enhancer.prompt_enhancer import PromptEnhancer
import traceback

def main():
    try:
        # Initialize configuration
        config = Config()

        # Step 1: Analyze the Prompt
        analyzer = PromptAnalyzer(config)
        prompt = "Write a sorting algorithm in Python."
        analysis = analyzer.analyze_prompt(prompt)
        print(f"Prompt: {prompt}")
        print(f"Analysis: {analysis}\n")

        # Step 2: Select the Model
        selector = LLMSelector()
        selected_model = selector.select_model(analysis)
        print("\nSelected Model:")
        print(selected_model)

        # Step 3: Enhance the Prompt
        enhancer = PromptEnhancer(config)
        enhanced_prompt = enhancer.enhance_prompt(prompt, analysis)
        print("\nOriginal Prompt:", prompt)
        print("Enhanced Prompt:", enhanced_prompt["enhanced_prompt"]["text"])

        # Structure the output
        output = {
            "analysis": analysis,
            "recommended_llm": {
                "model": selected_model["recommended_llm"]["model"],
                "reasoning": selected_model["recommended_llm"]["reasoning"]
            },
            "enhanced_prompt": {
                "text": enhanced_prompt["enhanced_prompt"]["text"],
                "technique": "Specification Expansion",
                "improvement_metrics": {
                    "clarity": enhanced_prompt["enhanced_prompt"]["improvement_metrics"]["clarity"],
                    "context": enhanced_prompt["enhanced_prompt"]["improvement_metrics"]["context"],
                    "specificity": enhanced_prompt["enhanced_prompt"]["improvement_metrics"]["specificity"]
                }
            }
        }

        # Print the structured output as beautiful JSON
        print("\nStructured Output:\n")
        print(json.dumps(output, indent=4))

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
