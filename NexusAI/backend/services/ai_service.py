"""
Single point of contact with LLM providers.

Every other service (chat, coding, study, resume, pdf_chat) calls
`generate_response()` instead of talking to OpenAI or Anthropic directly.
The provider used is controlled by AI_PROVIDER in .env, and can optionally
be overridden per-call (e.g. from a query param) via the `provider` arg.

Message format is the same regardless of provider:
    [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
"""
from config import Config
from middleware.error_handler import AppError
from utils.logger import get_logger

logger = get_logger(__name__)


def _call_openai(system_prompt, messages, model=None, max_tokens=1024, temperature=0.7):
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise AppError("openai package not installed on the server", 500) from exc

    if not Config.OPENAI_API_KEY:
        raise AppError("OPENAI_API_KEY is not configured", 500)

    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    chat_messages = [{"role": "system", "content": system_prompt}] + messages

    try:
        response = client.chat.completions.create(
            model=model or Config.OPENAI_MODEL,
            messages=chat_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except Exception as exc:
        logger.error("OpenAI call failed: %s", exc)
        raise AppError("The AI provider request failed. Please try again.", 502)

    return response.choices[0].message.content


def _call_anthropic(system_prompt, messages, model=None, max_tokens=1024, temperature=0.7):
    try:
        import anthropic
    except ImportError as exc:
        raise AppError("anthropic package not installed on the server", 500) from exc

    if not Config.ANTHROPIC_API_KEY:
        raise AppError("ANTHROPIC_API_KEY is not configured", 500)

    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    try:
        response = client.messages.create(
            model=model or Config.ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=messages,
        )
    except Exception as exc:
        logger.error("Anthropic call failed: %s", exc)
        raise AppError("The AI provider request failed. Please try again.", 502)

    return "".join(block.text for block in response.content if block.type == "text")


_PROVIDERS = {
    "openai": _call_openai,
    "anthropic": _call_anthropic,
}


def generate_response(system_prompt, messages, provider=None, model=None,
                       max_tokens=1024, temperature=0.7):
    """
    system_prompt: str - instructions defining the agent's behavior
    messages: list[{"role": "user"|"assistant", "content": str}] - conversation so far
    provider: optional override of AI_PROVIDER ("openai" | "anthropic")
    model: optional override of the default model for the chosen provider
    """
    chosen = (provider or Config.AI_PROVIDER).lower()
    fn = _PROVIDERS.get(chosen)
    if fn is None:
        raise AppError(f"Unknown AI provider '{chosen}'. Use 'openai' or 'anthropic'.", 400)

    logger.info("Generating response via provider=%s", chosen)
    return fn(system_prompt, messages, model=model, max_tokens=max_tokens, temperature=temperature)
