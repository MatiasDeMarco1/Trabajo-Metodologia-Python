from Main_menu.register.register import register
from Main_menu.login.login import login
from Main_menu.ranking.ranking import ranking_plays,ranking_wins

def print_menu(filename):
    with open(filename, "r") as file:
        options = file.readlines()
    return [option.strip() for option in options]
        
def menus():
    menu = print_menu("menu.txt")
    while True:
        for option in menu:
            print(option)
        choice = input("Seleccione una opción: ")
        if choice == '1':
            print("Iniciar sesión")
            login()
        elif choice == '2':
            print("Registrarse")
            register()
        elif choice == '3':
            print("Ranking")
            ranking_choice = input("Seleccione ranking (1: Victorias, 2: Partidas jugadas, 0: Volver): ")
            if ranking_choice == '1':
                print("Mostrar ranking de victorias")
                ranking_wins()
            elif ranking_choice == '2':
                print("Mostrar ranking de partidas jugadas")
                ranking_plays()
            elif ranking_choice == '0':
                continue
        elif choice == '4':
            print("Inicio de juego...")
        elif choice == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")