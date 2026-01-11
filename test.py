import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #020617;
        color: #f8fafc;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 1.25rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    /* Top Ticker Style */
    .ticker-box {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        padding: 8px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 10px;
    }
    
    .ticker-symbol { font-size: 0.8rem; font-weight: 700; color: #94a3b8; }
    .ticker-price { font-size: 0.9rem; font-weight: 900; color: #f8fafc; }
    .ticker-up { color: #34d399; font-size: 0.75rem; font-weight: 700; }
    .ticker-down { color: #fb7185; font-size: 0.75rem; font-weight: 700; }

    .kpi-label {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.15em;
        margin-bottom: 0.5rem;
    }

    .kpi-value {
        font-size: 1.75rem;
        font-weight: 900;
        color: #38bdf8;
    }

    .kpi-sub {
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 0.25rem;
    }

    .gradient-text {
        background: linear-gradient(45deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
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
    st.markdown('<p style="text-align: right; color: #38bdf8; font-size: 10px; font-weight: 900; letter-spacing: 0.1em; border: 1px solid #38bdf8; padding: 5px 10px; border-radius: 50px;">POWERED BY AIVAN SOLUTIONS</p>', unsafe_allow_html=True)

st.write("---")

# --- TOP MARKET TICKER (NOVA FUNKCIONALNOST) ---
# Данните са примерни за визията. В реално приложение ще се връзват с API.
m1, m2, m3, m4, m5 = st.columns(5)

market_data = [
    {"sym": "S&P 500", "price": "5,940.12", "chg": "+0.45%", "dir": "up"},
    {"sym": "NASDAQ 100", "price": "19,850.50", "chg": "+0.82%", "dir": "up"},
    {"sym": "GOLD (XAU)", "price": "$3,142.00", "chg": "+1.20%", "dir": "up"},
    {"sym": "CRUDE OIL", "price": "$74.50", "chg": "-0.30%", "dir": "down"},
    {"sym": "NAT GAS", "price": "$2.14", "chg": "-4.50%", "dir": "down"}
]

cols_market = [m1, m2, m3, m4, m5]

for i, m in enumerate(market_data):
    color_class = "ticker-up" if m['dir'] == "up" else "ticker-down"
    arrow = "▲" if m['dir'] == "up" else "▼"
    
    with cols_market[i]:
        st.markdown(f"""
            <div class="ticker-box">
                <div>
                    <div class="ticker-symbol">{m['sym']}</div>
                    <div class="ticker-price">{m['price']}</div>
                </div>
                <div class="{color_class}">{arrow} {m['chg']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- KPI TICKER SECTION (Wheel Strategy Stats) ---
st.write("")
t1, t2, t3, t4, t5, t6 = st.columns(6)

ticker_items = [
    {"label": "Active Puts", "val": "$4,250", "sub": "Premium Collected", "color": "#34d399"},
    {"label": "Assigned Stock", "val": "$12,400", "sub": "Cost Basis", "color": "#fbbf24"},
    {"label": "VIX Index", "val": "14.2", "sub": "▼ Low Volatility", "color": "#fb7185"}, 
    {"label": "Monthly Yield", "val": "+2.4%", "sub": "On Capital", "color": "#34d399"},
    {"label": "Beta Weight", "val": "1.15", "sub": "SPY Correlation", "color": "#94a3b8"},
    {"label": "Buying Power", "val": "$8,500", "sub": "Available", "color": "#38bdf8"}
]

cols = [t1, t2, t3, t4, t5, t6]
for i, item in enumerate(ticker_items):
    with cols[i]:
        st.markdown(f"""
            <div class="glass-card" style="padding: 1rem;">
                <div class="kpi-label">{item['label']}</div>
                <div class="kpi-value" style="font-size: 1.4rem;">{item['val']}</div>
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
            <p style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
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
            <div style="display: flex; justify-content: space-between; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 12px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.05);">
                <span style="font-size: 11px; font-weight: 700; color: #f8fafc;">{p['name']}</span>
                <div style="text-align: right;">
                    <div style="font-size: 11px; font-weight: 900; color: #f8fafc;">{p['price']}</div>
                    <div style="font-size: 9px; font-weight: 700; color: {p['color']};">{p['action']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 4. Income Split Pie
    st.write("")
    st.markdown('<p class="kpi-label">Income Source Breakdown</p>', unsafe_allow_html=True)
    income_df = pd.DataFrame({'Source': ['Puts', 'Calls', 'Dividends', 'Cap Gains'], 'Value': [45, 30, 10, 15]})
    fig_inc = px.pie(income_df, values='Value', names='Source', hole=0.6, color_discrete_sequence=['#38bdf8', '#818cf8', '#c084fc', '#475569'])
    fig_inc.update_layout(showlegend=False, height=200, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_inc, use_container_width=True)

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05);">
        <p style="color: #334155; font-size: 10px; font-weight: 900; letter-spacing: 0.3em; text-transform: uppercase;">
            © 2026 AIVAN CAPITAL | WHEEL STRATEGY PRO | POWERED BY AIVAN SOLUTIONS
        </p>
    </div>
""", unsafe_allow_html=True)
