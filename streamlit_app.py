import joblib
import streamlit as st
import pandas as pd
from autogluon.tabular import TabularDataset, TabularPredictor

# -----------------------------------------
# FUNKCJE POMOCNICZE
# -----------------------------------------
DEFAULTS = {
    # ─── Dane demograficzne ─────────────────────────────
    "age": "",
    "gender": "Female",
    "ethnicity": "White",
    "education_level": "Highschool",
    "income_level": "Middle",
    "employment_status": "Employed",

    # ─── Styl życia (SLIDERY → LICZBY) ──────────────────
    "activity": 300,  # <-- DODANE (bo slider ma key="activity")
    "diet_score": 5,
    "sleep_hours_per_day": 8,
    "screen_time_hours_per_day": 4,
    "alcohol_consumption_per_week": 0,
    "smoking_status": "Never",

    # ─── Historia medyczna ──────────────────────────────
    "family_history_diabetes": "0",
    "hypertension_history": "0",
    "cardiovascular_history": "0",

    # ─── Parametry antropometryczne ─────────────────────
    "whr": "",

    # ─── Parametry kliniczne (text_input → liczby) ──────
    "sbp": "",
    "dbp": "",
    "hr": "",
    "hdl": "",
    "ldl": "",
    "tg": "",
    "insulin": "",
    "hba1c": "",
    "score": "",

    # ─── UI ─────────────────────────────────────────────
    "show_result": False,
}

# Walidujemy tylko to, co użytkownik wpisuje jako tekst i ma być liczbą
NUMERIC_FIELDS = [
    "age", "whr", "sbp", "dbp", "hr", "hdl", "ldl", "tg", "insulin", "hba1c", "score"
]

# Function to validate numeric inputs
def validate_number(value, field_name):
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return None, f"Pole '{field_name}' nie może być puste."
    try:
        return float(value), None
    except ValueError:
        return None, f"Pole '{field_name}' musi być liczbą."


# Reset inputs to defaults
def reset_inputs():
    for key, val in DEFAULTS.items():
        st.session_state[key] = val
    st.session_state["show_result"] = False


def reset_inputs():
    st.session_state.clear()
    st.session_state.update(DEFAULTS)

# -----------------------------------------
# KONFIGURACJA STRONY
# -----------------------------------------
st.set_page_config(page_title="Predykcja Cukrzycy", layout="wide")

# -----------------------------------------
# STYL
# -----------------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"]{
  background: linear-gradient(135deg,#e6f0ff,#f9f9ff);
  background-attachment: fixed;
  font-family: "Segoe UI", sans-serif;
  color:#222;
}

