from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


def make_llm(model_name: str = "openai/gpt-oss-120b:free", temperature: float = 0.0) -> ChatOpenAI:
    """
   OpenRouter uses the OpenAI-compatible API.
    For any free model, you can start with model_name='openrouter/free'.

    If the calling tool is unstable, replace it with a specific OpenRouter model.,
    which supports tools, the default model is gpt-oss-120b:free.
    """
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY не найден. Создайте .env по примеру .env.example"
        )

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=temperature,
        default_headers={
            "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost:3000"),
            "X-OpenRouter-Title": os.getenv(
                "OPENROUTER_APP_NAME", "Interpretability Agent Tutorial"
            ),
        },
    )