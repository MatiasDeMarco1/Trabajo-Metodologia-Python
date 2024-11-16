import json
import os

def users():
    USERS_FILE = os.path.join(os.path.dirname(__file__), '../../users.JSON')
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
        return users #Se abre r el archivo users, solo necesitamos leer este archivo para ver los datos de los usuarios.
    else:
        print("No hay jugadores registrados.")
        return {} #Si no hay usuarios... para que continuar?

def ranking_wins():
    # Obtiene los datos de los usuarios llamando a la función 'users()'
    user_data = users() 
    # Si no hay datos de usuarios, la función termina.
    if not user_data:
        return
    # Ordena los usuarios por la cantidad de partidas ganadas en orden descendente
    user_order = sorted(user_data.items(), key=lambda item: item[1]['partidas_ganadas'], reverse=True)
    # Imprime el título del ranking
    print("Ranking de partidas ganadas:")
    # Itera sobre la lista de usuarios ordenados, asignando la posición y descomponiendo en 'username' y 'data'
    for position, (username, data) in enumerate(user_order, start=1):
        # Imprime la posición, nombre de usuario y partidas ganadas
        print(f"{position} - {username} - {data['partidas_ganadas']}") 

def ranking_plays():
    # Obtiene los datos de los usuarios llamando a la función 'users()'
    user_data = users()
    # Si no hay datos de usuarios, la función termina.
    if not user_data:
        return
    # Ordena los usuarios por la cantidad de partidas jugadas en orden descendente
    user_order = sorted(user_data.items(), key=lambda item: item[1]['partidas_jugadas'], reverse=True)
    # Imprime el título del ranking
    print("Ranking de partidas jugadas:")
    # Itera sobre la lista de usuarios ordenados, asignando la posición y descomponiendo en 'username' y 'data'
    for position, (username, data) in enumerate(user_order, start=1):
        # Imprime la posición, nombre de usuario y partidas jugadas
        print(f"{position} - {username} - {data['partidas_jugadas']}")
