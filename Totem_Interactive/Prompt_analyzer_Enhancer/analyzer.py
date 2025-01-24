# analyzer.py
import re
from typing import Dict, Any, List
from Prompt_analyzer_Enhancer.templates import create_analysis_prompt_template
from Prompt_analyzer_Enhancer.config import Config

class PromptAnalyzer:
    def __init__(self, config: Config):
        self.llm = config.llm
        self.analysis_prompt = create_analysis_prompt_template()

    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Comprehensive prompt analysis"""
        chain = self.analysis_prompt | self.llm

        try:
            response = chain.invoke({"prompt": prompt})
            print("The response of the prompt is this ", response)
            return self._parse_analysis(response.content, prompt)
        except Exception as e:
            return self._fallback_analysis(prompt, str(e))

    def _parse_analysis(self, response: str, original_prompt: str) -> Dict[str, Any]:
        """Parse and validate LLM's analysis response"""
        try:
            # Extract JSON-like content
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if not json_match:
                return self._fallback_analysis(
                    original_prompt, "No structured response"
                )

            parsed_response = json_match.group(0)

            # Validate and extract key components
            analysis = {
                "task_type": self._extract_task_type(parsed_response, original_prompt),
                "complexity": self._extract_complexity(parsed_response),
                "missing_elements": self._extract_missing_elements(parsed_response),
                "context_score": self._extract_score(parsed_response, "context"),
                "clarity_score": self._extract_score(parsed_response, "clarity"),
            }
            return analysis

        except Exception as e:
            return self._fallback_analysis(original_prompt, str(e))

    def _extract_task_type(self, response: str, prompt: str) -> str:
        """Extract task type with fallback mechanism"""
        task_types = ["code", "writing", "analysis", "general"]

        # Try extracting from response
        for task in task_types:
            if task.lower() in response.lower():
                return task

        # Fallback to heuristic detection
        return self._detect_task_type(prompt)

    def _extract_complexity(self, response: str) -> str:
        """Extract complexity level"""
        complexities = ["Low", "Medium", "High"]
        for complexity in complexities:
            if complexity.lower() in response.lower():
                return complexity
        return "Medium"

    def _extract_missing_elements(self, response: str) -> List[str]:
        """Extract missing elements with robust parsing"""
        missing_patterns = [
            r'"missing_elements":\s*\[(.*?)\]',
            r"missing\s*elements?:\s*\[(.*?)\]",
        ]

        for pattern in missing_patterns:
            match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if match:
                # Clean and split elements
                elements = re.findall(r'"([^"]*)"', match.group(1))
                return [elem.strip() for elem in elements if elem.strip()]

        return ["Insufficient context details"]

    def _extract_score(self, response: str, score_type: str) -> float:
        """Extract numeric score with error handling"""
        try:
            score_pattern = f'"{score_type}_score":\s*(\d+\.?\d*)'
            match = re.search(score_pattern, response)
            return float(match.group(1)) if match else 0.5
        except Exception:
            return 0.5

    def _fallback_analysis(self, prompt: str, error: str = "") -> Dict[str, Any]:
        """Robust fallback analysis method"""
        return {
            "task_type": self._detect_task_type(prompt),
            "complexity": "Medium",
            "missing_elements": ["Insufficient context", f"Parse error: {error}"],
            "context_score": 0.4,
            "clarity_score": 0.5,
        }

    def _detect_task_type(self, prompt: str) -> str:
        """Detect task type using comprehensive heuristics"""
        prompt_lower = prompt.lower()
        task_mappings = {
            "code": ["code", "algorithm", "function", "implement", "programming"],
            "writing": ["write", "essay", "article", "story", "draft", "blog"],
            "analysis": [
                "analyze",
                "research",
                "data",
                "study",
                "investigate",
                "examine",
            ],
        }

        for task, keywords in task_mappings.items():
            if any(kw in prompt_lower for kw in keywords):
                return task

        return "general"


# Example usage
# def main():
#     try:
#         config = Config()
#         analyzer = PromptAnalyzer(config)

#         prompts = "Write a sorting algorithm in Python."

#         result = analyzer.analyze_prompt(prompts)
#         print(f"Prompt: {prompts}")
#         print(f"Analysis: {result}\n")

#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     main()



# output
# Analysis: {'task_type': 'code', 'complexity': 'Low', 'missing_elements': ['Sorting algorithm type (e.g., bubble sort, merge sort, quicksort)', 'Input data type (e.g., integers, floats, strings)', 'Desired output format (e.g., in-place sorting, return a new sorted list)', 'Constraints on space and time complexity'], 'context_score': 0.2, 'clarity_score': 0.7}