import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import yfinance as yf  # Библиотека за пазарни данни
from datetime import datetime

# --- КОНФИГУРАЦИЯ НА СТРАНИЦАТА ---
st.set_page_config(
    page_title="Aivan Capital | Wheel Strategy Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ДИНАМИЧНА ДАТА ---
current_date = datetime.now().strftime("%b %d, %Y")

# --- ДИЗАЙНЕРСКИ СТИЛОВЕ (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #020617; /* Deep Slate Background */
        color: #f8fafc;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
        box-shadow: 0 8px 32px rgba(56, 189, 248, 0.1);
    }

    /* Top Ticker Style - PRO VERSION */
    .ticker-box {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
        border-radius: 12px;
        padding: 12px 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 10px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .ticker-box:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.2);
    }
    
    .ticker-row-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }
    
    .ticker-symbol { 
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem; 
        font-weight: 800; 
        color: #64748b; 
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    
    .ticker-price { 
        font-family: 'JetBrains Mono', monospace; /* Tech Font */
        font-size: 1.1rem; 
        font-weight: 700; 
        color: #f8fafc; 
        letter-spacing: -0.02em;
    }
    
    .ticker-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem; 
        font-weight: 700; 
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    .pill-up { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
    .pill-down { background: rgba(244, 63, 94, 0.15); color: #fb7185; }

    /* KPI Styles */
    .kpi-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    .kpi-sub {
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.25rem;
    }

    .gradient-text {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -0.02em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(' <h1 style="font-size: 3.5rem; margin-bottom: -10px; font-style: italic;">AIVAN <span class="gradient-text">CAPITAL</span></h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.4em; text-transform: uppercase;">Wheel Strategy Pro Terminal | {current_date}</p>', unsafe_allow_html=True)

with header_col2:
    st.write("")
    st.markdown('<div style="text-align: right;"><span style="color: #38bdf8; font-size: 10px; font-weight: 900; letter-spacing: 0.1em; border: 1px solid rgba(56,189,248,0.3); background: rgba(56,189,248,0.1); padding: 6px 12px; border-radius: 50px;">POWERED BY AIVAN SOLUTIONS</span></div>', unsafe_allow_html=True)

st.write("---")

# --- TOP MARKET TICKER (PRO VERSION) ---
# Сега с 6 колони, за да включим VIX
m1, m2, m3, m4, m5, m6 = st.columns(6)

market_data = [
    {"sym": "S&P 500", "price": "5,942.15", "chg": "+0.45%", "dir": "up"},
    {"sym": "NASDAQ 100", "price": "19,855.20", "chg": "+0.82%", "dir": "up"},
    {"sym": "VIX (FEAR)", "price": "13.85", "chg": "-4.20%", "dir": "down"},  # VIX ADDED
    {"sym": "GOLD (XAU)", "price": "$3,145.50", "chg": "+1.15%", "dir": "up"},
    {"sym": "CRUDE OIL", "price": "$74.20", "chg": "-0.65%", "dir": "down"},
    {"sym": "NAT GAS", "price": "$2.12", "chg": "-5.10%", "dir": "down"}
]

cols_market = [m1, m2, m3, m4, m5, m6]

for i, m in enumerate(market_data):
    pill_class = "pill-up" if m['dir'] == "up" else "pill-down"
    arrow = "▲" if m['dir'] == "up" else "▼"
    
    with cols_market[i]:
        st.markdown(f"""
            <div class="ticker-box">
                <div class="ticker-row-top">
                    <span class="ticker-symbol">{m['sym']}</span>
                    <span class="ticker-pill {pill_class}">{arrow} {m['chg']}</span>
                </div>
                <div class="ticker-price">{m['price']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- KPI TICKER SECTION (Wheel Strategy Stats) ---
st.write("")
t1, t2, t3, t4, t5, t6 = st.columns(6)

ticker_items = [
    {"label": "Active Puts", "val": "$4,250", "sub": "Premium Collected", "color": "#34d399"},
    {"label": "Assigned Stock", "val": "$12,400", "sub": "Cost Basis", "color": "#fbbf24"},
    {"label": "Net Delta", "val": "+125", "sub": "Long Bias", "color": "#38bdf8"}, 
    {"label": "Monthly Yield", "val": "+2.4%", "sub": "On Capital", "color": "#34d399"},
    {"label": "Beta Weight", "val": "1.15", "sub": "SPY Correlation", "color": "#94a3b8"},
    {"label": "Buying Power", "val": "$8,500", "sub": "Available", "color": "#38bdf8"}
]

cols = [t1, t2, t3, t4, t5, t6]
for i, item in enumerate(ticker_items):
    with cols[i]:
        st.markdown(f"""
            <div class="glass-card" style="padding: 1rem; min-height: 140px;">
                <div class="kpi-label">{item['label']}</div>
                <div class="kpi-value">{item['val']}</div>
                <div class="kpi-sub" style="color: {item['color']};">{item['sub']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- MAIN ANALYSIS LAYOUT ---
col_left, col_right = st.columns([2.2, 1])

with col_left:
    # 1. Performance Chart
    st.markdown('### <span style="color: #38bdf8;">■</span> Wheel Strategy Performance (YTD)', unsafe_allow_html=True)
    
    perf_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Profit': [450, 520, 380, 600, 550, 700, 400, 350, 800, 650, 500, 920] 
    })
    
    fig_perf = px.area(perf_data, x='Month', y='Profit', line_shape='spline', color_discrete_sequence=['#38bdf8'])
    fig_perf.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8', height=320, margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title=None, yaxis_title="Net Premium ($)",
        showlegend=False
    )
    st.plotly_chart(fig_perf, use_container_width=True)
    
    st.markdown("""
        <div style="background: rgba(56, 189, 248, 0.05); border-left: 4px solid #38bdf8; padding: 1.5rem; border-radius: 0 1rem 1rem 0; margin-top: 10px;">
            <p style="font-size: 13px; color: #cbd5e1; line-height: 1.6; font-family: 'Inter', sans-serif;">
                <b>Strategy Commentary:</b> Put selling on Vistra ($VST) and Nvidia ($NVDA) generated 60% of monthly alpha. 
                Current market conditions (Low VIX) favor Covered Calls over aggressive Put selling. 
                <i>Watchlist: Look for IV expansion in Uranium sector.</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # 3. Active Positions (Watchlist)
    st.markdown('<p class="kpi-label">Active Wheel Targets</p>', unsafe_allow_html=True)
    positions = [
        {"name": "Vistra (VST)", "price": "$166.00", "action": "HOLD CC", "color": "#34d399"},
        {"name": "Nvidia (NVDA)", "price": "$145.20", "action": "SELL PUT", "color": "#fbbf24"},
        {"name": "Cameco (CCJ)", "price": "$54.10", "action": "ASSIGNED", "color": "#fb7185"},
        {"name": "EQT Corp", "price": "$54.50", "action": "BUY DIP", "color": "#38bdf8"},
        {"name": "Uranium (URA)", "price": "$32.15", "action": "HEDGED", "color": "#94a3b8"}
    ]
    
    for p in positions:
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 12px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.05); transition: background 0.2s;">
                <span style="font-size: 12px; font-weight: 700; color: #f8fafc; font-family: 'Inter', sans-serif;">{p['name']}</span>
                <div style="text-align: right;">
                    <div style="font-size: 12px; font-weight: 700; color: #f8fafc; font-family: 'JetBrains Mono', monospace;">{p['price']}</div>
                    <div style="font-size: 10px; font-weight: 700; color: {p['color']}; letter-spacing: 0.05em;">{p['action']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 4. Income Split Pie
    st.write("")
    st.markdown('<p class="kpi-label">Income Source Breakdown</p>', unsafe_allow_html=True)
    income_df = pd.DataFrame({'Source': ['Puts', 'Calls', 'Dividends', 'Cap Gains'], 'Value': [45, 30, 10, 15]})
    fig_inc = px.pie(income_df, values='Value', names='Source', hole=0.6, color_discrete_sequence=['#38bdf8', '#818cf8', '#c084fc', '#475569'])
    fig_inc.update_layout(
        showlegend=False, 
        height=200, 
        margin=dict(l=0, r=0, t=0, b=0), 
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1')
    )
    st.plotly_chart(fig_inc, use_container_width=True)

# --- SECTION 5: LIVE MARKET DATA INSPECTOR (INTEGRATED) ---
st.write("---")
st.markdown('### <span style="color: #c084fc;">📡</span> LIVE MARKET DATA INSPECTOR', unsafe_allow_html=True)
st.markdown('<p style="font-size: 11px; color: #64748b;">Real-time data fetched via Yahoo Finance API. Analyze option chains instantly.</p>', unsafe_allow_html=True)

col_md1, col_md2 = st.columns([1, 2])

with col_md1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    ticker_symbol = st.text_input("ENTER TICKER SYMBOL", value="", placeholder="e.g. NVDA, VST, U-UN.TO").upper()
    
    current_price = None
    if ticker_symbol:
        try:
            stock = yf.Ticker(ticker_symbol)
            # Fetch generic info fast
            info = stock.info
            current_price = info.get('regularMarketPrice', info.get('currentPrice', info.get('previousClose', None)))
            
            if current_price:
                st.metric("CURRENT PRICE", f"${current_price:,.2f}")
            else:
                st.warning("Price unavailable.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_md2:
    if ticker_symbol and current_price:
        try:
            stock = yf.Ticker(ticker_symbol)
            expirations = stock.options
            
            if expirations:
                c1, c2 = st.columns(2)
                with c1:
                    sel_exp = st.selectbox("EXPIRATION DATE", expirations)
                with c2:
                    opt_type = st.radio("OPTION TYPE", ["Put", "Call"], horizontal=True)
                
                if sel_exp:
                    opt_chain = stock.option_chain(sel_exp)
                    data = opt_chain.puts if opt_type == "Put" else opt_chain.calls
                    
                    # Clean DataFrame for display
                    df_show = data[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']]
                    df_show.columns = ['Strike', 'Last', 'Bid', 'Ask', 'Vol', 'OI', 'IV']
                    
                    st.dataframe(
                        df_show.style.format({'Last': '{:.2f}', 'Bid': '{:.2f}', 'Ask': '{:.2f}', 'IV': '{:.2%}'}), 
                        use_container_width=True, 
                        height=300
                    )
            else:
                st.info("No options data available for this ticker.")
        except Exception as e:
            st.error(f"Could not load option chain: {e}")
    else:
        st.info("Enter a valid ticker symbol to load Option Chain.")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05);">
        <p style="color: #334155; font-size: 10px; font-weight: 900; letter-spacing: 0.3em; text-transform: uppercase;">
            © 2026 AIVAN CAPITAL | WHEEL STRATEGY PRO | POWERED BY AIVAN SOLUTIONS
        </p>
    </div>
""", unsafe_allow_html=True)
