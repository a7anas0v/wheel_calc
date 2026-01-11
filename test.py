import streamlit as st
from datetime import datetime
import yfinance as yf
import pandas as pd

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(
    page_title="Aivan Capital | Strategy Terminal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM CSS (Обединен дизайн) ---
st.markdown("""
    <style>
    /* Импорт на шрифт Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Основен фон */
    .stApp {
        background-color: #020617; /* Тъмно синьо-черно (Slate 950) */
        color: #f8fafc;
    }

    /* --- ЛОГО И ЗАГЛАВИЕ (от weekly.py) --- */
    .gradient-text {
        background: linear-gradient(45deg, #38bdf8, #818cf8, #c084fc); /* Sky to Violet */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    
    .brand-sub {
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.4em;
        text-transform: uppercase;
        margin-top: -15px;
        margin-bottom: 30px;
    }

    /* --- ЛЕНТА С ДАННИ (от test.py) --- */
    .ticker-box {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
        border-radius: 12px;
        padding: 12px 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid rgba(255,255,255,0.08);
        transition: transform 0.2s ease, border-color 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .ticker-box:hover {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.4);
    }
    
    .ticker-row-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
    .ticker-symbol { font-size: 0.75rem; font-weight: 800; color: #94a3b8; letter-spacing: 0.1em; }
    .ticker-price { font-family: 'Inter', monospace; font-size: 1.1rem; font-weight: 700; color: #f8fafc; }
    .ticker-pill { font-family: monospace; font-size: 0.7rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; }
    
    .pill-up { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.2); }
    .pill-down { background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid rgba(251, 113, 133, 0.2); }
    .pill-neutral { background: rgba(148, 163, 184, 0.2); color: #94a3b8; }

    /* --- СТИЛОВЕ ЗА КАЛКУЛАТОРА --- */
    div[data-testid="stMetric"] {
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
    }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ФУНКЦИЯ ЗА ЖИВИ ДАННИ (от test.py) ---
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
        # Изтегляме само последните 2 дни за бързина
        data = yf.download(list(tickers.values()), period="2d", progress=False)['Close']
        
        for name, symbol in tickers.items():
            try:
                # Гъвкава обработка на данните (DataFrame vs Series)
                if isinstance(data, pd.DataFrame) and symbol in data.columns:
                    series = data[symbol]
                else:
                    series = data 
                
                # Почистване на NaN
                series = series.dropna()

                if len(series) >= 1:
                    price = series.iloc[-1]
                    change_pct = 0.0
                    
                    if len(series) >= 2:
                        prev_close = series.iloc[-2]
                        if prev_close != 0:
                            change_pct = ((price - prev_close) / prev_close) * 100
                    
                    # Посока за цвета
                    direction = "up" if change_pct >= 0 else "down"
                    if abs(change_pct) < 0.01: direction = "neutral"
                    
                    # Форматиране
                    if name == 'VIX (FEAR)': 
                        price_fmt = f"{price:.2f}"
                    else: 
                        price_fmt = f"${price:,.2f}"
                        
                    live_data.append({
                        "sym": name, 
                        "price": price_fmt, 
                        "chg": f"{change_pct:+.2f}%", 
                        "dir": direction
                    })
                else:
                    live_data.append({"sym": name, "price": "N/A", "chg": "0.00%", "dir": "neutral"})
            except Exception:
                 live_data.append({"sym": name, "price": "-", "chg": "-", "dir": "neutral"})
    except Exception:
        pass
    return live_data

# --- 4. HEADER (ЗАГЛАВИЕ & ДАТА) ---
# Динамична дата
today_str = datetime.now().strftime("%b %d, %Y").upper()

col_brand, col_powered = st.columns([4, 1])
with col_brand:
    st.markdown(f"""
        <h1 style="font-size: 3.5rem; margin-bottom: -5px; font-style: italic; line-height: 1.2;">
            AIVAN <span class="gradient-text">CAPITAL</span>
        </h1>
        <p class="brand-sub">GLOBAL MACRO STRATEGY TERMINAL | {today_str}</p>
    """, unsafe_allow_html=True)

with col_powered:
    st.write("")
    st.write("")
    st.markdown('<div style="text-align: right; border: 1px solid #38bdf8; border-radius: 20px; padding: 5px 15px; color: #38bdf8; font-size: 10px; font-weight: 900; letter-spacing: 1px; display: inline-block; float: right;">POWERED BY AIVAN SOLUTIONS</div>', unsafe_allow_html=True)

# --- 5. ЛЕНТА С ДАННИ (TICKER TAPE) ---
market_data = get_live_market_data()

if market_data:
    cols = st.columns(len(market_data))
    for i, m in enumerate(market_data):
        # Определяме класа за цвета
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
else:
    st.info("Market data is initializing...")

st.write("---")

# ==========================================
# 6. WHEEL CALCULATOR LOGIC (Основно приложение)
# ==========================================

# Управление на езика
if 'language' not in st.session_state:
    st.session_state.language = 'BG'
if 'fetched_price' not in st.session_state:
    st.session_state.fetched_price = None

# Текстове
texts = {
    'BG': {
        'choose_strat': "📂 Изберете Модул:",
        'tab_put': "🟢 1. Продажба на PUT (Вход)",
        'tab_call': "🔴 2. Продажба на CALL (Изход)",
        'tab_roll': "🔄 3. Ролване (Сценарии)",
        'tab_data': "🔎 4. Верига Опции (Data)",
        # ... (Останалите текстове са същите, съкратени за прегледност)
        'current_price': "Текуща цена на акцията ($)",
        'strike': "Страйк Цена ($)",
        'premium': "Премия на акция ($)",
        'date_expiry': "Дата на падеж",
        'contracts': "Брой контракти",
        'days_left': "Дни до падежа:",
        'days_count': "дни",
        'warning_today': "⚠️ Изберете бъдеща дата!",
        'put_header': "Анализ на Cash Secured Put",
        'collateral': "Капитал в риск (Collateral)",
        'breakeven': "Цена на нулата (Break-Even)",
        'return_annual': "Годишна Доходност (Ann. ROI)",
        'return_flat': "Доходност (Flat)",
        'call_header': "Анализ на Covered Call",
        'cost_basis': "Средна цена (Cost Basis)",
        'total_profit': "Потенциална Печалба",
        'roll_header': "Калкулатор за Ролване",
        'md_header': "Верига Опции & Данни",
        'md_input_lbl': "Въведете Тикер:",
        'md_btn_copy': "Използвай тази цена",
    },
    'EN': {
        'choose_strat': "📂 Select Module:",
        'tab_put': "🟢 1. Sell PUT (Entry)",
        'tab_call': "🔴 2. Sell CALL (Exit)",
        'tab_roll': "🔄 3. Rolling Logic",
        'tab_data': "🔎 4. Option Chain (Data)",
        'current_price': "Current Stock Price ($)",
        'strike': "Strike Price ($)",
        'premium': "Premium per Share ($)",
        'date_expiry': "Expiration Date",
        'contracts': "Number of Contracts",
        'days_left': "Days to Expiry:",
        'days_count': "days",
        'warning_today': "⚠️ Select a future date!",
        'put_header': "Cash Secured Put Analysis",
        'collateral': "Capital at Risk",
        'breakeven': "Break-Even Price",
        'return_annual': "Annualized ROI",
        'return_flat': "Return (Flat)",
        'call_header': "Covered Call Analysis",
        'cost_basis': "Cost Basis ($)",
        'total_profit': "Potential Profit",
        'roll_header': "Rolling Calculator",
        'md_header': "Option Chain & Data",
        'md_input_lbl': "Enter Ticker:",
        'md_btn_copy': "Use this price",
    }
}

# Език селектор (скрит вдясно или горе)
col_lang_spacer, col_lang = st.columns([6, 1])
with col_lang:
    lang_sel = st.selectbox("Language", ["BG", "EN"], index=0 if st.session_state.language=='BG' else 1, label_visibility="collapsed")
    if lang_sel != st.session_state.language:
        st.session_state.language = lang_sel
        st.rerun()

t = texts[st.session_state.language]

# ГЛАВНО МЕНЮ (Радио бутони хоризонтално)
selected_section = st.radio(
    t['choose_strat'],
    [t['tab_put'], t['tab_call'], t['tab_roll'], t['tab_data']],
    index=0,
    horizontal=True
)
st.write("---")

# Helper variable
val_price = st.session_state.fetched_price
today = datetime.now().date()

# === SECTION 1: PUT ===
if selected_section == t['tab_put']:
    st.subheader(t['put_header'])
    c1, c2 = st.columns(2)
    with c1:
        def_val = val_price if val_price else None
        cp = st.number_input(t['current_price'], value=def_val, step=0.10)
        strike = st.number_input(t['strike'], step=0.50)
    with c2:
        prem = st.number_input(t['premium'], step=0.01)
        contracts = st.number_input(t['contracts'], min_value=1, value=1)
        
    exp_date = st.date_input(t['date_expiry'], min_value=today, value=today)
    days = (exp_date - today).days
    
    if days > 0 and strike > 0:
        collateral = strike * 100 * contracts
        breakeven = strike - prem
        flat_ret = (prem / strike) * 100
        ann_ret = (flat_ret / days) * 365
        
        st.success(f"📊 **{t['return_annual']}: {ann_ret:.2f}%**")
        m1, m2, m3 = st.columns(3)
        m1.metric(t['return_flat'], f"{flat_ret:.2f}%")
        m2.metric(t['breakeven'], f"${breakeven:.2f}")
        m3.metric(t['collateral'], f"${collateral:,.0f}")

# === SECTION 2: CALL ===
elif selected_section == t['tab_call']:
    st.subheader(t['call_header'])
    c1, c2 = st.columns(2)
    with c1:
        cost = st.number_input(t['cost_basis'], step=0.10)
        strike = st.number_input(t['strike'], step=0.50)
    with c2:
        prem = st.number_input(t['premium'], step=0.01)
        contracts = st.number_input(t['contracts'], min_value=1, value=1)
        
    exp_date = st.date_input(t['date_expiry'], min_value=today, value=today)
    days = (exp_date - today).days
    
    if days > 0 and cost > 0:
        cap_gain = strike - cost
        total_profit = (prem + cap_gain) * 100 * contracts
        ret_pct = ((prem + cap_gain) / cost) * 100
        ann_ret = (ret_pct / days) * 365
        
        st.success(f"🚀 **{t['total_profit']}: ${total_profit:.2f}**")
        m1, m2 = st.columns(2)
        m1.metric("Total Return %", f"{ret_pct:.2f}%")
        m2.metric("Ann. Return %", f"{ann_ret:.2f}%")

# === SECTION 3: ROLL ===
elif selected_section == t['tab_roll']:
    st.subheader(t['roll_header'])
    col_l, col_r = st.columns(2)
    with col_l:
        curr_prem = st.number_input("Current Premium to Close ($)", step=0.01)
        new_prem = st.number_input("New Premium to Open ($)", step=0.01)
    with col_r:
        net_credit = new_prem - curr_prem
        st.metric("Net Credit", f"${net_credit:.2f}")
        if net_credit > 0:
            st.success("✅ Good Roll (Credit)")
        else:
            st.warning("⚠️ Debit Roll (Paying)")

# === SECTION 4: DATA ===
elif selected_section == t['tab_data']:
    st.subheader(t['md_header'])
    
    ticker = st.text_input(t['md_input_lbl'], value="").upper()
    if ticker:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get('regularMarketPrice', info.get('currentPrice', None))
            
            if price:
                st.metric(f"{ticker} Price", f"${price:.2f}")
                if st.button(t['md_btn_copy']):
                    st.session_state.fetched_price = price
                    st.success("Price copied!")
                
                # Option chain simple view
                exps = stock.options
                if exps:
                    exp = st.selectbox("Expiry", exps)
                    opt = stock.option_chain(exp)
                    st.write("Calls:")
                    st.dataframe(opt.calls[['strike', 'lastPrice', 'bid', 'ask', 'volume']].head(10), hide_index=True)
            else:
                st.error("Ticker not found.")
        except:
            st.error("Error fetching data.")

# --- FOOTER ---
st.write("")
st.write("")
st.markdown(
    """
    <div style='text-align: center; color: #475569; padding-top: 20px; border-top: 1px solid #1e293b;'>
        <small>© 2026 AIVAN CAPITAL | STRATEGIC INTELLIGENCE</small>
    </div>
    """, 
    unsafe_allow_html=True
)
