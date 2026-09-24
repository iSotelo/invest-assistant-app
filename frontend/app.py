import streamlit as st

from api_client import validate_story
from export_utils import build_csv_report

INVEST_LABELS = {
    "independent": "Independent",
    "negotiable": "Negotiable",
    "valuable": "Valuable",
    "estimable": "Estimable",
    "small": "Small",
    "testable": "Testable",
}


def _semaforo(score: int) -> str:
    if score >= 4:
        return "🟢"
    if score >= 3:
        return "🟡"
    return "🔴"


st.set_page_config(page_title="Asistente de Validación INVEST", page_icon=":clipboard:", layout="centered")
st.title("Asistente de Validación INVEST - Equipo 3012F")

# --- Panel A: Entrada de datos ---
como = st.text_input("Como (Rol)")
quiero = st.text_input("Quiero (Acción)")
para = st.text_input("Para (Valor)")
project_context = st.text_area(
    "Contexto del proyecto (opcional)",
    help="Backlog relacionado, dependencias o contexto de negocio. Mejora la evaluación de Independent, Valuable, Estimable y Small.",
)

if st.button("Analizar Historia", type="primary"):
    story_text = f"Como {como} quiero {quiero} para {para}"

    with st.spinner("Analizando historia..."):
        try:
            result = validate_story(story_text, project_context or None)
        except Exception as exc:  # noqa: BLE001 - se muestra al usuario, no se re-lanza
            st.error(f"No se pudo completar el análisis: {exc}")
            result = None

    if result:
        st.session_state["last_result"] = result
        st.session_state["last_story_text"] = story_text

# --- Panel B: Puntuación y semáforos ---
result = st.session_state.get("last_result")
if result:
    if result.get("degraded"):
        st.warning(result.get("degraded_reason", "Resultado parcial: el servicio de IA no está disponible."))

    st.metric("Calificación General", f"{result['score']}%")

    invest_results = result.get("invest_results")
    if invest_results:
        st.subheader("Semáforos INVEST")
        cols = st.columns(6)
        for col, (key, label) in zip(cols, INVEST_LABELS.items()):
            criterio = invest_results.get(key)
            if criterio:
                col.metric(label, _semaforo(criterio["score"]))

    # --- Panel C: Retroalimentación y sugerencias ---
    nlp_issues = result.get("nlp_issues", {})
    if nlp_issues.get("errores_sintacticos") or nlp_issues.get("ambiguedades_detectadas"):
        st.subheader("Problemas Detectados")
        for error in nlp_issues.get("errores_sintacticos", []):
            st.write(f"⚠️ {error}")
        for palabra in nlp_issues.get("ambiguedades_detectadas", []):
            st.write(f"⚠️ Término ambiguo detectado: '{palabra}'")

    if invest_results:
        st.subheader("Recomendaciones de la IA")
        for key, label in INVEST_LABELS.items():
            criterio = invest_results.get(key)
            if criterio and criterio["score"] < 4:
                st.write(f"**{label}:** {criterio['justificacion']} — _Sugerencia: {criterio['sugerencia']}_")

        historia_mejorada = invest_results.get("historia_mejorada")
        if historia_mejorada:
            st.subheader("Historia Sugerida por la IA")
            st.code(historia_mejorada, language=None)

    # --- Exportación (HU-05) ---
    story_text = st.session_state.get("last_story_text", "")
    st.download_button(
        "Exportar reporte a CSV",
        data=build_csv_report(story_text, result),
        file_name="reporte_validacion_invest.csv",
        mime="text/csv",
    )
