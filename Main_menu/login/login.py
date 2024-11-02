import json
import os

logged_player = {}

def login():
    global logged_player

    if len(logged_player) >= 2:
        print("Ya hay 2 jugadores logueados.")
        return

    USERS_FILE = os.path.join(os.path.dirname(__file__), '../../users.JSON')

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                print("Error al leer el archivo de usuarios.")
                return
    else:
        print("El archivo de usuarios no existe.")
        return

    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    correct = False
    while correct == False and username != "0":        
        user = users.get(username.lower())
        if user and user['password'] == password:
            if 'player 1' not in logged_player:
                logged_player['player 1'] = username
                print(f"{username} ha sido logueado como player 1.")
                correct = True
            elif 'player 2' not in logged_player:
                logged_player['player 2'] = username
                print(f"{username} ha sido logueado como player 2.")
                correct = True
        else:
            print("Nombre de usuario o contraseña incorrectos.")
            username = input("Ingrese su nombre de usuario o 0 para salir: ")
            password = input("Ingrese su contraseña: ")

    if len(logged_player) == 2:
        print("Ambos jugadores están listos para comenzar el juego.")