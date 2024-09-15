import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
import joblib

class CandidateData(BaseModel):
    age: int
    experience_years: int
    interview_score: int
    skill_score: int
    personality_score: int

def generate_model():
    # Carregar e preparar os dados
    data = pd.read_csv('recruitment_data.csv')
    X = data[['Age', 'ExperienceYears', 'InterviewScore', 'SkillScore', 'PersonalityScore']]
    y = data['HiringDecision']

    # Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Treinar o modelo
    model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=0)

    # Salvar o modelo
    model.save('recruitment_model.h5')
    
def predict_hiring(candidate: CandidateData):
    model = tf.keras.models.load_model('recruitment_model.h5')
    scaler = joblib.load('scaler.joblib')
    
    candidate_data = np.array([[
        candidate.age,
        candidate.experience_years,
        candidate.interview_score,
        candidate.skill_score,
        candidate.personality_score
    ]])
    
    # Normalizar os dados
    candidate_data_scaled = scaler.transform(candidate_data)
    
    # Fazer a previsão
    prediction = model.predict(candidate_data_scaled)
    
    hiring_probability = float(prediction[0][0])
    hiring_decision = "Likely to be hired" if hiring_probability > 0.5 else "Unlikely to be hired"
    
    return {
        "hiring_probability": hiring_probability,
        "hiring_decision": hiring_decision
    }