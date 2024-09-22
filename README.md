# Recruitment Model

## Installation

 - cp .env.example .env
 - Set your ngrok token
 - docker-compose up

## Usage

 - Check your http://localhost or ngrok generated url through the ngrok dashboard
 - Start by generating the model first with GET /generate
 - Then you must be able to predict with POST /predict, have a look at ./recruitment_data.postman_collection.json file.