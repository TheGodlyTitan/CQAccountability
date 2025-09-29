import logging
import tkinter as tk
from tkinter import ttk, messagebox
from logic.processing import (
    get_form_data, 
    format_email_body, 
    ValidationException
)


log = logging.getLogger('app.actions')


def display_result(parent_window: tk.Tk, content: str):
    """Creates a new window to display the generated email body."""
    log.debug("Displaying result window.")
    result_window = tk.Toplevel(parent_window)
    result_window.title("Generated Email Body")
    result_window.geometry("700x600")
    
    text_area = tk.Text(result_window, wrap="word", padx=10, pady=10)
    text_area.pack(expand=True, fill="both")
    text_area.insert("1.0", content)
    
    def copy_to_clipboard():
        log.info("Copying to clipboard.")
        parent_window.clipboard_clear()
        parent_window.clipboard_append(text_area.get("1.0", tk.END))
        copy_button.config(text="Copied!")
        parent_window.after(2000, lambda: copy_button.config(text="Copy to Clipboard"))

    copy_button = ttk.Button(result_window, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=5)

def generate_email_action(main_window: tk.Tk, ui_elements: dict):
    """Orchestrates the process of generating and displaying the email."""
    log.info("Generate Email action triggered.")
    
    try:
        form_data = get_form_data(ui_elements)
        email_body = format_email_body(form_data)
        display_result(main_window, email_body)
        
    except ValidationException as e:
        log.warning("Validation failed, showing error message.")
        error_message = "\n\n".join(e.errors)
        messagebox.showerror(
            "Warning!",
            f"Please correct the following errors before generating the email:\n\n{error_message}"
        )
