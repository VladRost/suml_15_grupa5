import streamlit as st
import pandas as pd
from autogluon.tabular import TabularDataset, TabularPredictor

# -----------------------------------------
# FUNKCJE POMOCNICZE
# -----------------------------------------
DEFAULTS = {
"family_history_diabetes": "",
    "bmi": "",
    "age": "",
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
    "gender": "",
    "ethnicity": "",
    "education_level": "",
    "income_level": "",
    "employment_status": "",
    "smoking_status": "",
    "physical_activity_minutes_per_week": "",
    "diet_score": "",
    "sleep_hours_per_day": "",
    "screen_time_hours_per_day": "",
    "family_history_diabetes": "",
    "hypertension_history": "",
    "cardiovascular_history": "",
    "bmi": "",
    "waist_to_hip_ratio": "",
    "systolic_bp": "",
    "diastolic_bp": "",
    "heart_rate": "",
    "cholesterol_total": "",
    "glucose_fasting": "",
    "glucose_postprandial": "",
    "insulin_level": "",
    "diabetes_risk_score": "",
    "diabetes_stage": "",
}

NUMERIC_FIELDS = [
    "age", "activity", "whr", "sbp", "dbp", "hr", "hdl", "ldl", "tg", "insulin", "hba1c"
]

# Function to validate numeric inputs
def validate_number(value, field_name):
    if value == 0:
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
        activity = st.slider("Aktywność fizyczna (min/tydzień)", 0, 1000, 300, key="activity")
        diet = st.slider("Wynik diety", 0, 10, 5, key="diet_score")
    with col_l2:
        alcohol = st.slider("Spożycie alkoholu tygodniowo", 0, 7, 0, key="alcohol_consumption_per_week")
        sleep = st.slider("Godziny snu dziennie", 0, 24, 8, key="sleep_hours_per_day")
    with col_l3:
        smoking_status = st.selectbox("Status palenia", ["Never", "Current", "Former"], key="smoking_status")
        screen = st.slider("Godziny przed ekranem dziennie", 0, 24, 4, key="screen_time_hours_per_day")

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
            validated = {}

            for field in NUMERIC_FIELDS:
                value = st.session_state.get(field, "")
                val, err = validate_number(value, field)
                if err:
                    errors.append(err)
                else:
                    validated[field] = val

            # Collecting all data, including sliders and checkboxes
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
            validated["waist_to_hip_ratio"] = whr
            validated["systolic_bp"] = sbp
            validated["diastolic_bp"] = dbp
            validated["heart_rate"] = hr
            validated["cholesterol_total"] = 239
            validated["hdl_cholesterol"] = hdl
            validated["ldl_cholesterol"] = ldl
            validated["triglycerides"] = tg
            validated["glucose_fasting"] = 136
            validated["glucose_postprandial"] = 236
            validated["insulin_level"] = insulin
            validated["diabetes_risk_score"] = score
            validated["diabetes_stage"] = 2
            validated["family_history_diabetes"] = ""
            validated["bmi"] = 30

            # Handle validation errors
            if errors:
                for e in errors:
                    st.error(e)
            else:
                input_data = pd.DataFrame([validated])

                # Load model and make prediction
                predictor = TabularPredictor.load('modelePPvsNPP/NPP')
                prediction = predictor.predict(input_data)
                st.session_state["show_result"] = True
                st.success(f"✅ Wynik: Cukrzyca {'obecna' if prediction[0] == 1 else 'nieobecna'} z prawdopodobieństwem **{prediction[0]}**.")

    with col_btn2:
        if st.button("🧹 Wyczyść dane"):
            reset_inputs()
            st.rerun()

    if st.session_state.get("show_result"):
        st.markdown("---")