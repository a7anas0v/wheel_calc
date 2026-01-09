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
            background-color: #374151;
            border: 1px solid #4b5563;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            transition: all 0.2s ease-in-out;
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
schema = {
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "changeAmount": {"type": "number"},
        "changePercent": {"type": "number"},
        "movementReason": {"type": "string"},
        "sentiment": {"type": "string", "enum": ["Positive", "Neutral", "Negative"]},
        "news": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "snippet": {"type": "string"},
                    "publishDate": {"type": "string"},
                    "category": {"type": "string", "enum": ["Today", "This Week", "Older"]},
                    "url": {"type": "string"}
                },
                "required": ["title", "snippet", "publishDate", "category", "url"]
            }
        }
    },
    "required": ["price", "changeAmount", "changePercent", "movementReason", "sentiment", "news"]
}

# --- API Call ---
@st.cache_data(ttl=900)
def fetch_stock_news(ticker: str):
    # ТУК Е ПРОМЯНАТА: Ползваме 'google_search_retrieval' вместо старото име
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        generation_config={"response_mime_type": "application/json", "response_schema": schema},
        tools=[{"google_search_retrieval": {}}] 
    )
    
    prompt = f"""
    For the stock ticker "{ticker}", provide:
    1. Latest price, dollar change, percent change.
    2. One-sentence explanation for movement.
    3. Sentiment (Positive/Neutral/Negative).
    4. Recent news list (title, snippet, YYYY-MM-DD date, url, category: Today/This Week/Older).
    Use real-time data via Google Search tool.
    """
    
    response = model.generate_content(prompt)
    return json.loads(response.text)

# --- UI Rendering ---
st.markdown(
    '<div style="display: flex; align-items: center; justify-content: center; gap: 12px;">'
    '<span style="font-size: 2rem;">📈</span>'
    '<h1 style="font-size: 2.25rem; font-weight: bold; color: white;">Stock News Summarizer</h1>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 1.125rem;">Enter a ticker (e.g. TSLA, NVDA) for real-time AI analysis.</p>', unsafe_allow_html=True)

with st.form(key="ticker_form"):
    ticker_input = st.text_input("Stock Ticker", placeholder="e.g., GOOGL, TSLA, AAPL", label_visibility="collapsed")
    submit_button = st.form_submit_button("Get News")

if submit_button and ticker_input:
    with st.spinner(f"🔍 Analyzing latest market news for {ticker_input.upper()}..."):
        try:
            data = fetch_stock_news(ticker_input)
            if not data:
                st.warning("No data found.")
            else:
                # --- Quote ---
                is_pos = data['changeAmount'] >= 0
                delta = f"{data['changeAmount']:+.2f} ({data['changePercent']:+.2%})"
                
                st.subheader(f"{ticker_input.upper()} Quote")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Price", f"${data['price']:.2f}", delta)
                with c2:
                    st.info(f"**Insight:** {data['movementReason']}")

                # --- News ---
                st.subheader("News Analysis")
                sent = data['sentiment']
                emoji = {"Positive": "😊", "Neutral": "😐", "Negative": "😞"}.get(sent, "🤔")
                st.success(f"**Sentiment:** {sent} {emoji}")

                for cat in ['Today', 'This Week', 'Older']:
                    articles = [a for a in data.get('news', []) if a['category'] == cat]
                    if articles:
                        st.markdown(f"### {cat}")
                        for a in articles:
                            st.markdown(f"""
                            <a href="{a['url']}" target="_blank" style="text-decoration: none;">
                                <div class="article-card">
                                    <h4>{a['title']}</h4>
                                    <div class="date-info">📅 {a['publishDate']}</div>
                                    <p>{a['snippet']}</p>
                                </div>
                            </a>
                            """, unsafe_allow_html=True)
                            
        except Exception as e:
            st.error(f"Error: {e}")

# --- Footer ---
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; margin-top: 4rem;'>
        <small>Powered by <b>Aivan Capital</b> | AI Generated Data</small>
    </div>
    """, 
    unsafe_allow_html=True
)
