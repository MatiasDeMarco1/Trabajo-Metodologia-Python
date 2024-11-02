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
        return users
    else:
        print("No hay jugadores registrados.")
        return {}

def ranking_wins():
    user_data = users()
    if not user_data:
        return
    user_order = sorted(user_data.items(), key=lambda item: item[1]['partidas_ganadas'], reverse=True)
    print("Ranking de partidas ganadas:")
    for position, (username, data) in enumerate(user_order, start=1):
        print(f"{position} - {username} - {data['partidas_ganadas']}")

def ranking_plays():
    user_data = users()
    if not user_data:
        return
    user_order = sorted(user_data.items(), key=lambda item: item[1]['partidas_jugadas'], reverse=True)
    print("Ranking de partidas jugadas:")
    for position, (username, data) in enumerate(user_order, start=1):
        print(f"{position} - {username} - {data['partidas_jugadas']}")