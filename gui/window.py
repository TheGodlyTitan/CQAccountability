
import logging
import tkinter as tk
from tkinter import ttk
from utils import resource_path


TITLE = "CQ Accountability Email Generator"
ICON_PATH = "assets/app_icon.png"


log = logging.getLogger('app.window')


def create_main_window() -> tk.Tk:
    """Creates and configures the main application window."""
    log.debug(f"Creating main window with title: '{TITLE}'")
    
    window = tk.Tk()
    window.title(TITLE)
    window.state('zoomed')  # Start maximized
    window.minsize(800, 600)  # Minimum size to prevent too small windows
    
    try:
        icon_path = resource_path(ICON_PATH)
        app_icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(False, app_icon)
        log.info("Window icon set successfully.")
    
    except Exception as e:
        log.warning(f"Failed to set window icon: {e}")
        
    return window
    
def setup_scrollable_area(parent: tk.Widget) -> tuple[ttk.Frame, tk.Canvas]:
    """Creates a scrollable area and returns the content frame and canvas."""
    log.debug("Setting up scrollable area.")
    container = ttk.Frame(parent)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        # Cross-platform scroll handling
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")

    parent.bind_all("<MouseWheel>", _on_mousewheel)
    parent.bind_all("<Button-4>", _on_mousewheel)
    parent.bind_all("<Button-5>", _on_mousewheel)

    return scrollable_frame, canvas
