import logging
import tkinter as tk
from tkinter import ttk
from constants import Constants
from gui.widgets import (
    create_combobox, 
    create_person_entry_fields, 
    layout_widgets_in_grid,
)


log = logging.getLogger('app.sections')


def create_manor_selector(parent: tk.Widget, manor_options: list[str]) -> tk.StringVar:
    """Creates the manor selection UI and returns the associated StringVar."""
    log.debug("Creating manor selector.")
    frame = ttk.Frame(parent)
    frame.pack(side="top", fill="x", padx=10, pady=5)
    ttk.Label(frame, text="Manor:").pack(side="left", padx=(0, 5))
    manor_var = tk.StringVar()
    manor_combobox = create_combobox(frame, manor_var, manor_options, 15)
    manor_combobox.pack(side="left")
    return manor_var

def create_cq_team_section(parent: tk.Widget, roles: list[str]) -> dict:
    """Creates the entire CQ Team section UI."""
    log.debug("Creating CQ Team section.")
    frame = tk.LabelFrame(parent, text="CQ Team")
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    entries_dict = {}

    def create_single_person_role_ui(role: str):
        log.debug(f"Creating single person UI for role: {role}")
        role_frame = ttk.LabelFrame(frame, text=role)
        role_frame.pack(pady=5, padx=5, fill="x")
        person_entries = create_person_entry_fields(role_frame)
        entries_dict[role] = person_entries
        layout_widgets_in_grid(role_frame, person_entries)

    def create_multi_person_role_ui(role: str):
        log.debug(f"Creating multi-person UI for role: {role}")
        role_frame = ttk.LabelFrame(frame, text=role)
        role_frame.pack(pady=5, padx=5, fill="x")
        container = ttk.Frame(role_frame)
        container.pack(fill="x")
        entries_dict[role] = []

        def add_new_person_row():
            log.debug(f"Adding new person row for {role}.")
            row_frame = ttk.Frame(container)
            row_frame.pack(fill="x", pady=2)
            person_entries = create_person_entry_fields(row_frame)
            entries_dict[role].append(person_entries)
            layout_widgets_in_grid(row_frame, person_entries)

        add_button = ttk.Button(role_frame, text=f"Add {role.split()[-1]}", command=add_new_person_row)
        add_button.pack(side="left", padx=5, pady=(5, 0))
        add_new_person_row()

    for role in roles:
        if role == "CQ Runner":
            create_multi_person_role_ui(role)
        else:
            create_single_person_role_ui(role)
    return entries_dict

def create_dynamic_entry_section(parent: tk.Widget, title: str, widget_factory: callable, layout_function: callable, add_button_text: str) -> list:
    """Creates a section with a button to dynamically add new entry rows."""
    log.debug(f"Creating dynamic entry section: {title}")
    frame = tk.LabelFrame(parent, text=title, padx=10, pady=10)
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    container = ttk.Frame(frame)
    container.pack(fill="x")
    entries_list = []

    rows = 0
    
    def add_new_row():
        log.debug(f"Adding new row in {title} section.")
        nonlocal rows 
        rows += 1
        row_frame = ttk.Frame(container)
        row_frame.pack(fill="x", pady=2)
        entry_widgets = widget_factory(row_frame)
        entries_list.append(entry_widgets)
        layout_function(row_frame, entry_widgets)

    add_button = ttk.Button(frame, text=add_button_text, command=add_new_row)
    add_button.pack(side="left", padx=5, pady=(5, 0))
    
    def remove_last_row():
        nonlocal rows 
        if rows == 1:
            return
        if entries_list:
            rows -= 1
            log.debug(f"Removing last row in {title} section.")
            last_widgets = entries_list.pop()
            for widget in last_widgets.values():
                widget.master.destroy()
                
    remove_button = ttk.Button(frame, text="Remove Last", command=remove_last_row)
    remove_button.pack(side="left", padx=5, pady=(5, 0))
        
    add_new_row()
    return entries_list

