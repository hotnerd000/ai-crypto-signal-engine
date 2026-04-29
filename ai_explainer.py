import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
#MODEL = "llama3"   # change if needed
MODEL = "mistral"


def explain_coin(data):
    prompt = f"""
You are an expert crypto quantitative analyst.

Be precise, data-driven, and realistic.

Coin: {data['coin']}
Score: {data['avg_score']}
Expected Profit: {data['expected_profit']:.2f}%

Output:
- Signal reasoning
- Risk factors
- Trade recommendation
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

        result = response.json()
        return result.get("response", "No response from model.")

    except Exception as e:
        return f"Local AI error: {str(e)}"
    
