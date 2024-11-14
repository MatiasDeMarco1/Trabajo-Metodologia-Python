import tkinter as tk
from tkinter import filedialog, messagebox
from Main_menu.login.login import logged_player
import json
import time
import random
import os
JSON_PATH = "users.json"
REPLAYS_FOLDER = "replays"
SAVES_FOLDER = "saves"

class Piece:
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king

    def promote_to_king(self):
        self.is_king = True


def game():
    def save_game(board, turn):
        game_data = {
            "board": [[piece.color if piece else None for piece in row] for row in board],
            "turn": turn,
            "player_1": logged_player["player 1"],
            "player_2": logged_player["player 2"],
        }

        save_path = os.path.join(SAVES_FOLDER, f"game_{logged_player["player 1"] + "" + logged_player["player 2"]}.json")

        with open(save_path, "w") as f:
            json.dump(game_data, f, indent=4)
        messagebox.showinfo("Guardar partida", "La partida ha sido guardada exitosamente.")

    def load_game(board, canvases):
        nonlocal turn
        file_path = filedialog.askopenfilename(initialdir=SAVES_FOLDER, title="Seleccionar partida guardada", filetypes=(("Archivos JSON", "*.json"),))
        if not file_path:
            return  
        with open(file_path, "r") as f:
            game_data = json.load(f)

        if game_data["player_1"] != logged_player["player 1"] or game_data["player_2"] != logged_player["player 2"]:
            logged_player["player 1"], logged_player["player 2"] = logged_player["player 2"], logged_player["player 1"]

        for row in range(8):
            for col in range(8):
                canvases[(row, col)].delete("all") 

        for row in range(8):
            for col in range(8):
                piece_color = game_data["board"][row][col]
                if piece_color:
                    piece = Piece(piece_color)
                    board[row][col] = piece
                    canvas = canvases[(row, col)]
                    piece_tag = f"{piece_color}_piece"
                    canvas.create_oval(10, 10, 50, 50, fill=piece_color, outline="", tags=piece_tag)
                    if piece.is_king:
                        canvas.create_text(30, 30, text="K", fill="black", font=("Arial", 20, "bold"))

        turn = game_data["turn"]
        messagebox.showinfo("Cargar partida", "La partida ha sido cargada exitosamente.")
        return turn

    def create_board():
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  
                    if row < 3: 
                        board[row][col] = Piece("red")
                    elif row > 4:  
                        board[row][col] = Piece("white")
        return board

    def draw_board(board):
        for row in range(8):
            for col in range(8):
                color = "black" if (row + col) % 2 == 1 else "red"
                canvas = tk.Canvas(window, width=60, height=60, bg=color)
                canvas.grid(row=row, column=col)
                canvas.bind("<Button-1>", lambda event, r=row, c=col: on_click(event, r, c))
                canvases[(row, col)] = canvas
                piece = board[row][col]
                if piece:
                    piece_color = "red" if piece.color == "red" else "white"
                    tag = "king_piece" if piece.is_king else ("red_piece" if piece.color == "red" else "white_piece")
                    oval_id = canvas.create_oval(10, 10, 50, 50, fill=piece_color, outline="", tags=tag)
                    if piece.is_king:  
                        canvas.create_text(30, 30, text="K", fill="black", font=("Arial", 20, "bold"))

    def on_click(event, row, col):
            nonlocal selected_piece, selected_coords, turn
            if selected_piece is None:
                piece = (
                    canvases[(row, col)].find_withtag("red_piece") or
                    canvases[(row, col)].find_withtag("red_king") if turn == "red" else
                    canvases[(row, col)].find_withtag("white_piece") or
                    canvases[(row, col)].find_withtag("white_king")
                )
                if piece:
                    selected_piece = board[row][col]
                    selected_coords = (row, col)
                    highlight_piece(row, col)
                    highlight_valid_moves()
            else:
                if is_valid_move(row, col):
                    capture_found = move_piece(row, col)
                    if not capture_found:
                        turn = "white" if turn == "red" else "red"
                    elif capture_found:
                        if not check_for_chain_capture(row, col):
                            turn = "white" if turn == "red" else "red"
                    selected_piece = None
                    selected_coords = None
                    remove_highlight()
                    check_game_over()
                else:
                    remove_highlight()
                    selected_piece = None
                    highlight_valid_moves()

    def check_for_chain_capture(row, col):
        piece_color = selected_piece.color
        captured_coords = None
        for d_row, d_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            current_row, current_col = row, col
            if not selected_piece.is_king:
                if piece_color == "red" and d_row < 0:  
                    continue
                elif piece_color == "white" and d_row > 0:  
                    continue
            while True:
                current_row += d_row
                current_col += d_col
                if not (0 <= current_row < 8 and 0 <= current_col < 8):
                    break
                opponent_piece_tag = "white_piece" if piece_color == "red" else "red_piece"
                opponent_king_tag = "white_king" if piece_color == "red" else "red_king"
                if (canvases[(current_row, current_col)].find_withtag(opponent_piece_tag) or 
                    canvases[(current_row, current_col)].find_withtag(opponent_king_tag)):
                    next_row = current_row + d_row
                    next_col = current_col + d_col
                    if 0 <= next_row < 8 and 0 <= next_col < 8 and (next_row + next_col) % 2 == 1:
                        if not (canvases[(next_row, next_col)].find_withtag("red_piece") or
                                canvases[(next_row, next_col)].find_withtag("white_piece") or
                                canvases[(next_row, next_col)].find_withtag("red_king") or
                                canvases[(next_row, next_col)].find_withtag("white_king")):
                            return True 
                        else:
                            break  
        return False
    def highlight_piece(row, col):
        canvas = canvases[(row, col)]
        piece_tag = (
            "red_king" if selected_piece.color == "red" and selected_piece.is_king else
            "white_king" if selected_piece.color == "white" and selected_piece.is_king else
            "red_piece" if selected_piece.color == "red" else "white_piece"
        )
        pieces = canvas.find_withtag(piece_tag)
        for piece in pieces:
            canvas.itemconfig(piece, outline="yellow", width=3)
    def highlight_valid_moves():
        if selected_piece: 
            old_row, old_col = selected_coords
            move_directions = [(1, 1), (1, -1)] if turn == "red" else [(-1, -1), (-1, 1)]
            if selected_piece.is_king:
                move_directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)] 
            for d_row, d_col in move_directions:
                new_row = old_row + d_row
                new_col = old_col + d_col
                while 0 <= new_row < 8 and 0 <= new_col < 8:  
                    if (new_row + new_col) % 2 == 1:
                        if is_valid_move(new_row, new_col) and not (canvases[(new_row, new_col)].find_withtag("red_piece") or canvases[(new_row, new_col)].find_withtag("white_piece")):
                            canvases[(new_row, new_col)].create_rectangle(0, 0, 60, 60, outline="gray", width=60, tags="valid_move")
                    else:
                        break 
                    new_row += d_row
                    new_col += d_col
    def remove_highlight():
        for r in range(8):
            for c in range(8):
                canvases[(r, c)].itemconfig("red_piece", outline="")
                canvases[(r, c)].itemconfig("white_piece", outline="")
                canvases[(r, c)].itemconfig("red_king", outline="")
                canvases[(r, c)].itemconfig("white_king", outline="")
                canvases[(r, c)].delete("valid_move")
    def is_valid_move(row, col):
        if (row + col) % 2 == 1:  
            old_row, old_col = selected_coords
            piece_present = canvases[(row, col)].find_withtag("red_piece") or canvases[(row, col)].find_withtag("white_piece") or canvases[(row, col)].find_withtag("red_king") or canvases[(row, col)].find_withtag("white_king")
            
            if selected_piece.is_king:
                for d_row, d_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    current_row, current_col = old_row, old_col
                    capture_found = False
                    while True:
                        current_row += d_row
                        current_col += d_col
                        if not (0 <= current_row < 8 and 0 <= current_col < 8):
                            break
                        if (canvases[(current_row, current_col)].find_withtag("white_piece") or canvases[(current_row, current_col)].find_withtag("white_king")) and turn == "red":
                            capture_found = True  
                        elif (canvases[(current_row, current_col)].find_withtag("red_piece") or canvases[(current_row, current_col)].find_withtag("red_king")) and turn == "white":
                            capture_found = True  
                        elif (canvases[(current_row, current_col)].find_withtag("white_piece") or canvases[(current_row, current_col)].find_withtag("white_king")) and turn == "white":
                            break  
                        elif (canvases[(current_row, current_col)].find_withtag("red_piece") or canvases[(current_row, current_col)].find_withtag("red_king")) and turn == "red":
                            break 
                        if (canvases[(current_row, current_col)].find_withtag("red_piece") == [] and canvases[(current_row, current_col)].find_withtag("white_piece") == [] and 
                            canvases[(current_row, current_col)].find_withtag("red_king") == [] and canvases[(current_row, current_col)].find_withtag("white_king") == []):
                            if capture_found:
                                next_row = current_row + d_row
                                next_col = current_col + d_col
                                if 0 <= next_row < 8 and 0 <= next_col < 8 and (next_row + next_col) % 2 == 1:
                                    if canvases[(next_row, next_col)].find_withtag("red_piece") == [] and canvases[(next_row, next_col)].find_withtag("white_piece") == [] and \
                                    canvases[(next_row, next_col)].find_withtag("red_king") == [] and canvases[(next_row, next_col)].find_withtag("white_king") == []:
                                        if (next_row, next_col) == (row, col):
                                            return True
                                break
                        elif (current_row, current_col) == (row, col):
                            return not piece_present 
            if turn == "red":
                if old_row >= row: 
                    return False
                if abs(old_row - row) == 1 and abs(old_col - col) == 1:
                    return not piece_present 
                elif abs(old_row - row) == 2 and abs(old_col - col) == 2:  
                    mid_row = (old_row + row) // 2
                    mid_col = (old_col + col) // 2
                    if canvases[(mid_row, mid_col)].find_withtag("white_piece") or canvases[(mid_row, mid_col)].find_withtag("white_king"):
                        return not piece_present
            else:
                if old_row <= row: 
                    return False
                if abs(old_row - row) == 1 and abs(old_col - col) == 1:
                    return not piece_present  
                elif abs(old_row - row) == 2 and abs(old_col - col) == 2:  
                    mid_row = (old_row + row) // 2
                    mid_col = (old_col + col) // 2
                    if canvases[(mid_row, mid_col)].find_withtag("red_piece") or canvases[(mid_row, mid_col)].find_withtag("red_king"):
                        return not piece_present
        return False
    def move_piece(row, col):
        old_row, old_col = selected_coords
        piece_color = selected_piece.color
        piece_tag = "red_king" if piece_color == "red" and selected_piece.is_king else \
                    "white_king" if piece_color == "white" and selected_piece.is_king else \
                    "red_piece" if piece_color == "red" else "white_piece"
        canvases[(old_row, old_col)].delete(piece_tag)
        board[old_row][old_col] = None
        capture_found = False  
        captured_coords = None
        if selected_piece.is_king:
            for d_row, d_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                current_row, current_col = old_row, old_col
                while True:
                    current_row += d_row
                    current_col += d_col
                    if not (0 <= current_row < 8 and 0 <= current_col < 8):
                        break
                    opponent_piece_tag = "white_piece" if piece_color == "red" else "red_piece"
                    opponent_king_tag = "white_king" if piece_color == "red" else "red_king"
                    if (canvases[(current_row, current_col)].find_withtag(opponent_piece_tag) or 
                        canvases[(current_row, current_col)].find_withtag(opponent_king_tag)):
                        next_row = current_row + d_row
                        next_col = current_col + d_col
                        if (next_row, next_col) == (row, col):
                            captured_coords = (current_row, current_col)
                            capture_found = True
                            break
                        else:
                            break  
                    if (current_row, current_col) == (row, col):
                        break  
            if captured_coords:
                captured_row, captured_col = captured_coords
                opponent_piece_tag = "white_piece" if piece_color == "red" else "red_piece"
                opponent_king_tag = "white_king" if piece_color == "red" else "red_king"
                canvases[(captured_row, captured_col)].delete(opponent_piece_tag)
                canvases[(captured_row, captured_col)].delete(opponent_king_tag)
                board[captured_row][captured_col] = None
            board[row][col] = selected_piece
            canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                            tags="red_king" if piece_color == "red" else "white_king")
            canvases[(row, col)].create_text(30, 30, text="K", fill="black", font=("Arial", 20, "bold"))
        else:
            if abs(old_row - row) == 2: 
                mid_row = (old_row + row) // 2
                mid_col = (old_col + col) // 2
                if piece_color == "red":
                    if canvases[(mid_row, mid_col)].find_withtag("white_piece") or canvases[(mid_row, mid_col)].find_withtag("white_king"):
                        canvases[(mid_row, mid_col)].delete("white_piece")
                        canvases[(mid_row, mid_col)].delete("white_king")
                        board[mid_row][mid_col] = None
                        capture_found = True  
                        captured_coords = (mid_row, mid_col)
                else:
                    if canvases[(mid_row, mid_col)].find_withtag("red_piece") or canvases[(mid_row, mid_col)].find_withtag("red_king"):
                        canvases[(mid_row, mid_col)].delete("red_piece")
                        canvases[(mid_row, mid_col)].delete("red_king")
                        board[mid_row][mid_col] = None
                        capture_found = True
                        captured_coords = (mid_row, mid_col)
                board[row][col] = selected_piece
                canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                                tags="red_piece" if piece_color == "red" else "white_piece")
                canvases[(old_row, old_col)].delete("red_piece" if piece_color == "red" else "white_piece")
            if not capture_found:
                board[row][col] = selected_piece
                canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                                tags="red_piece" if piece_color == "red" else "white_piece")
        if (piece_color == "red" and row == 7) or (piece_color == "white" and row == 0):
            canvases[(row, col)].delete("red_piece" if piece_color == "red" else "white_piece")
            selected_piece.promote_to_king()
            canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                            tags="red_king" if piece_color == "red" else "white_king")
            canvases[(row, col)].create_text(30, 30, text="K", fill="black", font=("Arial", 20, "bold"))
            capture_found = False
        if capture_found:
            if check_for_chain_capture(row, col):
                return True 
        return capture_found

    def check_game_over():
        red_count = sum(1 for row in board for piece in row if piece and piece.color == "red")
        white_count = sum(1 for row in board for piece in row if piece and piece.color == "white")
        if red_count == 0:
            winner = "player 2"
            loser = "player 1"
            messagebox.showinfo("Fin del juego", "¡Las blancas ganan!")
        elif white_count == 0:
            winner = "player 1"
            loser = "player 2"
            messagebox.showinfo("Fin del juego", "¡Las rojas ganan!")
        else:
            return
        player_winner = logged_player[winner]
        player_loser = logged_player[loser]

        with open(JSON_PATH, 'r') as file:
            users_data = json.load(file)
        users_data[player_winner]["partidas_ganadas"] += 1
        users_data[player_winner]["partidas_jugadas"] += 1
        users_data[player_loser]["partidas_jugadas"] += 1

        with open(JSON_PATH, 'w') as file:
            json.dump(users_data, file, indent=4)
        window.quit()

    window = tk.Tk()
    window.title("Damas")
    selected_piece = None
    selected_coords = None
    canvases = {}
    turn ="red" 
    board = create_board()
    draw_board(board)
    replay_button = tk.Button(window, text="Ver repeticiones")
    save_button = tk.Button(window, text="Guardar partida")
    load_button= tk.Button(window, text="Cargar partida")
    replay_button.grid(row=8, column=0, columnspan=2, sticky="ew")
    save_button = tk.Button(window, text="Guardar partida", command=lambda: save_game(board, turn))
    save_button.grid(row=8, column=2, columnspan=2, sticky="ew")
    load_button = tk.Button(window, text="Cargar partida", command=lambda: load_game(board, canvases))
    load_button.grid(row=8, column=4, columnspan=2, sticky="ew")
    window.mainloop()
