import streamlit as st
import numpy as np
import pickle

# Page config
st.set_page_config(page_title="Heart Disease Predictor", layout="wide")

# Load model
model = pickle.load(open('trained_model.sav','rb'))

# Title
st.markdown("<h1 style='text-align: center;'>❤️ Heart Disease Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter patient details to assess heart disease risk</p>", unsafe_allow_html=True)

st.divider()

# Sidebar info
st.sidebar.header("ℹ️ Instructions")
st.sidebar.write("Fill all patient details carefully and click **Check Risk**.")

# Layout (2 columns)
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Personal Details")
    age = st.slider("Age (years)", 20, 80, 40)
    
    gender = st.selectbox("Gender", ["Female", "Male"])
    sex = 1 if gender == "Male" else 0

    chest_pain = st.selectbox(
        "Chest Pain Type",
        ["No Pain", "Mild Pain", "Moderate Pain", "Severe Pain"]
    )
    cp = ["No Pain", "Mild Pain", "Moderate Pain", "Severe Pain"].index(chest_pain)

    exercise_pain = st.selectbox("Chest Pain During Exercise?", ["No", "Yes"])
    exang = 1 if exercise_pain == "Yes" else 0


with col2:
    st.subheader("🩺 Medical Details")
    bp = st.slider("Resting Blood Pressure (mm Hg)", 90, 200, 120)
    chol = st.slider("Cholesterol (mg/dl)", 100, 400, 200)

    sugar = st.selectbox("Fasting Blood Sugar > 120 mg/dl?", ["No", "Yes"])
    fbs = 1 if sugar == "Yes" else 0

    heart_rate = st.slider("Maximum Heart Rate", 70, 210, 150)

# More inputs (full width)
st.subheader("🔬 Advanced Health Metrics")

col3, col4, col5 = st.columns(3)

with col3:
    restecg = st.selectbox(
        "ECG Result",
        ["Normal", "Mild Abnormality", "Severe Abnormality"]
    )
    restecg = ["Normal", "Mild Abnormality", "Severe Abnormality"].index(restecg)

with col4:
    oldpeak = st.slider("ST Depression (Heart Stress Level)", 0.0, 6.0, 1.0)

with col5:
    slope = st.selectbox(
        "Slope of Exercise",
        ["Upsloping (Normal)", "Flat (Moderate Risk)", "Downsloping (High Risk)"]
    )
    slope = ["Upsloping (Normal)", "Flat (Moderate Risk)", "Downsloping (High Risk)"].index(slope)

col6, col7 = st.columns(2)

with col6:
    vessels = st.selectbox("Blocked Blood Vessels", [0,1,2,3,4])
    ca = vessels

with col7:
    thal = st.selectbox(
        "Blood Flow Condition",
        ["Normal", "Fixed Defect", "Reversible Defect", "Unknown"]
    )
    thal = ["Normal", "Fixed Defect", "Reversible Defect", "Unknown"].index(thal)

st.divider()

# Confirmation
confirm = st.checkbox("✅ I have reviewed all inputs")

# Button
if st.button("🔍 Check Heart Risk"):
    if not confirm:
        st.warning("⚠️ Please review and confirm your inputs before prediction.")
    else:
        input_data = np.array([[age, sex, cp, bp, chol, fbs,
                                restecg, heart_rate, exang,
                                oldpeak, slope, ca, thal]])

        prediction = model.predict(input_data)
        prob = model.predict_proba(input_data)[0][1]

        st.subheader("📊 Result")

        if prediction[0] == 1:
            st.error(f"⚠️ High Risk of Heart Disease\n\nRisk Probability: {prob:.2f}")
        else:
            st.success(f"✅ Low Risk of Heart Disease\n\nRisk Probability: {prob:.2f}")

st.markdown("---")
st.caption("⚠️ This tool is for educational purposes only and not a medical diagnosis.")