def create_red_card_late_entry_widgets(parent: tk.Widget) -> dict:
    """Factory for widgets in a red card late entry row."""
    person_widgets = create_person_entry_fields(parent)
    other_widgets = {
        "Room": tk.Entry(parent, width=10),
        "Time": create_combobox(parent, tk.StringVar(parent), ['0900', '1200', '1500', '1800', '2100'], 7),
        "Type": create_combobox(parent, tk.StringVar(parent), Constants.redcard_late_types, 8),
        "Reason": tk.Entry(parent, width=20)
    }
    return {**person_widgets, **other_widgets}

def create_late_entry_widgets(parent: tk.Widget) -> dict:
    """Factory for widgets in a standard late entry row."""
    person_widgets = create_person_entry_fields(parent)
    type_var = tk.StringVar(parent, value='Late Turn-in')
    other_widgets = {
        "Room": tk.Entry(parent, width=10),
        "Time": create_combobox(parent, tk.StringVar(parent), ['0000', '2200'], 7),
        "Reason": tk.Entry(parent, width=20)
    }
    return {**person_widgets, **other_widgets}

def create_notes_section(parent: tk.Widget) -> tuple:
    """Creates the notes section UI."""
    log.debug("Creating notes section.")
    frame = tk.LabelFrame(parent, text="Notes", padx=10, pady=10)
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    frame.grid_columnconfigure(1, weight=1)

    cac_var = tk.BooleanVar()
    ttk.Checkbutton(frame, text="CAC Scanner Unavailable", variable=cac_var).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    ttk.Label(frame, text="On-Call MTL:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    mtl_var = tk.StringVar()
    create_combobox(frame, mtl_var, Constants.on_call_mtls, 25).grid(row=1, column=1, sticky="w", padx=5, pady=5)

    notes_container = ttk.Frame(frame)
    notes_container.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 0))
    notes_entries = []
    note_rows = 0
    
    def add_note_field():
        nonlocal note_rows
        note_rows += 1
        row = ttk.Frame(notes_container)
        row.pack(fill="x", expand=True, pady=2)
        ttk.Label(row, text="Note:").pack(side="left", padx=(0, 5))
        entry = ttk.Entry(row)
        entry.pack(side="left", fill="x", expand=True)
        notes_entries.append(entry)

    ttk.Button(frame, text="Add Note", command=add_note_field).grid(row=3, column=0, sticky="w", padx=5, pady=5)
    add_note_field()

    return cac_var, mtl_var, notes_entries

def create_signature_section(parent: tk.Widget) -> dict:
    """Creates the signature section UI."""
    log.debug("Creating signature section.")
    frame = tk.LabelFrame(parent, text="Signature", padx=10, pady=10)
    frame.pack(padx=10, pady=10, fill="both", expand="yes")

    widgets = {
        "Rank": create_combobox(frame, tk.StringVar(frame), Constants.rank_options, 12),
        "Last": tk.Entry(frame, width=15), "First": tk.Entry(frame, width=15), "MI": tk.Entry(frame, width=3),
        "Branch": create_combobox(frame, tk.StringVar(frame), Constants.branch_options, 7),
        "AFSC/Job": create_combobox(frame, tk.StringVar(frame), Constants.job_options, 25),
        "Squadron": create_combobox(frame, tk.StringVar(frame), Constants.squadron_options, 7),
    }

    layout_map = [("Rank", "Last", "First", "MI"), ("Branch", "AFSC/Job"), ("Squadron",)]
    for r, row_keys in enumerate(layout_map):
        col = 0
        for key in row_keys:
            ttk.Label(frame, text=f"{key}:").grid(row=r, column=col, sticky="w", padx=5, pady=2)
            col += 1
            colspan = 3 if key == "AFSC/Job" else 1
            widgets[key].grid(row=r, column=col, columnspan=colspan, sticky="ew", padx=5, pady=2)
            col += colspan
    return widgets
