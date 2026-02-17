import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.score import calculate_score
from src.advisor import get_advice

# Page config
st.set_page_config(page_title='Dr.Cre', page_icon='🏦')

st.title('🏦 Dr.Cre')
st.subheader('Your Personal Credit Score Advisor')

st.divider()

# User inputs
st.header('Enter Your Information')

col1, col2 = st.columns(2)

with col1:
    age = st.number_input('Age', min_value=18, max_value=100, value=35)
    monthly_income = st.number_input('Monthly Income ($)', min_value=0, value=5000)
    debt_ratio = st.slider('Debt Ratio', 0.0, 1.0, 0.3)
    credit_utilization = st.slider('Credit Utilization', 0.0, 1.0, 0.3)
    dependents = st.number_input('Number of Dependents', min_value=0, max_value=10, value=0)

with col2:
    open_credits = st.number_input('Open Credit Lines', min_value=0, max_value=58, value=5)
    real_estate_loans = st.number_input('Real Estate Loans', min_value=0, max_value=54, value=0)
    late_30_59 = st.number_input('Late Payments (30-59 days)', min_value=0, max_value=50, value=0)
    late_60_89 = st.number_input('Late Payments (60-89 days)', min_value=0, max_value=50, value=0)
    late_90 = st.number_input('Late Payments (90+ days)', min_value=0, max_value=50, value=0)

st.divider()

# Calculate button
if st.button('Calculate My Credit Score', type='primary'):
    user_data = {
        'RevolvingUtilizationOfUnsecuredLines': credit_utilization,
        'age': age,
        'NumberOfTime30-59DaysPastDueNotWorse': late_30_59,
        'DebtRatio': debt_ratio,
        'MonthlyIncome': monthly_income,
        'NumberOfOpenCreditLinesAndLoans': open_credits,
        'NumberOfTimes90DaysLate': late_90,
        'NumberRealEstateLoansOrLines': real_estate_loans,
        'NumberOfTime60-89DaysPastDueNotWorse': late_60_89,
        'NumberOfDependents': dependents
    }

    with st.spinner('Calculating...'):
        result = calculate_score(user_data)
    
    st.header(f'Your Credit Score: {result["score"]}')
    st.subheader(f'Rating: {result["rating"]}')
    st.write(f'Default Probability: {result["default_probability"]}%')

    st.divider()

    with st.spinner('Getting advice from Dr.Cre...'):
        advice = get_advice(user_data, result['score'], result['rating'])
    
    st.header('Dr.Cre\'s Advice')
    st.write(advice)