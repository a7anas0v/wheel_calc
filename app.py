import streamlit as st
from datetime import date

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="Wheel Strategy Pro", page_icon="💰", layout="centered")

# --- 2. УПРАВЛЕНИЕ НА ЕЗИКА ---
if 'language' not in st.session_state:
    st.session_state.language = 'BG'

# --- 3. РЕЧНИК С ПРЕВОДИ (FIXED) ---
texts = {
    'BG': {
        'title': "Wheel Strategy Calculator",
        'subtitle': "Професионален анализ на опции и риск",
        'tab_put': "🟢 1. Продажба на PUT (Вход)",
        'tab_call': "🔴 2. Продажба на CALL (Изход)",
        'tab_roll': "🔄 3. Ролване (Стратегия)",
        # Общи
        'current_price': "Текуща цена на акцията ($)",
        'strike': "Страйк Цена ($)",
        'premium': "Премия на акция ($)",
        'date_expiry': "Дата на падеж",
        'contracts': "Брой контракти",
        'days_left': "Оставащи дни до падежа:",
        'days_count': "дни",
        'warning_today': "⚠️ Изберете бъдеща дата!",
        # PUT
        'put_header': "Анализ на Cash Secured Put",
        'collateral': "Капитал в риск (Collateral)",
        'breakeven': "Цена на нулата (Break-Even)",
        'buffer': "Буфер (Discount)",
        'return_flat': "Възвращаемост (Flat)",
        'return_annual': "Годишна (Annualized)",
        'safety_msg': "Колко може да падне акцията, преди да сте на загуба.",
        'danger_msg': "⚠️ Внимание: Текущата цена вече е под вашата Break-Even точка!",
        # CALL
        'call_header': "Анализ на Covered Call",
        'cost_basis': "Средна цена (Cost Basis) ($)",
        'cap_gains': "Капиталова Печалба ($)",
        'total_profit': "ОБЩА потенциална печалба",
        'total_return': "Общ ROI (Total Return)",
        'prem_return': "Доход от Премия",
        # ROLLING (FIXED MISSING KEYS)
        'roll_header': "Стратегически Анализ на Ролване",
        'roll_strategy': "Каква позиция ролвате?",
        'strat_call': "Covered CALL (Ролване нагоре/напред)",
        'strat_put': "Cash Secured PUT (Ролване надолу/напред)",
        'col_curr': "🏦 ТЕКУЩА Позиция (От какво бягате?)",
        'col_new': "✨ НОВА Позиция (Към какво отивате?)",
        'roll_expiry': "Нова дата на падеж",
        'roll_type': "Тип на транзакцията:",  # <--- ВЪРНАТ ЛИПСВАЩИЯ КЛЮЧ
        'roll_cost_lbl': "Цена на ролването (Net Price)",
        'roll_credit': "Credit (Взимам пари)",
        'roll_debit': "Debit (Плащам пари)",
        'analysis_title': "📊 Сравнителен Анализ",
        'metric_cash': "Кеш ефект днес",
        'metric_cap': "Доп. Капиталов Потенциал",
        'metric_total': "Общо Подобрение (Net Economic Value)",
        'metric_ann': "Годишна доходност на ролването",
        'verdict_good': "✅ ОТЛИЧЕН ХОД",
        'verdict_bad': "🛑 НЕИЗГОДНО",
        'verdict_ok': "⚠️ ПРИЕМЛИВО",
        'reason_credit': "Взимате пари + Вдигате тавана на печалбата.",
        'reason_debit_good': "Плащате малко, за да отключите голям потенциал.",
        'reason_debit_bad': "Плащате твърде скъпо (>33%) за този потенциал.",
        'msg_strike_imp': "Разлика в страйковете",
        'msg_days_added': "Добавени дни риск"
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
        'days_count': "days",
        'warning_today': "⚠️ Please select a future date!",
        # PUT
        'put_header': "Cash Secured Put Analysis",
        'collateral': "Capital at Risk (Collateral)",
        'breakeven': "Break-Even Price",
        'buffer': "Discount / Buffer",
        'return_flat': "Return (Flat)",
        'return_annual': "Annualized ROI",
        'safety_msg': "How much the stock can drop before you lose money.",
        'danger_msg': "⚠️ Warning: Current price is already below your Break-Even point!",
        # CALL
        'call_header': "Covered Call Analysis",
        'cost_basis': "Net Cost Basis ($)",
        'cap_gains': "Capital Gains ($)",
        'total_profit': "TOTAL Potential Profit",
        'total_return': "Total Return %",
        'prem_return': "Premium Return",
        # ROLLING
        'roll_header': "Rolling Strategy Analysis",
        'roll_strategy': "Which Strategy?",
        'strat_call': "Covered CALL (Rolling UP/OUT)",
        'strat_put': "Cash Secured PUT (Rolling DOWN/OUT)",
        'col_curr': "🏦 CURRENT Position (From)",
        'col_new': "✨ NEW Position (To)",
        'roll_expiry': "New Expiration Date",
        'roll_type': "Transaction Type:", # <--- ВЪРНАТ ЛИПСВАЩИЯ КЛЮЧ
        'roll_cost_lbl': "Net Roll Price",
        'roll_credit': "Credit (Receive Cash)",
        'roll_debit': "Debit (Pay Cash)",
        'analysis_title': "📊 Comparative Analysis",
        'metric_cash': "Immediate Cash Flow",
        'metric_cap': "Added Capital Potential",
        'metric_total': "Total Economic Value",
        'metric_ann': "Annualized Roll Return",
        'verdict_good': "✅ GREAT TRADE",
        'verdict_bad': "🛑 BAD DEAL",
        'verdict_ok': "⚠️ ACCEPTABLE",
        'reason_credit': "You get cash + Higher profit ceiling.",
        'reason_debit_good': "Small cost to unlock big potential.",
        'reason_debit_bad': "Too expensive (>33%) for the gain.",
        'msg_strike_imp': "Strike Difference",
        'msg_days_added': "Days Added"
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

# --- 5. ТАБОВЕ ---
tab1, tab2, tab3 = st.tabs([t['tab_put'], t['tab_call'], t['tab_roll']])

# ==========================================
# TAB 1: SELLING PUT
# ==========================================
with tab1:
    st.header(t['put_header'])
    col1, col2 = st.columns(2)
    with col1:
        cp_input = st.number_input(t['current_price'], value=None, step=0.10, placeholder="0.00")
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
# TAB 2: SELLING CALL
# ==========================================
with tab2:
    st.header(t['call_header'])
    col1, col2 = st.columns(2)
    with col1:
        cb_input = st.number_input(t['cost_basis'], value=None, step=0.10, help="Вашата средна цена", placeholder="0.00")
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
# TAB 3: ROLLING (NEW STRATEGIC VIEW)
# ==========================================
with tab3:
    st.header(t['roll_header'])
    
    # 1. Избор на стратегия
    roll_strat = st.radio(t['roll_strategy'], (t['strat_call'], t['strat_put']), horizontal=True)
    is_call = (roll_strat == t['strat_call'])
    
    st.divider()
    
    # 2. Входни данни (Сравнителен изглед)
    col_old, col_new = st.columns(2)
    
    with col_old:
        st.subheader(t['col_curr'])
        old_strike_in = st.number_input(t['strike'], value=None, step=0.5, key="old_strike", placeholder="0.00")
        
    with col_new:
        st.subheader(t['col_new'])
        new_strike_in = st.number_input(t['strike'], value=None, step=0.5, key="new_strike", placeholder="0.00")
        new_expiry = st.date_input(t['roll_expiry'], min_value=today, key="roll_date")
    
    old_strike = old_strike_in if old_strike_in is not None else 0.0
    new_strike = new_strike_in if new_strike_in is not None else 0.0
    
    st.write("") # Spacer
    
    # Данни за самата сделка (Net Price)
    c1, c2 = st.columns([1, 2])
    with c1:
        # ЕТО ТУК БЕШЕ ГРЕШКАТА - Ключът 'roll_type' сега съществува
        roll_type = st.radio(t['roll_type'], (t['roll_credit'], t['roll_debit']))
    with c2:
        price_in = st.number_input(t['roll_cost_lbl'], value=None, step=0.01, placeholder="0.00")
        roll_price = price_in if price_in is not None else 0.0

    days_roll = (new_expiry - today).days
    if days_roll > 0:
        st.caption(f"📅 +{days_roll} {t['days_count']}")

    # 3. АНАЛИЗ
    if old_strike > 0 and new_strike > 0:
        st.divider()
        st.subheader(t['analysis_title'])
        
        # Логика за "Подобрение на страйка" (Strike Improvement)
        strike_diff = 0.0
        if is_call:
            # При Call искаме по-висок страйк (Upside)
            strike_diff = new_strike - old_strike
        else:
            # При Put искаме по-нисък страйк (Lower buying price)
            strike_diff = old_strike - new_strike 
            
        # Финансова логика
        net_cash_impact = roll_price if roll_type == t['roll_credit'] else -roll_price
        total_economic_value = net_cash_impact + strike_diff
        
        # Годишна доходност на самото ролване
        # Използваме "Risk Capital" = New Strike (за Put) или Current Strike (за Call)
        # Това е приблизително, но достатъчно за сравнение
        capital_locked = new_strike
        ann_roll_return = 0.0
        if days_roll > 0 and capital_locked > 0:
             # ROI на "Net Economic Value" върху капитала
             ann_roll_return = ((total_economic_value / capital_locked) * 100 / days_roll) * 365

        # ВИЗУАЛИЗАЦИЯ НА РЕЗУЛТАТИТЕ
        col_res1, col_res2, col_res3 = st.columns(3)
        
        # 1. Кеш ефект
        col_res1.metric(
            t['metric_cash'], 
            f"${net_cash_impact:.2f}", 
            delta="Credit" if net_cash_impact > 0 else "-Debit"
        )
        
        # 2. Капиталов ефект
        col_res2.metric(
            t['metric_cap'], 
            f"${strike_diff:.2f}",
            delta=f"{t['msg_strike_imp']}"
        )
        
        # 3. ОБЩО (Total Economic Value)
        col_res3.metric(
            t['metric_total'], 
            f"${total_economic_value:.2f}",
            delta="Net Value"
        )

        # 4. ГОДИШНА ДОХОДНОСТ И ПРИСЪДА
        st.write("---")
        
        # Логика за "Присъда" (Verdict)
        is_good_deal = False
        reason = ""
        
        if roll_type == t['roll_credit']:
            # Credit Roll: Винаги е добре, ако вдигаме и страйка
            if strike_diff >= 0:
                is_good_deal = True
                verdict = t['verdict_good']
                reason = t['reason_credit']
                st.success(f"## {verdict}")
                st.write(reason)
            else:
                # Credit Roll, но губим страйк (Defensive roll)
                verdict = t['verdict_ok']
                st.warning(f"## {verdict}")
                st.write("Взимате кредит, но 'затваряте' потенциала на позицията (Inverted roll?).")

        else: # Debit Roll
            # Debit Roll: Трябва да спазваме правилото на 33%
            if strike_diff > 0:
                cost_percent = (roll_price / strike_diff) * 100
                st.write(f"Плащате **{cost_percent:.1f}%** от новия потенциал.")
                st.progress(min(cost_percent / 100, 1.0))
                
                if cost_percent <= 33:
                    verdict = t['verdict_good']
                    reason = t['reason_debit_good']
                    st.success(f"## {verdict}")
                    st.write(reason)
                else:
                    verdict = t['verdict_bad']
                    reason = t['reason_debit_bad']
                    st.error(f"## {verdict}")
                    st.write(reason)
            else:
                st.error("🛑 Плащате пари (Debit), без да подобрявате страйка! Това е сигурна загуба.")

        if days_roll > 0:
            st.caption(f"📈 {t['metric_ann']}: **{ann_roll_return:.2f}%**")
