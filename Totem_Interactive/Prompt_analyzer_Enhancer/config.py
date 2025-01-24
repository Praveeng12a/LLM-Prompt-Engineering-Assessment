# config.py
from typing import Dict, Any
import os
from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

# Load environment variables
load_dotenv()

class Config:
    def __init__(self, temperature: float = 0.4):
        self.api_key = self.load_api_key()
        self.temperature = temperature
        self.llm = self.initialize_llm()

    @staticmethod
    def load_api_key() -> str:
        """Load API key from environment variable"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        return api_key

    def initialize_llm(self):
        """Initialize Google Generative AI model"""
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=self.api_key,
            temperature=self.temperature,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )
