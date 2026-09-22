# FinSight

FinSight is a simple GenAI-powered Streamlit chatbot for educational finance questions.

It answers only finance-related questions, including topics such as stock markets,
mutual funds, bonds, banking, accounting basics, financial ratios, portfolio concepts,
valuation, derivatives, IPOs, personal finance concepts, and finance-related economics.

For non-finance questions, it responds exactly:

```text
I can't say that because I'm not trained on it.
```

FinSight is for education and financial insight only. It does not provide personalized
financial advice, buy/sell recommendations, stock tips, guaranteed returns, or certain
market predictions.

## Project Structure

```text
.
├── app.py
├── finsight_llm.py
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Add your Groq API key to `.env`.

```text
GROQ_API_KEY=your_real_groq_api_key_here
GROQ_MODEL=groq/compound-mini
```

## Run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal.

## How It Works

The app follows a simple flow:

```text
User Question
→ Finance-domain check using GenAI
→ If unrelated, return the exact refusal message
→ If finance-related, generate a clear educational response
→ Display the answer in the chat interface
```

## Example Questions

```text
What is a P/E ratio?
Explain futures and options.
What is the difference between debt and equity?
Should I buy Reliance stock?
Who is Virat Kohli?
```
