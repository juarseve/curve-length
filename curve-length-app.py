import ttkbootstrap as ttk
import numpy as np
import funciones as f

from sympy import symbols, sin, cos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calcular_longitud():
    radio = entrada1.get()
    intervalos = entrada2.get()

    if is_float(radio) and float(radio) > 0 and intervalos.isdigit() and (0 < int(intervalos) < 999999):

        radio = float(radio)
        intervalos = int(intervalos)

        t = symbols("t")
        funciones_coordenadas = [radio * cos(t),
                                 radio * sin(t),
                                 4 - (radio / 2) * cos(t) - (radio / 2) * sin(t)]

        funcion = f.crear_funcion(funciones_coordenadas)

        suma_teorica = f.suma_de_riemann(funcion, 999999)
        suma_aprox = f.suma_de_riemann(funcion, intervalos)
        error = abs((suma_teorica - suma_aprox)) / suma_teorica * 100

        linea = "Aproximacion: " + str(suma_aprox) + " cm\nError: " + str(error) + " %"
        salida.set(linea)
    else:
        salida.set("Parámetros Incorrectos")


def dibujar_figura():
    radio = entrada1.get()

    if is_float(radio) and float(radio) <= 60:
        radio = float(radio)
        if radio < 0.5:
            A = 1
        else:
            A = round(radio)

        # coordenadas cilindricas
        theta = np.linspace(0, 2 * np.pi, 20)
        X_1, Y_1 = radio * np.cos(theta), radio * np.sin(theta)
        Z_1 = np.linspace(-A * 2, A * 2 + A * 2.8, A * 10)
        _, Z = np.meshgrid(theta, Z_1)

        # coordenadas cartesianas
        A = A + 1
        x, y = np.linspace(-A * 2, A * 2, A * 10), np.linspace(-A * 2, A * 2, A * 10)
        X_2, Y_2 = np.meshgrid(x, y)
        Z_2 = (8 - X_2 - Y_2) / 2

        # funcion z
        Z_3 = 4 - (radio / 2) * (np.cos(theta) + np.sin(theta))

        plano.clear()
        plano.set_title("Intersección entre Cilindro y Plano", family="times New Roman", size="10")
        plano.set_xlabel("Eje X", family="Times New Roman", size="10")
        plano.set_ylabel("Eje Y", family="Times New Roman", size="10")
        plano.set_zlabel("Eje Z", family="Times New Roman", size="10")

        # cilindro
        plano.plot_surface(X_1, Y_1, Z, alpha=0.5, color="aquamarine", rstride=100, cstride=1)
        # plano
        plano.plot_surface(X_2, Y_2, Z_2, alpha=0.5, color="darkorange", rstride=100, cstride=1)
        # vectores
        plano.quiver(0, 0, 0, X_1, Y_1, Z_3, color="black", edgecolor="black")

        canvas.draw()
        grafico.pack()


def clear():
    plano.clear()
    plano.set_xlabel("Eje X", family="Times New Roman", size="10")
    plano.set_ylabel("Eje Y", family="Times New Roman", size="10")
    plano.set_zlabel("Eje Z", family="Times New Roman", size="10")
    canvas.draw()
    salida.set("")


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# ----APP----
main_root = ttk.Window(themename='minty', title='Length Calculator', iconphoto='cilindro.png')
main_root.state('zoomed')

# ---title---
ttk.Label(master=main_root, text='Longitud de Traza', font="Times 26").pack(pady=50)

# ---input frame---
input_frame = ttk.Frame(master=main_root)

entrada1 = ttk.StringVar()
ttk.Label(master=input_frame, text='Radio (cm):', font="Times 16").pack(side='left')
ttk.Entry(master=input_frame, textvariable=entrada1).pack(side='left', padx=10)

entrada2 = ttk.StringVar()
ttk.Label(master=input_frame, text='Subintervalos:', font="Times 16").pack(side='left')
ttk.Entry(master=input_frame, textvariable=entrada2).pack(side='left', padx=10)

input_frame.pack(pady=10)

# ---button frame---
button_frame = ttk.Frame()

ttk.Button(master=button_frame, text='Calcular', command=calcular_longitud).pack(side='left', padx=20)
ttk.Button(master=button_frame, text='Mostrar Figura', command=dibujar_figura).pack(side='left')
ttk.Button(master=button_frame, text='Clear', command=clear).pack(side='left', padx=20)

button_frame.pack(pady=20)

# ---output frame---
output_frame = ttk.Frame(master=main_root)

salida = ttk.StringVar()
ttk.Label(master=output_frame, font='Times 18', textvariable=salida).pack()

output_frame.pack(pady=50)

# ---figure flame---
grafico = ttk.Frame(master=main_root)

figura = Figure(figsize=(5, 5), dpi=140)
plano = figura.add_subplot(111, projection="3d")

canvas = FigureCanvasTkAgg(figura, master=grafico)
widget = canvas.get_tk_widget()
widget.pack()

if __name__ == '__main__':
    main_root.mainloop()
