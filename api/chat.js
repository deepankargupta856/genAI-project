const REFUSAL_MESSAGE = "I can't say that because I'm not trained on it.";

const SYSTEM_PROMPT = `You are FinSight, an educational finance assistant. Only answer questions substantially related to finance, financial markets, banking, investments, accounting, corporate finance, personal finance concepts, and related economics. Never provide personalized investment advice, direct buy/sell recommendations, guaranteed returns, or predictions presented as certainty. If a question is outside the finance domain, reply exactly: '${REFUSAL_MESSAGE}'. Keep explanations clear, educational, neutral, and easy to understand.`;

async function callGroq(messages, maxTokens = 700) {
  const apiKey = process.env.GROQ_API_KEY;
  const model = process.env.GROQ_MODEL || "groq/compound-mini";

  if (!apiKey) {
    throw new Error("GROQ_API_KEY is not configured in Vercel environment variables.");
  }

  const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.3,
      max_tokens: maxTokens,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Groq API error ${response.status}: ${errorText}`);
  }

  const data = await response.json();
  return data.choices?.[0]?.message?.content?.trim() || "";
}

async function isFinanceQuestion(question) {
  const classifierPrompt = `Decide whether the user's question is substantially related to finance education.

Finance includes stock markets, mutual funds, bonds, banking, corporate finance, accounting basics, financial ratios, finance-related economics, portfolio concepts, risk and return, derivatives, IPOs, valuation, personal finance concepts, and financial news or market terminology.

Questions asking for personalized financial advice, buy/sell recommendations, or stock tips are still finance-related, but must be handled with a safety disclaimer later.

Reply with exactly one word:
FINANCE
or
NOT_FINANCE

User question: ${question}`;

  const label = await callGroq(
    [
      { role: "system", content: "You classify user questions by domain. Reply only FINANCE or NOT_FINANCE." },
      { role: "user", content: classifierPrompt },
    ],
    10
  );

  return label.toUpperCase().includes("FINANCE") && !label.toUpperCase().includes("NOT_FINANCE");
}

export default async function handler(request, response) {
  if (request.method !== "POST") {
    response.setHeader("Allow", "POST");
    return response.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { message } = request.body || {};

    if (!message || typeof message !== "string") {
      return response.status(400).json({ error: "Message is required." });
    }

    if (!(await isFinanceQuestion(message))) {
      return response.status(200).json({ reply: REFUSAL_MESSAGE });
    }

    const reply = await callGroq([
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: message },
    ]);

    return response.status(200).json({ reply: reply || REFUSAL_MESSAGE });
  } catch (error) {
    return response.status(500).json({
      error: "Sorry, I could not generate a response right now. Please check your API key, internet connection, and model configuration.",
      detail: error.message,
    });
  }
}
