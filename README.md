# Veronica
Veronica, a closed-domain generative-based weather assistant using RASA, using both Rasa NLU( for nlu part ) and Rasa Core( for dialogue management part ). It gives current weather and can forecast tomorrow’s weather of a given location. On typos it also suggests correct names using fuzzy matching and can handle name ambiguity if in case more than places with same exists. It will be soon integrated with telegram.

### nlu model: 
    train nlu:
        rasa train nlu
    test nlu:
        rasa shell nlu

### dialogue/core model:
    start custom action server:
        rasa run actions
    train core in new terminal:
        rasa train --out models --fixed-model-name rasa_models

### run chatbot:
    rasa shell

### run interative training:
    start custom action server:
        rasa run actions
    start interactive training in new terminal:
        rasa interactive

### integrate with telegram:
    start custom action server:
        rasa run actions
    start ngrok in new terminal:
        ./ngrok http 5005
        change webhook_url in credentials.yml
    connect to telegram in new terminal:
        rasa run --port 5005 --credentials credentials.yml --endpoints endpoints.yml

### run using rasa x:
    start custom action server:
        rasa run actions
    start ngrok in new terminal:
        ./ngrok http 5002
    export RASA_X_HOSTNAME=https://{number you get after running ngrok}.ngrok.io; rasa x
