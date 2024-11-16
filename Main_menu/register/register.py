import json
import os
import re

def register():
    USERS_FILE = os.path.join(os.path.dirname(__file__), '../../users.JSON') #Necesito abrir el archivo si existe, de manera "r", asi verifico la existencia de los users.
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
        # El nombre se guarda en minusculas y asi evitamos nombres "iguales" pero validos por las minusculas y mayusculas 
    while True:
        password = input("Ingrese una contraseña (al menos 7 caracteres, solo letras y números): ")
        if len(password) < 7 or not re.match('^[a-zA-Z0-9]+$', password):
            print("La contraseña no es válida. Debe tener al menos 7 caracteres y ser alfanumérica.")
            continue # Valido la contraseña, que esta cumpla con los requisitos.
        confirm_password = input("Confirme su contraseña: ") # Se pide confirmar la contraseña, dado que tiene que ser identica a la anterior, no verifico los requisitos, solo que sean iguales.
        if password != confirm_password:
            print("Las contraseñas no coinciden. Intente de nuevo.")
            continue # En caso negativo, se resetea el register.
        break
    users[username] = {
        'password': password,
        'partidas_ganadas': 0,
        'partidas_jugadas': 0
    } #Como guardamos el user.

    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4) #Carga del user al archivo users.json
    
    print(f"Usuario {username} registrado exitosamente.")
