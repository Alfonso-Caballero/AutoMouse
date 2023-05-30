import ctypes
import keyboard
import pyautogui as pa
import random
import threading
import GUI
import datetime

# Sencillo programa que me propuse en base al comentario de unos de mis compañeros, que controla el ratón de un
# usuario, moviéndolo a posiciones aleatorias de la pantalla, y presiona el botón de windows cada minuto,
# en cualquier momento el programa puede ser parado con la tecla 'S' del teclado.
# También le he añadido una interfaz sencilla, la librería tkinter o customtkinter se
# queda corta para el desarrollo de interfaces

pa.FAILSAFE = False  # Al quitarlo si el puntero del ratón golpea una esquina, salta una excepción
flag = False  # Boolean flag


def on_closed(window, windows_event, execute_event, timer_event):
    """
    When you press the 'X' button of the window, the flag sets to 'False', the window is closed, and thread events
    are cleared and set to 'False'
    :param window:
    :param windows_event: Event  of a thread
    :param execute_event: Event  of a thread
    :param timer_event: Event  of a thread
    """
    global flag
    flag = False
    window.destroy()
    timer_event.clear()
    windows_event.clear()
    execute_event.clear()
    timer_event.set()
    windows_event.set()
    execute_event.set()


def popup_window(speed, hour, minute):
    """
    Checks the parameters, if any of them are incorrect it shows a 'pop-up' window with the error message
    :param speed: Selected number of speed in the GUI
    :param hour: Selected hour in the GUI
    :param minute: Selected minute in the GUI
    :return:
    """
    if speed is "" or not speed.isdigit():  # Comprobamos que el campo 'speed' no está vacío y es número
        message = "! Speed cell is incorrect !"
        errorWindow = GUI.ErrorWindow(message)  # Objeto 'ErrorWindow', con un mensaje como parámetro

    elif (hour is "" or minute is "") or (not len(hour) == 2 or not len(minute) == 2) or (
            not hour.isdigit() or not minute.isdigit()):
        # Comprobamos que el campo de la fecha no está vacío, tiene dos carácteres y es un número positivo

        message = "! Date cell is incorrect !"
        errorWindow = GUI.ErrorWindow(message)

    else:
        message = "! Date cell is incorrect !"
        errorWindow = GUI.ErrorWindow(message)

    errorWindow.mainloop()  # Lanzamos la ventana


