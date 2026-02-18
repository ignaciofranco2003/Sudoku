from tkinter import ttk

def apply_style(root):
    style = ttk.Style(root) # Crea un objeto de estilo asociado a la ventana principal
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # ESTILOS DE TEXTOS -----------------------------------------------------------------------------

    style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))  # Título principal
    style.configure("Sub.TLabel", font=("Segoe UI", 10))    # Subtítulo
    style.configure("Status.TLabel", font=("Segoe UI", 10, "italic"))   # Mensajes

    # CONTENEDORES -----------------------------------------------------------------------------

    style.configure("Card.TFrame", background="#f6f7fb")    # Tarjeta donde se muestra el tablero
    style.configure("Panel.TFrame", background="#ffffff")   # Panel lateral derecho

    # TEXTOS DEL PANEL -----------------------------------------------------------------------------

    # Título de secciones del panel
    style.configure(
        "PanelTitle.TLabel",
        font=("Segoe UI", 12, "bold"),
        background="#ffffff",
        foreground="#111827"
    )

    # Texto común dentro del panel
    style.configure(
        "PanelText.TLabel",
        background="#ffffff",
        foreground="#111827",
        font=("Segoe UI", 9)
    )

    # GRUPOS -----------------------------------------------------------------------------

    style.configure("TLabelframe", background="#ffffff")    # Estilo de los contenedores con título
    style.configure("TLabelframe.Label", background="#ffffff", font=("Segoe UI", 10, "bold"))   # Estilo del texto del título