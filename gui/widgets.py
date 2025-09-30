import logging
import tkinter as tk
from tkinter import ttk
from constants import Constants


log = logging.getLogger('app.widgets')


def create_combobox(parent: tk.Widget, variable: tk.StringVar, values: list[str], width: int) -> ttk.Combobox:
    """Generic factory for creating a readonly ttk.Combobox."""
    log.debug(f"Creating combobox in {parent.winfo_class()} with {len(values)} values.")
    
    # Automatic Blank Value Addition
    new_values = list(values) 
    if not new_values or new_values[0] != '':
        new_values.insert(0, '')
    variable.set('')
    
    return ttk.Combobox(
        parent, 
        textvariable=variable, 
        values=new_values, 
        state="readonly", 
        width=width
    )


def create_person_entry_fields(parent: tk.Widget) -> dict[str, tk.Widget]:
    """Creates a standard set of widgets for entering a person's details."""
    log.debug(f"Creating person entry fields in {parent.winfo_class()}.")
    rank_var = tk.StringVar(parent)
    return {
        "Rank": create_combobox(parent, rank_var, Constants.rank_options, 12),
        "Last": tk.Entry(parent, width=20),
        "First": tk.Entry(parent, width=20),
        "MI": tk.Entry(parent, width=3)
    }


def layout_widgets_in_grid(parent: tk.Widget, widgets: dict[str, tk.Widget], custom_labels: dict = None):
    """Lays out labels and widgets in a grid format."""
    log.debug(f"Laying out {len(widgets)} widgets in grid for {parent.winfo_class()}.")
    if custom_labels is None:
        custom_labels = {}
    col = 0
    for key, widget in widgets.items():
        label_text = custom_labels.get(key, key)
        label = ttk.Label(parent, text=f"{label_text}:")
        label.grid(row=0, column=col, sticky="w", padx=(5, 2), pady=2)
        widget.grid(row=0, column=col + 1, sticky="ew", padx=(2, 5), pady=2)
        col += 2
