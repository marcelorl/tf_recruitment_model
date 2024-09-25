import streamlit as st
import requests
import json

from services import predict_hiring


def main():
    st.set_page_config(page_title="Decisão de Contratação", layout="centered")
    st.title("Decisão de Contratação")
    st.markdown("### Insira os dados do candidato abaixo")

    with st.form(key='candidate_form'):
        name = st.text_input("Nome do Candidato", max_chars=100)
        age = st.number_input("Idade", min_value=0, max_value=100, step=1)
        gender = st.selectbox(
            "Sexo", options=["Selecione...", "Masculino", "Feminino"])
        education_level = st.selectbox("Nível Educacional", options=[
                                       "Selecione...", "Ensino Médio", "Graduação", "Mestrado", "Doutorado"])
        experience_years = st.number_input(
            "Experiência (anos)", min_value=0, max_value=100, step=1)
        interview_score = st.number_input(
            "Pontuação na Entrevista", min_value=0.0, max_value=100.0, step=0.01)
        skill_score = st.number_input(
            "Pontuação nas Skills Técnicas", min_value=0.0, max_value=100.0, step=0.01)
        personality_score = st.number_input(
            "Pontuação na Personalidade", min_value=0.0, max_value=100.0, step=0.01)
        recruitment_strategy = st.selectbox("Estratégia de Recrutamento", options=[
                                            "Selecione...", "Estratégia 1", "Estratégia 2", "Estratégia 3"])
        previous_companies = st.number_input(
            "Empresas Anteriores", min_value=0, max_value=100, step=1)
        distance_from_company = st.number_input(
            "Distância da Empresa (km)", min_value=0.0, max_value=1000.0, step=0.01)

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
            # st.write('====>', data)

            # Call the prediction function
            result = predict_hiring(data)

            # print(result)

            # Display the result
            if result['contratar']:
                st.success(f"{result['mensagem']} ({result['porcentagem']}%)")
            else:
                st.error(f"{result['mensagem']} ({result['porcentagem']}%)")


if __name__ == "__main__":
    main()
