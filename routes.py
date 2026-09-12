import tkinter as tk

from map import Map

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 480

root = tk.Tk()
root.title("Hex Map")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()

max = Map(canvas)

root.mainloop()
