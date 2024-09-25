import pandas as pd
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import OneHotEncoder
from tensorflow import keras
from normalization import normalization_


class CandidateData(BaseModel):
    Age: int
    ExperienceYears: int
    InterviewScore: int
    SkillScore: int
    PersonalityScore: int
    Name: str
    Gender: str
    EducationLevel: str
    DistanceFromCompany: int
    PreviousCompanies: int
    RecruitmentStrategy: str


def load_model():
    # Carregar a arquitetura do modelo do arquivo JSON
    with open('model.json', 'r') as json_file:
        loaded_model_json = json_file.read()

    custom_objects = {
        'Sequential': keras.Sequential,
        'Dense': keras.layers.Dense,
        'BatchNormalization': keras.layers.BatchNormalization
    }

    # Carregar o modelo com objetos personalizados
    model = model_from_json(
        loaded_model_json, custom_objects=custom_objects)

    # Carregar os pesos no modelo
    model.load_weights('weights.h5')

    # Compilar o modelo
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

    return model


def predict_hiring(candidate: CandidateData):
    # Carregar o modelo
    model = load_model()

    # Preparar os dados do candidato
    candidate_dict = {
        'Age': [candidate['Age']],
        'ExperienceYears': [candidate['ExperienceYears']],
        'InterviewScore': [candidate['InterviewScore']],
        'SkillScore': [candidate['SkillScore']],
        'PersonalityScore': [candidate['PersonalityScore']],
        'EducationLevel': [candidate['EducationLevel']],
        'RecruitmentStrategy': [candidate['RecruitmentStrategy']],
        'DistanceFromCompany': [candidate['DistanceFromCompany']],
        'PreviousCompanies': [candidate['PreviousCompanies']],
        'Gender': [candidate['Gender']],
        'Name': [candidate['Name']]
    }

    # Criar o DataFrame a partir do dicionário
    df_input = pd.DataFrame(candidate_dict)

    # Selecionar as features relevantes
    features = ['EducationLevel', 'ExperienceYears', 'InterviewScore',
                'SkillScore', 'PersonalityScore', 'RecruitmentStrategy']

    recrutamento = [[1, 2, 3]]

    filtrado = df_input[features]

    # One-hot encoding para a estratégia de recrutamento
    ohe = OneHotEncoder(categories=recrutamento, handle_unknown='ignore')
    ohe_df = pd.DataFrame(ohe.fit_transform(filtrado[['RecruitmentStrategy']]).toarray(
    ), columns=['RecruitmentStrategy_1', 'RecruitmentStrategy_2', 'RecruitmentStrategy_3'])
    df = filtrado.join(ohe_df)
    filtrado = df.drop(['RecruitmentStrategy'], axis=1)
    filtrado = filtrado.astype(float)

    input_final_np = normalization_(filtrado.to_numpy())

    # Fazer a predição com o modelo carregado
    out = model.predict(input_final_np)

    # Calcular a porcentagem
    percentage = float(out[0][0]) * 100

    # Determinar a mensagem baseada na porcentagem
    if percentage >= 80:
        message = "O candidato deve ser contratado."
    else:
        message = "O candidato não deve ser contratado."

    # Preparar a resposta
    response = {
        'contratar': percentage >= 80,
        'porcentagem': f"{percentage:.2f}",
        'mensagem': message
    }

    return response
