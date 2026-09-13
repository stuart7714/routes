import math
import tkinter as tk

from enum import Enum

HEX_SIZE = 30


# A hex can be in a number of states
class HexState(Enum):
    EMPTY = 1,  # The hex contains nothing
    BARRIER = 2,  # The hex is a barrier and a route cannot pass through
    START = 3,  # The hex is a start location for a route
    END = 4  # The hex is an end location for a route


# A hexagon with a pointed top located at an axial coordinate
# The user can interact with the hex to add barriers and to find a route
class Hex:
    # Create the hex
    def __init__(self, canvas, axial_coord, on_start, on_end, on_clear, on_debug, on_barrier):
        self.canvas = canvas
        self.axial_coord = axial_coord
        self.on_start = on_start
        self.on_end = on_end
        self.on_clear = on_clear
        self.on_debug = on_debug
        self.on_barrier = on_barrier
        self.cartesian_coord = self.axial_to_cartesian()
        q, r = axial_coord
        self.tag = f"hex_{q}_{r}"
        self.create_polygon()
        self.create_text()
        self.create_events()
        self.set_state(HexState.EMPTY)

    # Colour the hex according to the state of the hex
    def set_colour_from_state(self):
        match self.state:
            case HexState.EMPTY:
                self.canvas.itemconfig(self.polygon, fill="lightgreen")
            case HexState.BARRIER:
                self.canvas.itemconfig(self.polygon, fill="darkgreen")
            case HexState.START:
                self.canvas.itemconfig(self.polygon, fill="yellow")
            case HexState.END:
                self.canvas.itemconfig(self.polygon, fill="red")

    # Set the state of the hex
    def set_state(self, state):
        self.state = state
        self.set_colour_from_state()

    # Convert the axial coordinate to a Cartesian coordinate
    def axial_to_cartesian(self):
        q, r = self.axial_coord
        x = HEX_SIZE * math.sqrt(3) * (q + r / 2) + \
            int(self.canvas["width"]) / 2
        y = HEX_SIZE * 3 / 2 * r + int(self.canvas["height"]) / 2
        return (x, y)

    # Find the six vertices of the hex
    def hex_points(self):
        x, y = self.cartesian_coord
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            vx = x + HEX_SIZE * math.cos(angle)
            vy = y + HEX_SIZE * math.sin(angle)
            points.extend((vx, vy))
        return points

    # Create a polygon to allow the hex to the drawn
    def create_polygon(self):
        self.polygon = self.canvas.create_polygon(
            self.hex_points(),
            outline="black",
            tags=self.tag
        )

    # Create a text overlay for the hex
    def create_text(self):
        x, y = self.cartesian_coord
        self.text = self.canvas.create_text(
            x, y, tags=self.tag, state="hidden")

    # Set the text to be shown on the overlay
    def set_text(self, text):
        self.canvas.itemconfig(self.text, text=text)

    # Set whether to show the text overlay
    def show_text(self, show_text):
        if show_text:
            self.canvas.itemconfig(self.text, state="normal")
        else:
            self.canvas.itemconfig(self.text, state="hidden")

    # The user has clicked on a hex
    def on_clicked(self, event):
        if self.state == HexState.EMPTY:
            self.set_state(HexState.BARRIER)
            self.on_barrier()
        elif self.state == HexState.BARRIER:
            self.set_state(HexState.EMPTY)
            self.on_barrier()

    # The user has right clicked on a hex so show a context menu
    def on_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=False)
        menu.add_command(label="Start", command=lambda: self.on_start(self))
        menu.add_command(label="End", command=lambda: self.on_end(self))
        menu.add_command(label="Clear", command=lambda: self.on_clear(self))
        menu.add_command(label="Debug", command=lambda: self.on_debug())
        menu.tk_popup(event.x_root, event.y_root)

    # The user can click on a hex to add or remove a barrier
    # The user can right click on a hex to set or clear start and end hexes
    def create_events(self):
        self.canvas.tag_bind(self.tag, "<Button-1>", self.on_clicked)
        self.canvas.tag_bind(self.tag, "<Button-3>", self.on_menu)
