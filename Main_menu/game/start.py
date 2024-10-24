import tkinter as tk
def game():
    def table():
        table = []
        for rows in range(8):
            table.append(
                ["B" if(rows + col) % 2 == 1 else "R" for col in range(8)]
            )
        return table
    def table_make(table):
        for rows in range(8):
            for col in range(8):
                color = "black" if table[rows][col] == "B" else "red"
                chart = tk.Canvas(window, width=60, height=60, bg=color)
                chart.grid(row=rows, column=col)
    window = tk.Tk()
    window.title("Damas")
    table_damas= table()
    table_make(table_damas)
    window.mainloop()
            