def check_info(width_label, height_label, speed_options, run_button, hour_entry, min_entry, check_button, windows_event,
               execute_event, vel_entry, timer_event):
    """
    Gets the info of the GUI, if any of it is incorrect, will launch a error window
    :param width_label: The x dimension of screen
    :param height_label: The y dimension of screen
    :param speed_options: The speed number selected
    :param run_button: The 'run' of the GUI
    :param hour_entry: The chosen hour of the GUI
    :param min_entry: The chosen minute of the GUI
    :param check_button: The checkbox of the GUI
    :param window_event: Thread Event
    :param execute_event: Thread Event
    :param vel_entry: The speed entry of the GUI
    :param timer_event: Thread Event
    :return:
    """
    global flag
    widthString = width_label.cget("text")  # Cogemos la información de la primera label
    heightString = height_label.cget("text")  # Cogemos la información de la segunda label
    speedString = speed_options.get()  # Cogemos la información de la caja de 'speed'
    hour = hour_entry.get()  # Cogemos la información de la entrada de la hora
    minutes = min_entry.get()  # Cogemos la información de la entrada de los minutos
    if check_button.get() == 1:  # Comprobamos que el checkbox está marcado,
        # si está marcado, el tiempo que se ejecutará el programa es indefinido
        if speedString.isdigit():  # Comprobamos si ha sido seleccionada alguna opción del combox de la velocidad
            flag = True  # Ponemos la bandera a True
            initialize(widthString, heightString, speedString, windows_event, execute_event, run_button, hour_entry,
                       min_entry, vel_entry, timer_event)  # Lanzamos el método que empezará la ejecución del programa
        else:
            popup_window(speedString, hour, minutes)
    else:  # Si el checkbox no está marcado
        if (hour is "" or minutes is "") or (not hour.isdigit() or not minutes.isdigit()) or (
                not speedString.isdigit()):
            # Comprobamos si el campo de la hora y los minutos está en un formato incorrecto
            popup_window(speedString, hour, minutes)
        else:  # Sí está en el formato correcto
            hour_number = int(hour)  # Parseamos el string de la hora a un entero
            min_number = int(minutes)  # Parseamos el string de los minutos a un entero
            if hour_number > 23 or min_number > 59:  # Comprobamos que los números se encuentran fuera de rango correcto
                popup_window(speedString, hour, minutes)
            else:  # Sí están dentro del rango correcto
                actual_time = datetime.datetime.now()  # Obtenemos la fecha actual
                now_epoch = int(actual_time.timestamp())  # Parseamos la fecha actual a fecha epoch
                chrono_time = int((datetime.datetime(actual_time.year, actual_time.month, actual_time.day, hour_number,
                                                     min_number, actual_time.second)).timestamp())
                # Parseamos la fecha seleccionada por el usuario, en decir, las horas y minutos, junto con los demás
                # parámetros del día actual, a una fecha epoch

                if chrono_time > now_epoch:  # Comprobamos que la hora es correcta, tiene que ser pasadas la hora
                    # actual, siendo la fecha seleccionada por el usuario mayor que la actual
                    flag = True  # Ponemos la flag a 'True'
                    time_to_wait = chrono_time - now_epoch  # Restamos la diferencia entre la fecha epoch actual
                    # y la seleccionada por el usuario, nos dará los segundos de diferencia
                    timer_event.clear()  # Reseteamos el evento del hilo
                    thread_timer = threading.Thread(target=initialize_timer, args=(
                        time_to_wait, run_button, vel_entry, hour_entry, min_entry, windows_event, execute_event,
                        timer_event))  # Creamos el hilo del temporizador
                    thread_timer.start()  # Iniciamos el hilo
                    initialize(widthString, heightString, speedString, windows_event, execute_event, run_button,
                               hour_entry,
                               min_entry, vel_entry, timer_event)
                else:  # En caso de que la fecha del usuario sea menor a la actual, lanzamos una ventana de error
                    message = "! Date cell is incorrect !"
                    errorWindow = GUI.ErrorWindow(message)

                    errorWindow.mainloop()


def initialize(width_string, height_string, speed_string, windows_event, execute_event, run_button, hour_entry,
               min_entry, vel_entry, timer_event):
    """
    With the info received from the 'check_info' method, launch the program
    :param width_string: check_info -- width
    :param height_string: check_info -- height
    :param speed_string: check_info -- speed
    :param windows_event: check_info -- Thread Event
    :param execute_event: check_info -- Thread Event
    :param run_button: check_info -- Run button of the GUI
    :param hour_entry: check_info -- Hour info of the GUI
    :param min_entry: check_info -- Min info of the GUI
    :param vel_entry: check_info -- Speed entry of the GUI
    :param timer_event: check_info -- Thread Event
    :return:
    """
    vel_entry.configure(state="disabled")  # Ponemos el 'entry' de la velocidad a 'disabled
    run_button.configure(state="disabled")  # Ponemos el botón de 'run' a 'disabled
    hour_entry.configure(state="disabled")  # Ponemos el 'entry' de la hora a 'disabled
    min_entry.configure(state="disabled")  # Ponemos el 'entry' de los minutos a 'disabled
    width_number = int(width_string)  # Parseamos la label con el ancho de la pantalla a un número
    height_number = int(height_string)  # Parseamos la label con el alto de la pantalla a un número
    speed_number = int(speed_string)  # Parseamos el número seleccionado del combobox de la velocidad a un número entero
    windows_event.clear()  # Reset de los evento -- Por si acaso
    execute_event.clear()  # Reset del evento  -- Por si acaso
    thread_stop = threading.Thread(target=stop_process,
                                   args=(windows_event, execute_event, run_button, vel_entry, hour_entry, min_entry,
                                         timer_event))
    # Creamos el hilo, que se encarga de parar en cualquier momento el programa
    thread_execute = threading.Thread(target=pointer_movement,
                                      args=(speed_number, height_number, width_number, execute_event))
    # Creamos el hilo, que se encarga de lanzar la ejecución del programa
    thread_windows = threading.Thread(target=windows_button, args=(windows_event, 1))
    # Creamos el hilo que se encarga de controlar el botón de windows
    thread_stop.start()  # Lanzamos los hilos
    thread_execute.start()
    thread_windows.start()


