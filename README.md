# Trabajo Practico Metodologia de la Programación - Damas
**En este trabajo realizaremos el famoso juego de Damas, el cual se podra jugar de a 2 usuarios.
Se podran crear usuarios y estos podran jugar el uno contra el otro.
Las victorias de cada usuario se acumularan y se podra visualizar en un ranking global.**

## ¿Que es nuestro programa?
Nuestro programa tiene la finalidad de entretenimiento en base a un juego de 2 jugadores.
Es un juego dinanimico y de estrategia que tiene como objetivo dejar sin fichas en el tablero a nuestro rival

## ¿Que nos motivo? 
Nos son de interes los juegos antiguos de estrategia y como poder desarrollar esos juegos de mesa en un programa utilizando Python.
Tambien representa un gran desafío para nosotros realizar este programa.

## Participantes:
- Melgratti Juan Bautista
- De Marco Matías

##  Modulos:
-  Registro: Se le pedira al usuario registrarse con su nombre o un alias, que este no este ya registrado, su contraseña y la confirmación de esta misma. Al crearse el usuario se le asignara como valor principal de victorias 0 y partidas jugadas 0
-  Inicio de sesión: Al usuario se le pedira su nombre o alias con el cual se registro, se validara que los datos ingresados sean correctos, es decir que el usuario exista y la contraseña corresponda a ese usuario.
-  Ranking de victorias: Se podra visualizar de mayor a menor los usuarios con mayor cantidad de victorias.
-  Ranking de partidas: Se podra visualizar de mayor a menor los usuarios con mayor cantidad de partidas jugadas, se tendra en cuanta "partidas jugadas" aquellas que se hayan finalizado.
-  Comienzo del juego: Al haber ingresado 2 usuarios para jugar, se podra comenzar la partida. Se visualizara un tablero con sus respectivas fichas y el modo de juego sera por turnos comenzando por el Player 1.
-  Fin del juego: Se contara como fin del juego cuando 1 de los jugadores se haya quedado sin fichas para mover, lo cual le dara la victoria al jugador que si tenga por lo menos 1 ficha en juego o algun jugador decida rendirse.
-  Archivo Users.JSON: Este archivo lo usaremos para almacenar los usuarios registrados con su nombre, contraseña, cantidad de victorias, cantidad de partidas jugadas.

## Menú

-  (1) Iniciar sesion: Se pedira que ingrese usuario y contraseña.
-  (2) Registrarse: Se podra registrar un nuevo usuario.
-  (3) Ranking: Se visualizara los ranking con todos sus jugadores, asi tambien como un "Top 10".
-  -  (1) Victorias: Se visualiza el ranking de victorias.
   -  (2) Partidas jugadas: Se visualiza el ranking de partidas.
   -  (0) Volver al menu principal: Vuelve al menu principal.
-  (4) Inicio de juego: Se comenzara el juego si y solo si hay 2 jugadores logeados para jugar.
-  (0) Exit: Finalizara el programa.  



