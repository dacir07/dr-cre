import ollama

def get_advice(user_data: dict, score: int, rating: str):
    """
    Stream advice from Ollama (generator)
    """
    prompt = f"""
You are Dr.Cre, a credit score advisor.

User's credit score: {score} ({rating})

Give exactly 2 short, actionable tips to improve their score.
Keep each tip to one sentence.
Be direct and helpful.
"""

    stream = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True
    )
    
    for chunk in stream:
        yield chunk['message']['content']

def chat(messages: list):
    """
    Stream chat response (generator)
    """
    stream = ollama.chat(
        model='llama3.1',
        messages=messages,
        stream=True
    )
    
    for chunk in stream:
        yield chunk['message']['content']