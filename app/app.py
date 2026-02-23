import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.score import calculate_score
from src.advisor import get_advice, chat

# Page config
st.set_page_config(
    page_title='Dr.Cre',
    page_icon='🎓',
    layout='centered'
)

# CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    /* Base styles */
    html, body, [class*="st-"], .stMarkdown, p, label {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #475569 !important;    
    }

    .stApp {
        background-color: #FFFFFF !important;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Hide header and reduce top padding */
    header {visibility: hidden;}
    .main > div {padding-top: 1rem !important;}
    .block-container {padding-top: 1rem !important;}

    /* Title styles */
    h1 {
        font-size: 2.5em !important;
        font-weight: 600 !important;
        text-align: center;
        color: #475569 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        font-size: 1.3em !important;
        color: #475569 !important;
    }
    
    .subtitle {
        text-align: center;
        color: #666 !important;
        margin-bottom: 1.5em !important;
    }

    /* Button center alignment */
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }
    
    .stButton button {
        padding: 5px 25px !important;
        border-radius: 25px !important;
        border: 2px solid #1a1a1a !important;
        background: white !important;
        color: #1a1a1a !important;
        font-size: 1.1em !important;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background: #f5f5f5 !important;
        border-color: #666 !important;
    }

    /* Input field styles */
    .stNumberInput > div > div {
        background-color: #f9f9f9 !important;
        border-radius: 15px !important;
    }
    
    .stNumberInput input {
        background-color: #f9f9f9 !important;
        color: #475569 !important;
    }
    
    .stNumberInput label {
        color: #475569 !important;
    }
    
    /* +/- button visibility fix */
    .stNumberInput button {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #ddd !important;
    }
    
    .stNumberInput button:hover {
        background-color: #f5f5f5 !important;
    }

    /* Slider styles */
    .stSlider [data-baseweb="slider"] {
        background-color: transparent !important;
    }
    
    .stSlider label {
        color: #475569 !important;
    }

    /* Chat message boxes */
    .message-box {
        border-radius: 18px;
        padding: 12px 18px;
        margin-bottom: 10px;
        max-width: 85%;
        line-height: 1.5;
        color: #1a1a1a !important;
    }
    
    .assistant-msg {
        background: #f0f2f6 !important;
        border-bottom-left-radius: 2px;
        margin-right: auto;
    }
    
    .user-msg {
        background: #eeeeee !important;
        border-bottom-right-radius: 2px;
        margin-left: auto;
    }
    
    /* Chat input field */
    .stChatInput textarea {
        background: white !important;
        color: #1a1a1a !important;
        border: 2px solid #ddd !important;
        border-radius: 15px !important;
        padding-left: 15px;
    }
    
    .stChatInput textarea::placeholder {
        color: #999 !important;
        opacity: 1 !important;
    }
    
    /* Score display */
    .score-display {
        font-size: 4em;
        font-weight: 700;
        text-align: center;
        color: #475569 !important;
        margin: 10px 0 5px 0 !important;
    }
    
    .score-rating {
        font-size: 1.5em;
        color: #666 !important;
        text-align: center;
        margin-bottom: 15px !important;
    }
    
    /* Divider spacing */
    hr {
        margin: 15px 0 !important;
    }
    
    /* Chat messages container */
    .chat-messages {
        margin-top: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'score_result' not in st.session_state:
    st.session_state.score_result = None

# ===== PAGE 2: Results & Chat =====
if st.session_state.page == 'chat':
    # Back button
    if st.button('← Back'):
        st.session_state.page = 'input'
        st.session_state.messages = []
        st.session_state.score_result = None
        st.rerun()
    
    # Header
    st.title('🎓 Dr.Cre')
    st.markdown('<p class="subtitle">Your Credit Score Advisor</p>', unsafe_allow_html=True)
    
    # Display credit score
    score = st.session_state.score_result['score']
    rating = st.session_state.score_result['rating']
    
    st.markdown(f'<div class="score-display">{score}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="score-rating">{rating}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Get initial advice from Dr.Cre
    if len(st.session_state.messages) == 0:
        with st.spinner('Dr.Cre is thinking...'):
            advice = get_advice(st.session_state.user_data, score, rating)
            st.session_state.messages.append({'role': 'assistant', 'content': advice})
    
    # Display chat history
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg['role'] == 'assistant':
            st.markdown(f"""
            <div class="message-box assistant-msg">
                <div style="font-weight: 600; font-size: 0.9em; margin-bottom: 5px;">🎓 Dr.Cre</div>
                <div>{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-box user-msg">
                <div style="font-weight: 600; font-size: 0.9em; margin-bottom: 5px; text-align: right;">👤 You</div>
                <div>{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input('Ask Dr.Cre a question...')
    if user_input:
        # Add user message
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        
        # Build conversation context
        messages = [
            {'role': 'system', 'content': f'You are Dr.Cre. User score: {score}. Answer briefly in 2-3 sentences.'}
        ]
        
        for msg in st.session_state.messages[-4:]:  # Keep last 4 messages for context
            messages.append({'role': msg['role'], 'content': msg['content']})
        
        # Get LLM response
        with st.spinner('Thinking...'):
            response = chat(messages)
            st.session_state.messages.append({'role': 'assistant', 'content': response})
            st.rerun()

# ===== PAGE 1: Input Form =====
elif st.session_state.page == 'input':
    # Header
    st.title('🎓 Dr.Cre')
    st.markdown('<p class="subtitle">Your Credit Score Advisor</p>', unsafe_allow_html=True)
    
    st.subheader('Tell me about yourself')
    
    # Two-column input form
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input('Age', 18, 100, 30)
        monthly_income = st.number_input('Monthly Income ($)', 0, 1000000, 5000)
        credit_utilization = st.slider('Credit Utilization (%)', 0, 100, 30)
        debt_ratio = st.slider('Debt Ratio (%)', 0, 100, 20)
        dependents = st.number_input('Dependents', 0, 10, 0)
    
    with col2:
        open_credits = st.number_input('Open Credit Lines', 0, 58, 3)
        real_estate_loans = st.number_input('Real Estate Loans', 0, 54, 0)
        late_30_59 = st.number_input('Late (30-59 days)', 0, 50, 0)
        late_60_89 = st.number_input('Late (60-89 days)', 0, 50, 0)
        late_90 = st.number_input('Late (90+ days)', 0, 50, 0)
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Calculate button
    if st.button('Calculate My Score', use_container_width=False):
        # Prepare user data
        st.session_state.user_data = {
            'RevolvingUtilizationOfUnsecuredLines': credit_utilization / 100,
            'age': age,
            'NumberOfTime30-59DaysPastDueNotWorse': late_30_59,
            'DebtRatio': debt_ratio / 100,
            'MonthlyIncome': monthly_income,
            'NumberOfOpenCreditLinesAndLoans': open_credits,
            'NumberOfTimes90DaysLate': late_90,
            'NumberRealEstateLoansOrLines': real_estate_loans,
            'NumberOfTime60-89DaysPastDueNotWorse': late_60_89,
            'NumberOfDependents': dependents
        }
        
        # Calculate credit score
        with st.spinner('Calculating...'):
            st.session_state.score_result = calculate_score(st.session_state.user_data)
        
        # Switch to chat page
        st.session_state.page = 'chat'
        st.session_state.messages = []
        st.rerun()