/* Sidebar: tło + biały tekst (całość) */
[data-testid="stSidebar"]{
  background: linear-gradient(180deg,#002b5b,#004080);
}
[data-testid="stSidebar"], [data-testid="stSidebar"] *{
  color:#fff !important;
}

/* Etykiety nad polami: czarne */
div[data-testid="stWidgetLabel"] > label, label{
  color:#000 !important;
  font-weight:600;
}

/* Przyciski: niebieskie tło + biały tekst (w tym emoji/span) */
div.stButton > button{
  background:#004080;
  border:0;
  border-radius:10px;
  padding:.6em 1.4em;
  font-weight:600;
}
div.stButton > button, div.stButton > button *{
  color:#fff !important;
  fill:#fff !important;
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

    # Collecting Data Using Different Widgets
    st.markdown("## 🧍 Dane demograficzne")
    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        gender = st.selectbox("Płeć", ["Female", "Male", "Other"], key="gender")
        age = st.text_input("Wiek", key="age")

    with col_d2:
        education_level = st.selectbox("Poziom edukacji", ["Highschool", "Graduate", "Postgraduate", "No formal"], key="education_level")
        ethnicity = st.selectbox("Grupa etniczna", ["White", "Hispanic", "Black", "Asian", "Other"], key="ethnicity")

    with col_d3:
        employment_status = st.selectbox("Status zatrudnienia", ["Employed", "Retired", "Unemployed", "Student"], key="employment_status")
        income_level = st.selectbox("Poziom dochodów", ["Middle", "Lower-Middle", "Upper-Middle", "Low", "High"], key="income_level")

    st.markdown("---")
    st.markdown("## 🏃 Styl życia")

    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        activity = st.slider("Aktywność fizyczna (min/tydzień)", 0, 1000, key="activity")
        diet = st.slider("Wynik diety", 0, 10, key="diet_score")
    with col_l2:
        alcohol = st.slider("Spożycie alkoholu tygodniowo", 0, 7, key="alcohol_consumption_per_week")
        sleep = st.slider("Godziny snu dziennie", 0, 24, key="sleep_hours_per_day")
    with col_l3:
        smoking_status = st.selectbox("Status palenia", ["Never", "Current", "Former"], key="smoking_status")
        screen = st.slider("Godziny przed ekranem dziennie", 0, 24, key="screen_time_hours_per_day")

    st.markdown("---")
    st.markdown("## 🩺 Historia medyczna")

    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        hypertension = st.selectbox("Historia nadciśnienia", ["0", "1"], key="hypertension_history")
    with col_h2:
        cardio = st.selectbox("Choroby sercowo-naczyniowe", ["0", "1"], key="cardiovascular_history")
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

    # Button to trigger prediction
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🔎 Przewidź ryzyko"):
            errors = []
            validated_numeric = {}

            for field in NUMERIC_FIELDS:
                value = st.session_state.get(field, "")
                val, err = validate_number(value, field)
                if err:
                    errors.append(err)
                else:
                    validated_numeric[field] = val

            if errors:
                for e in errors:
                    st.error(e)
            else:
                validated = {}

                # numeryczne z text_input (już jako float)
                validated["age"] = validated_numeric["age"]
                validated["waist_to_hip_ratio"] = validated_numeric["whr"]
                validated["systolic_bp"] = validated_numeric["sbp"]
                validated["diastolic_bp"] = validated_numeric["dbp"]
                validated["heart_rate"] = validated_numeric["hr"]
                validated["hdl_cholesterol"] = validated_numeric["hdl"]
                validated["ldl_cholesterol"] = validated_numeric["ldl"]
                validated["triglycerides"] = validated_numeric["tg"]
                validated["insulin_level"] = validated_numeric["insulin"]
                validated["hba1c"] = validated_numeric["hba1c"]
                validated["diabetes_risk_score"] = validated_numeric["score"]

                # kategorie / slidery
                validated["gender"] = gender
                validated["ethnicity"] = ethnicity
                validated["education_level"] = education_level
                validated["income_level"] = income_level
                validated["employment_status"] = employment_status
                validated["smoking_status"] = smoking_status
                validated["alcohol_consumption_per_week"] = alcohol
                validated["physical_activity_minutes_per_week"] = activity
                validated["diet_score"] = diet
                validated["sleep_hours_per_day"] = sleep
                validated["screen_time_hours_per_day"] = screen
                validated["hypertension_history"] = hypertension
                validated["cardiovascular_history"] = cardio

                # stałe / brakujące (Twoje dotychczasowe)
                validated["cholesterol_total"] = 239
                validated["glucose_fasting"] = 136
                validated["glucose_postprandial"] = 236
                validated["diabetes_stage"] = 2
                validated["family_history_diabetes"] = "0"
                validated["bmi"] = 30
                validated["Unnamed: 0"] = 0

                input_data = pd.DataFrame([validated])

                predictor = TabularPredictor.load("modelePPvsNPP/PP")

                scaler = joblib.load("modelePPvsNPP/PP/scaler.pkl")
                numeric_cols = joblib.load("modelePPvsNPP/PP/numeric_cols.pkl")
                feature_cols = joblib.load("modelePPvsNPP/PP/feature_cols.pkl")

                input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

                cat_cols = input_data.select_dtypes(include=["object","category"]).columns
                input_data = pd.get_dummies(input_data, columns=cat_cols, drop_first=True)

                input_data = input_data.reindex(columns=feature_cols, fill_value=0.0)

                pred_label = predictor.predict(input_data).iloc[0]
                proba = predictor.predict_proba(input_data)
                p1 = float(proba.iloc[0, 1])

                st.session_state["show_result"] = True
                if pred_label == 1:
                    st.error(
                        f"🚨 Wynik: Cukrzyca {'obecna' if pred_label == 1 else 'nieobecna'} "
                        f"z prawdopodobieństwem **{p1*100:.2f}%**."
                    )
                else: 
                    st.success(
                        f"✅ Wynik: Cukrzyca {'obecna' if pred_label == 1 else 'nieobecna'} "
                        f"z prawdopodobieństwem **{p1*100:.2f}%**."
                    )

    with col_btn2:
        if st.button("🧹 Wyczyść dane", on_click=reset_inputs):
            st.rerun()

    if st.session_state.get("show_result"):
        st.markdown("---")