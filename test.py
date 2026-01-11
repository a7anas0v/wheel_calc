import streamlit as st
import google.generativeai as genai
import json
import os
import yfinance as yf
from datetime import datetime
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock News Summarizer | Aivan Capital",
    page_icon="📈",
    layout="wide", # Промених на wide, за да се събере добре тикерът
    initial_sidebar_state="collapsed",
)

# --- 1. ФУНКЦИЯ ЗА ЖИВИ ДАННИ (ОТ WHEEL TERMINAL) ---
@st.cache_data(ttl=300)
def get_live_market_data():
    tickers = {
        'S&P 500': '^GSPC',
        'NASDAQ 100': '^NDX',
        'VIX (FEAR)': '^VIX',
        'GOLD': 'GC=F',
        'CRUDE OIL': 'CL=F',
        'NAT GAS': 'NG=F'
    }
    live_data = []
    try:
        data = yf.download(list(tickers.values()), period="2d", progress=False)['Close']
        for name, symbol in tickers.items():
            try:
                # Обработка на данните (същата логика като преди)
                if isinstance(data, pd.DataFrame) and symbol in data.columns:
                    series = data[symbol]
                else:
                    series = data 
                
                if len(series) >= 1:
                    price = series.iloc[-1]
                    change_pct = 0.0
                    if len(series) >= 2:
                        prev_close = series.iloc[-2]
                        change_pct = ((price - prev_close) / prev_close) * 100
                    
                    direction = "up" if change_pct >= 0 else "down"
                    if change_pct == 0: direction = "neutral"
                    
                    if name == 'VIX (FEAR)': price_fmt = f"{price:.2f}"
                    else: price_fmt = f"${price:,.2f}" if price > 1000 else f"${price:.2f}"
                    if name in ['S&P 500', 'NASDAQ 100']: price_fmt = f"{price:,.2f}"
                        
                    live_data.append({"sym": name, "price": price_fmt, "chg": f"{change_pct:+.2f}%", "dir": direction})
                else:
                    live_data.append({"sym": name, "price": "N/A", "chg": "0.00%", "dir": "neutral"})
            except:
                live_data.append({"sym": name, "price": "ERR", "chg": "---", "dir": "neutral"})
    except:
        pass
    return live_data

