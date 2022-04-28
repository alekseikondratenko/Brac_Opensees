import streamlit as st
import pandas as pd
import joblib
from PIL import Image

image = Image.open('brac.png')

beams = pd.read_excel('Sections.xlsx', sheet_name='IPE_S275')
cols = pd.read_excel('Sections.xlsx', sheet_name='HEA_S275')
bracings = pd.read_excel('Sections.xlsx', sheet_name='CHS_S235')

# Title
st.header("Prediction of lateral displacement in 2-storey steel braced frame")

# Dropdown input 1
listb = beams.iloc[:10,0].values
beams_sel = st.selectbox("Select beam's cross-section", listb)

# Dropdown input 2
listc = cols.iloc[:10,0].values
col_sel = st.selectbox("Select column's cross-section", listc)

# Dropdown input 3
listbr = bracings.iloc[:10,0].values
brac_sel = st.selectbox("Select bracing's cross-section", listbr)

# Dropdown input 4
loadlist = [10, 20, 30, 40, 50]
load_sel = st.selectbox("Select applied lateral load", loadlist)

if st.button("Predict the displacement"):
    # Unpickle classifier
    knn = joblib.load("knn.pkl")

    # Store inputs into dataframe
    X = pd.DataFrame([[beams_sel, col_sel, brac_sel, load_sel]],
                     columns=["Beam", "Column", "Bracing", "Load"])
    X = X.replace(beams.iloc[:10,0].values, beams.iloc[:10,12].values)
    X = X.replace(cols.iloc[:10,0].values, cols.iloc[:10,12].values)
    X = X.replace(bracings.iloc[:10, 0].values, bracings.iloc[:10, 6].values)

    # Get prediction
    prediction = knn.predict(X)[0]

    # Output prediction
    st.text(f"The lateral displacement is {prediction} m or {prediction*1000} mm")

st.image(image, caption='Loading scheme')
