from .custom_class import ChatAnthropicCustom
from .custom_class_gemini import ChatGoogleGenerativeAICustom
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_model(model_name, temperature=0):
    # Check for custom endpoint keys - use custom endpoints if available, otherwise use standard APIs
    has_custom_anthropic = bool(os.getenv("CUSTOM_ANTHROPIC_API_KEY")) and bool(os.getenv("CUSTOM_ANTHROPIC_API_URL"))
    has_custom_google = bool(os.getenv("CUSTOM_GOOGLE_API_KEY")) and bool(os.getenv("CUSTOM_GOOGLE_API_ENDPOINT"))

    # Prepare OpenAI kwargs - explicitly pass api_key and base_url if available
    openai_base_url = os.getenv("OPENAI_API_BASE")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_kwargs = {}
    if openai_base_url:
        openai_kwargs["base_url"] = openai_base_url
    if openai_api_key:
        openai_kwargs["api_key"] = openai_api_key

    # OpenAI models - only create when requested
    if model_name in ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "o1", "gpt-4-turbo", "gpt-3.5-turbo"]:
        if model_name == "gpt-4o":
            return ChatOpenAI(model="gpt-4o", temperature=temperature, **openai_kwargs)
        elif model_name == "gpt-4o-mini":
            return ChatOpenAI(model="gpt-4o-mini", temperature=temperature, **openai_kwargs)
        elif model_name == "gpt-4.1":
            return ChatOpenAI(model="gpt-4.1", temperature=temperature, **openai_kwargs)
        elif model_name == "o1":
            return ChatOpenAI(model="o1", **openai_kwargs)
        elif model_name == "gpt-4-turbo":
            return ChatOpenAI(model="gpt-4-turbo", temperature=temperature, **openai_kwargs)
        elif model_name == "gpt-3.5-turbo":
            return ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature, **openai_kwargs)

    # Anthropic models - use custom endpoint if available, otherwise use standard Anthropic API
    if model_name in ['claude_4_sonnet', 'claude_4_opus', 'claude_3_7_sonnet', 'claude_3_5_sonnet', 'claude_3_opus', 'claude_3_haiku', 'claude_3_sonnet']:
        if has_custom_anthropic:
            if model_name == 'claude_4_sonnet':
                return ChatAnthropicCustom(model='claude-sonnet-4-20250514-v1', temperature=temperature)
            elif model_name == 'claude_4_opus':
                return ChatAnthropicCustom(model='claude-opus-4-20250514-v1', temperature=temperature)
            elif model_name == 'claude_3_7_sonnet':
                return ChatAnthropicCustom(model='claude-3-7-sonnet-20250219-v1', temperature=temperature)
            elif model_name == 'claude_3_5_sonnet':
                return ChatAnthropicCustom(model_name="claude-3-5-sonnet-20240620-v1", temperature=temperature)
            elif model_name == 'claude_3_opus':
                return ChatAnthropicCustom(model_name="claude-3-opus-20240229-v1", temperature=temperature)
            elif model_name == 'claude_3_haiku':
                return ChatAnthropicCustom(model_name="claude-3-haiku-20240307-v1", temperature=temperature)
            elif model_name == 'claude_3_sonnet':
                return ChatAnthropicCustom(model_name="claude-3-sonnet-20240229-v1", temperature=temperature)
        else:
            # Use standard Anthropic API with ANTHROPIC_API_KEY
            if model_name == 'claude_4_sonnet':
                return ChatAnthropic(model='claude-sonnet-4-20250514', temperature=temperature)
            elif model_name == 'claude_4_opus':
                return ChatAnthropic(model='claude-opus-4-20250514', temperature=temperature)
            elif model_name == 'claude_3_7_sonnet':
                return ChatAnthropic(model='claude-3-7-sonnet-20250219', temperature=temperature)
            elif model_name == 'claude_3_5_sonnet':
                return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=temperature)
            elif model_name == 'claude_3_opus':
                return ChatAnthropic(model="claude-3-opus-20240229", temperature=temperature)
            elif model_name == 'claude_3_haiku':
                return ChatAnthropic(model="claude-3-haiku-20240307", temperature=temperature)
            elif model_name == 'claude_3_sonnet':
                return ChatAnthropic(model="claude-3-sonnet-20240229", temperature=temperature)

    # Google/Gemini models
    if model_name == "gemini-2.5-pro":
        if has_custom_google:
            return ChatGoogleGenerativeAICustom(
                model="gemini-2.5-pro",
                temperature=temperature,
                client_options={"api_endpoint": os.getenv("CUSTOM_GOOGLE_API_ENDPOINT")},
                google_api_key=os.getenv("CUSTOM_GOOGLE_API_KEY"),
                thinking_budget=200
            )
        else:
            return ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=temperature)
    elif model_name == "gemini-2.0-flash-exp":
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=temperature)
    elif model_name == "gemini-1.5-flash":
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature)
    elif model_name == "gemini-1.5-flash-8b":
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=temperature)
    elif model_name == "gemini-1.5-pro":
        return ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=temperature)

    raise ValueError(f"Unknown model name: {model_name}")
