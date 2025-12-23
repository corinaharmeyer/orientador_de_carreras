import streamlit as st

from career_orientator.models import UserProfile
from career_orientator.recommender import recommend
from career_orientator.persistence import save_run

st.set_page_config(page_title="Orientador de Carreras", page_icon="🧭")
st.title("🧭 Orientador de Carreras")
st.caption("Recomendación explicable según intereses, habilidades y aptitudes.")

# Sugerencias (podés ampliar)
interest_options = [
    "datos","tecnologia","inteligencia_artificial","creatividad","producto",
    "arte","visualizacion","sistemas","investigacion","robotica","juegos"
]
skill_options = [
    "python","sql","ml","nlp","cv","analisis","visualizacion","testing","api",
    "prototipado","design","cloud","ci_cd"
]

col1, col2 = st.columns(2)

with col1:
    interests = st.multiselect("🎯 Intereses", interest_options)
    skills = st.multiselect("🛠️ Habilidades", skill_options)
    people_work = st.checkbox("🙂 Me gusta trabajar con personas")

with col2:
    math = st.slider("➗ Matemática", 1, 3, 2)
    communication = st.slider("🗣️ Comunicación", 1, 3, 2)
    creativity = st.slider("🎨 Creatividad", 1, 3, 2)
    teamwork = st.slider("🤝 Trabajo en equipo", 1, 3, 2)

top_k = st.slider("Top recomendaciones", 1, 10, 5)

if st.button("✨ Recomendar"):
    user = UserProfile(
        interests=interests,
        skills=skills,
        math=math,
        communication=communication,
        creativity=creativity,
        people_work=1 if people_work else 0,
        teamwork=teamwork,
    )

    recs = recommend(user, top_k=top_k)

    st.subheader("📌 Resultados")
    for r in recs:
        st.markdown(f"### {r.career}  —  `{r.score:.2f}`")
        if r.reasons:
            st.markdown("✅ **Por qué encaja**")
            for x in r.reasons:
                st.write("•", x)
        if r.cautions:
            st.markdown("⚠️ **A considerar**")
            for x in r.cautions:
                st.write("•", x)
        st.divider()

    path = save_run(user, recs)
    st.success(f"Guardado en: {path}")
