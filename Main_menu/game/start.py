import tkinter as tk

def game():
    def table():
        return [["B" if (rows + col) % 2 == 1 else "R" for col in range(8)] for rows in range(8)]

    def table_make(table):
        for rows in range(8):
            for col in range(8):
                color = "black" if table[rows][col] == "B" else "red"
                chart = tk.Canvas(window, width=60, height=60, bg=color)
                chart.grid(row=rows, column=col)
                chart.bind("<Button-1>", lambda event, r=rows, c=col: on_click(event, r, c))
                canvases[(rows, col)] = chart
                
                if color == "black" and rows < 3:  
                    chart.create_oval(10, 10, 50, 50, fill="red", outline="red", tags="red_piece")
                elif color == "black" and rows > 4:  
                    chart.create_oval(10, 10, 50, 50, fill="white", outline="white", tags="white_piece")

    def on_click(event, row, col):
        nonlocal selected_piece, selected_coords

        if selected_piece is None:
            piece = canvases[(row, col)].find_withtag("red_piece") or canvases[(row, col)].find_withtag("white_piece")
            if piece:
                selected_piece = piece
                selected_coords = (row, col)
        else:
            if is_valid_move(row, col):
                move_piece(row, col)
                selected_piece = None
                selected_coords = None

    def is_valid_move(row, col):
        return (canvases[(row, col)].find_withtag("red_piece") == [] and 
                canvases[(row, col)].find_withtag("white_piec") == [])

    def move_piece(row, col):
        old_row, old_col = selected_coords
        piece_color = "red" if selected_piece[0] == "red_piece" else "white"
        canvases[(row, col)].create_oval(10, 10, 50, 50, fill=piece_color, outline="")
        canvases[(old_row, old_col)].delete(selected_piece[0]) 
    window = tk.Tk()
    window.title("Damas") 
    selected_piece = None
    selected_coords = None
    canvases = {}
    table_damas = table()
    table_make(table_damas)
    window.mainloop()