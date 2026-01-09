import streamlit as st
from datetime import date

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="Wheel Strategy Pro", page_icon="💰", layout="centered")

# --- 2. УПРАВЛЕНИЕ НА ЕЗИКА ---
if 'language' not in st.session_state:
    st.session_state.language = 'BG'

# --- 3. РЕЧНИК С ПРЕВОДИ ---
texts = {
    'BG': {
        'title': "Wheel Strategy Calculator",
        'subtitle': "Професионален анализ на опции и риск",
        'tab_put': "🟢 1. Продажба на PUT (Вход)",
        'tab_call': "🔴 2. Продажба на CALL (Изход)",
        'tab_roll': "🔄 3. Ролване (Управление)",
        # Общи
        'current_price': "Текуща цена на акцията ($)",
        'strike': "Страйк Цена ($)",
        'premium': "Премия на акция ($)",
        'date_expiry': "Дата на падеж",
        'contracts': "Брой контракти",
        'days_left': "Дни до падежа:",
        'warning_today': "⚠️ Изберете бъдеща дата!",
        # PUT Метрики
        'put_header': "Анализ на Cash Secured Put",
        'collateral': "Капитал в риск (Collateral)",
        'breakeven': "Цена на нулата (Break-Even)",
        'buffer': "Буфер от текущата цена",
        'return_flat': "Възвращаемост (Flat)",
        'return_annual': "Годишна доходност (Annualized)",
        'safety_msg': "Колко може да падне акцията, преди да сте на загуба.",
        'danger_msg': "⚠️ Внимание: Текущата цена вече е под вашата Break-Even точка!",
        # CALL Метрики
        'call_header': "Анализ на Covered Call",
        'cost_basis': "Вашата средна цена (Net Cost Basis) ($)",
        'cap_gains': "Печалба от акциите (ако ви ги вземат)",
        'total_profit': "ОБЩА потенциална печалба",
        'total_return': "Обща възвращаемост % (Ако ви 'асайнат')",
        'prem_return': "Доходност само от премията",
        # Rolling
        'roll_header': "Калкулатор за Ролване",
        'old_strike': "Стар Страйк ($)",
        'new_strike': "Нов Страйк ($)",
        'roll_type': "Тип Ролване:",
        'credit_txt': "Credit (Взимам пари)",
        'debit_txt': "Debit (Плащам пари)",
        'roll_price': "Цена на ролването ($)",
        'new_expiry_lbl': "Нова Дата на падеж",
        'roll_res_credit': "✅ CREDIT ROLL: Отлична сделка!",
        'roll_res_debit': "Анализ на Debit Roll",
        'cash_in': "Взимаш кеш:",
        'strike_imp': "Подобрение на страйка:",
        'net_imp': "Нетно подобрение:",
        'stop_msg': "🛑 STOP! Това е над 33%",
        'ok_msg': "✅ ОДОБРЕНО: Рискът е приемлив"
    },
    'EN': {
        'title': "Wheel Strategy Calculator",
        'subtitle': "Professional Option & Risk Analysis",
        'tab_put': "🟢 1. Sell PUT (Entry)",
        'tab_call': "🔴 2. Sell CALL (Exit)",
        'tab_roll': "🔄 3. Rolling Logic",
        # General
        'current_price': "Current Stock Price ($)",
        'strike': "Strike Price ($)",
        'premium': "Premium per Share ($)",
        'date_expiry': "Expiration Date",
        'contracts': "Number of Contracts",
        'days_left': "Days to Expiration:",
        'warning_today': "⚠️ Please select a future date!",
        # PUT Metrics
        'put_header': "Cash Secured Put Analysis",
        'collateral': "Capital at Risk (Collateral)",
        'breakeven': "Break-Even Price",
        'buffer': "Discount / Safety Buffer",
        'return_flat': "Return on Risk (Flat)",
        'return_annual': "Annualized ROI",
        'safety_msg': "How much the stock can drop before you lose money.",
        'danger_msg': "⚠️ Warning: Current price is already below your Break-Even point!",
        # CALL Metrics
        'call_header': "Covered Call Analysis",
        'cost_basis': "Your Net Cost Basis ($)",
        'cap_gains': "Capital Gains (if called away)",
        'total_profit': "TOTAL Potential Profit",
        'total_return': "Total Return % (if assigned)",
        'prem_return': "Premium Return (Flat)",
        # Rolling
        'roll_header': "Rolling Calculator",
        'old_strike': "Old Strike ($)",
        'new_strike': "New Strike ($)",
        'roll_type': "Roll Type:",
        'credit_txt': "Credit (Receive Cash)",
        'debit_txt': "Debit (Pay Cash)",
        'roll_price': "Roll Price ($)",
        'new_expiry_lbl': "New Expiration Date",
        'roll_res_credit': "✅ CREDIT ROLL: Great Trade!",
        'roll_res_debit': "Debit Roll Analysis",
        'cash_in': "Cash Received:",
        'strike_imp': "Strike Improved:",
        'net_imp': "Net Improvement:",
        'stop_msg': "🛑 STOP! This is over 33%",
        'ok_msg': "✅ APPROVED: Acceptable risk"
    }
}

