from Main_menu.register.register import register
from Main_menu.login.login import login, logged_player
from Main_menu.ranking.ranking import ranking_plays, ranking_wins
from Main_menu.game.start import game 
## ^Los import que necesitamos para el funcionamiento del programa.^

def print_menu(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "..", filename)
    with open(file_path, "r") as file:
        options = file.readlines()
    return [option.strip() for option in options]#Abrimos el archivo "r" = Reading, solo lectura ya que lo que necesitamos es leer el menu.

def menus():
    global logged_player
    menu = print_menu("menu.txt") #le doy el valor de menu al archivo que abrimos solo lectura.
    while True: # El programa se mantendra abierto hasta que se seleccione la opcion 0
        for option in menu:
            print(option) #Aqui se muestra el menu
        choice = input("Seleccione una opción: ")
        if choice == '1': # Inicio de sesion
            print("Iniciar sesión")
            login()
        elif choice == '2':  # Registro
            print("Registrarse")
            register()
        elif choice == '3': # Rankin
            print("Ranking")
            ranking_choice = input("Seleccione ranking (1: Victorias, 2: Partidas jugadas, 0: Volver): ") # Menu para ranking
            if ranking_choice == '1':
                print("Mostrar ranking de victorias") # Ranking de victorias
                ranking_wins()
            elif ranking_choice == '2':
                print("Mostrar ranking de partidas jugadas") # Ranking de partidas jugadas
                ranking_plays() 
            elif ranking_choice == '0': # Vuevo al menu
                continue
        elif choice == '4':
            # Aqui verificamos que hayan 2 jugadores logeados para comenzar a jugar.
            if len(logged_player) < 2: 
                print("Se necesitan 2 jugadores para iniciar el juego")
            else:
                print("Inicio de juego...") # Si lo hay, se inicia el juego. Have fun
                print(logged_player)
                game()
        elif choice == "5": # Deslogeo los jugadores, asi evitamos tener que cerrar el programa si otros players desea jugar
                logged_player = {}
                print("Sesion Cerrada.")
        elif choice == '0': # Cierro el programa
            print("Saliendo del programa.")
            break 
        else: # Al no ingresar una opcion valida da este mensaje.
            print("Opción no válida.")
