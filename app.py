import streamlit as st

# Настройка страницы
st.set_page_config(page_title="СППВР: ИТ ЖКТ", page_icon="🏥", layout="centered")

# Инициализация состояния
if 'step' not in st.session_state:
    st.session_state.step = 'start'
if 'protocol' not in st.session_state:
    st.session_state.protocol = []

def add_log(text):
    st.session_state.protocol.append(text)

def reset():
    st.session_state.step = 'start'
    st.session_state.protocol = []

# --- БОКОВАЯ ПАНЕЛЬ (ПРОТОКОЛ) ---
with st.sidebar:
    st.header("📋 Протокол врача")
    if not st.session_state.protocol:
        st.info("Опрос начался...")
    else:
        for i, step in enumerate(st.session_state.protocol, 1):
            st.write(f"**{i}.** {step}")
    st.divider()
    st.button("🔄 Начать заново", on_click=reset, use_container_width=True)

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🏥 Алгоритм ведения пациентов с ИТ")
st.write("ИТ дистального отдела пищеварительного тракта")
st.write("---")

# --- МАШИНА СОСТОЯНИЙ (СТРОГО ПО БЛОК-СХЕМЕ) ---

if st.session_state.step == 'start':
    st.markdown("### Шаг 1. Клинические признаки перитонита")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Да, есть признаки перитонита", type="primary", use_container_width=True):
            add_log("Выявлены клинические признаки перитонита")
            st.session_state.step = 'peritonitis_actions'
            st.rerun()
    with col2:
        if st.button("Нет, признаков перитонита нет", use_container_width=True):
            add_log("Без клинических признаков перитонита")
            st.session_state.step = 'examination'
            st.rerun()

# ЛЕВАЯ ВЕТКА (ПЕРИТОНИТ)
elif st.session_state.step == 'peritonitis_actions':
    st.error("### Клинические признаки перитонита")
    st.markdown("""
    **Действия:**
    *   Дообследование
    *   Предоперационная подготовка
    *   Оперативное лечение в экстренном порядке
    
    **Оперативное вмешательство:**
    *   Лапаротомия
    *   Ревизия, санация брюшной полости
    *   Колотомия (если ИТ не находится в брюшной полости)
    *   Удаление ИТ
    *   Устранение повреждений внутренних органов при необходимости
    *   Колостомия
    """)
    if st.button("Перейти к этапу «Извлечение ИТ» ➡️", type="primary"):
        add_log("Выполнено экстренное оперативное вмешательство")
        st.session_state.step = 'extraction'
        st.rerun()

# ПРАВАЯ ВЕТКА (БЕЗ ПЕРИТОНИТА)
elif st.session_state.step == 'examination':
    st.markdown("### Шаг 2. Дообследование")
    st.write("Оцените инородное тело (ИТ):")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Потенциально не опасное (без признаков включения в просвет кишки)", use_container_width=True):
            add_log("ИТ потенциально не опасное, без включения")
            st.session_state.step = 'attempt_transanal'
            st.rerun()
    with col2:
        if st.button("Потенциально опасное (признаки включения в просвет кишки)", type="primary", use_container_width=True):
            add_log("ИТ потенциально опасное, с признаками включения")
            st.session_state.step = 'dangerous_preop'
            st.rerun()

# --- СРЕДНЯЯ ВЕТКА (НЕ ОПАСНОЕ ИТ) ---
elif st.session_state.step == 'attempt_transanal':
    st.markdown("### Попытка транснального извлечения ИТ")
    st.write("С помощью доступных инструментов.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Извлечение успешно (переход к «Извлечение ИТ»)", use_container_width=True):
            add_log("Успешное транснальное извлечение")
            st.session_state.step = 'extraction'
            st.rerun()
    with col2:
        if st.button("Неудача (переход к «Низведение»)", use_container_width=True):
            add_log("Неудачная попытка транснального извлечения")
            st.session_state.step = 'attempt_reduction'
            st.rerun()

elif st.session_state.step == 'attempt_reduction':
    st.markdown("### Попытка низведения и транснального извлечения ИТ")
    st.write("С помощью доступного инструментария или эндоскопического оборудования (ректо-, колоноскоп, операционный ректоскоп).")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Извлечение успешно (переход к «Извлечение ИТ»)", use_container_width=True):
            add_log("Успешное низведение и извлечение")
            st.session_state.step = 'extraction'
            st.rerun()
    with col2:
        if st.button("Неудача (переход к «Лапаротомия с попыткой»)", use_container_width=True):
            add_log("Неудачная попытка низведения")
            st.session_state.step = 'laparotomy_attempt'
            st.rerun()

elif st.session_state.step == 'laparotomy_attempt':
    st.markdown("### Лапаротомия с попыткой низведения и транснального извлечения ИТ")
    st.write("Выберите исход операции:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Извлечение успешно (переход к «Извлечение ИТ»)", use_container_width=True):
            add_log("Успешное извлечение при лапаротомии")
            st.session_state.step = 'extraction'
            st.rerun()
    with col2:
        if st.button("Неудача (переход к «Колотомия»)", use_container_width=True):
            add_log("Выполнена лапаротомия с неудачной попыткой извлечения")
            st.session_state.step = 'colotomy'
            st.rerun()

# --- ПРАВАЯ КРАЙНЯЯ ВЕТКА (ОПАСНОЕ ИТ) ---
elif st.session_state.step == 'dangerous_preop':
    st.error("### Потенциально опасное ИТ (признаки включения)")
    st.markdown("**Предоперационная подготовка**")
    if st.button("Перейти к «Лапаротомия» ➡️", type="primary"):
        add_log("Проведена предоперационная подготовка")
        st.session_state.step = 'dangerous_laparotomy'
        st.rerun()

elif st.session_state.step == 'dangerous_laparotomy':
    st.error("### Лапаротомия")
    if st.button("Перейти к «Решение вопроса о необходимости колостомии» ➡️", type="primary"):
        add_log("Выполнена лапаротомия")
        st.session_state.step = 'colostomy_decision'
        st.rerun()

elif st.session_state.step == 'colostomy_decision':
    st.error("### Решение вопроса о необходимости колостомии")
    if st.button("Перейти к «Колотомия» ➡️", type="primary"):
        add_log("Принято решение о необходимости колостомии")
        st.session_state.step = 'colotomy'
        st.rerun()

# --- ФИНАЛЬНЫЕ БЛОКИ ---
elif st.session_state.step == 'extraction':
    st.success("### Извлечение ИТ")
    st.write("Инородное тело извлечено.")
    if st.button("Перейти к «Контрольное эндоскопическое исследование» ➡️", type="primary"):
        add_log("Извлечение ИТ завершено")
        st.session_state.step = 'control_endoscopy'
        st.rerun()

elif st.session_state.step == 'colotomy':
    st.warning("### Колотомия")
    st.write("Выполнена колотомия (извлечение ИТ через разрез кишки).")
    if st.button("Перейти к «Контрольное эндоскопическое исследование» ➡️", type="primary"):
        add_log("Выполнена колотомия")
        st.session_state.step = 'control_endoscopy'
        st.rerun()

elif st.session_state.step == 'control_endoscopy':
    st.info("### Контрольное эндоскопическое исследование")
    st.write("Алгоритм завершен. Протокол сформирован.")
    if st.button("Начать новый опрос"):
        reset()
        st.rerun()