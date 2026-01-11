import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

# --- КОНФИГУРАЦИЯ НА СТРАНИЦАТА ---
st.set_page_config(
    page_title="Aivan Capital | Macro Intelligence Terminal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-track {
        background: #020617;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(' <h1 style="font-size: 3.5rem; margin-bottom: -10px; font-style: italic;">AIVAN <span class="gradient-text">CAPITAL</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.4em; text-transform: uppercase;">Global Macro Strategy Terminal | Jan 11, 2026</p>', unsafe_allow_html=True)

with header_col2:
    st.write("")
    st.markdown('<p style="text-align: right; color: #38bdf8; font-size: 10px; font-weight: 900; letter-spacing: 0.1em; border: 1px solid #38bdf8; padding: 5px 10px; border-radius: 50px;">POWERED BY AIVAN SOLUTIONS</p>', unsafe_allow_html=True)

# --- KPI TICKER SECTION ---
st.write("")
t1, t2, t3, t4, t5, t6 = st.columns(6)

ticker_items = [
    {"label": "Unemployment (U3)", "val": "4.4%", "sub": "▲ Rising", "color": "#fb7185"},
    {"label": "Fed Balance", "val": "$8.24T", "sub": "▲ Expanding", "color": "#34d399"},
    {"label": "Gold (ATH)", "val": "$3,142", "sub": "▲ Safe Haven", "color": "#fbbf24"},
    {"label": "GDP Growth", "val": "+1.8%", "sub": "● Fragile", "color": "#94a3b8"},
    {"label": "Copper (Cu)", "val": "$5.18", "sub": "▲ AI Cycle", "color": "#34d399"},
    {"label": "CPI Inflation", "val": "2.7%", "sub": "● Sticky", "color": "#fbbf24"}
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
    # 1. Weekly Fed Liquidity Injection (Requested Feature)
    st.markdown('### <span style="color: #38bdf8;">■</span> Weekly Fed Liquidity Injections (Last 12 Weeks)', unsafe_allow_html=True)
    
    liq_data = pd.DataFrame({
        'Week': ['W1-Oct', 'W2-Oct', 'W3-Oct', 'W4-Oct', 'W1-Nov', 'W2-Nov', 'W3-Nov', 'W4-Nov', 'W1-Dec', 'W2-Dec', 'W3-Dec', 'W4-Dec'],
        'Injection': [8.5, 9.2, 12.4, 11.8, 14.5, 13.2, 12.8, 15.4, 16.2, 14.8, 15.5, 12.1]
    })
    
    fig_liq = px.bar(liq_data, x='Week', y='Injection', color_discrete_sequence=['#38bdf8'])
    fig_liq.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8', height=320, margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title=None, yaxis_title="Billions USD ($)",
        showlegend=False
    )
    st.plotly_chart(fig_liq, use_container_width=True)
    
    st.markdown("""
        <div style="background: rgba(56, 189, 248, 0.05); border-left: 4px solid #38bdf8; padding: 1.5rem; border-radius: 0 1rem 1rem 0; margin-top: 10px;">
            <p style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
                <b>Macro Commentary (Stealth QE):</b> The Federal Reserve is aggressively utilizing T-Bill purchases to inject liquidity without moving the long end of the yield curve. Average weekly injections of <b>$13.4B</b> are supporting asset prices while domestic labor fundamentals weaken. 
                <i>Note: Inflationary transmission lag is estimated at 12-16 months.</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 2. Historical Labor Market (Old Data Recovered)
    st.write("")
    st.markdown('### <span style="color: #fb7185;">■</span> Labor Market & Unemployment Trends', unsafe_allow_html=True)
    
    labor_df = pd.DataFrame({
        'Month': ['Sep 25', 'Oct 25', 'Nov 25', 'Dec 25', 'Jan 26'],
        'U3': [4.2, 4.3, 4.5, 4.4, 4.4],
        'U6': [7.8, 7.9, 8.2, 8.1, 8.1],
        'NFP': [73, -105, -173, 56, 50]
    })
    
    fig_labor = go.Figure()
    fig_labor.add_trace(go.Scatter(x=labor_df['Month'], y=labor_df['U3'], name='U-3 Unemployment %', line=dict(color='#fb7185', width=4)))
    fig_labor.add_trace(go.Scatter(x=labor_df['Month'], y=labor_df['U6'], name='U-6 Broad %', line=dict(color='#f8fafc', width=2, dash='dot')))
    
    fig_labor.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8', height=300, margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_labor, use_container_width=True)

with col_right:
    # 3. Commodity Heatmap
    st.markdown('<p class="kpi-label">Commodity Market Ticker</p>', unsafe_allow_html=True)
    commodities = [
        {"name": "Gold (XAU)", "price": "$3,142.50", "chg": "▲ 1.2%", "color": "#fbbf24"},
        {"name": "Copper (HG)", "price": "$5.18", "chg": "▲ 0.8%", "color": "#fb923c"},
        {"name": "Silver (XAG)", "price": "$38.40", "chg": "▲ 2.1%", "color": "#cbd5e1"},
        {"name": "WTI Crude", "price": "$61.20", "chg": "▼ 2.4%", "color": "#fb7185"},
        {"name": "Nat Gas", "price": "$2.14", "chg": "▼ 4.5%", "color": "#fb7185"}
    ]
    
    for c in commodities:
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 12px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.05);">
                <span style="font-size: 11px; font-weight: 700; color: {c['color']};">{c['name']}</span>
                <div style="text-align: right;">
                    <div style="font-size: 11px; font-weight: 900; color: #f8fafc;">{c['price']}</div>
                    <div style="font-size: 9px; font-weight: 700; color: {c['color']};">{c['chg']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 4. Geopolitical Risk Radar
    st.write("")
    st.markdown('<p class="kpi-label">Geopolitical Risk Matrix</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card" style="padding: 1rem; border-left: 4px solid #f43f5e;">
            <p style="font-size: 12px; font-weight: 800; color: #f8fafc; margin-bottom: 4px;">Greenland: US vs EU</p>
            <p style="font-size: 10px; color: #64748b; line-height: 1.4;">Resource sovereignty clash over rare earths. High NATO friction potential.</p>
        </div>
        <div class="glass-card" style="padding: 1rem; border-left: 4px solid #fbbf24;">
            <p style="font-size: 12px; font-weight: 800; color: #f8fafc; margin-bottom: 4px;">Venezuela: US vs China</p>
            <p style="font-size: 10px; color: #64748b;">Oil concession struggle in Essequibo. China debt-diplomacy vs US licensing.</p>
        </div>
    """, unsafe_allow_html=True)

    # 5. GDP Composition (Restored)
    st.markdown('<p class="kpi-label">GDP Breakdown (Q4 2025)</p>', unsafe_allow_html=True)
    gdp_df = pd.DataFrame({'Component': ['Consumption', 'Gov Spend', 'Investment', 'Export'], 'Value': [68, 18, 15, -1]})
    fig_gdp = px.pie(gdp_df, values='Value', names='Component', hole=0.5, color_discrete_sequence=['#38bdf8', '#818cf8', '#c084fc', '#475569'])
    fig_gdp.update_layout(showlegend=False, height=200, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gdp, use_container_width=True)

# --- AI FACT CHECK INTERFACE ---
st.write("---")
col_f1, col_f2 = st.columns([1, 2])
with col_f1:
    st.markdown('### <span style="color: #c084fc;">✨</span> AI Intelligence Engine')
    st.markdown('<p style="font-size: 11px; color: #64748b;">Verify rumors or run complex macro simulations via Aivan Capital Neural Nodes.</p>', unsafe_allow_html=True)

with col_f2:
    query = st.text_input("Enter market rumor or data query...", placeholder="Is the Fed planning to increase the repo facility limit?")
    if st.button("EXECUTE FACT CHECK", use_container_width=True):
        st.info("Analysis requested. Connecting to Gemini-2.5-Flash...")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05);">
        <p style="color: #334155; font-size: 10px; font-weight: 900; letter-spacing: 0.3em; text-transform: uppercase;">
            © 2026 AIVAN CAPITAL | STRATEGIC INTELLIGENCE | POWERED BY AIVAN SOLUTIONS
        </p>
    </div>
""", unsafe_allow_html=True)
