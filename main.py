import os
from flask import Flask, request
from json import dump, load
from json.decoder import JSONDecodeError

app=Flask(__name__)

@app.get('/user')
def get_database():
    file = os.environ['DIRECTORY'] + 'database.json'
    list = {'data': []}
    try:
        with open(file + 'database.json', 'r') as json_file:
            dados = load(json_file)
        if(len(dados) == 0):
            with open (file + 'database.json', 'w') as json_file:
                dump(list, json_file)
        with open(file + 'database.json', 'r') as json_file:
            dados = load(json_file)
            return dados, 200
    except FileNotFoundError:
        with open (file + 'database.json', 'w') as json_file:
                dump(list, json_file)
        with open(file + 'database.json', 'r') as json_file:
            dados = load(json_file)
            return dados, 200

@app.post('/user')
def post_database():
    file = os.environ['DIRECTORY'] + 'database.json'
    data = request.get_json()
    list = {'data': []}
    try:
        name = data.get("name")
        email = data.get("email") 
        with open(file + 'database.json', 'r') as json_file:
            dados = load(json_file)
            for dado in dados['data']:
                if(dado['email'] == email.lower()):
                    return {'message': 'Email already exists'}, 409
        with open(file + 'database.json', 'w') as json_file:
            newData = {'id': len(dados['data']), 'name': name.capitalize(), 'email': email.lower()}
            dados['data'].append(newData)
            dump(dados, json_file)
        with open(file + 'database.json', 'r') as json_file:
            dados = load(json_file)
            return dados, 201
    except FileNotFoundError:
        with open (file + 'database.json', 'w') as json_file:
            dump(list, json_file)
        with open('database.json', 'r') as json_file:
            dados = load(json_file)
        with open(file + 'database.json', 'w') as json_file:
            newData = {'id': len(dados['data']), 'name': name.capitalize(), 'email': email.lower()}
            dados['data'].append(newData)
            dump(dados, json_file)
        with open(file + 'database.json', 'r') as json_file:
            dados = load(json_file)
            return dados, 201
    except JSONDecodeError:
        return {"wrong fields": [{"nome": type(data['name']).__name__},{"email": type(data['email']).__name__}]}, 400