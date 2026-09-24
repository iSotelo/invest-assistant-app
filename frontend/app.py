import os

import streamlit as st

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.set_page_config(page_title="Asistente de Validación INVEST", page_icon=":clipboard:")
st.title("Asistente de Validación INVEST - Equipo 3012F")

como = st.text_input("Como (Rol)")
quiero = st.text_input("Quiero (Acción)")
para = st.text_input("Para (Valor)")

st.button("Analizar Historia", disabled=True, help="Disponible al completar HU-03 (orquestación backend)")