# --- 4. ЗАГЛАВИЕ И ЕЗИК ---
col_header, col_lang = st.columns([5, 1])
with col_lang:
    lang_sel = st.selectbox("🌐", ["BG", "EN"], index=0 if st.session_state.language=='BG' else 1, label_visibility="collapsed", key="lang_select")
    if lang_sel != st.session_state.language:
        st.session_state.language = lang_sel
        st.rerun()

t = texts[st.session_state.language]

with col_header:
    st.title(t['title'])
st.caption(t['subtitle'])

today = date.today()

# --- 5. ТАБОВЕ (НОВОТО МЕНЮ) ---
tab1, tab2, tab3 = st.tabs([t['tab_put'], t['tab_call'], t['tab_roll']])

# ==========================================
# TAB 1: SELLING PUT (ENTRY)
# ==========================================
with tab1:
    st.header(t['put_header'])
    
    col1, col2 = st.columns(2)
    with col1:
        current_price = st.number_input(t['current_price'], value=0.0, step=0.10, key="put_price")
        strike = st.number_input(t['strike'], value=0.0, step=0.5, key="put_strike")
    with col2:
        premium = st.number_input(t['premium'], value=0.0, step=0.01, key="put_prem")
        contracts = st.number_input(t['contracts'], value=1, step=1, key="put_cont")
    
    expiry_date = st.date_input(t['date_expiry'], min_value=today, value=today, key="put_date")
    days = (expiry_date - today).days

    if days == 0:
        st.warning(t['warning_today'])
    elif strike > 0:
        # ИЗЧИСЛЕНИЯ
        collateral = strike * 100 * contracts
        breakeven = strike - premium
        
        # Buffer % (Discount)
        buffer_pct = 0.0
        if current_price > 0:
            buffer_pct = ((current_price - breakeven) / current_price) * 100
        
        # ROI
        flat_return = (premium / strike) * 100
        ann_return = (flat_return / days) * 365
        
        st.write("---")
        
        # Основен панел с резултати (Зелен)
        st.success(f"📊 **{t['return_annual']}: {ann_return:.2f}%**")
        
        # Детайли в 3 колони
        c1, c2, c3 = st.columns(3)
        c1.metric(t['return_flat'], f"{flat_return:.2f}%")
        c2.metric(t['breakeven'], f"${breakeven:.2f}")
        
        # --- ПРОМЯНАТА Е ТУК ---
        # Използваме параметъра 'delta', за да оцветим автоматично.
        # Ако е положително -> Зелено. Ако е отрицателно -> Червено.
        c3.metric(
            label=t['buffer'], 
            value=f"{buffer_pct:.2f}%", 
            delta=f"{buffer_pct:.2f}%" if current_price > 0 else None
        )
        # -----------------------
        
        if buffer_pct < 0 and current_price > 0:
             st.error(t['danger_msg'])
        else:
             st.caption(f"🛡️ {t['safety_msg']}")
        
        # Collateral Info
        st.info(f"💰 {t['collateral']}: **${collateral:,.0f}**")


