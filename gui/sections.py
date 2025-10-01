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


def create_email_preview_section(parent: tk.Widget, check_email_callback=None) -> tuple[tk.Text, tk.Text]:
    """Creates the email preview section with a main text widget and a line number widget."""
    log.debug("Creating email preview section.")
    
    frame = tk.LabelFrame(parent, text="Email Preview", padx=10, pady=10)
    frame.pack(fill="both", expand=True)
    
    # Create a container for the text widgets and scrollbar
    text_container = ttk.Frame(frame)
    text_container.pack(fill="both", expand=True)
    text_container.grid_rowconfigure(0, weight=1)
    text_container.grid_columnconfigure(1, weight=1)

    # Line Numbers Widget
    line_numbers = tk.Text(
        text_container,
        width=3,  # Reduced width
        padx=3,   # Reduced horizontal padding
        pady=10,
        highlightthickness=0,
        bd=0,
        font=("Courier", 10),
        fg="grey",
        state="disabled",
        exportselection=0  # Prevent selection from being copied
    )
    line_numbers.grid(row=0, column=0, sticky="ns")

    # Make the line numbers unselectable
    line_numbers.bind("<Button-1>", lambda e: "break")
    line_numbers.bind("<B1-Motion>", lambda e: "break")
    line_numbers.bind("<Double-Button-1>", lambda e: "break")
    line_numbers.bind("<Triple-Button-1>", lambda e: "break")

    # Main Text Widget
    text_widget = tk.Text(
        text_container, 
        wrap="word", 
        padx=10, 
        pady=10,
        state="disabled",
        font=("Courier", 10),
        highlightthickness=0,
        bd=0
    )
    text_widget.grid(row=0, column=1, sticky="nsew")
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(text_container, orient="vertical")
    scrollbar.grid(row=0, column=2, sticky="ns")
    
    # Synchronize scrolling
    def sync_scroll(*args):
        line_numbers.yview_moveto(args[0])
        text_widget.yview_moveto(args[0])
        scrollbar.set(*args)

    text_widget.configure(yscrollcommand=sync_scroll)
    line_numbers.configure(yscrollcommand=sync_scroll) # Sync both ways
    scrollbar.configure(command=text_widget.yview)
    
    # Add button frame
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", pady=(10, 0))
    
    def copy_preview():
        content = text_widget.get("1.0", tk.END)
        parent.clipboard_clear()
        parent.clipboard_append(content)
        copy_button.config(text="Copied!")
        parent.after(2000, lambda: copy_button.config(text="Copy Email"))
    
    copy_button = ttk.Button(
        button_frame, 
        text="Copy Email", 
        command=copy_preview
    )
    copy_button.pack(side="left", padx=(0, 5))
    
    # Add Check Email button if callback is provided
    if check_email_callback:
        check_button = ttk.Button(
            button_frame,
            text="Check Email",
            command=check_email_callback
        )
        check_button.pack(side="left")
    
    return text_widget, line_numbers

def create_manor_section(parent: tk.Widget, manor_options: list[str]) -> tk.StringVar:
    """Creates the manor selection UI and returns the associated StringVar."""
    log.debug("Creating manor selector.")
    frame = ttk.Frame(parent)
    frame.pack(side="top", fill="x", padx=10, pady=5)
    ttk.Label(frame, text="Manor:").pack(side="left", padx=(0, 5))
    manor_var = tk.StringVar()
    manor_combobox = create_combobox(frame, manor_var, manor_options, 15)
    manor_combobox.pack(side="left")
    return manor_var

def create_airman_leaders_section(parent: tk.Widget, roles: list[str]) -> dict:
    """Creates the AL Team section UI."""
    log.debug("Creating AL Team section.")
    frame = tk.LabelFrame(parent, text="Airman Leaders")
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    entries_dict = {}

    for role in roles:
        log.debug(f"Creating single person UI for AL role: {role}")
        role_frame = ttk.LabelFrame(frame, text=role)
        role_frame.pack(pady=5, padx=5, fill="x")
        person_entries = create_person_entry_fields(role_frame)
        entries_dict[role] = person_entries
        layout_widgets_in_grid(role_frame, person_entries)

    return entries_dict

