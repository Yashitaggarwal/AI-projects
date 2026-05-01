"""
models_config.py — Centralized LLM Configuration
Manages model selection across all projects with intelligent fallback.

Strategy:
- THINKING/DIRECTOR agents  → gemini-2.5-pro  (deep reasoning)
- RESEARCH/SEARCH agents    → gemini-2.5-flash (fast, high-throughput)
- Optional: Azure GPT-5.4, AWS Bedrock Claude Sonnet 4.6
"""

import os
from enum import Enum


class Provider(str, Enum):
    GEMINI   = "gemini"
    AZURE    = "azure"
    BEDROCK  = "bedrock"


# ── Model IDs (as specified) ───────────────────────────────────────────────────
MODELS = {
    # Google Gemini
    "gemini_pro"   : "gemini-2.5-pro",         # Deep reasoning, synthesis, directors
    "gemini_flash" : "gemini-2.5-flash",         # Fast research, search, data agents

    # Azure OpenAI
    "azure_gpt"    : "gpt-5.4",                  # Azure OpenAI GPT-5.4

    # AWS Bedrock
    "bedrock_sonnet": "anthropic.claude-sonnet-4-6-20250514-v1:0",  # Claude Sonnet 4.6
}


def get_langchain_llm(
    role: str = "research",
    provider: Provider = None,
    temperature: float = 0.7,
):
    """
    Returns the best LangChain LLM for the given role.
    role: 'thinking' | 'research'  
    provider: overrides auto-selection if set
    Falls back through: Bedrock → Azure → Gemini Pro → Gemini Flash
    """
    if provider is None:
        # Auto-detect available provider based on env vars
        if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
            provider = Provider.BEDROCK
        elif os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            provider = Provider.AZURE
        else:
            provider = Provider.GEMINI

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")

    if provider == Provider.BEDROCK:
        try:
            from langchain_aws import ChatBedrock
            import boto3
            session = boto3.Session(
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
            return ChatBedrock(
                model_id=MODELS["bedrock_sonnet"],
                client=session.client("bedrock-runtime"),
                model_kwargs={"temperature": temperature},
            )
        except Exception as e:
            print(f"⚠️ Bedrock unavailable ({e}), falling back to Gemini.")
            provider = Provider.GEMINI

    if provider == Provider.AZURE:
        try:
            from langchain_openai import AzureChatOpenAI
            return AzureChatOpenAI(
                azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", MODELS["azure_gpt"]),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
                temperature=temperature,
            )
        except Exception as e:
            print(f"⚠️ Azure unavailable ({e}), falling back to Gemini.")
            provider = Provider.GEMINI

    # Default: Gemini
    from langchain_google_genai import ChatGoogleGenerativeAI
    model_id = MODELS["gemini_pro"] if role == "thinking" else MODELS["gemini_flash"]
    return ChatGoogleGenerativeAI(
        model=model_id,
        google_api_key=api_key,
        temperature=temperature,
    )


def get_agno_model(role: str = "research", api_key: str = None):
    """
    Returns the best Agno model for the given role.
    role: 'thinking' | 'research'
    """
    from agno.models.google import Gemini
    model_id = MODELS["gemini_pro"] if role == "thinking" else MODELS["gemini_flash"]
    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    return Gemini(id=model_id, api_key=key)


def get_available_provider_info() -> dict:
    """Returns a dict describing which providers are available."""
    return {
        "gemini"  : bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")),
        "azure"   : bool(os.getenv("AZURE_OPENAI_API_KEY")),
        "bedrock" : bool(os.getenv("AWS_ACCESS_KEY_ID")),
    }
