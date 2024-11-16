import json
import os

# Diccionario para almacenar los jugadores logueados
logged_player = {}

def login():
    # Usa la variable global 'logged_player' para almacenar los jugadores logueados
    global logged_player

    # Verifica si ya hay 2 jugadores logueados, en cuyo caso no permite más
    if len(logged_player) >= 2:
        print("Ya hay 2 jugadores logueados.")
        return

    # Define la ruta al archivo de usuarios 'users.JSON'
    USERS_FILE = os.path.join(os.path.dirname(__file__), '../../users.JSON')

    # Verifica si el archivo de usuarios existe
    if os.path.exists(USERS_FILE):
        # Abre el archivo de usuarios en modo lectura
        with open(USERS_FILE, 'r') as file:
            try:
                # Intenta cargar los datos de usuarios en formato JSON
                users = json.load(file)
            except json.JSONDecodeError:
                # Si ocurre un error al leer el JSON, muestra un mensaje de error
                print("Error al leer el archivo de usuarios.")
                return
    else:
        # Si el archivo no existe, muestra un mensaje de error
        print("El archivo de usuarios no existe.")
        return

    # Solicita al usuario que ingrese su nombre de usuario y contraseña
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    correct = False  # Bandera para verificar si el login es correcto

    # Bucle para intentar el login mientras no sea exitoso y el usuario no ingrese "0"
    while correct == False and username != "0":        
        # Busca al usuario en el diccionario, ignorando mayúsculas/minúsculas
        user = users.get(username.lower())
        # Verifica si el usuario existe y si la contraseña es correcta
        if user and user['password'] == password:
            # Si no hay 'player 1' logueado, asigna al usuario como 'player 1'
            if 'player 1' not in logged_player:
                logged_player['player 1'] = username
                print(f"{username} ha sido logueado como player 1.")
                correct = True
            # Si no hay 'player 2' logueado, asigna al usuario como 'player 2'
            elif 'player 2' not in logged_player:
                logged_player['player 2'] = username
                print(f"{username} ha sido logueado como player 2.")
                correct = True
        else:
            # Si el nombre de usuario o la contraseña no son correctos, muestra un mensaje de error
            print("Nombre de usuario o contraseña incorrectos.")
            # Solicita de nuevo el nombre de usuario o permite salir ingresando "0"
            username = input("Ingrese su nombre de usuario o 0 para salir: ")
            password = input("Ingrese su contraseña: ")

    # Si hay 2 jugadores logueados, muestra un mensaje indicando que están listos
    if len(logged_player) == 2:
        print("Ambos jugadores están listos para comenzar el juego.")