def create_charge_quarters_section(parent: tk.Widget, roles: list[str]) -> dict:
    """Creates the CQ Team section UI."""
    log.debug("Creating CQ Team section.")
    frame = tk.LabelFrame(parent, text="Charge of Quarters")
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    entries_dict = {}

    def create_single_person_role_ui(role: str):
        log.debug(f"Creating single person UI for CQ role: {role}")
        role_frame = ttk.LabelFrame(frame, text=role)
        role_frame.pack(pady=5, padx=5, fill="x")
        person_entries = create_person_entry_fields(role_frame)
        entries_dict[role] = person_entries
        layout_widgets_in_grid(role_frame, person_entries)

    def create_multi_person_role_ui(role: str):
        log.debug(f"Creating multi-person UI for CQ role: {role}")
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

        def remove_last_runner():
            if len(entries_dict[role]) <= 1:
                return  # Keep at least one runner
            if entries_dict[role]:
                log.debug(f"Removing last runner from {role}.")
                last_entries = entries_dict[role].pop()
                # Find one widget to get the parent frame from
                any_widget = next(iter(last_entries.values()))
                any_widget.master.destroy()

        button_frame = ttk.Frame(role_frame)
        button_frame.pack(fill="x", pady=(5, 5))  # Added 5px bottom padding

        add_button = ttk.Button(button_frame, text=f"Add {role.split()[-1]}", command=add_new_person_row)
        add_button.pack(side="left", padx=5)

        remove_button = ttk.Button(button_frame, text="Remove Runner", command=remove_last_runner)
        remove_button.pack(side="left", padx=5)

        add_new_person_row()  # Start with one runner

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
        row_frame = ttk.LabelFrame(container, text=f"Entry #{rows}")
        row_frame.pack(fill="x", pady=2, padx=5)
        
        # Create a sub-frame for the top row of widgets
        top_row_frame = ttk.Frame(row_frame)
        top_row_frame.pack(fill="x", expand=True)
        
        entry_widgets = widget_factory(top_row_frame, row_frame)
        entries_list.append(entry_widgets)
        
        # Layout only the widgets intended for the top row
        top_row_widgets = {k: v for k, v in entry_widgets.items() if k != "Reason"}
        layout_function(top_row_frame, top_row_widgets)

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
            # The master of the widgets is the LabelFrame for the row
            if last_widgets:
                # Find one widget to get the master from
                any_widget = next(iter(last_widgets.values()))
                any_widget.master.master.destroy()
                
    remove_button = ttk.Button(frame, text="Remove Last", command=remove_last_row)
    remove_button.pack(side="left", padx=5, pady=(5, 0))
        
    add_new_row()
    return entries_list

def create_notes_section(parent: tk.Widget, update_callback=None) -> tuple[tk.BooleanVar, tk.StringVar, list]:
    """
    Creates the notes section UI.
    
    Specifications
    --------------
    - Checkbox for "CAC Scanner Unavailable"
    - Combobox for "On-Call MTL" with predefined options
    - Dynamic list of additional notes fields with add/remove functionality
    """
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
    rows = 0
    
    def add_note_field():
        log.debug("Adding new note field.")
        nonlocal rows
        rows += 1
        row = ttk.Frame(notes_container)
        row.pack(fill="x", pady=2)
        
        ttk.Label(row, text="Note:").pack(side="left", padx=(0, 5))
        entry = ttk.Entry(row)
        entry.pack(side="left", fill="x", expand=True)
        notes_entries.append(entry)
        
        # Bind update callback to new entry if provided
        if update_callback:
            entry.bind('<KeyRelease>', lambda e: parent.after_idle(update_callback))
    
    def remove_last_note_field():
        nonlocal rows 
        if rows <= 1: # Always keep at least one note field
            return
        if notes_entries:
            log.debug("Removing last note field.")
            rows -= 1
            last_entry = notes_entries.pop()
            last_entry.master.destroy()
            notes_container.update_idletasks()
            # Trigger update after removal
            if update_callback:
                parent.after_idle(update_callback)
    
    button_row = ttk.Frame(frame)
    button_row.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=(5, 0))

    add_button = ttk.Button(button_row, text="Add Note", command=add_note_field)
    add_button.pack(side="left", padx=5)

    remove_button = ttk.Button(button_row, text="Remove Note", command=remove_last_note_field)
    remove_button.pack(side="left", padx=5)

    add_note_field()
    return cac_var, mtl_var, notes_entries

def create_signature_section(parent: tk.Widget) -> dict:
    """Creates the signature section UI."""
    log.debug("Creating signature section.")
    frame = tk.LabelFrame(parent, text="Signature", padx=10, pady=10)
    frame.pack(padx=10, pady=10, fill="both", expand="yes")

    widgets = {
        "Rank": create_combobox(frame, tk.StringVar(frame), Constants.rank_options, 12),
        "Last": tk.Entry(frame, width=15), 
        "First": tk.Entry(frame, width=15),
        "MI": tk.Entry(frame, width=3),
        "Squadron": create_combobox(frame, tk.StringVar(frame), Constants.squadron_options, 7),
        "AFSC/Job": create_combobox(frame, tk.StringVar(frame), Constants.job_options, 30),
    }

    layout_map = [("Rank", "Last", "First", "MI"), ("Squadron", "AFSC/Job")]
    for r, row_keys in enumerate(layout_map):
        col = 0
        for key in row_keys:
            ttk.Label(frame, text=f"{key}:").grid(row=r, column=col, sticky="w", padx=5, pady=2)
            col += 1
            colspan = 3 if key == "AFSC/Job" else 1
            widgets[key].grid(row=r, column=col, columnspan=colspan, sticky="ew", padx=5, pady=2)
            col += colspan
    return widgets
