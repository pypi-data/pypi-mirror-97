from pyrustic.app import App
import tkinter as tk
from pyrustic.widget.scrollbox import Scrollbox


app = App(__package__)
app.view = lambda: Scrollbox(app.root)
app.start()
