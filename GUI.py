import threading
import customtkinter as ctk
from PIL import Image
from main import check_info, on_closed


# Dos objetos, uno de ellos es la ventana principal de la interfaz, y el otro es una ventana
# que saltará en caso de que el usuario introduzca parámetros incorrectos

class MainWindow(ctk.CTk):
    """
    Main window, the GUI of the program, inherits from CTK class
    """
    def __init__(self, width, height, windows_event, execute_event, time_event):  # Constructor
        height_number = int(height / 2)  # La mitad de la altura total de la pantalla, será el tamaño de la ventana
        width_number = int(width / 2)  # La mitad del ancho total de la pantalla, será el tamaño de la ventana
        ctk.CTk.__init__(self)
        self.title(" AutoMouse")  # Nombre de la ventana
        ctk.set_appearance_mode("dark")  # Ponemos el modo oscuro
        self.geometry("{}x{}".format(width_number, height_number))  # Establecemos las dimensiones de la ventana
        # No quiero que el tamaño de la ventana pueda cambiar
        self.minsize(width_number, height_number)  # Establecemos un tamaño mínimo
        self.maxsize(width_number, height_number)  # Establecemos un tamaño máximo, que es el mismo que el mínimo
        # De esta forma el tamaño nunca cambia
        self.configure(fg_color="black")  # Establecemos el fondo de la ventana negro
        self.iconbitmap("imagenes/icono.ico")  # Establecemos el icono de la ventana
        background_image = ctk.CTkImage(Image.open("imagenes/prueba5.jpg"), size=(width, height))  # Imagen de fondo de la ventana
        # Label que contiene la imagen para el fondo de la ventana
        label_image = ctk.CTkLabel(self, image=background_image, text="", fg_color="transparent",
                                   bg_color="transparent")
        # La colocamos en la posición 0, 0, y la estiramos
        label_image.place(x=0, y=0, relwidth=1, relheight=1)
        # Label que contiene el texto, "Screen Size"
        widthTextL = ctk.CTkLabel(self, text="Screen Size", fg_color="transparent", text_color="#F5F2E7",
                                  font=("Trebuchet", 20, "bold"), corner_radius=100, bg_color="transparent", width=250)
        # Label que contiene el número del ancho de la pantalla
        width_number_label = ctk.CTkLabel(self, text=width, fg_color="black", text_color="#0091FF",
                                          font=("Trebuchet", 19, "bold"), corner_radius=50, bg_color="black")
        # Label que contiene el número del alto de la pantalla
        height_number_label = ctk.CTkLabel(self, text=height, fg_color="black", text_color="#0091FF",
                                   font=("Trebuchet", 19, "bold"), corner_radius=50, bg_color="transparent")
        # Label que contiene el texto, "Pointer Blink Speed"
        velTextL = ctk.CTkLabel(self, text="Pointer blink speed", fg_color="black", text_color="#F5F2E7",
                                font=("Trebuchet", 20, "bold"), corner_radius=50, bg_color="transparent", width=250)
        # Combobox con las diferentes opciones de velocidad
        velEntry = ctk.CTkOptionMenu(self, width=70, corner_radius=0, bg_color="black", fg_color="black",
                                     button_color="black", dropdown_font=("Trebuchet", 16, "italic"),
                                     dropdown_fg_color="black", font=("Trebuchet", 17, "bold"),
                                     button_hover_color="#0A0057")
        # Valores del combobox
        velEntry.configure(values=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        # Texto de base, e informativo, 0 es la velocidad máxima
        velEntry.set("0 max")
        # Progress Bar, como elemento decorativo
        progress_bar = ctk.CTkProgressBar(self, orientation="horizontal", progress_color="black",
                                          fg_color="black", border_color="purple", border_width=2,
                                          height=5)
        # Poniéndolo a uno, se establece 'lleno'
        progress_bar.set(1)
        # Label que contiene el texto "Schedule Time"
        chronoText = ctk.CTkLabel(self, text="Schedule Time", fg_color="black", text_color="#F5F2E7",
                                  font=("Trebuchet", 20, "bold"), corner_radius=50, bg_color="black", width=250)
        # Entry para poner la hora
        hourEntry = ctk.CTkEntry(self, placeholder_text="Hour", justify="center", width=65, corner_radius=50,
                                 bg_color="black", border_width=2, border_color="#0091FF", fg_color="transparent",
                                 text_color="white", placeholder_text_color="white", font=("Trebuchet", 14, "bold"))
        # Entry para poner los minutos
        minutesEntry = ctk.CTkEntry(self, placeholder_text="Min", justify="center", width=65, corner_radius=50,
                                    bg_color="black", border_width=2, border_color="#0091FF", fg_color="transparent",
                                    text_color="white", placeholder_text_color="white", font=("Trebuchet", 14, "bold"))
        # CheckBox, para seleccionar si se quiere un tiempo indefinido o no
        undefined_check = ctk.CTkCheckBox(self, text="Undefined Time", font=("Trebuchet", 14, "bold"), border_width=1,
                                          hover_color="#5C469C", fg_color="blue")
        # Label informativa, para saber con qué tecla para la ejecución del programa
        stopTextL = ctk.CTkLabel(self, text="* Stop the programm with 'S' key", fg_color="black", text_color="#0091FF",
                                 font=("Trebuchet", 18, "bold"), corner_radius=50, bg_color="transparent", width=250)
        # Botón 'Run' para lanzar el programa, con el parámetro 'command', decimos que método ejecutar al presionar
        # el botón, tiene una función lambda para meter parámetros al método
        executeButton = ctk.CTkButton(self, text="Run", height=30, width=150, font=("Trebuchet", 15), corner_radius=40,
                                      border_width=2, text_color="white", fg_color="black", hover_color="#470080",
                                      command=lambda: check_info(width_number_label, height_number_label, velEntry,
                                                                 executeButton,
                                                                 hourEntry, minutesEntry, undefined_check,
                                                                 windows_event, execute_event, velEntry, time_event),
                                      bg_color="black",
                                      border_color="purple")

        # Las siguientes líneas son para posicionar todos los elementos previos, hay diferentes formas de hacerlo
        # En este caso hemos utilizado el 'grid', se hace una división por celdas, y se van colocando los elementos,
        # estableciendo unos márgenes, y diversos parámetros, el grid se suele usar para interfaces simétricas por así
        # llamarlo, y de forma más sencilla
        widthTextL.grid(row=0, column=0, padx=(100, 150), pady=40)
        width_number_label.grid(row=0, column=1, padx=(30, 150), pady=40)
        height_number_label.grid(row=0, column=1, padx=(30, 15), pady=40)
        velTextL.grid(row=1, column=0, padx=(100, 150), pady=40)
        velEntry.grid(row=1, column=1, padx=(100, 150), pady=40)
        chronoText.grid(row=2, column=0, padx=(100, 150), pady=40)
        hourEntry.grid(row=2, column=1, padx=(30, 150), pady=40)
        minutesEntry.grid(row=2, column=1, padx=(30, 15), pady=40)
        undefined_check.grid(row=2, column=1, padx=(250, 15), pady=40)
        progress_bar.grid(row=3, column=0, padx=(150, 150), pady=40, columnspan=3, sticky="EW")
        stopTextL.grid(row=4, column=0, padx=(100, 150), pady=40)
        executeButton.grid(row=4, column=1, padx=(100, 150), pady=40)

        # Función que se ejecuta al cerrar la ventana con el botón de "X" de la ventana, cuando la ventana se cierre
        # se ejecutará la función 'on_closed', volvemos a utilizar una lambda para meter parámetros
        self.wm_protocol("WM_DELETE_WINDOW", lambda: on_closed(self, windows_event, execute_event, time_event))


class ErrorWindow(ctk.CTkToplevel):
    """
    Window that will appear when any of the parameters are wrong or not in the correct format
    Inherits from CTKTopLevel class
    """
    def __init__(self, string):
        ctk.CTkToplevel.__init__(self)
        self.configure(fg_color="black")  # Establecemos el fondo a color negro
        self.title(" Datos incorrectos")  # Establecemos el título de la ventana
        self.geometry("200x200")  # Las dimensiones de la pantalla
        # Quiero un tamaño fijo
        self.minsize(400, 200) # Tamaño mínimo de la pantalla
        self.maxsize(400, 200)  # Tamaño máximo de la pantalla
        # Al ser el mismo la ventana tiene un tamaño fijo
        self.grab_set()  # Establecemos que la ventana se muestra por encima del resto
        error = ctk.CTkLabel(self, text=string, fg_color="transparent",
                             font=("Trebuchet", 16, "bold"), text_color="#F64848")
        # Texto que se mostrará, texto de error
        okayButton = ctk.CTkButton(self, text=" Okay ", fg_color="black", text_color="white",
                                   font=("Trebuchet", 16), border_width=2, hover_color="#616889",
                                   command=self.destroy)
        # Botón para cerrar la venta

        # Colocamos los elementos con el grid
        error.grid(row=0, column=0, padx=(100, 150), pady=60)
        okayButton.grid(row=1, column=0, padx=(100, 150), pady=0)