# ==========================================
# TAB 2: SELLING CALL (EXIT)
# ==========================================
with tab2:
    st.header(t['call_header'])
    
    col1, col2 = st.columns(2)
    with col1:
        # Тук е важното ново поле - Cost Basis
        cost_basis = st.number_input(t['cost_basis'], value=0.0, step=0.10, help="Цената, на която сте купили акциите (или break-even от пута).")
        strike_call = st.number_input(t['strike'], value=0.0, step=0.5, key="call_strike")
    with col2:
        premium_call = st.number_input(t['premium'], value=0.0, step=0.01, key="call_prem")
        contracts_call = st.number_input(t['contracts'], value=1, step=1, key="call_cont")
        
    expiry_date_call = st.date_input(t['date_expiry'], min_value=today, value=today, key="call_date")
    days_call = (expiry_date_call - today).days

    if days_call == 0:
        st.warning(t['warning_today'])
    elif strike_call > 0 and cost_basis > 0:
        # ИЗЧИСЛЕНИЯ
        
        # 1. Печалба само от премията
        flat_prem_return = (premium_call / cost_basis) * 100
        ann_prem_return = (flat_prem_return / days_call) * 365
        
        # 2. Печалба от ръст на акцията (Capital Gains)
        cap_gains_per_share = strike_call - cost_basis
        total_profit_per_share = premium_call + cap_gains_per_share
        
        # Обща сума в долари
        total_profit_usd = total_profit_per_share * 100 * contracts_call
        cap_gains_usd = cap_gains_per_share * 100 * contracts_call
        
        # 3. Обща възвращаемост (Total Return)
        total_return_pct = (total_profit_per_share / cost_basis) * 100
        
        st.write("---")
        
        st.success(f"🚀 **{t['total_profit']}: ${total_profit_usd:,.2f}**")
        
        c1, c2, c3 = st.columns(3)
        # Показваме ROI на премията + годишна база
        c1.metric(t['prem_return'], f"{flat_prem_return:.2f}%", f"{ann_prem_return:.1f}% Ann.")
        c2.metric(t['cap_gains'], f"${cap_gains_usd:,.2f}")
        
        # Използваме delta и тук за общата възвращаемост
        c3.metric(
            label=t['total_return'], 
            value=f"{total_return_pct:.2f}%",
            delta=f"{total_return_pct:.2f}%"
        )
        
        if cap_gains_per_share < 0:
            st.error(f"⚠️ Внимание: Страйкът (${strike_call}) е под вашата цена на купуване (${cost_basis}). Заключвате загуба от капитала!")

# ==========================================
# TAB 3: ROLLING (MANAGEMENT)
# ==========================================
with tab3:
    st.header(t['roll_header'])
    
    col1, col2 = st.columns(2)
    with col1:
        old_strike = st.number_input(t['old_strike'], value=0.0, step=0.5)
        new_strike = st.number_input(t['new_strike'], value=0.0, step=0.5)
    with col2:
        roll_type = st.radio(t['roll_type'], (t['credit_txt'], t['debit_txt']))
        price = st.number_input(t['roll_price'], value=0.0, step=0.01)

    new_expiry_date = st.date_input(t['new_expiry_lbl'], min_value=today, key="roll_date")
    days_roll = (new_expiry_date - today).days
    
    if days_roll > 0:
        st.caption(f"📅 +{days_roll} дни")

    if old_strike > 0 and new_strike > 0:
        strike_diff = abs(new_strike - old_strike)
        st.write("---")
        
        if roll_type == t['credit_txt']:
            total_benefit = price + strike_diff
            st.success(t['roll_res_credit'])
            
            c1, c2, c3 = st.columns(3)
            c1.metric(t['cash_in'], f"${price:.2f}")
            c2.metric(t['strike_imp'], f"${strike_diff:.2f}")
            c3.metric(t['net_imp'], f"${total_benefit:.2f}")
            
        else: # Debit Roll
            st.subheader(t['roll_res_debit'])
            
            if strike_diff == 0:
                st.error("Грешка: Плащате дебит без да променяте страйка!")
            else:
                cost_percent = (price / strike_diff) * 100
                
                c1, c2 = st.columns(2)
                c1.metric("Ширина на страйковете", f"${strike_diff:.2f}")
                c2.metric("Цена (Дебит)", f"${price:.2f}")
                
                st.write(f"Плащате **{cost_percent:.1f}%** от ширината на страйка.")
                st.progress(min(cost_percent / 100, 1.0))
                
                if cost_percent > 33:
                    st.error(f"{t['stop_msg']} ({cost_percent:.1f}%)")
                else:
                    st.success(f"{t['ok_msg']} ({cost_percent:.1f}%)")
