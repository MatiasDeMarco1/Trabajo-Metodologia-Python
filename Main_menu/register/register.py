import json
import os
import re

def register():
    USERS_FILE = os.path.join(os.path.dirname(__file__), '../../users.JSON')
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}
    username = input("Ingrese un nombre de usuario: ")
    username = username.lower()
    if username in users:
        print("El nombre de usuario ya existe. Intente con otro.")
        return
    while True:
        password = input("Ingrese una contraseña (al menos 7 caracteres, solo letras y números): ")
        if len(password) < 7 or not re.match('^[a-zA-Z0-9]+$', password):
            print("La contraseña no es válida. Debe tener al menos 7 caracteres y ser alfanumérica.")
            continue
        confirm_password = input("Confirme su contraseña: ")
        if password != confirm_password:
            print("Las contraseñas no coinciden. Intente de nuevo.")
            continue
        break
    users[username] = {
        'password': password,
        'partidas_ganadas': 0,
        'partidas_jugadas': 0
    }

    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)
    
    print(f"Usuario {username} registrado exitosamente.")