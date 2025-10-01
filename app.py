import tkinter as tk
from tkinter import ttk
from constants import Constants
from utils import setup_logging
from gui.window import (
    create_main_window, 
    setup_scrollable_area,
)
from gui.sections import (
    create_manor_section,
    create_airman_leaders_section,
    create_charge_quarters_section, 
    create_dynamic_entry_section,
    create_notes_section, 
    create_signature_section, 
    create_email_preview_section,
)
from gui.widgets import (
    layout_widgets_in_grid, 
    create_red_card_late_entry_widgets, 
    create_late_entry_widgets
)
from logic.processing import (
    format_email_body, 
    get_form_data_for_preview, 
    ValidationException
)
from logic.actions import check_email_action


log = setup_logging()


def main():
    """Main function to build the UI and run the application."""
    log.info("Application starting up...")
    
    # 1. Create the main window
    window = create_main_window()
    
    # 2. Create main container with two panels
    main_container = ttk.Frame(window)
    main_container.pack(fill="both", expand=True, padx=10, pady=10)
    main_container.grid_columnconfigure(0, weight=3) # Give more weight to the left panel
    main_container.grid_columnconfigure(1, weight=1) # Smaller preview panel
    main_container.grid_rowconfigure(0, weight=1)
    
    # Left panel for inputs
    left_panel = ttk.Frame(main_container)
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
    
    # Right panel for email preview
    right_panel = ttk.Frame(main_container)
    right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
    
    # Set up scrollable area for left panel
    scrollable_frame, _ = setup_scrollable_area(left_panel)

    # 5. Create check email callback function
    def check_email_callback():
        check_email_action(window, ui_elements)

    # 6. Create email preview section with check email button
    preview_text_widget, line_numbers_widget = create_email_preview_section(right_panel, check_email_callback)
    
    # Define update_preview early so it can be passed as a callback
    def update_preview():
        try:
            form_data = get_form_data_for_preview(ui_elements)
            email_body = format_email_body(form_data)
            
            # Update main content
            preview_text_widget.config(state="normal")
            preview_text_widget.delete("1.0", tk.END)
            preview_text_widget.insert("1.0", email_body)
            preview_text_widget.config(state="disabled")

            # Update line numbers
            line_count = email_body.count('\n') + 1
            line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
            line_numbers_widget.config(state="normal")
            line_numbers_widget.delete("1.0", tk.END)
            line_numbers_widget.insert("1.0", line_numbers_text)
            line_numbers_widget.config(state="disabled")

        except ValidationException:
            # Don't show errors in preview, just show incomplete data
            preview_text_widget.config(state="normal")
            preview_text_widget.delete("1.0", tk.END)
            preview_text_widget.insert("1.0", "Fill out required fields to see email preview...")
            preview_text_widget.config(state="disabled")
            # Clear line numbers
            line_numbers_widget.config(state="normal")
            line_numbers_widget.delete("1.0", tk.END)
            line_numbers_widget.config(state="disabled")
        except Exception as e:
            log.debug(f"Preview update error: {e}")

    # 3. Build UI sections and collect widget references
    manor_var = create_manor_section(scrollable_frame, Constants.manor_options)
    
    al_members_entries = create_airman_leaders_section(scrollable_frame, Constants.al_roles)
    
    cq_members_entries = create_charge_quarters_section(scrollable_frame, Constants.cq_roles)
    
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

    cac_scanner_var, mtl_var, notes_entries = create_notes_section(scrollable_frame, update_preview)
    
    signature_entries = create_signature_section(scrollable_frame)

    # 4. Store references to all UI elements
    ui_elements = {
        "manor": manor_var,
        "al_members": al_members_entries,
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
    
    # 7. Set up live preview update function (already defined above)
    
    # 8. Bind update function to all relevant widgets
    def bind_update_events(widget_dict):
        """Recursively bind update events to all input widgets."""
        for key, value in widget_dict.items():
            if isinstance(value, dict):
                bind_update_events(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        bind_update_events(item)
                    # Note: We don't bind to list items here because dynamic lists
                    # (like notes) handle their own binding internally.
            # For tk.Variable subclasses (StringVar, BooleanVar)
            elif hasattr(value, 'trace_add'):
                value.trace_add('write', lambda *args: window.after_idle(update_preview))
            # For tk.Widget subclasses (Entry, Combobox)
            elif hasattr(value, 'bind'):
                try:
                    # Bind text entry widgets
                    value.bind('<KeyRelease>', lambda e: window.after_idle(update_preview))
                    # Bind combobox selection changes
                    if isinstance(value, ttk.Combobox):
                        value.bind('<<ComboboxSelected>>', lambda e: window.after_idle(update_preview))
                except tk.TclError:
                    # Ignore errors for widgets that might be destroyed
                    pass

    bind_update_events(ui_elements)
    
    # Initial preview update
    window.after_idle(update_preview)

    # 9. Start the application (removed bottom button section)
    log.info("Starting main application loop.")
    window.mainloop()
    log.info("Application shut down.")

if __name__ == "__main__":
    main()
