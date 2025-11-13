import streamlit as st

# streamlit run streamlit_app.py

# -----------------------------------------------------------
# KONFIGURACJA STRONY
# -----------------------------------------------------------
st.set_page_config(page_title="Predykcja Cukrzycy", layout="wide")

# -----------------------------------------------------------
# STYL – CSS
# -----------------------------------------------------------
page_bg = """
<style>
/* Tło i ogólny wygląd */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(135deg, #e6f0ff, #f9f9ff);
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
    color: #222;
}

/* Pasek boczny */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #002b5b, #004080);
    color: white;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
    color: white !important;
}

/* Przyciski */
div.stButton > button {
    background-color: #004080;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6em 1.4em;
    font-weight: 600;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background-color: #0066cc;
    transform: scale(1.05);
}

/* Nagłówki i sekcje */
h1, h2, h3 {
    color: #002b5b;
}
hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #004080, #66a3ff);
    margin: 1.5em 0;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------------------------------------
# NAWIGACJA
# -----------------------------------------------------------
menu = st.sidebar.radio("📋 Nawigacja", ["🏠 Wprowadzenie", "🔍 Predykcja"])

# -----------------------------------------------------------
# STRONA 1 – WPROWADZENIE
# -----------------------------------------------------------
if menu == "🏠 Wprowadzenie":
    st.title("💙 Witamy w aplikacji do oceny ryzyka cukrzycy")

    st.markdown("""
    ### 👋 Wstęp  
    Witaj w aplikacji służącej do **oceny prawdopodobieństwa wystąpienia cukrzycy**  
    na podstawie Twoich danych zdrowotnych.

    ### 🧠 Jak to działa?
    1. Przejdź do zakładki **„Predykcja”**.  
    2. Wprowadź swoje dane dotyczące stylu życia i stanu zdrowia.  
    3. System analizuje informacje zdrowotne i na ich podstawie szacuje ryzyko wystąpienia cukrzycy. 
    4. Wynik ma charakter orientacyjny i ma na celu wsparcie użytkownika w ocenie potencjalnego zagrożenia.

    ### ⚠️ Ważne ostrzeżenie
    - Wyniki generowane przez aplikację nie stanowią diagnozy medycznej. 
    - Nie mogą być traktowane jako zastępstwo profesjonalnej opinii lekarskiej. 
    - W przypadku jakichkolwiek wątpliwości dotyczących zdrowia zalecana jest konsultacja z lekarzem specjalistą.
    """)

# -----------------------------------------------------------
# STRONA 2 – PREDYKCJA
# -----------------------------------------------------------

if menu == "🔍 Predykcja":
    st.title("🔮 Predykcja ryzyka cukrzycy")
    st.markdown("""
    Wprowadź poniższe dane w odpowiednich kategoriach, aby system mógł oszacować 
    **orientacyjne ryzyko wystąpienia cukrzycy**.
    """)

    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False

    # -------------------------------------------------------
    # 🧍 1. DANE DEMOGRAFICZNE
    # -------------------------------------------------------
    st.markdown("## 🧍 Dane demograficzne")

    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        gender = st.selectbox("Płeć", ["Female", "Male", "Other"])
        age = st.text_input("Wiek", placeholder="Wprowadź wartość liczbową")

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

    # -------------------------------------------------------
    # 🏃‍♂️ 2. STYL ŻYCIA
    # -------------------------------------------------------
    st.markdown("---")
    st.markdown("## 🏃 Styl życia")

    col_l1, col_l2, col_l3 = st.columns(3)

    with col_l1:
        activity = st.text_input("Aktywność fizyczna (min/tydzień)",
                                placeholder="Wprowadź wartość liczbową")
        diet = st.slider("Wynik diety", 0, 10, 5)

    with col_l2:
        alcohol = st.slider("Spożycie alkoholu tygodniowo", 0, 7, 0)
        sleep = st.slider("Godziny snu dziennie", 0, 24, 8)

    with col_l3:
        smoking_status = st.selectbox("Status palenia", ["Never", "Current", "Former"])
        screen = st.slider("Godziny przed ekranem dziennie", 0, 24, 4)

    # -------------------------------------------------------
    # 🩺 3. HISTORIA MEDYCZNA
    # -------------------------------------------------------
    st.markdown("---")
    st.markdown("## 🩺 Historia medyczna")

    col_h1, col_h2, col_h3 = st.columns(3)

    with col_h1:
        hypertension = st.selectbox("Historia nadciśnienia", ["0", "1"])

    with col_h2:
        cardio = st.selectbox("Choroby sercowo-naczyniowe", ["0", "1"])

    with col_h3:
        whr = st.text_input("Wskaźnik talii do bioder (WHR)",
                            placeholder="Wprowadź wartość liczbową")

    # -------------------------------------------------------
    # 🧪 4. PARAMETRY KLINICZNE
    # -------------------------------------------------------
    st.markdown("---")
    st.markdown("## 🧪 Parametry kliniczne")

    col_k1, col_k2, col_k3 = st.columns(3)

    with col_k1:
        sbp = st.text_input("Ciśnienie skurczowe", placeholder="Wprowadź wartość liczbową")
        dbp = st.text_input("Ciśnienie rozkurczowe", placeholder="Wprowadź wartość liczbową")

    with col_k2:
        hr = st.text_input("Tętno", placeholder="Wprowadź wartość liczbową")
        hdl = st.text_input("Cholesterol HDL", placeholder="Wprowadź wartość liczbową")

    with col_k3:
        ldl = st.text_input("Cholesterol LDL", placeholder="Wprowadź wartość liczbową")
        tg = st.text_input("Trójglicerydy", placeholder="Wprowadź wartość liczbową")

    col_k4, col_k5 = st.columns(2)

    with col_k4:
        insulin = st.text_input("Poziom insuliny", placeholder="Wprowadź wartość liczbową")

    with col_k5:
        hba1c = st.text_input("HbA1c", placeholder="Wprowadź wartość liczbową")

    # -------------------------------------------------------
    # 📊 5. OGÓLNY WYNIK RYZYKA
    # -------------------------------------------------------
    st.markdown("---")
    st.markdown("## 📊 Ogólny wynik ryzyka")

    score = st.text_input("Wartość indeksu ryzyka",
                        placeholder="Wprowadź wartość liczbową")

    # -------------------------------------------------------
    # PRZYCISKI
    # -------------------------------------------------------
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🔎 Przewidź ryzyko"):
            st.session_state["show_result"] = True

    with col_btn2:
        if st.button("🧹 Wyczyść dane"):
            st.session_state.clear()
            st.rerun()

    # -------------------------------------------------------
    # WYNIK – przykładowy
    # -------------------------------------------------------
    if st.session_state.get("show_result", False):
        st.markdown("---")
        st.success("✅ **Wynik przykładowy:** Cukrzyca obecna z prawdopodobieństwem **67%**.")
