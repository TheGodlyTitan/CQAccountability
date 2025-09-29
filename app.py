import tkinter as tk
from tkinter import ttk

from constants import Constants
from utils import setup_logging
from gui.window import (
  create_main_window,
  setup_scrollable_area
)
from gui.sections import (
  create_manor_selector, 
  create_cq_team_section, 
  create_dynamic_entry_section,
  create_red_card_late_entry_widgets, 
  create_late_entry_widgets,
  create_notes_section, 
  create_signature_section
)
from gui.widgets import layout_widgets_in_grid
from logic.actions import generate_email_action


log = setup_logging()


def main():
    """
    Main function to build the UI and run the application.
    """
    log.info("Application starting up...")
    
    # 1. Create the main window and scrollable area
    window = create_main_window()
    scrollable_frame, _ = setup_scrollable_area(window) 

    # 2. Build UI sections and collect widget references
    manor_var = create_manor_selector(scrollable_frame, Constants.manor_options)
    
    cq_members_entries = create_cq_team_section(scrollable_frame, Constants.cq_roles)
    
    red_card_lates_entries = create_dynamic_entry_section(
        parent=scrollable_frame, 
        title="Red Card Lates",
        widget_factory=create_red_card_late_entry_widgets,
        layout_function=lambda p, w: layout_widgets_in_grid(p, w, {"Type": "Late To"}),
        add_button_text="Add Late"
    )

    lates_entries = create_dynamic_entry_section(
        parent=scrollable_frame, 
        title="Lates",
        widget_factory=create_late_entry_widgets,
        layout_function=layout_widgets_in_grid,
        add_button_text="Add Late"
    )

    cac_scanner_var, mtl_var, notes_entries = create_notes_section(scrollable_frame)
    
    signature_entries = create_signature_section(scrollable_frame)

    # 3. Store references to all UI elements for the action function
    ui_elements = {
        "manor": manor_var,
        "cq_members": cq_members_entries,
        "red_card_lates": red_card_lates_entries,
        "lates": lates_entries,
        "notes": {
            "cac_scanner": cac_scanner_var,
            "on_call_mtl": mtl_var,
            "additional_notes": notes_entries,
        },
        "signature": signature_entries,
    }

    # 4. Create the main action button
    generate_button_frame = ttk.Frame(window)
    generate_button_frame.pack(side="bottom", fill="x", pady=10, padx=10)
    
    generate_button = ttk.Button(
        generate_button_frame,
        text="Generate Email",
        command=lambda: generate_email_action(window, ui_elements)
    )
    generate_button.pack()

    # 5. Start the application
    log.info("Starting main application loop.")
    window.mainloop()
    log.info("Application shut down.")

if __name__ == "__main__":
    main()
