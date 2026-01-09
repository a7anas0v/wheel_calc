import streamlit as st

# --- Настройки на страницата ---
st.set_page_config(page_title="Wheel Strategy Calc", page_icon="💰", layout="centered")

st.title("💰 The Wheel Calculator")
st.write("Инструмент за анализ на опции и ролване")

# --- Меню за навигация ---
option = st.selectbox(
    "Избери калкулатор:",
    ("1. Нова Позиция (Put/Call)", "2. Ролване (Rolling Logic)")
)

# --- ФУНКЦИЯ 1: НОВА ПОЗИЦИЯ ---
if option == "1. Нова Позиция (Put/Call)":
    st.header("Анализ на Нова Сделка")
    
    col1, col2 = st.columns(2)
    with col1:
        strike = st.number_input("Страйк Цена ($)", value=0.0, step=0.5)
        premium = st.number_input("Премия на акция ($)", value=0.0, step=0.01)
    with col2:
        days = st.number_input("Дни до падеж", value=30, step=1)
        contracts = st.number_input("Брой контракти", value=1, step=1)

    if strike > 0 and days > 0:
        capital = strike * 100 * contracts
        total_income = premium * 100 * contracts
        
        # Изчисления
        abs_return = (premium / strike) * 100
        ann_return = (abs_return / days) * 365
        
        # Risk/Reward
        max_risk = (strike - premium) * 100 * contracts
        # Reward / Risk ratio (e.g. 1 : 50)
        rr_ratio = max_risk / total_income if total_income > 0 else 0
        
        st.divider()
        
        # Показване на резултатите
        c1, c2 = st.columns(2)
        c1.metric("Капитал (Collateral)", f"${capital:,.0f}")
        c2.metric("Чиста Печалба", f"${total_income:.2f}", delta_color="normal")
        
        st.subheader("Доходност")
        
        # Логика за цветовете
        if ann_return > 20:
            st.success(f"🚀 Годишна доходност: {ann_return:.2f}% (Отлична)")
        elif ann_return > 10:
            st.warning(f"⚠️ Годишна доходност: {ann_return:.2f}% (Средна)")
        else:
            st.error(f"🛑 Годишна доходност: {ann_return:.2f}% (Ниска)")
            
        st.info(f"Risk / Reward Ratio = 1 : {rr_ratio:.1f}")
        st.caption(f"Рискуваш ${rr_ratio:.1f}, за да спечелиш $1.00")

# --- ФУНКЦИЯ 2: РОЛВАНЕ ---
elif option == "2. Ролване (Rolling Logic)":
    st.header("Калкулатор за Ролване")
    
    col1, col2 = st.columns(2)
    with col1:
        old_strike = st.number_input("Стар Страйк ($)", value=0.0, step=0.5)
        new_strike = st.number_input("Нов Страйк ($)", value=0.0, step=0.5)
    with col2:
        roll_type = st.radio("Тип Ролване:", ("Credit (Взимам пари)", "Debit (Плащам пари)"))
        price = st.number_input("Цена на ролването ($)", value=0.0, step=0.01)

    if old_strike > 0 and new_strike > 0:
        strike_diff = abs(new_strike - old_strike)
        
        st.divider()
        
        if roll_type == "Credit (Взимам пари)":
            total_benefit = price + strike_diff
            st.balloons()
            st.success("✅ CREDIT ROLL: Отлична сделка!")
            st.write(f"Взимаш кеш: **${price}**")
            st.write(f"Вдигаш тавана с: **${strike_diff}**")
            st.metric("Общо подобрение на позицията", f"${total_benefit:.2f}")
            
        else: # Debit Roll
            st.subheader("Анализ на Debit Roll")
            
            if strike_diff == 0:
                st.error("Грешка: Не променяш страйка, а плащаш пари!")
            else:
                cost_percent = (price / strike_diff) * 100
                
                c1, c2 = st.columns(2)
                c1.metric("Ширина на страйковете", f"${strike_diff:.2f}")
                c2.metric("Цена (Дебит)", f"${price:.2f}")
                
                st.write(f"Плащаш **{cost_percent:.1f}%** от потенциалната печалба.")
                
                # ЛОГИКАТА ЗА ЧЕРВЕНАТА ЗОНА
                if cost_percent > 33:
                    st.error(f"🛑 STOP! Това е над 33% ({cost_percent:.1f}%).")
                    st.write("Сделката е математически неизгодна. По-добре остави да те 'асайнат'.")
                elif cost_percent > 25:
                    st.warning(f"⚠️ Внимание: Гранична стойност ({cost_percent:.1f}%).")
                else:
                    st.success(f"✅ ОДОБРЕНО: Рискът е приемлив ({cost_percent:.1f}%).")
