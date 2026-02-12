from tkinter import ttk

def apply_style(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
    style.configure("Sub.TLabel", font=("Segoe UI", 10))
    style.configure("Status.TLabel", font=("Segoe UI", 10, "italic"))

    style.configure("Card.TFrame", background="#f6f7fb")
    style.configure("Panel.TFrame", background="#ffffff")

    style.configure(
        "PanelTitle.TLabel",
        font=("Segoe UI", 12, "bold"),
        background="#ffffff",
        foreground="#111827"
    )

    style.configure(
        "PanelText.TLabel",
        background="#ffffff",
        foreground="#111827",
        font=("Segoe UI", 9)
    )

    style.configure("TLabelframe", background="#ffffff")
    style.configure("TLabelframe.Label", background="#ffffff", font=("Segoe UI", 10, "bold"))
