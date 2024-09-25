import streamlit as st
import requests
import json

from services import predict_hiring


def main():
    st.set_page_config(page_title="Decisão de Contratação", layout="centered")
    st.title("Decisão de Contratação")
    st.markdown("### Insira os dados do candidato abaixo")

    with st.form(key='candidate_form'):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Nome do Candidato", max_chars=100)
            age = st.number_input("Idade", min_value=18, max_value=100, step=1)
            gender = st.selectbox(
                "Sexo", options=["Selecione...", "Masculino", "Feminino"])
            education_level = st.selectbox("Nível Educacional", options=[
                "Selecione...", "Ensino Médio", "Graduação", "Mestrado", "Doutorado"])
            experience_years = st.number_input(
                "Experiência (anos)", min_value=0, max_value=50, step=1)

        with col2:
            interview_score = st.slider(
                "Pontuação na Entrevista", min_value=0, max_value=100, step=1)
            skill_score = st.slider(
                "Pontuação nas Skills Técnicas", min_value=0, max_value=100, step=1)
            personality_score = st.slider(
                "Pontuação na Personalidade", min_value=0, max_value=100, step=1)
            recruitment_strategy = st.selectbox("Estratégia de Recrutamento", options=[
                "Selecione...", "Estratégia 1", "Estratégia 2", "Estratégia 3"])
            previous_companies = st.number_input(
                "Empresas Anteriores", min_value=0, max_value=20, step=1)
            distance_from_company = st.number_input(
                "Distância da Empresa (km)", min_value=0, max_value=1000, step=1)

        submit_button = st.form_submit_button(label='Devo contratar?')

    if submit_button:
        # Validate required fields
        if (not name or not gender or gender == "Selecione..." or
            not education_level or education_level == "Selecione..." or
                not recruitment_strategy or recruitment_strategy == "Selecione..."):
            st.error("Por favor, preencha todos os campos obrigatórios.")
        else:
            # Prepare data
            data = {
                "Name": name,
                "Age": age,
                "Gender": 0 if gender == "Masculino" else 1,
                "EducationLevel": {
                    "Ensino Médio": 1,
                    "Graduação": 2,
                    "Mestrado": 3,
                    "Doutorado": 4
                }.get(education_level, 0),
                "ExperienceYears": experience_years,
                "InterviewScore": interview_score,
                "SkillScore": skill_score,
                "PersonalityScore": personality_score,
                "RecruitmentStrategy": {
                    "Estratégia 1": 1,
                    "Estratégia 2": 2,
                    "Estratégia 3": 3
                }.get(recruitment_strategy, 0),
                "PreviousCompanies": previous_companies,
                "DistanceFromCompany": distance_from_company
            }

            # Call the prediction function
            result = predict_hiring(data)

            # Display the result
            st.markdown("---")
            st.subheader("Resultado da Análise")
            if result['contratar']:
                st.success(f"{result['mensagem']} ({result['porcentagem']}%)")
            else:
                st.error(f"{result['mensagem']} ({result['porcentagem']}%)")

            # Display candidate details
            st.markdown("### Detalhes do Candidato")
            st.json(data)


if __name__ == "__main__":
    main()
