# GUI for guided mindfulness and exercises
# src/gui/mindfulness.py

import tkinter as tk

class Mindfulness:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Mindfulness Exercises")

        tk.Label(self.window, text="Guided Mindfulness Exercises Coming Soon!").pack()