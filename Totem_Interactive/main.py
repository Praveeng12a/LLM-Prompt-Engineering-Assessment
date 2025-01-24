# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Prompt_analyzer_Enhancer.analyzer import PromptAnalyzer
from Prompt_analyzer_Enhancer.config import Config
from Prompt_analyzer_Enhancer.llm_selector import LLMSelector
from Prompt_analyzer_Enhancer.prompt_enhancer import PromptEnhancer

app = FastAPI(
    title="Prompt Processing API",
    description="API for analyzing, enhancing, and selecting LLM for prompts",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/documentation"
)

class PromptRequest(BaseModel):
    prompt: str
    analysis: dict = None

class AnalysisResponse(BaseModel):
    analysis: dict

class LLMResponse(BaseModel):
    recommended_llm: dict

class EnhancedPromptResponse(BaseModel):
    enhanced_prompt: dict

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize configuration and components
config = Config()
analyzer = PromptAnalyzer(config)
selector = LLMSelector()
enhancer = PromptEnhancer(config)

@app.get("/", response_class=HTMLResponse)
async def welcome():
    with open("Prompt_analyzer_Enhancer/welcome.html", "r") as f:
        welcome_html = f.read()
    return welcome_html


@app.post("/analyze-prompt", response_model=AnalysisResponse)
async def analyze_prompt(request: PromptRequest):
    try:
        analysis = analyzer.analyze_prompt(request.prompt)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/select-llm", response_model=LLMResponse)
async def select_llm(request: PromptRequest):
    try:
        selected_model = selector.select_model(request.analysis)
        return {"recommended_llm": selected_model["recommended_llm"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enhance-prompt", response_model=EnhancedPromptResponse)
async def enhance_prompt(request: PromptRequest):
    try:
        enhanced_prompt = enhancer.enhance_prompt(request.prompt, request.analysis)
        return {"enhanced_prompt": enhanced_prompt["enhanced_prompt"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run with: uvicorn main:app --reload