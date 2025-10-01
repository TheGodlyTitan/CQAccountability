import logging
import tkinter as tk
from tkinter import ttk
from constants import Constants


log = logging.getLogger('app.widgets')


def create_combobox(parent: tk.Widget, variable: tk.StringVar, values: list[str], width: int) -> ttk.Combobox:
    """Generic factory for creating a readonly ttk.Combobox."""
    log.debug(f"Creating combobox in {parent.winfo_class()} with {len(values)} values.")
    
    # Automatic Blank Value Addition ---
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
    return {
        "Rank": create_combobox(parent, tk.StringVar(parent), Constants.rank_options, 12),
        "Last": tk.Entry(parent, width=15), 
        "First": tk.Entry(parent, width=15),
        "MI": tk.Entry(parent, width=3),
    }

def create_red_card_late_entry_widgets(parent: tk.Widget, bottom_parent: tk.Widget) -> dict:
    """Factory for widgets in a red card late entry row."""
    person_widgets = create_person_entry_fields(parent)
    other_widgets = {
        "Room": tk.Entry(parent, width=6),
        "Time": create_combobox(parent, tk.StringVar(parent), ['0900', '1200', '1500', '1800', '2100'], 5),
        "Type": create_combobox(parent, tk.StringVar(parent), Constants.redcard_late_types, 8),
    }
    
    reason_frame = ttk.Frame(bottom_parent)
    reason_frame.pack(fill='x', padx=5, pady=(0, 9))
    ttk.Label(reason_frame, text="Reason:", width=8).pack(side="left", padx=(0, 2))
    reason_entry = tk.Entry(reason_frame)
    reason_entry.pack(side="left", fill="x", expand=True)
    
    return {**person_widgets, **other_widgets, "Reason": reason_entry}

def create_late_entry_widgets(parent: tk.Widget, bottom_parent: tk.Widget) -> dict:
    """Factory for widgets in a standard late entry row."""
    person_widgets = create_person_entry_fields(parent)
    other_widgets = {
        "Room": tk.Entry(parent, width=6),
        "Time": create_combobox(parent, tk.StringVar(parent), ['0000', '2200'], 5),
    }

    reason_frame = ttk.Frame(bottom_parent)
    reason_frame.pack(fill='x', padx=5, pady=(0, 9))
    ttk.Label(reason_frame, text="Reason:", width=8).pack(side="left", padx=(0, 2))
    reason_entry = tk.Entry(reason_frame)
    reason_entry.pack(side="left", fill="x", expand=True)

    return {**person_widgets, **other_widgets, "Reason": reason_entry}

def layout_widgets_in_grid(parent: tk.Widget, widgets: dict[str, tk.Widget], custom_labels: dict = None):
    """Lays out labels and widgets in a grid format."""
    log.debug(f"Laying out {len(widgets)} widgets in grid for {parent.winfo_class()}.")
    if custom_labels is None:
        custom_labels = {}
    col = 0
    for key, widget in widgets.items():
        label_text = custom_labels.get(key, key)
        label = ttk.Label(parent, text=f"{label_text}:", width=8)
        label.grid(row=0, column=col, sticky="w", padx=(5, 1), pady=2)  # Reduced right padding from 2 to 1
        widget.grid(row=0, column=col + 1, sticky="ew", padx=(1, 5), pady=2)  # Reduced left padding from 2 to 1
        col += 2
