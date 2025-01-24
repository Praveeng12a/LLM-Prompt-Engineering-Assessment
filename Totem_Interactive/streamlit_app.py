# streamlit_app.py

import streamlit as st
import json
from Prompt_analyzer_Enhancer.analyzer import PromptAnalyzer
from Prompt_analyzer_Enhancer.config import Config
from Prompt_analyzer_Enhancer.llm_selector import LLMSelector
from Prompt_analyzer_Enhancer.prompt_enhancer import PromptEnhancer

def analyze_prompt(prompt: str):
    config = Config()

    # Analyze the Prompt
    analyzer = PromptAnalyzer(config)
    analysis = analyzer.analyze_prompt(prompt)

    # Select the Model
    selector = LLMSelector()
    selected_model = selector.select_model(analysis)

    # Enhance the Prompt
    enhancer = PromptEnhancer(config)
    enhanced_prompt = enhancer.enhance_prompt(prompt, analysis)

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

    return output

def main():
    st.set_page_config(page_title="Prompt Analyzer and Enhancer", layout="wide")

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("Prompt Analyzer and Enhancer")
    st.write("Enter a prompt to analyze, select the appropriate model, and enhance it.")

    # Chat interface
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['User']}")
        st.json(chat["Assistant"])

    # User input
    with st.form(key="user_input_form", clear_on_submit=True):
        user_input = st.text_input("You:")
        submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            output = analyze_prompt(user_input)

            # Store the conversation in session state
            st.session_state.chat_history.append({
                "User": user_input,
                "Assistant": output
            })

    # Display the current chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['User']}")
        st.json(chat["Assistant"])

if __name__ == "__main__":
    main()






