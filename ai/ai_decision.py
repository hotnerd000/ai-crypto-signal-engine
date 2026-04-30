import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
#MODEL = "llama3" qwen3.6   # change if needed
MODEL = "mistral"



def get_ai_decision(data):
    prompt = f"""
You are a crypto trading decision engine.

Given:
Coin: {data['coin']}
Rule Score: {data['score']}
Expected Profit: {data['expected_profit']:.2f}%

Return ONLY JSON:

{{
  "decision": "BUY or SELL or HOLD",
  "confidence": number between 0 and 1
}}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()["response"]

        # 🔥 Extract JSON safely
        start = result.find("{")
        end = result.rfind("}") + 1
        json_str = result[start:end]

        parsed = json.loads(json_str)

        return parsed

    except Exception as e:
        return {"decision": "HOLD", "confidence": 0.0}