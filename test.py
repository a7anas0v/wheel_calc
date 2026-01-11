import streamlit as st
from datetime import date, datetime
import yfinance as yf
import pandas as pd

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(
    page_title="Aivan Capital | The Wheel Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. УПРАВЛЕНИЕ НА ЕЗИКА ---
if 'language' not in st.session_state:
    st.session_state.language = 'BG'

# --- 3. ДИЗАЙН И CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Основен тъмен фон */
    .stApp {
        background-color: #020617;
        color: #f8fafc;
    }
    
    /* --- MOBILE KEYBOARD FIX --- */
    .main .block-container {
        padding-bottom: 350px !important;
    }

    /* ЛОГО И ЗАГЛАВИЕ */
    .gradient-text {
        background: linear-gradient(45deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .brand-sub {
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: -15px;
        margin-bottom: 30px;
    }

    /* --- БУТОНИ ЗА МЕНЮТО (Tabs) --- */
    .stRadio > div[role="radiogroup"] > label > div:first-child {
        display: none;
    }
    .stRadio > div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap; 
        gap: 10px;
        background-color: transparent;
        padding: 0;
        border: none;
        justify-content: flex-start;
    }
    .stRadio > div[role="radiogroup"] > label {
        flex: 1 1 auto;
        min-width: 130px;
        text-align: center;
        padding: 12px 15px;
        background-color: rgba(30, 41, 59, 0.6);
        border-radius: 10px;
        cursor: pointer;
        font-weight: 700;
        color: #94a3b8;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stRadio > div[role="radiogroup"] > label:hover {
        background-color: rgba(56, 189, 248, 0.1);
        color: #f8fafc;
        border-color: rgba(56, 189, 248, 0.3);
    }
    .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.8), rgba(192, 132, 252, 0.8));
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }

    /* СТИЛ ЗА GLOBAL TICKER INPUT */
    .ticker-input-container {
        background-color: rgba(30, 41, 59, 0.4);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* ЛЕНТА С ДАННИ */
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
        min-width: 140px;
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

    div[data-testid="stMetric"] {
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ФУНКЦИЯ ЗА ЖИВИ ДАННИ (TAPE) ---
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
                if isinstance(data, pd.DataFrame) and symbol in data.columns:
                    series = data[symbol].dropna()
                else:
                    series = data.dropna()
                
                if len(series) >= 1:
                    price = series.iloc[-1]
                    change_pct = 0.0
                    if len(series) >= 2:
                        prev_close = series.iloc[-2]
                        if prev_close != 0:
                            change_pct = ((price - prev_close) / prev_close) * 100
                    
                    direction = "up" if change_pct >= 0 else "down"
                    if abs(change_pct) < 0.01: direction = "neutral"
                    
                    if name == 'VIX (FEAR)': price_fmt = f"{price:.2f}"
                    else: price_fmt = f"${price:,.2f}"
                        
                    live_data.append({
                        "sym": name, "price": price_fmt, "chg": f"{change_pct:+.2f}%", "dir": direction
                    })
                else:
                    live_data.append({"sym": name, "price": "N/A", "chg": "0.00%", "dir": "neutral"})
            except:
                 live_data.append({"sym": name, "price": "-", "chg": "-", "dir": "neutral"})
    except:
        pass
    return live_data

# --- 5. HEADER ---
today_str = datetime.now().strftime("%b %d, %Y").upper()

col_brand, col_lang = st.columns([5, 1])
with col_brand:
    st.markdown(f"""
        <div>
            <h1 style="font-size: 3.5rem; margin-bottom: -5px; font-style: italic; line-height: 1.2;">
                AIVAN <span class="gradient-text">CAPITAL</span>
            </h1>
            <p class="brand-sub">THE WHEEL PRO STRATEGY TERMINAL | {today_str}</p>
        </div>
    """, unsafe_allow_html=True)

with col_lang:
    lang_sel = st.selectbox("Language", ["BG", "EN"], index=0 if st.session_state.language=='BG' else 1, label_visibility="collapsed", key="lang_select_top")
    if lang_sel != st.session_state.language:
        st.session_state.language = lang_sel
        st.rerun()

# --- 6. ЛЕНТА С ДАННИ ---
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
else:
    st.info("Initializing Data Feed...")

st.write("---")

# --- 7. РЕЧНИК С ТЕКСТОВЕ ---
texts = {
    'BG': {
        'choose_strat': "Модул:",
        'global_ticker_label': "⚡ Търси Акция (Въведи Тикер за Авто-Цена):",
        'tab_put': "PUT (Вход)",
        'tab_call': "CALL (Изход)",
        'tab_roll': "Ролване",
        'tab_data': "Пазарни Данни",
        'current_price': "Текуща цена на акцията ($)",
        'strike': "Страйк Цена ($)",
        'premium': "Премия на акция ($)",
        'date_expiry': "Дата на падеж",
        'contracts': "Брой контракти",
        'days_left': "Оставащи дни до падежа:",
        'days_count': "дни",
        'warning_today': "⚠️ Изберете бъдеща дата!",
        'put_header': "Анализ на Cash Secured Put",
        'collateral': "Капитал в риск (Collateral)",
        'breakeven': "Цена на нулата (Break-Even)",
        'buffer': "Буфер (Discount)",
        'return_flat': "Възвращаемост (Flat)",
        'return_annual': "Годишна (Annualized)",
        'safety_msg': "Колко може да падне акцията, преди да сте на загуба.",
        'danger_msg': "⚠️ Внимание: Текущата цена вече е под вашата Break-Even точка!",
        'call_header': "Анализ на Covered Call",
        'cost_basis': "Средна цена (Cost Basis) ($)",
        'cap_gains': "Капиталова Печалба ($)",
        'total_profit': "ОБЩА потенциална печалба",
        'total_return': "Общ ROI (Total Return)",
        'prem_return': "Доход от Премия",
        'roll_header': "Стратегически Анализ на Ролване",
        'roll_strategy': "Стратегия:",
        'strat_call': "Covered CALL (Ролване нагоре)",
        'strat_put': "Cash Secured PUT (Ролване надолу)",
        'orig_data': "📜 История на позицията",
        'orig_date': "Дата на отваряне (Start Date)",
        'orig_prem': "Първоначална премия ($)",
        'curr_exp': "Текущ падеж (Current Expiry)",
        'new_data': "✨ Параметри на Ролването",
        'old_strike': "Текущ Страйк ($)",
        'new_strike': "Нов Страйк ($)",
        'roll_type': "Тип транзакция:",
        'roll_cost_lbl': "Цена на ролването (Net Price)",
        'roll_credit': "Credit (Взимам)",
        'roll_debit': "Debit (Плащам)",
        'new_expiry': "Нов Падеж",
        'an_comparison': "📊 Сравнение на Сценариите",
        'scen_base': "1️⃣ БАЗОВ: Не правите нищо",
        'scen_fail': "2️⃣ ЛОШ КЪСМЕТ (Failed Roll)",
        'scen_win': "3️⃣ УСПЕХ (Max Profit)",
        'row_profit': "Нетна Печалба",
        'row_days': "Общо дни в сделката",
        'row_ann': "Годишна Доходност (APR)",
        'risk_insight': "💡 ИЗВОД И РИСК",
        'risk_text_1': "Рискувате доходността ви да падне от",
        'risk_text_2': "на",
        'risk_text_3': "за да гоните потенциал за",
        'verdict_great': "✅ ОТЛИЧНО: Малък риск за голяма награда.",
        'verdict_bad': "🛑 НЕ СИ СТРУВА: Рискувате твърде много доходност.",
        'md_header': "📡 Пазарни Данни & Верига Опции",
        'md_input_lbl': "Въведете Тикер (Yahoo Finance Symbol):",
        'md_note': "ℹ️ Бележка: Данните са с ~15 мин закъснение.",
        'md_note_ex': "Примери: 'TSLA', 'AAPL'. За канадски акции добавете '.TO'",
        'md_price': "Текуща Цена:",
        'md_btn_copy': "👉 Използвай тази цена в калкулатора",
        'md_chain_head': "⛓️ Верига Опции (Option Chain)",
        'md_exp': "Избери Падеж:",
        'md_type': "Тип Опция:",
        'md_no_data': "Няма намерени данни за опции или тикерът е грешен.",
        'md_error': "Грешка при търсене. Проверете символа."
    },
    'EN': {
        'choose_strat': "Module:",
        'global_ticker_label': "⚡ Search Ticker (Auto-Populate Price):",
        'tab_put': "PUT (Entry)",
        'tab_call': "CALL (Exit)",
        'tab_roll': "Rolling",
        'tab_data': "Market Data",
        'current_price': "Current Stock Price ($)",
        'strike': "Strike Price ($)",
        'premium': "Premium per Share ($)",
        'date_expiry': "Expiration Date",
        'contracts': "Number of Contracts",
        'days_left': "Days to Expiration:",
        'days_count': "days",
        'warning_today': "⚠️ Please select a future date!",
        'put_header': "Cash Secured Put Analysis",
        'collateral': "Capital at Risk (Collateral)",
        'breakeven': "Break-Even Price",
        'buffer': "Discount / Buffer",
        'return_flat': "Return (Flat)",
        'return_annual': "Annualized ROI",
        'safety_msg': "How much the stock can drop before you lose money.",
        'danger_msg': "⚠️ Warning: Current price is already below your Break-Even point!",
        'call_header': "Covered Call Analysis",
        'cost_basis': "Net Cost Basis ($)",
        'cap_gains': "Capital Gains ($)",
        'total_profit': "TOTAL Potential Profit",
        'total_return': "Total Return %",
        'prem_return': "Premium Return",
        'roll_header': "Rolling Strategy Analysis",
        'roll_strategy': "Strategy:",
        'strat_call': "Covered CALL (Rolling UP)",
        'strat_put': "Cash Secured PUT (Rolling DOWN)",
        'orig_data': "📜 Position History",
        'orig_date': "Original Open Date",
        'orig_prem': "Original Premium ($)",
        'curr_exp': "Current Expiry Date",
        'new_data': "✨ Roll Parameters",
        'old_strike': "Current Strike ($)",
        'new_strike': "New Strike ($)",
        'roll_type': "Transaction Type:",
        'roll_cost_lbl': "Net Roll Price",
        'roll_credit': "Credit (Receive)",
        'roll_debit': "Debit (Pay)",
        'new_expiry': "New Expiry Date",
        'an_comparison': "📊 Scenario Comparison",
        'scen_base': "1️⃣ BASE: Do Nothing",
        'scen_fail': "2️⃣ BAD LUCK (Failed Roll)",
        'scen_win': "3️⃣ SUCCESS (Max Profit)",
        'row_profit': "Net Profit",
        'row_days': "Total Days Held",
        'row_ann': "Annualized ROI (APR)",
        'risk_insight': "💡 RISK INSIGHT",
        'risk_text_1': "You risk dropping your yield from",
        'risk_text_2': "to",
        'risk_text_3': "to chase a potential",
        'verdict_great': "✅ GREAT TRADE: Low risk for high reward.",
        'verdict_bad': "🛑 BAD DEAL: Giving up too much yield.",
        'md_header': "📡 Market Data & Option Chain",
        'md_input_lbl': "Enter Ticker (Yahoo Finance Symbol):",
        'md_note': "ℹ️ Note: Data is delayed by ~15 mins.",
        'md_note_ex': "Examples: 'TSLA', 'AAPL'. For Canadian stocks try adding '.TO'",
        'md_price': "Current Price:",
        'md_btn_copy': "👉 Use this price in calculator",
        'md_chain_head': "⛓️ Option Chain",
        'md_exp': "Select Expiry:",
        'md_type': "Option Type:",
        'md_no_data': "No option data found or invalid ticker.",
        'md_error': "Error fetching data. Check symbol."
    }
}

t = texts[st.session_state.language]
today = date.today()

# --- ГЛАВНО МЕНЮ (РАДИО) ---
selected_section = st.radio(
    t['choose_strat'],
    [t['tab_put'], t['tab_call'], t['tab_roll'], t['tab_data']],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)

# --- 8. ГЛОБАЛЕН TICKER INPUT (НОВО) ---
# Инициализация на Session State за цената
if 'global_fetched_price' not in st.session_state:
    st.session_state.global_fetched_price = 0.0
if 'last_ticker' not in st.session_state:
    st.session_state.last_ticker = ""

# Визуална кутия за търсене
st.markdown('<div class="ticker-input-container">', unsafe_allow_html=True)
c_search, c_display = st.columns([1, 1])

with c_search:
    global_ticker = st.text_input(t['global_ticker_label'], key="master_ticker_input", placeholder="e.g. NVDA").upper()

with c_display:
    if global_ticker:
        # Проверяваме дали е нов тикер, за да изтеглим цената
        if global_ticker != st.session_state.last_ticker:
            try:
                with st.spinner("⏳"):
                    live_data = yf.Ticker(global_ticker).fast_info
                    current_price = live_data.last_price
                    st.session_state.global_fetched_price = current_price
                    st.session_state.last_ticker = global_ticker
            except:
                st.warning("Ticker not found")
        
        # Показваме цената, ако я имаме
        if st.session_state.global_fetched_price > 0:
            st.markdown(f"<h3 style='margin:0; color:#38bdf8;'>${st.session_state.global_fetched_price:,.2f}</h3>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# ==========================================
# SECTION 1: SELLING PUT
# ==========================================
if selected_section == t['tab_put']:
    st.header(t['put_header'])
    col1, col2 = st.columns(2)
    with col1:
        # Използваме глобалната цена като 'value', ако съществува.
        # Streamlit позволява промяна на стойността, дори ако е зададена с value.
        default_price = st.session_state.global_fetched_price if st.session_state.global_fetched_price > 0 else 0.0
        
        # ВАЖНО: Използваме 'value' аргумента. Ако потребителят промени числото, Streamlit го запомня в key.
        # За да се обнови при нов тикер, използваме key, който зависи от тикера, или просто разчитаме на rerender
        # Най-добрият начин за "default but modifiable" в Streamlit е да се подаде value само при първоначално зареждане или промяна
        
        cp_input = st.number_input(t['current_price'], value=default_price, step=0.10, placeholder="0.00", key="put_price_input")
        strike_input = st.number_input(t['strike'], value=None, step=0.5, placeholder="0.00")
        current_price = cp_input if cp_input is not None else 0.0
        strike = strike_input if strike_input is not None else 0.0
    with col2:
        prem_input = st.number_input(t['premium'], value=None, step=0.01, placeholder="0.00")
        contracts = st.number_input(t['contracts'], value=1, step=1)
        premium = prem_input if prem_input is not None else 0.0
    
    expiry_date = st.date_input(t['date_expiry'], min_value=today, value=today, key="put_date")
    days = (expiry_date - today).days

    if days > 0:
        st.caption(f"📅 {t['days_left']} **{days}** {t['days_count']}")
    elif days == 0:
        st.warning(t['warning_today'])

    if strike > 0 and days > 0:
        collateral = strike * 100 * contracts
        breakeven = strike - premium
        buffer_pct = 0.0
        if current_price > 0:
            buffer_pct = ((current_price - breakeven) / current_price) * 100
        
        flat_return = (premium / strike) * 100
        ann_return = (flat_return / days) * 365
        
        st.write("---")
        st.success(f"📊 **{t['return_annual']}: {ann_return:.2f}%**")
        c1, c2, c3 = st.columns(3)
        c1.metric(t['return_flat'], f"{flat_return:.2f}%")
        c2.metric(t['breakeven'], f"${breakeven:.2f}")
        c3.metric(label=t['buffer'], value=f"{buffer_pct:.2f}%", delta=f"{buffer_pct:.2f}%" if current_price > 0 else None)
        
        if buffer_pct < 0 and current_price > 0:
             st.error(t['danger_msg'])
        else:
             st.caption(f"🛡️ {t['safety_msg']}")
        st.info(f"💰 {t['collateral']}: **${collateral:,.0f}**")

# ==========================================
# SECTION 2: SELLING CALL
# ==========================================
elif selected_section == t['tab_call']:
    st.header(t['call_header'])
    col1, col2 = st.columns(2)
    with col1:
        # Тук също използваме глобалната цена за 'Cost Basis', ако потребителят иска да анализира нова позиция
        default_cost = st.session_state.global_fetched_price if st.session_state.global_fetched_price > 0 else 0.0
        
        cb_input = st.number_input(t['cost_basis'], value=default_cost, step=0.10, help="Вашата средна цена", placeholder="0.00", key="call_cost_input")
        strike_call_input = st.number_input(t['strike'], value=None, step=0.5, key="call_strike", placeholder="0.00")
        cost_basis = cb_input if cb_input is not None else 0.0
        strike_call = strike_call_input if strike_call_input is not None else 0.0
    with col2:
        prem_call_input = st.number_input(t['premium'], value=None, step=0.01, key="call_prem", placeholder="0.00")
        contracts_call = st.number_input(t['contracts'], value=1, step=1, key="call_cont")
        premium_call = prem_call_input if prem_call_input is not None else 0.0
    
    expiry_date_call = st.date_input(t['date_expiry'], min_value=today, value=today, key="call_date")
    days_call = (expiry_date_call - today).days

    if days_call > 0:
        st.caption(f"📅 {t['days_left']} **{days_call}** {t['days_count']}")
    elif days_call == 0:
        st.warning(t['warning_today'])

    if strike_call > 0 and cost_basis > 0 and days_call > 0:
        flat_prem_return = (premium_call / cost_basis) * 100
        ann_prem_return = (flat_prem_return / days_call) * 365
        cap_gains_per_share = strike_call - cost_basis
        cap_gains_pct = (cap_gains_per_share / cost_basis) * 100
        total_profit_per_share = premium_call + cap_gains_per_share
        total_profit_usd = total_profit_per_share * 100 * contracts_call
        cap_gains_usd = cap_gains_per_share * 100 * contracts_call
        total_return_pct = (total_profit_per_share / cost_basis) * 100
        
        st.write("---")
        st.success(f"🚀 **{t['total_profit']}: ${total_profit_usd:,.2f}**")
        c1, c2, c3 = st.columns(3)
        c1.metric(t['prem_return'], f"{flat_prem_return:.2f}%", f"{ann_prem_return:.1f}% Ann.")
        c2.metric(label=t['cap_gains'], value=f"${cap_gains_usd:,.2f}", delta=f"{cap_gains_pct:.2f}%")
        c3.metric(label=t['total_return'], value=f"{total_return_pct:.2f}%", delta=f"{total_return_pct:.2f}%")
        
        if cap_gains_per_share < 0:
            st.error(f"⚠️ Внимание: Страйкът (${strike_call}) е под вашата цена на купуване (${cost_basis}).")

# ==========================================
# SECTION 3: ROLLING
# ==========================================
elif selected_section == t['tab_roll']:
    st.header(t['roll_header'])
    
    roll_strat = st.radio(t['roll_strategy'], (t['strat_call'], t['strat_put']), horizontal=True)
    is_call = (roll_strat == t['strat_call'])
    
    st.divider()
    
    col_hist, col_new = st.columns(2)
    
    with col_hist:
        st.subheader(t['orig_data'])
        orig_date = st.date_input(t['orig_date'], value=today, key="orig_date_in")
        op_input = st.number_input(t['orig_prem'], value=None, step=0.01, placeholder="0.00")
        orig_premium = op_input if op_input is not None else 0.0
        
        os_input = st.number_input(t['old_strike'], value=None, step=0.5, placeholder="0.00")
        old_strike = os_input if os_input is not None else 0.0
        
        curr_expiry = st.date_input(t['curr_exp'], value=today, key="curr_exp_in")

    with col_new:
        st.subheader(t['new_data'])
        ns_input = st.number_input(t['new_strike'], value=None, step=0.5, placeholder="0.00")
        new_strike = ns_input if ns_input is not None else 0.0
        
        new_expiry = st.date_input(t['new_expiry'], value=today, key="new_exp_in")
        
        roll_type = st.radio(t['roll_type'], (t['roll_credit'], t['roll_debit']), horizontal=True)
        rp_input = st.number_input(t['roll_cost_lbl'], value=None, step=0.01, placeholder="0.00")
        roll_price = rp_input if rp_input is not None else 0.0

    if old_strike > 0 and new_strike > 0 and orig_premium > 0:
        st.divider()
        st.subheader(t['an_comparison'])
        
        days_base = (curr_expiry - orig_date).days
        days_total = (new_expiry - orig_date).days
        
        if days_base <= 0: days_base = 1 
        if days_total <= 0: days_total = 1
        
        profit_base = orig_premium
        roi_base = (profit_base / old_strike) * 100
        ann_base = (roi_base / days_base) * 365
        
        net_premium = 0.0
        if roll_type == t['roll_credit']:
            net_premium = orig_premium + roll_price
        else:
            net_premium = orig_premium - roll_price
            
        profit_fail = net_premium
        roi_fail = (profit_fail / old_strike) * 100 
        ann_fail = (roi_fail / days_total) * 365
        
        strike_diff = 0.0
        if is_call:
             strike_diff = new_strike - old_strike
        else:
             strike_diff = old_strike - new_strike 
        
        profit_win = net_premium + strike_diff
        roi_win = (profit_win / old_strike) * 100
        ann_win = (roi_win / days_total) * 365

        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            st.info(t['scen_base'])
            st.metric(t['row_profit'], f"${profit_base:.2f}")
            st.metric(t['row_days'], f"{days_base} {t['days_count']}")
            st.metric(t['row_ann'], f"{ann_base:.2f}%")
            
        with col_s2:
            st.warning(t['scen_fail'])
            delta_val = None
            if profit_fail < profit_base: delta_val = f"-${(profit_base - profit_fail):.2f}"
            else: delta_val = f"+${(profit_fail - profit_base):.2f}"
            
            st.metric(t['row_profit'], f"${profit_fail:.2f}", delta=delta_val)
            st.metric(t['row_days'], f"{days_total} {t['days_count']}")
            
            ann_delta = f"{(ann_fail - ann_base):.2f}%"
            st.metric(t['row_ann'], f"{ann_fail:.2f}%", delta=ann_delta)

        with col_s3:
            st.success(t['scen_win'])
            st.metric(t['row_profit'], f"${profit_win:.2f}", delta=f"+${(profit_win - profit_fail):.2f}")
            st.metric(t['row_days'], f"{days_total} {t['days_count']}")
            st.metric(t['row_ann'], f"{ann_win:.2f}%", delta=f"{(ann_win - ann_base):.2f}%")

        st.write("---")
        st.subheader(t['risk_insight'])
        
        if ann_fail < ann_base:
            st.write(f"""
            📉 {t['risk_text_1']} **{ann_base:.2f}%** {t['risk_text_2']} **{ann_fail:.2f}%** (в случай на провал),
            {t['risk_text_3']} **{ann_win:.2f}%** (при успех).
            """)
        else:
            st.write(f"📈 Дори при провал, доходността ви се повишава до **{ann_fail:.2f}%**! Това е чиста победа.")
            
        if ann_win > ann_base and ann_fail > (ann_base * 0.5):
             st.success(t['verdict_great'])
        elif ann_fail < (ann_base * 0.5): 
             st.error(t['verdict_bad'])
        else:
             st.info("⚠️ Сделката е неутрална/приемлива.")

# ==========================================
# SECTION 4: MARKET DATA (LEGACY TAB)
# ==========================================
elif selected_section == t['tab_data']:
    st.header(t['md_header'])
    
    st.info(f"{t['md_note']}\n\n{t['md_note_ex']}")
    
    # Тъй като вече имаме глобален инпут, тук може да оставим локален за детайлни данни
    ticker_symbol = st.text_input(t['md_input_lbl'], value=st.session_state.last_ticker).upper()
    
    if ticker_symbol:
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            current_live_price = info.get('regularMarketPrice', info.get('currentPrice', None))
            
            if current_live_price:
                st.metric(t['md_price'], f"${current_live_price:.2f}")
                
                st.divider()
                st.subheader(t['md_chain_head'])
                
                expirations = stock.options
                if expirations:
                    c1, c2 = st.columns(2)
                    with c1:
                        sel_exp = st.selectbox(t['md_exp'], expirations)
                    with c2:
                        opt_type = st.radio(t['md_type'], ["Put", "Call"], horizontal=True)
                    
                    if sel_exp:
                        opt_chain = stock.option_chain(sel_exp)
                        data = opt_chain.puts if opt_type == "Put" else opt_chain.calls
                        
                        df_show = data[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']]
                        st.dataframe(df_show, hide_index=True, use_container_width=True)
                else:
                    st.warning(t['md_no_data'])
            else:
                st.warning(f"Не мога да намеря цена за: {ticker_symbol}. Проверете дали тикерът е правилен в Yahoo Finance.")
        except Exception as e:
            st.error(f"{t['md_error']} ({e})")

# --- FOOTER ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; color: grey;'>
        <small>Powered by <b>AIVAN Solutions</b> | © 2026 Aivan Capital</small>
    </div>
    """, 
    unsafe_allow_html=True
)
