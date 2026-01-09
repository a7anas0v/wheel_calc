import streamlit as st
from datetime import date

# --- Настройки на страницата ---
st.set_page_config(page_title="Wheel Strategy Pro", page_icon="📅", layout="centered")

st.title("📅 Wheel Strategy Calculator")
st.write("С автоматично изчисляване на дните чрез календар")

# Взимаме днешната дата
today = date.today()
st.write(f"Днешна дата: **{today.strftime('%d.%m.%Y')}**")

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
        # ТУК Е ПРОМЯНАТА: Календар вместо число
        expiry_date = st.date_input(
            "Дата на падеж (Expiration Date)",
            min_value=today,  # Не позволява минали дати
            value=today       # По подразбиране е днес
        )
        contracts = st.number_input("Брой контракти", value=1, step=1)

    # Автоматично смятане на дните
    days = (expiry_date - today).days
    
    # Показваме колко дни са сметнати
    if days == 0:
        st.warning("⚠️ Избрали сте днешната дата! Изберете бъдеща дата.")
    else:
        st.info(f"📆 Дни до падежа: **{days}**")

    if strike > 0 and days > 0:
        capital = strike * 100 * contracts
        total_income = premium * 100 * contracts
        
        # Изчисления
        abs_return = (premium / strike) * 100
        ann_return = (abs_return / days) * 365
        
        # Risk/Reward
        max_risk = (strike - premium) * 100 * contracts
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
            
        st.caption(f"Risk / Reward Ratio = 1 : {rr_ratio:.1f}")

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

    st.write("---")
    st.write("Кога изтича НОВАТА опция?")
    
    # Календар и за ролването
    new_expiry_date = st.date_input(
        "Нова Дата на падеж",
        min_value=today
    )
    
    # Тук смятаме дните от днес до новия падеж
    days_to_new_expiry = (new_expiry_date - today).days
    
    if days_to_new_expiry > 0:
        st.info(f"📆 Новата позиция ще бъде отворена за **{days_to_new_expiry}** дни (от днес).")

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
            
            # Допълнителна статистика за годишна доходност на кредита
            if days_to_new_expiry > 0:
                ann_roll_return = ((price / old_strike) * 100 / days_to_new_expiry) * 365
                st.caption(f"Този кредит носи {ann_roll_return:.1f}% годишна доходност върху капитала.")
            
        else: # Debit Roll
            st.subheader("Анализ на Debit Roll")
            
            if strike_diff == 0:
                st.error("Грешка: Не променяш страйка, а плащаш пари!")
            else:
                cost_percent = (price / strike_diff) * 100
                
                c1, c2 = st.columns(2)
                c1.metric("Ширина на страйковете", f"${strike_diff:.2f}")
                c2.metric("Цена (Дебит)", f"${price:.2f}")
                
                # Визуализация с прогрес бар за риска
                st.write("Процент на платения дебит:")
                bar_color = "red" if cost_percent > 33 else "green"
                st.progress(min(cost_percent / 100, 1.0))
                
                # ЛОГИКАТА ЗА ЧЕРВЕНАТА ЗОНА
                if cost_percent > 33:
                    st.error(f"🛑 STOP! Това е {cost_percent:.1f}%. (Над допустимите 33%)")
                    st.write("Сделката е математически неизгодна.")
                elif cost_percent > 25:
                    st.warning(f"⚠️ Внимание: Гранична стойност ({cost_percent:.1f}%).")
                else:
                    st.success(f"✅ ОДОБРЕНО: Рискът е приемлив ({cost_percent:.1f}%).")
