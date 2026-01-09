import streamlit as st
import google.generativeai as genai
import json
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock News Summarizer | Aivan Capital",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #030712; }
        .main .block-container { max-width: 900px; padding-top: 2rem; padding-bottom: 2rem; }
        .stTextInput > div > div > input { background-color: #1f2937; border: 2px solid #4b5563; color: white; }
        .stButton > button { background-color: #0891b2; color: white; font-weight: bold; border-radius: 0.375rem; width: 100%; }
        .stButton > button:hover { background-color: #06b6d4; }
        .article-card {
            background-color: #374151; border: 1px solid #4b5563; padding: 1.5rem;
            border-radius: 0.5rem; margin-bottom: 1rem; transition: all 0.2s ease-in-out;
        }
        .article-card:hover { background-color: #4b5563; border-color: #6b7280; }
        .article-card a { text-decoration: none; color: #f9fafb; }
        .article-card h4 { font-weight: 600; margin-bottom: 0.5rem; }
        .article-card .date-info { font-size: 0.875rem; color: #9ca3af; margin-bottom: 0.5rem; }
        .article-card p { color: #d1d5db; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- Gemini API Configuration ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("🚨 Google API Key not found. Please add it to your Streamlit secrets.")
    st.stop()

# --- Schema ---
# Описваме структурата на данните, които искаме
response_schema = {
    "type": "OBJECT",
    "properties": {
        "price": {"type": "NUMBER"},
        "changeAmount": {"type": "NUMBER"},
        "changePercent": {"type": "NUMBER"},
        "movementReason": {"type": "STRING"},
        "sentiment": {"type": "STRING", "enum": ["Positive", "Neutral", "Negative"]},
        "news": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "snippet": {"type": "STRING"},
                    "publishDate": {"type": "STRING"},
                    "category": {"type": "STRING", "enum": ["Today", "This Week", "Older"]},
                    "url": {"type": "STRING"}
                }
            }
        }
    }
}

# --- API Call ---
@st.cache_data(ttl=900)
def fetch_stock_news(ticker: str):
    # Използваме най-новия и стабилен синтаксис за версия 0.8.3
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools='google_search_retrieval' # В новата версия може да е просто 'google_search', но retrieval е по-сигурен за structured data
    )
    
    prompt = f"""
    Get real-time stock data and news for {ticker}.
    Return a JSON object with:
    - price, changeAmount, changePercent
    - movementReason (one sentence)
    - sentiment
    - news (list of articles with title, snippet, publishDate, url, category)
    """
    
    # Използваме response_mime_type за JSON отговор
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema
        )
    )
    return json.loads(response.text)

# --- UI Rendering ---
st.markdown('<div style="text-align: center;"><span style="font-size: 2rem;">📈</span><h1 style="display:inline;"> Stock News Summarizer</h1></div>', unsafe_allow_html=True)

with st.form(key="ticker_form"):
    ticker_input = st.text_input("Stock Ticker", placeholder="e.g., TSLA", label_visibility="collapsed")
    submit_button = st.form_submit_button("Get News")

if submit_button and ticker_input:
    with st.spinner(f"🔍 Analyzing {ticker_input.upper()}..."):
        try:
            data = fetch_stock_news(ticker_input)
            
            # Quote Section
            st.subheader(f"{ticker_input.upper()} Quote")
            c1, c2 = st.columns(2)
            delta = f"{data.get('changeAmount', 0):+.2f} ({data.get('changePercent', 0):+.2%})"
            c1.metric("Price", f"${data.get('price', 0):.2f}", delta)
            c2.info(data.get('movementReason', 'N/A'))

            # News Section
            st.subheader("News Analysis")
            st.success(f"Sentiment: {data.get('sentiment', 'Neutral')}")
            
            news_items = data.get('news', [])
            if not news_items:
                st.write("No news found.")
            
            for cat in ['Today', 'This Week', 'Older']:
                articles = [a for a in news_items if a.get('category') == cat]
                if articles:
                    st.markdown(f"### {cat}")
                    for a in articles:
                        st.markdown(f"""
                        <a href="{a.get('url', '#')}" target="_blank" style="text-decoration: none;">
                            <div class="article-card">
                                <h4>{a.get('title', 'No Title')}</h4>
                                <div class="date-info">📅 {a.get('publishDate', '')}</div>
                                <p>{a.get('snippet', '')}</p>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
            # Ако гръмне, показваме точната грешка, за да я оправим

# --- Footer ---
st.markdown("<div style='text-align: center; color: #6b7280; margin-top: 4rem;'><small>Powered by <b>Aivan Capital</b></small></div>", unsafe_allow_html=True)