# --- Custom CSS (Обединено) ---
st.markdown("""
    <style>
        /* Основен фон */
        .stApp { background-color: #030712; color: #f8fafc; }
        
        /* Стилове за Новините */
        .main .block-container { max-width: 1000px; padding-top: 2rem; padding-bottom: 2rem; }
        .stTextInput > div > div > input { background-color: #1f2937; border: 2px solid #4b5563; color: white; }
        .stButton > button { background-color: #0891b2; color: white; font-weight: bold; border-radius: 0.375rem; width: 100%; }
        .stButton > button:hover { background-color: #06b6d4; }
        
        .article-card {
            background-color: #1f2937; border: 1px solid #374151; padding: 1.5rem;
            border-radius: 0.75rem; margin-bottom: 1rem; transition: all 0.2s ease-in-out;
        }
        .article-card:hover { background-color: #374151; border-color: #0891b2; }
        .article-card a { text-decoration: none; color: #f9fafb; }
        .article-card h4 { font-weight: 600; margin-bottom: 0.5rem; color: #38bdf8; }
        .article-card .date-info { font-size: 0.8rem; color: #9ca3af; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }
        .article-card p { color: #d1d5db; font-size: 0.95rem; line-height: 1.5; }

        /* Стилове за TICKER (Лентата с данни) */
        .ticker-box {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
            border-radius: 8px;
            padding: 10px 14px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 20px;
            transition: transform 0.2s ease;
        }
        .ticker-box:hover { transform: translateY(-2px); border-color: rgba(56,189,248,0.3); }
        
        .ticker-row-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
        .ticker-symbol { font-family: sans-serif; font-size: 0.7rem; font-weight: 800; color: #94a3b8; letter-spacing: 0.1em; }
        .ticker-price { font-family: monospace; font-size: 1.0rem; font-weight: 700; color: #f8fafc; }
        .ticker-pill { font-family: monospace; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; }
        
        .pill-up { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
        .pill-down { background: rgba(244, 63, 94, 0.15); color: #fb7185; }
        .pill-neutral { background: rgba(148, 163, 184, 0.15); color: #94a3b8; }
        
        footer { visibility: hidden; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- Gemini API Configuration ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    # За демо цели, ако няма ключ, показваме предупреждение, но зареждаме UI
    pass

# --- Schema ---
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
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools='google_search_retrieval'
        )
        prompt = f"""
        Get real-time stock data and news for {ticker}.
        Return a JSON object with:
        - price, changeAmount, changePercent
        - movementReason (one sentence explanation of why it moved today)
        - sentiment (Bullish/Bearish based on news)
        - news (list of top 5 relevant articles with title, snippet, publishDate, url, category)
        """
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

# --- UI RENDERING ---

# 1. LIVE MARKET TICKER (НАЙ-ГОРЕ)
market_data = get_live_market_data()
if market_data:
    cols = st.columns(len(market_data))
    for i, m in enumerate(market_data):
        pill_class = "pill-up" if m['dir'] == "up" else ("pill-down" if m['dir'] == "down" else "pill-neutral")
        arrow = "▲" if m['dir'] == "up" else ("▼" if m['dir'] == "down" else "●")
        
        with cols[i]:
            st.markdown(f"""
                <div class="ticker-box">
                    <div class="ticker-row-top">
                        <span class="ticker-symbol">{m['sym']}</span>
                        <span class="ticker-pill {pill_class}">{arrow} {m['chg']}</span>
                    </div>
                    <div class="ticker-price">{m['price']}</div>
                </div>
            """, unsafe_allow_html=True)

st.write("---")

# 2. MAIN HEADER
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<h1 style="margin-bottom: 0;">Stock Intelligence</h1>', unsafe_allow_html=True)
    st.caption("Powered by Aivan Capital AI Node")
with col_h2:
    st.markdown('<div style="text-align: right; font-family: monospace; color: #0891b2; font-weight: bold; margin-top: 20px;">LIVE FEED</div>', unsafe_allow_html=True)

# 3. SEARCH FORM
with st.form(key="ticker_form"):
    c1, c2 = st.columns([4, 1])
    with c1:
        ticker_input = st.text_input("Enter Ticker", placeholder="e.g. NVDA, TSLA, PLTR", label_visibility="collapsed")
    with c2:
        submit_button = st.form_submit_button("ANALYZE")

# 4. RESULTS
if submit_button and ticker_input:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ Please configure GOOGLE_API_KEY in secrets.")
    else:
        with st.spinner(f"⚡ Scanning markets for {ticker_input.upper()}..."):
            data = fetch_stock_news(ticker_input)
            
            if "error" in data:
                st.error(f"Failed to fetch data: {data['error']}")
            else:
                # Quote Section
                st.write("")
                quote_col1, quote_col2, quote_col3 = st.columns([1, 2, 1])
                
                with quote_col1:
                    change_color = "off"
                    if data.get('changeAmount', 0) > 0: change_color = "normal" 
                    elif data.get('changeAmount', 0) < 0: change_color = "inverse"
                    
                    st.metric(
                        label=f"{ticker_input.upper()} Price",
                        value=f"${data.get('price', 0):.2f}",
                        delta=f"{data.get('changeAmount', 0):+.2f} ({data.get('changePercent', 0):+.2%})"
                    )
                
                with quote_col2:
                    st.markdown(f"**Market Context:**")
                    st.info(data.get('movementReason', 'No context available.'))

                with quote_col3:
                    sent = data.get('sentiment', 'Neutral')
                    sent_color = "#22c55e" if sent == "Positive" else ("#ef4444" if sent == "Negative" else "#9ca3af")
                    st.markdown(f"<div style='text-align:center; border:1px solid {sent_color}; padding:10px; border-radius:8px; color:{sent_color}; font-weight:bold;'>{sent.upper()} SENTIMENT</div>", unsafe_allow_html=True)

                st.write("---")
                
                # News Feed
                news_items = data.get('news', [])
                if not news_items:
                    st.warning("No recent news articles found.")
                
                for cat in ['Today', 'This Week', 'Older']:
                    articles = [a for a in news_items if a.get('category') == cat]
                    if articles:
                        st.subheader(f"📅 {cat}")
                        for a in articles:
                            st.markdown(f"""
                            <a href="{a.get('url', '#')}" target="_blank">
                                <div class="article-card">
                                    <h4>{a.get('title', 'No Title')}</h4>
                                    <div class="date-info">{a.get('publishDate', '')}</div>
                                    <p>{a.get('snippet', '')}</p>
                                </div>
                            </a>
                            """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("<div style='text-align: center; color: #6b7280; margin-top: 4rem; border-top: 1px solid #1f2937; padding-top: 20px;'><small>AIVAN CAPITAL | SYSTEM VERSION 2.0</small></div>", unsafe_allow_html=True)
