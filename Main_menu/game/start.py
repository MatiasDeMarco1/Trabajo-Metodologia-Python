import tkinter as tk

class Piece:
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king  

    def promote_to_king(self):
        self.is_king = True  

def game():
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
                move_piece(row, col)
                turn = "white" if turn == "red" else "red"  # Cambiar turno solo si el movimiento es válido
                selected_piece = None
                selected_coords = None
                remove_highlight() 
            else:
                remove_highlight()
                selected_piece = None 
                highlight_valid_moves() 

    def highlight_piece(row, col):
        canvas = canvases[(row, col)]
        # Cambiar el tag para incluir reyes
        piece_tag = (
            "red_king" if selected_piece.color == "red" and selected_piece.is_king else
            "white_king" if selected_piece.color == "white" and selected_piece.is_king else
            "red_piece" if selected_piece.color == "red" else "white_piece"
        )
        print(piece_tag)  # Para verificar el tag correcto
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
                # Eliminar el resaltado de las piezas rojas y blancas, tanto normales como reyes
                canvases[(r, c)].itemconfig("red_piece", outline="")
                canvases[(r, c)].itemconfig("white_piece", outline="")
                canvases[(r, c)].itemconfig("red_king", outline="")
                canvases[(r, c)].itemconfig("white_king", outline="")
                canvases[(r, c)].delete("valid_move")

    def is_valid_move(row, col):
        if (row + col) % 2 == 1:  # Verifica que la casilla de destino sea válida
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
                        if (canvases[(current_row, current_col)].find_withtag("white_piece") or canvases[(current_row, current_col)].find_withtag("white_king") ) and turn == "red":
                            capture_found = True  
                        elif (canvases[(current_row, current_col)].find_withtag("red_piece") or canvases[(current_row, current_col)].find_withtag("red_piece")) and turn == "white":
                            capture_found = True  
                        elif piece_present and current_row == row and current_col == col:
                            return False  

                        if capture_found:
                            next_row = current_row + d_row
                            next_col = current_col + d_col
                            if 0 <= next_row < 8 and 0 <= next_col < 8 and (next_row + next_col) % 2 == 1:
                                if not ( canvases[(next_row, next_col)].find_withtag("red_piece") or canvases[(next_row, next_col)].find_withtag("red_king")  ) and \
                                not (canvases[(next_row, next_col)].find_withtag("white_piece") or canvases[(next_row, next_col)].find_withtag("white_king")):
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
                elif abs(old_row - row) == 2 and abs(old_col - col) == 2:  # Movimiento de captura
                    mid_row = (old_row + row) // 2
                    mid_col = (old_col + col) // 2
                    if canvases[(mid_row, mid_col)].find_withtag("white_piece") or canvases[(mid_row, mid_col)].find_withtag("white_king") :
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

        # Determina el tag de la pieza a eliminar
        piece_tag = "red_king" if piece_color == "red" and selected_piece.is_king else \
                    "white_king" if piece_color == "white" and selected_piece.is_king else \
                    "red_piece" if piece_color == "red" else "white_piece"
        
        # Eliminar la pieza de la posición anterior
        canvases[(old_row, old_col)].delete(piece_tag)
        board[old_row][old_col] = None  

        capture_found = False

        # Verificar captura para el rey
        if selected_piece.is_king:
            for d_row, d_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                current_row, current_col = old_row, old_col
                while True:
                    current_row += d_row
                    current_col += d_col

                    # Verifica límites
                    if not (0 <= current_row < 8 and 0 <= current_col < 8):
                        break

                    # Verifica captura de piezas
                    if (canvases[(current_row, current_col)].find_withtag("white_piece") and piece_color == "red") or \
                    (canvases[(current_row, current_col)].find_withtag("red_piece") and piece_color == "white") or \
                    (canvases[(current_row, current_col)].find_withtag("white_king") and piece_color == "red") or \
                    (canvases[(current_row, current_col)].find_withtag("red_king") and piece_color == "white"):
                        # Verifica si hay una casilla vacía después de la pieza capturada
                        next_row = current_row + d_row
                        next_col = current_col + d_col
                        if 0 <= next_row < 8 and 0 <= next_col < 8 and (next_row + next_col) % 2 == 1:
                            if not (canvases[(next_row, next_col)].find_withtag("red_piece") or 
                                    canvases[(next_row, next_col)].find_withtag("white_piece")):
                                # Captura la pieza
                                if piece_color == "red":
                                    if canvases[(current_row, current_col)].find_withtag("white_piece"):
                                        canvases[(current_row, current_col)].delete("white_piece")
                                    if canvases[(current_row, current_col)].find_withtag("white_king"):
                                        canvases[(current_row, current_col)].delete("white_king")
                                else:
                                    if canvases[(current_row, current_col)].find_withtag("red_piece"):
                                        canvases[(current_row, current_col)].delete("red_piece")
                                    if canvases[(current_row, current_col)].find_withtag("red_king"):
                                        canvases[(current_row, current_col)].delete("red_king")
                                
                                capture_found = True
                                break

                    # Si se llega a la posición de destino
                    if (current_row, current_col) == (row, col):
                        break

            # Si se capturó una pieza, redibuja el rey en la nueva posición
            if capture_found:
                board[row][col] = selected_piece  
                canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                                tags="red_king" if piece_color == "red" else "white_king")
                canvases[(row, col)].create_text(30, 30, text="K", fill="black", font=("Arial", 20, "bold"))
            else:
                # Verifica si se puede mover sin capturar
                if not (canvases[(row, col)].find_withtag("red_piece") or 
                        canvases[(row, col)].find_withtag("white_piece") or 
                        canvases[(row, col)].find_withtag("red_king") or 
                        canvases[(row, col)].find_withtag("white_king")):
                    # Redibuja el rey en la nueva posición
                    board[row][col] = selected_piece  
                    canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                                    tags="red_king" if piece_color == "red" else "white_king")
                    canvases[(row, col)].create_text(30, 30, text="K", fill="black", font=("Arial", 20, "bold"))
        else:
            # Captura para piezas comunes
            if abs(old_row - row) == 2:  # Solo puede capturar si se mueve 2 casillas
                mid_row = (old_row + row) // 2
                mid_col = (old_col + col) // 2
                if piece_color == "red":
                    if canvases[(mid_row, mid_col)].find_withtag("white_piece"):
                        canvases[(mid_row, mid_col)].delete("white_piece")
                        board[mid_row][mid_col] = None
                    if canvases[(mid_row, mid_col)].find_withtag("white_king"):
                        canvases[(mid_row, mid_col)].delete("white_king")
                        board[mid_row][mid_col] = None
                else:
                    if canvases[(mid_row, mid_col)].find_withtag("red_piece"):
                        canvases[(mid_row, mid_col)].delete("red_piece")
                        board[mid_row][mid_col] = None
                    if canvases[(mid_row, mid_col)].find_withtag("red_king"):
                        canvases[(mid_row, mid_col)].delete("red_king")
                        board[mid_row][mid_col] = None 

            # Redibuja la pieza común
            board[row][col] = selected_piece
            canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                            tags="red_piece" if piece_color == "red" else "white_piece")

        if (piece_color == "red" and row == 7) or (piece_color == "white" and row == 0):
            canvases[(row, col)].delete("red_piece" if piece_color == "red" else "white_piece")

            selected_piece.promote_to_king()
            canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="", 
                                            tags="red_king" if piece_color == "red" else "white_king")
            canvases[(row, col)].create_text(30, 30, text="K", fill="black", font=("Arial", 20, "bold"))

        board[row][col] = selected_piece

    window = tk.Tk()
    window.title("Damas")
    selected_piece = None
    selected_coords = None
    turn = "red"
    canvases = {}
    board = create_board()
    draw_board(board)
    window.mainloop()

game()