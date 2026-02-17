import ollama

def get_advice(user_data: dict, score: int, rating: str) -> str:
    
    prompt = f"""
You are Dr.Cre, a friendly and professional credit score advisor.

User credit profile:
- Credit score: {score} ({rating})
- Credit utilization: {user_data['RevolvingUtilizationOfUnsecuredLines'] * 100:.0f}%
- Age: {user_data['age']}
- Late payments (30-59 days): {user_data['NumberOfTime30-59DaysPastDueNotWorse']}
- Late payments (60-89 days): {user_data['NumberOfTime60-89DaysPastDueNotWorse']}
- Late payments (90+ days): {user_data['NumberOfTimes90DaysLate']}
- Monthly income: ${user_data['MonthlyIncome']:,}
- Debt ratio: {user_data['DebtRatio'] * 100:.0f}%
- Open credit lines: {user_data['NumberOfOpenCreditLinesAndLoans']}
- Dependents: {user_data['NumberOfDependents']}

Give exactly 3 specific tips to improve this credit score.
Each tip must include estimated score improvement (e.g. +20 points).
Keep it simple, friendly and actionable.
End with a short encouraging message.
"""

    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response['message']['content']