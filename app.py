import streamlit as st
from datetime import date

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="Wheel Strategy Pro", page_icon="💰", layout="centered")

# --- 2. УПРАВЛЕНИЕ НА STATE (СЪСТОЯНИЕ) ---
if 'language' not in st.session_state:
    st.session_state.language = 'BG'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False 

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# --- 3. МОЩЕН CSS ЗА ОПРАВЯНЕ НА БЪГОВЕТЕ ---
# Този път целим директно "popover" елементите (календар и менюта)

if st.session_state.dark_mode:
    # === DARK MODE (ТЪМЕН РЕЖИМ) ===
    st.markdown("""
    <style>
        /* 1. Основни цветове */
        .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
        header { background-color: #0E1117 !important; }
        
        /* 2. Текстове */
        h1, h2, h3, p, div, span, label, li { color: #FAFAFA !important; }
        
        /* 3. Полета (Inputs) */
        input, select, textarea {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* 4. Dropdowns и Selectbox кутийки */
        div[data-baseweb="select"] > div {
            background-color: #262730 !important;
            border-color: #4F4F4F !important;
            color: #FAFAFA !important;
        }
        
        /* 5. ПОП-ЪПИ: Менюта и Календар (КРИТИЧНО ЗА DARK MODE) */
        div[data-baseweb="popover"], div[data-baseweb="menu"], div[data-baseweb="calendar"] {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Опциите в менюто */
        ul[data-testid="stSelectboxVirtualDropdown"] li {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Дните в календара */
        div[data-baseweb="calendar"] button {
            color: #FAFAFA !important;
        }

        /* Метрики */
        [data-testid="stMetricValue"] { color: #FAFAFA !important; }
    </style>
    """, unsafe_allow_html=True)
    
