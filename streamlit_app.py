import streamlit as st

# -----------------------------------------
# FUNKCJE POMOCNICZE
# -----------------------------------------
DEFAULTS = {
    "age": "",
    "activity": "",
    "whr": "",
    "sbp": "",
    "dbp": "",
    "hr": "",
    "hdl": "",
    "ldl": "",
    "tg": "",
    "insulin": "",
    "hba1c": "",
    "score": "",
}

NUMERIC_FIELDS = [
    "age", "activity", "whr", "sbp", "dbp", "hr", "hdl", "ldl", "tg", "insulin", "hba1c"
]

def validate_number(value, field_name):
    if value.strip() == "":
        return None, f"Pole '{field_name}' nie może być puste."
    try:
        return float(value), None
    except ValueError:
        return None, f"Pole '{field_name}' musi być liczbą."

def reset_inputs():
    for key, val in DEFAULTS.items():
        st.session_state[key] = val
    st.session_state["show_result"] = False


# -----------------------------------------
# KONFIGURACJA STRONY
# -----------------------------------------
st.set_page_config(page_title="Predykcja Cukrzycy", layout="wide")

# -----------------------------------------
# STYL
# -----------------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(135deg, #e6f0ff, #f9f9ff);
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
    color: #222;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #002b5b, #004080);
    color: white;
}
div.stButton > button {
    background-color: #004080;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6em 1.4em;
    font-weight: 600;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------------------
# NAWIGACJA
# -----------------------------------------
menu = st.sidebar.radio("📋 Nawigacja", ["🏠 Wprowadzenie", "🔍 Predykcja"])

# -----------------------------------------
# STRONA 1 – WPROWADZENIE
# -----------------------------------------
if menu == "🏠 Wprowadzenie":
    st.title("💙 Witamy w aplikacji do oceny ryzyka cukrzycy")
    st.markdown("""
    ### 👋 Wstęp  
    Aplikacja ocenia **orientacyjne prawdopodobieństwo wystąpienia cukrzycy** 
    na podstawie danych użytkownika.  
    """)

# -----------------------------------------
# STRONA 2 – PREDYKCJA
# -----------------------------------------
if menu == "🔍 Predykcja":
    for key, val in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val


    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False

    st.title("🔮 Predykcja ryzyka cukrzycy")

    st.markdown("## 🧍 Dane demograficzne")
    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        gender = st.selectbox("Płeć", ["Female", "Male", "Other"])
        age = st.text_input("Wiek", key="age")

    with col_d2:
        education_level = st.selectbox("Poziom edukacji",
                                       ["Highschool", "Graduate", "Postgraduate", "No formal"])
        ethnicity = st.selectbox("Grupa etniczna",
                                 ["White", "Hispanic", "Black", "Asian", "Other"])

    with col_d3:
        employment_status = st.selectbox("Status zatrudnienia",
                                         ["Employed", "Retired", "Unemployed", "Student"])
        income_level = st.selectbox("Poziom dochodów",
                                    ["Middle", "Lower-Middle", "Upper-Middle", "Low", "High"])

    st.markdown("---")
    st.markdown("## 🏃 Styl życia")

    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        activity = st.text_input("Aktywność fizyczna (min/tydzień)", key="activity")
        diet = st.slider("Wynik diety", 0, 10, 5)
    with col_l2:
        alcohol = st.slider("Spożycie alkoholu tygodniowo", 0, 7, 0)
        sleep = st.slider("Godziny snu dziennie", 0, 24, 8)
    with col_l3:
        smoking_status = st.selectbox("Status palenia", ["Never", "Current", "Former"])
        screen = st.slider("Godziny przed ekranem dziennie", 0, 24, 4)

    st.markdown("---")
    st.markdown("## 🩺 Historia medyczna")

    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        hypertension = st.selectbox("Historia nadciśnienia", ["0", "1"])
    with col_h2:
        cardio = st.selectbox("Choroby sercowo-naczyniowe", ["0", "1"])
    with col_h3:
        whr = st.text_input("Wskaźnik talii do bioder (WHR)", key="whr")

    st.markdown("---")
    st.markdown("## 🧪 Parametry kliniczne")

    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        sbp = st.text_input("Ciśnienie skurczowe", key="sbp")
        dbp = st.text_input("Ciśnienie rozkurczowe", key="dbp")
    with col_k2:
        hr = st.text_input("Tętno", key="hr")
        hdl = st.text_input("Cholesterol HDL", key="hdl")
    with col_k3:
        ldl = st.text_input("Cholesterol LDL", key="ldl")
        tg = st.text_input("Trójglicerydy", key="tg")

    col_k4, col_k5 = st.columns(2)
    with col_k4:
        insulin = st.text_input("Poziom insuliny", key="insulin")
    with col_k5:
        hba1c = st.text_input("HbA1c", key="hba1c")

    st.markdown("---")
    st.markdown("## 📊 Ogólny wynik ryzyka")
    score = st.text_input("Wartość indeksu ryzyka", key="score")

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🔎 Przewidź ryzyko"):
            errors = []
            validated = {}

            for field in NUMERIC_FIELDS:
                value = st.session_state.get(field, "")
                val, err = validate_number(value, field)
                if err:
                    errors.append(err)
                else:
                    validated[field] = val

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.session_state["show_result"] = True

    with col_btn2:
        if st.button("🧹 Wyczyść dane"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if st.session_state.get("show_result"):
        st.markdown("---")
        st.success("✅ **Wynik przykładowy:** Cukrzyca obecna z prawdopodobieństwem **67%**.")
