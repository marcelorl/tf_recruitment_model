import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
import joblib
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import OneHotEncoder
from tensorflow import keras


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


def generate_model():
    # Carregar e preparar os dados
    data = pd.read_csv('recruitment_data.csv')
    X = data[['Age', 'ExperienceYears', 'InterviewScore',
              'SkillScore', 'PersonalityScore']]
    y = data['HiringDecision']

    # Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Normalizar os dados
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    joblib.dump(scaler, 'scaler.joblib')

    # Criar o modelo
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(5,)),
        tf.keras.layers.Dense(5, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compilar o modelo
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Treinar o modelo
    model.fit(X_train_scaled, y_train, epochs=50,
              batch_size=32, validation_split=0.2, verbose=0)

    # Salvar o modelo
    model.save('recruitment_model.h5')


def load_model():
    try:
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
    except Exception as e:
        logging.error(f"Erro ao carregar o modelo: {e}")
        raise HTTPException(
            status_code=500, detail="Erro interno do servidor ao carregar o modelo")


def predict_hiring(candidate: CandidateData):
    try:
        # Carregar o modelo
        model = load_model()

        # Preparar os dados do candidato
        candidate_dict = {
            'Age': [candidate.Age],
            'ExperienceYears': [candidate.ExperienceYears],
            'InterviewScore': [candidate.InterviewScore],
            'SkillScore': [candidate.SkillScore],
            'PersonalityScore': [candidate.PersonalityScore],
            'Name': [candidate.Name],
            'Gender': [candidate.Gender],
            'EducationLevel': [candidate.EducationLevel],
            'DistanceFromCompany': [candidate.DistanceFromCompany],
            'PreviousCompanies': [candidate.PreviousCompanies],
            'RecruitmentStrategy': [candidate.RecruitmentStrategy]
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

        # Converter para numpy array
        input_final_np = filtrado.to_numpy()

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
            'porcentagem': f"{percentage:.2f}%",
            'mensagem': message
        }

        return JSONResponse(content=response)
    except Exception as e:
        logging.error(f"Erro durante a predição: {e}")
        raise HTTPException(
            status_code=500, detail="Erro interno do servidor durante a predição")
