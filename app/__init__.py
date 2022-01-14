import os
from flask import Flask, request
from json import dump, load
from json.decoder import JSONDecodeError

app=Flask(__name__)

def load_file(filename):
    with open(filename, 'r') as json_file:
        return load(json_file)

def edit_file(filename, edit):
    with open (filename, 'w') as json_file:
        dump(edit, json_file)

@app.get('/user')
def get_database():
    file = os.environ['DIRECTORY'] + 'database.json'
    list = {'data': []}
    try:
        dados = load_file(file)
        if(len(dados) == 0):
            edit_file(file, list)
        return load_file(file), 200
    except FileNotFoundError:
        edit_file(file, list)
        return load_file(file), 200

@app.post('/user')
def post_database():
    file = os.environ['DIRECTORY'] + 'database.json'
    data = request.get_json()
    list = {'data': []}
    try:
        name = data.get("name")
        email = data.get("email") 
        dados = load_file(file)
        for dado in dados['data']:
            if(dado['email'] == email.lower()):
                return {'message': 'Email already exists'}, 409
        new_data = {'id': len(dados['data']), 'name': name.capitalize(), 'email': email.lower()}
        dados['data'].append(new_data)
        edit_file(file, dados)
        return new_data, 201
    except FileNotFoundError:
        edit_file(file, list)
        dados = load_file(file)
        new_data = {'id': len(dados['data']), 'name': name.capitalize(), 'email': email.lower()}
        dados['data'].append(new_data)
        edit_file(file, dados)
        return new_data, 201
    except JSONDecodeError:
        return {"wrong fields": [{"nome": type(data['name']).__name__},{"email": type(data['email']).__name__}]}, 400
    except AttributeError:
        return {"wrong fields": [{"nome": type(data['name']).__name__},{"email": type(data['email']).__name__}]}, 400