else:
    # === LIGHT MODE (СВЕТЪЛ РЕЖИМ - FIX) ===
    st.markdown("""
    <style>
        /* 1. Основни цветове */
        .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
        header { background-color: #FFFFFF !important; }
        
        /* 2. Текстове - Насилваме черно навсякъде */
        h1, h2, h3, p, div, span, label, li { color: #000000 !important; }
        
        /* 3. Полета (Inputs) - Светло сиво */
        input, select, textarea {
            background-color: #F0F2F6 !important;
            color: #000000 !important;
        }
        
        /* 4. Dropdowns (Самата кутийка) */
        div[data-baseweb="select"] > div {
            background-color: #F0F2F6 !important;
            border-color: #D3D3D3 !important;
            color: #000000 !important;
        }
        /* Текстът в затворено меню */
        div[data-baseweb="select"] span { color: #000000 !important; }
        
        /* 5. ПОП-ЪПИ: Менюта и Календар (ТУК БЕШЕ БЪГЪТ) */
        /* Насилваме белия фон на изскачащите прозорци */
        div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border: 1px solid #D3D3D3 !important;
        }
        
        div[data-baseweb="menu"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        /* Опциите в менюто (списъка) */
        ul[data-testid="stSelectboxVirtualDropdown"] li {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        /* Hover ефект за менюто (да се вижда къде е мишката) */
        ul[data-testid="stSelectboxVirtualDropdown"] li:hover {
            background-color: #F0F2F6 !important;
        }
        
        /* 6. КАЛЕНДАР FIX */
        div[data-baseweb="calendar"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        /* Заглавие на месеца и дните */
        div[data-baseweb="calendar"] div, div[data-baseweb="calendar"] button {
            color: #000000 !important;
        }
        /* Стрелките на календара */
        div[data-baseweb="calendar"] svg {
            fill: #000000 !important;
        }

        /* Метрики */
        [data-testid="stMetricValue"] { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)


# --- 4. РЕЧНИК С ПРЕВОДИ ---
texts = {
    'BG': {
        'title': "Wheel Strategy Calculator",
        'subtitle': "С автоматично изчисляване на дните чрез календар",
        'today': "Днешна дата:",
        'select_calc': "Избери калкулатор:",
        'opt_new': "1. Нова Позиция (Put/Call)",
        'opt_roll': "2. Ролване (Rolling Logic)",
        'header_new': "Анализ на Нова Сделка",
        'strike': "Страйк Цена ($)",
        'premium': "Премия на акция ($)",
        'date_expiry': "Дата на падеж",
        'contracts': "Брой контракти",
        'days_left': "Дни до падежа:",
        'warning_today': "⚠️ Избрали сте днешната дата! Изберете бъдеща дата.",
        'capital': "Капитал (Collateral)",
        'net_profit': "Чиста Печалба",
        'yield_header': "Доходност",
        'yield_annual': "Годишна доходност",
        'risk_reward': "Risk / Reward Ratio",
        'header_roll': "Калкулатор за Ролване",
        'old_strike': "Стар Страйк ($)",
        'new_strike': "Нов Страйк ($)",
        'roll_type': "Тип Ролване:",
        'credit_txt': "Credit (Взимам пари)",
        'debit_txt': "Debit (Плащам пари)",
        'roll_price': "Цена на ролването ($)",
        'new_expiry_q': "Кога изтича НОВАТА опция?",
        'new_expiry_lbl': "Нова Дата на падеж",
        'roll_days_info': "Новата позиция ще бъде отворена за",
        'days': "дни",
        'credit_success': "✅ CREDIT ROLL: Отлична сделка!",
        'cash_in': "Взимаш кеш:",
        'strike_up': "Вдигаш тавана с:",
        'total_improve': "Общо подобрение на позицията",
        'debit_header': "Анализ на Debit Roll",
        'error_same_strike': "Грешка: Не променяш страйка, а плащаш пари!",
        'strike_width': "Ширина на страйковете",
        'cost_debit': "Цена (Дебит)",
        'cost_percent_txt': "Процент на платения дебит:",
        'stop_msg': "🛑 STOP! Това е над 33%",
        'bad_deal': "Сделката е математически неизгодна. По-добре остави да те 'асайнат'.",
        'ok_deal': "✅ ОДОБРЕНО: Рискът е приемлив"
    },
    'EN': {
        'title': "Wheel Strategy Calculator",
        'subtitle': "Automated days calculation via calendar",
        'today': "Today's Date:",
        'select_calc': "Select Calculator:",
        'opt_new': "1. New Position (Put/Call)",
        'opt_roll': "2. Rolling Logic",
        'header_new': "New Trade Analysis",
        'strike': "Strike Price ($)",
        'premium': "Premium per Share ($)",
        'date_expiry': "Expiration Date",
        'contracts': "Number of Contracts",
        'days_left': "Days to Expiration:",
        'warning_today': "⚠️ You selected today's date! Please pick a future date.",
        'capital': "Collateral Required",
        'net_profit': "Net Profit",
        'yield_header': "Yield / Return",
        'yield_annual': "Annualized Return",
        'risk_reward': "Risk / Reward Ratio",
        'header_roll': "Rolling Calculator",
        'old_strike': "Old Strike ($)",
        'new_strike': "New Strike ($)",
        'roll_type': "Roll Type:",
        'credit_txt': "Credit (Receive Cash)",
        'debit_txt': "Debit (Pay Cash)",
        'roll_price': "Roll Price ($)",
        'new_expiry_q': "When does the NEW option expire?",
        'new_expiry_lbl': "New Expiration Date",
        'roll_days_info': "The new position will be open for",
        'days': "days",
        'credit_success': "✅ CREDIT ROLL: Great Trade!",
        'cash_in': "Cash Received:",
        'strike_up': "Strike Improved by:",
        'total_improve': "Total Position Improvement",
        'debit_header': "Debit Roll Analysis",
        'error_same_strike': "Error: Paying debit without changing strike!",
        'strike_width': "Strike Width",
        'cost_debit': "Cost (Debit)",
        'cost_percent_txt': "Debit cost percentage:",
        'stop_msg': "🛑 STOP! This is over 33%",
        'bad_deal': "Mathematically bad deal. Better take assignment.",
        'ok_deal': "✅ APPROVED: Acceptable risk"
    }
}

# --- 5. ГОРНА ЛЕНТА С БУТОНИ ---
col_title, col_lang, col_dark = st.columns([6, 1, 1])

with col_lang:
    # Език
    lang_sel = st.selectbox(
        "🌐", 
        ["BG", "EN"], 
        index=0 if st.session_state.language=='BG' else 1,
        label_visibility="collapsed",
        key="lang_select"
    )
    if lang_sel != st.session_state.language:
        st.session_state.language = lang_sel
        st.rerun()

with col_dark:
    # Toggle за темата
    st.toggle(
        "🌙", 
        value=st.session_state.dark_mode, 
        on_change=toggle_theme,
        key="theme_toggle"
    )

t = texts[st.session_state.language]

# --- 6. СЪДЪРЖАНИЕ ---

st.title(t['title'])
st.caption(t['subtitle'])

today = date.today()
st.write(f"{t['today']} **{today.strftime('%d.%m.%Y')}**")

option = st.selectbox(
    t['select_calc'],
    (t['opt_new'], t['opt_roll'])
)

# === НОВА ПОЗИЦИЯ ===
if option == t['opt_new']:
    st.header(t['header_new'])
    
    col1, col2 = st.columns(2)
    with col1:
        strike = st.number_input(t['strike'], value=0.0, step=0.5)
        premium = st.number_input(t['premium'], value=0.0, step=0.01)
    with col2:
        expiry_date = st.date_input(t['date_expiry'], min_value=today, value=today)
        contracts = st.number_input(t['contracts'], value=1, step=1)

    days = (expiry_date - today).days
    
    if days == 0:
        st.warning(t['warning_today'])
    else:
        st.info(f"📆 {t['days_left']} **{days}**")

    if strike > 0 and days > 0:
        capital = strike * 100 * contracts
        total_income = premium * 100 * contracts
        
        abs_return = (premium / strike) * 100
        ann_return = (abs_return / days) * 365
        
        max_risk = (strike - premium) * 100 * contracts
        rr_ratio = max_risk / total_income if total_income > 0 else 0
        
        st.divider()
        
        c1, c2 = st.columns(2)
        c1.metric(t['capital'], f"${capital:,.0f}")
        c2.metric(t['net_profit'], f"${total_income:.2f}")
        
        st.subheader(t['yield_header'])
        
        if ann_return > 20:
            st.success(f"🚀 {t['yield_annual']}: {ann_return:.2f}%")
        elif ann_return > 10:
            st.warning(f"⚠️ {t['yield_annual']}: {ann_return:.2f}%")
        else:
            st.error(f"🛑 {t['yield_annual']}: {ann_return:.2f}%")
            
        st.caption(f"{t['risk_reward']} = 1 : {rr_ratio:.1f}")

# === РОЛВАНЕ ===
elif option == t['opt_roll']:
    st.header(t['header_roll'])
    
    col1, col2 = st.columns(2)
    with col1:
        old_strike = st.number_input(t['old_strike'], value=0.0, step=0.5)
        new_strike = st.number_input(t['new_strike'], value=0.0, step=0.5)
    with col2:
        roll_type_sel = st.radio(t['roll_type'], (t['credit_txt'], t['debit_txt']))
        price = st.number_input(t['roll_price'], value=0.0, step=0.01)

    st.write("---")
    st.write(t['new_expiry_q'])
    
    new_expiry_date = st.date_input(t['new_expiry_lbl'], min_value=today)
    
    days_to_new_expiry = (new_expiry_date - today).days
    
    if days_to_new_expiry > 0:
        st.info(f"📆 {t['roll_days_info']} **{days_to_new_expiry}** {t['days']}.")

    if old_strike > 0 and new_strike > 0:
        strike_diff = abs(new_strike - old_strike)
        
        st.divider()
        
        if roll_type_sel == t['credit_txt']:
            total_benefit = price + strike_diff
            st.balloons()
            st.success(t['credit_success'])
            st.write(f"{t['cash_in']} **${price}**")
            st.write(f"{t['strike_up']} **${strike_diff}**")
            st.metric(t['total_improve'], f"${total_benefit:.2f}")
            
        else: # Debit
            st.subheader(t['debit_header'])
            
            if strike_diff == 0:
                st.error(t['error_same_strike'])
            else:
                cost_percent = (price / strike_diff) * 100
                
                c1, c2 = st.columns(2)
                c1.metric(t['strike_width'], f"${strike_diff:.2f}")
                c2.metric(t['cost_debit'], f"${price:.2f}")
                
                st.write(t['cost_percent_txt'])
                st.progress(min(cost_percent / 100, 1.0))
                
                if cost_percent > 33:
                    st.error(f"{t['stop_msg']} ({cost_percent:.1f}%).")
                    st.write(t['bad_deal'])
                elif cost_percent > 25:
                    st.warning(f"⚠️ ({cost_percent:.1f}%).")
                else:
                    st.success(f"{t['ok_deal']} ({cost_percent:.1f}%).")
