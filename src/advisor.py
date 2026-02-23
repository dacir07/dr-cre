import ollama

def get_advice(user_data: dict, score: int, rating: str) -> str:
    prompt = f"""
You are Dr.Cre, a credit score advisor.

User's credit score: {score} ({rating})

Give exactly 2 short, actionable tips to improve their score.
Keep each tip to one sentence.
Be direct and helpful.
"""

    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response['message']['content']

def chat(messages: list) -> str:
    response = ollama.chat(
        model='llama3.1',
        messages=messages
    )
    
    return response['message']['content']