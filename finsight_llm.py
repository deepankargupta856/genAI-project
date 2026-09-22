import os

from dotenv import load_dotenv
from openai import OpenAI


REFUSAL_MESSAGE = "I can't say that because I'm not trained on it."

SYSTEM_PROMPT = f"""
You are FinSight, an educational finance assistant. Only answer questions substantially
related to finance, financial markets, banking, investments, accounting, corporate
finance, personal finance concepts, and related economics. Never provide personalized
investment advice, direct buy/sell recommendations, guaranteed returns, or predictions
presented as certainty. If a question is outside the finance domain, reply exactly:
"{REFUSAL_MESSAGE}" Keep explanations clear, educational, neutral, and easy to
understand.
""".strip()


load_dotenv()


def get_client() -> OpenAI:
    """Create a Groq client using Groq's OpenAI-compatible API."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


def is_finance_question(question: str) -> bool:
    """
    Use the LLM as a simple finance-domain classifier before generating an answer.

    The response is constrained to one token-like label so application logic can make
    a deterministic allow/refuse decision.
    """
    client = get_client()

    classifier_prompt = f"""
Decide whether the user's question is substantially related to finance education.

Finance includes stock markets, mutual funds, bonds, banking, corporate finance,
accounting basics, financial ratios, finance-related economics, portfolio concepts,
risk and return, derivatives, IPOs, valuation, personal finance concepts, and financial
news or market terminology.

Questions asking for personalized financial advice, buy/sell recommendations, or stock
tips are still finance-related, but must be handled with a safety disclaimer later.

Reply with exactly one word:
FINANCE
or
NOT_FINANCE

User question: {question}
""".strip()

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "groq/compound-mini"),
        messages=[
            {"role": "system", "content": "You classify user questions by domain."},
            {"role": "user", "content": classifier_prompt},
        ],
        temperature=0,
        max_tokens=5,
    )

    label = response.choices[0].message.content.strip().upper()
    return label == "FINANCE"


def generate_finsight_response(question: str) -> str:
    """Return an educational finance response or the exact out-of-domain refusal."""
    if not is_finance_question(question):
        return REFUSAL_MESSAGE

    client = get_client()

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "groq/compound-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0.3,
        max_tokens=700,
    )

    answer = response.choices[0].message.content.strip()

    if not answer:
        raise RuntimeError("The model returned an empty response.")

    return answer