def stop_process(window_event, execute_event, run_button, vel_entry, hour_entry, min_entry, timer_event):
    """
    This method-thread allows the user to stop the program with the 'S' key in any moment
    :param window_event: Thread Event
    :param execute_event: Thread Event
    :param run_button: The run button of the GUI
    :param vel_entry: The speed entry of the GUI
    :param hour_entry: The hour entry of the GUI
    :param min_entry: The min entry of the GUI
    :param timer_event: Thread Event
    """
    global flag
    while flag:
        if keyboard.is_pressed('s'):  # Si la tecla 'S' es presionada
            flag = False  # Ponemos la flag a 'False' para parar los bucles
            run_button.configure(state="normal")  # Ponemos los botones y entries de la GUI, habilitados
            hour_entry.configure(state="normal")
            min_entry.configure(state="normal")
            vel_entry.configure(state="normal")
            window_event.set()  # Con el método set despertamos los hilos, todos los hilos que se encuentren en wait,
            # despiertan, bueno, para ser más correctos, ponemos a 'True' el evento del hilo
            execute_event.set()
            timer_event.set()


def pointer_movement(speed, height, width, execute_event):
    """
    Moves the mouse pointer to a random position of the screen
    :param speed: Speed of the pointer, selected with the GUI
    :param height: Height of the user screen
    :param width: Width of the user screen
    :param execute_event: Thread Event
    :return:
    """
    while flag:
        execute_event.wait(speed)  # Durante los segundos seleccionados, se espera,
        # los segundos son el número seleccionado de la caja 'speed'
        pa.moveTo(x=random.randint(10, (height - 10)), y=random.randint(10, (width - 10)))
        # Con la librería pyautogui tenemos acceso al puntero, y lo movemos a una posición aleatoria


def windows_button(windows_event, i):
    """
    Controls the windows button of the keyboard
    :param windows_event: Thread Event
    :param i: Nothing, will launch an error, since just one element, its not iterable
    :return:
    """
    while flag:  # Mientras la bandera sea 'True'
        windows_event.wait(60)  # Hay una pausa de un minuto
        pa.press("win")  # Presiona el botón de windows, con la librería pyautogui
        pa.press("win")   # Presiona el botón de windows, con la librería pyautogui


def initialize_timer(time_to_wait, run_button, vel_entry, hour_entry, min_entry, windows_event, execute_event,
                     timer_event):
    """
    If the checkbox of the gui isn't checked, and the date format is correct, it will run the program till the date selected
    :param time_to_wait: The seconds to wait
    :param run_button: Run button of the GUI
    :param vel_entry: Speed entry of the GUI
    :param hour_entry: Hour entry of the GUI
    :param min_entry: Min entry of the GUI
    :param windows_event: Thread Event
    :param execute_event: Thread Event
    :param timer_event: Thread Event
    :return:
    """
    global flag
    while flag:
        timer_event.wait(time_to_wait)  # Tiempo de espera, en segundos
        flag = False
        run_button.configure(state="normal")  # Una vez finalizado el tiempo de espera, se ponen todos los elementos habilitados
        hour_entry.configure(state="normal")
        min_entry.configure(state="normal")
        vel_entry.configure(state="normal")
        if not windows_event.is_set():  # Comprobación de si los eventos, si están en falso los ponemos a 'True', los despertamos
            windows_event.set()
        elif not execute_event.is_set():
            execute_event.set()


if __name__ == '__main__':
    user32 = ctypes.windll.user32
    # Conseguimos las dimensiones de la pantalla del usuario
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # Creamos tres eventos, se encargarán del tiempo en espera durante el bucle de los hilos
    windows_event = threading.Event()
    execute_event = threading.Event()
    time_event = threading.Event()

    # Construimos un objeto ventana, con los parámetros que nos pide el constructor
    interface = GUI.MainWindow(width, height, windows_event, execute_event, time_event)
    interface.mainloop()  # Lanzamos la ventana de la interfaz
