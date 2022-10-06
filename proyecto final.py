import tkinter as tk
from tkinter import messagebox, NO
from tkinter import ttk
import csv


class Electrodomestico:

    def __init__(self, nombre: str, cantidad: int, vatios: int, horas_de_uso_por_dia: int, dias_de_uso_al_mes: int):
        self.nombre = nombre
        self.cantidad = cantidad
        self.consumo = vatios  # Watts(Vatios)
        self.horas_de_uso_por_dia = horas_de_uso_por_dia
        self.dias_de_uso_al_mes = dias_de_uso_al_mes
        self.kwh = self.calcular_kwh_electrodomestico()

    def calcular_kwh_electrodomestico(self):
        vatios_hora = self.consumo * self.horas_de_uso_por_dia
        kilovatios_hora = vatios_hora / 1000

        return kilovatios_hora

    def calcular_kwh_electrodomestico_mensual(self):
        return round(self.kwh * self.dias_de_uso_al_mes * self.cantidad)

    def calcular_kwh_electrodomestico_anual(self):
        return self.calcular_kwh_electrodomestico_mensual() * 12


class CalculadoraConsumo:
    def __init__(self, costo_kwh):
        self.costo_kwh = costo_kwh  # Pesos Col
        self.lista_de_electrodomesticos = []

    def calcular_consumo_mensual(self):
        total = 0
        for electrodomestico in self.lista_de_electrodomesticos:
            total += (electrodomestico.calcular_kwh_electrodomestico_mensual() * self.costo_kwh)

        return round(total)

    def calcular_kwh_mensual(self):
        total = 0
        for electrodomestico in self.lista_de_electrodomesticos:
            total += electrodomestico.calcular_kwh_electrodomestico_mensual()

        return total

    def agregar_electrodomestico(self, nombre, cantidad, consumo, horas, dias):
        electrodomestico_nuevo = Electrodomestico(nombre, cantidad, consumo, horas, dias)
        self.lista_de_electrodomesticos.append(electrodomestico_nuevo)
        ventana_emergente(f"¡Se agrego el electrodoméstico '{electrodomestico_nuevo.nombre}' exitosamente!", False)

    def calcular_cantidad_electrodomesticos(self):
        total = 0
        for electrodomestico in self.lista_de_electrodomesticos:
            total += electrodomestico.cantidad

        return round(total)


def ventana_emergente(msg, isError):
    if isError:
        messagebox.showerror(message=msg)
    else:
        messagebox.showinfo(message=msg)


class GUI:

    def __init__(self, master):

        self.ancho = 30
        self.alto = 2

        style = ttk.Style()
        style.configure("mystyle.Treeview.Heading", font=('Helvetica', 12, 'bold'))  # Modify the font of the headings

        self.calculadora = CalculadoraConsumo(217)

        self.master = master  # Instancia de TKINTER (ventana)
        # Definir tamaño de ventana ancho x alto
        self.master.geometry("600x350")
        # Titulo de la ventana
        self.master.title('ElectriCalc')

        self.image = tk.PhotoImage(file='logo.gif')

        self.master.config(bd=10)
        self.master.config(relief="sunken")

        # Instancia de la etiqueta de titulo
        self.label = tk.Label(master, text="Calculadora de Consumo Eléctrico",
                              font=('Helvetica', 18, 'bold'),
                              width=self.ancho, height=self.alto)
        # Posicionamiento del titulo
        self.label.pack(pady=5, side="top")

        self.label_img = tk.Label(master,
                                  width=250, height=250, image=self.image)
        # Posicionamiento del titulo
        self.label_img.pack(padx=15, side="right")

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=15, side="left")

        self.button1 = tk.Button(self.frame, text="Configurar costo kWh", command=self.ventana_configurar,
                                 width=self.ancho, height=self.alto)
        self.button1.pack(pady=5)

        self.button1 = tk.Button(self.frame, text="Agregar electrodoméstico", command=self.ventana_añadir,
                                 width=self.ancho, height=self.alto)
        self.button1.pack(pady=5)

        self.button2 = tk.Button(self.frame, text="Calcular consumo eléctrico",
                                 command=self.ventana_resultados,
                                 state="disabled", width=self.ancho, height=self.alto)
        self.button2.pack(pady=5)

        self.close_button = tk.Button(self.frame, text="Salir", command=master.quit, width=self.ancho, height=self.alto)
        self.close_button.pack(pady=5)

    def ventana_añadir(self):
        self.newWindow = tk.Toplevel(self.master)

        self.label_titulo = tk.Label(self.newWindow, relief="groove", bd="5", text="Agregar electrodoméstico",
                                     font=('Helvetica', 16))
        self.label_titulo.pack(pady=10)

        self.frame = tk.Frame(self.newWindow)
        self.frame.pack(pady=10)

        self.label_nombre = tk.Label(self.frame, text="Nombre")
        self.label_nombre.grid(row=1, column=1, sticky='W', padx=10)
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=1, column=2, sticky='W', padx=10)

        self.label_cantidad = tk.Label(self.frame, text="Cantidad de Equipos")
        self.label_cantidad.grid(row=2, column=1, sticky='W', padx=10)
        self.entry_cantidad = tk.Spinbox(self.frame,from_=1, to=100, width=18, state="readonly")
        self.entry_cantidad.grid(row=2, column=2, sticky='W', padx=10)

        self.label_consumo = tk.Label(self.frame, text="Potencia (Vatios)", justify="left")
        self.label_consumo.grid(row=3, column=1, sticky='W', padx=10)
        self.entry_consumo = tk.Entry(self.frame)
        self.entry_consumo.grid(row=3, column=2, sticky='W', padx=10)

        self.label_horas = tk.Label(self.frame, text="Horas de uso diarias (c/u)", justify="left")
        self.label_horas.grid(row=4, column=1, sticky='W', padx=10)
        self.entry_horas = tk.Spinbox(self.frame,from_=0.001, to=24, width=18)
        self.entry_horas.grid(row=4, column=2, sticky='W', padx=10)

        self.label_dias = tk.Label(self.frame, text="Dias de uso al mes (c/u)", justify="left")
        self.label_dias.grid(row=5, column=1, sticky='W', padx=10)
        self.entry_dias = tk.Spinbox(self.frame,from_=1, to=30, width=18)
        self.entry_dias.grid(row=5, column=2, sticky='W', padx=10)

        self.add_button = tk.Button(self.frame, text='Añadir', width=15, command=self.guardar_info)
        self.add_button.grid(row=6, column=2, sticky='N', padx=10, pady=10)

    def guardar_info(self):
        try:
            self.calculadora.agregar_electrodomestico(self.entry_nombre.get(), int(self.entry_cantidad.get()),
                                                      int(self.entry_consumo.get()),
                                                      float(self.entry_horas.get()), int(self.entry_dias.get()))
        except ValueError as error:
            ventana_emergente("¡El valor ingresado debe ser numérico!", True)
        else:
            self.newWindow.destroy()
            if len(self.calculadora.lista_de_electrodomesticos) >= 1:
                self.button2.config(state="normal")

    def ventana_resultados(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry("1050x400")

        self.label_titulo = tk.Label(self.newWindow, width=20, text="Resultados", relief="groove", bd="5",
                                     font=('Helvetica', 16))
        self.label_titulo.grid(row=0, column=1, sticky='N', pady=10, padx=10)

        # columns

        self.tree = ttk.Treeview(self.newWindow, show='headings', style="mystyle.Treeview")
        self.tree['columns'] = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8')
        self.tree.column('#1', width=150, stretch=NO, anchor=tk.CENTER)
        self.tree.column('#2', width=80, stretch=NO, anchor=tk.CENTER)
        self.tree.column('#3', width=80, stretch=NO, anchor=tk.CENTER)
        self.tree.column('#4', width=80, stretch=NO, anchor=tk.CENTER)
        self.tree.column('#5', width=150, stretch=NO, anchor=tk.CENTER)
        self.tree.column('#6', width=150, stretch=NO, anchor=tk.CENTER)
        self.tree.column('#7', width=150, stretch=NO, anchor=tk.CENTER)
        self.tree.column('#8', width=150, stretch=NO, anchor=tk.CENTER)

        self.tree.heading('#1', text='Electodoméstico')
        self.tree.heading('#2', text='Cantidad')
        self.tree.heading('#3', text='Horas')
        self.tree.heading('#4', text='Días')
        self.tree.heading('#5', text='Consumo mensual')
        self.tree.heading('#6', text='Costo mensual')
        self.tree.heading('#7', text='Consumo Anual')
        self.tree.heading('#8', text='Costo Anual')

        for electrodomestico in self.calculadora.lista_de_electrodomesticos:
            values = (electrodomestico.nombre,
                      electrodomestico.cantidad,
                      electrodomestico.horas_de_uso_por_dia,
                      electrodomestico.dias_de_uso_al_mes,
                      str(electrodomestico.calcular_kwh_electrodomestico_mensual()),
                      f"${round(electrodomestico.calcular_kwh_electrodomestico_mensual() * self.calculadora.costo_kwh)}",
                      str(electrodomestico.calcular_kwh_electrodomestico_anual()),
                      "$" + str(
                          round(electrodomestico.calcular_kwh_electrodomestico_anual() * self.calculadora.costo_kwh)))

            self.tree.insert('', tk.END, values=values)

        values = ("Total",
                  self.calculadora.calcular_cantidad_electrodomesticos(),
                  "-",
                  "-",
                  str(self.calculadora.calcular_kwh_mensual()),
                  "$" + str(self.calculadora.calcular_consumo_mensual()),
                  str(self.calculadora.calcular_kwh_mensual() * 12),
                  "$" + str(self.calculadora.calcular_consumo_mensual() * 12))

        self.tree.insert('', tk.END, values=values)

        self.tree.grid(row=1, column=1, sticky='nsew', padx=10)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.newWindow, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky='ns')

        # #

        self.exportar_boton = tk.Button(self.newWindow, text='Exportar a CSV', width=15, command=self.exportar_a_csv)
        self.exportar_boton.grid(row=2, column=1, sticky='N', padx=10, pady=10)

    def ventana_configurar(self):
        self.newWindow = tk.Toplevel(self.master)

        self.newWindow.geometry("200x350")

        self.label_nombre = tk.Label(self.newWindow, relief="groove", bd="5", text="Costo del kWh",
                                     font=('Helvetica', 16))

        self.label_nombre.pack(pady=15)

        self.frame = tk.Frame(self.newWindow)
        self.frame.pack(pady=10)
        self.frame.config(bd=5)
        self.frame.config(relief="sunken")

        self.costo_kwh = tk.IntVar(value=0)
        self.opcion = tk.BooleanVar(value=False)

        self.radio_button_list = []

        self.est1 = tk.Radiobutton(self.frame, text='Estrato 1', width=15, variable=self.costo_kwh, value=349,
                                   command=self.modificar_kwh)
        self.est1.pack(pady=5)
        self.radio_button_list.append(self.est1)

        self.est2 = tk.Radiobutton(self.frame, text='Estrato 2', width=15, variable=self.costo_kwh, value=375,
                                   command=self.modificar_kwh)
        self.est2.pack(pady=5)
        self.radio_button_list.append(self.est2)

        self.est3 = tk.Radiobutton(self.frame, text='Estrato 3', width=15, variable=self.costo_kwh, value=460,
                                   command=self.modificar_kwh)
        self.est3.pack(pady=5)
        self.radio_button_list.append(self.est3)

        self.est4 = tk.Radiobutton(self.frame, text='Estrato 4', width=15, variable=self.costo_kwh, value=496,
                                   command=self.modificar_kwh)
        self.est4.pack(pady=5)
        self.radio_button_list.append(self.est4)

        self.est5 = tk.Radiobutton(self.frame, text='Estrato 5-6', width=15, variable=self.costo_kwh, value=596,
                                   command=self.modificar_kwh)
        self.est5.pack(pady=5)
        self.radio_button_list.append(self.est5)

        self.c1 = tk.Checkbutton(self.newWindow, text='Costo personalizado', variable=self.opcion, onvalue=1,
                                 offvalue=0, command=self.actualizar_vista)
        self.c1.pack()

        self.actualizar_vista()

    def actualizar_vista(self):
        if self.opcion.get():
            for radio_button in self.radio_button_list:
                radio_button.configure(state=tk.DISABLED)

            self.entry_costo = tk.Entry(self.newWindow, width=15)
            self.entry_costo.pack()

            self.add_button = tk.Button(self.newWindow, text='Guardar', width=15,
                                        command=lambda: self.modificar_kwh(self.entry_costo.get()))

            self.add_button.pack(pady=5)

        else:
            try:
                self.entry_costo.pack_forget()
                self.add_button.pack_forget()
            except:
                pass

            for radio_button in self.radio_button_list:
                radio_button.configure(state=tk.NORMAL)

    def modificar_kwh(self, costo=None):
        try:
            if costo:
                self.calculadora.costo_kwh = int(costo)
            else:
                self.calculadora.costo_kwh = int(self.costo_kwh.get())
        except ValueError as error:
            ventana_emergente("El valor ingresado debe ser un número entero!", True)
            try:
                self.entry_costo.delete(0, tk.END)
            except:
                pass
        else:
            ventana_emergente("El costo del kWh será de $" + str(self.calculadora.costo_kwh), False)
            self.newWindow.destroy()

    def exportar_a_csv(self):
        with open('resultados.csv', mode='w') as resultados:
            resultados_writer = csv.writer(resultados, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for electrodomestico in self.calculadora.lista_de_electrodomesticos:
                resultados_writer.writerow(
                    [electrodomestico.nombre, electrodomestico.cantidad, electrodomestico.horas_de_uso_por_dia,
                     electrodomestico.dias_de_uso_al_mes, str(electrodomestico.calcular_kwh_electrodomestico_mensual()),
                     f"${round(electrodomestico.calcular_kwh_electrodomestico_mensual() * self.calculadora.costo_kwh)}",
                     str(electrodomestico.calcular_kwh_electrodomestico_anual()),
                     "$" + str(
                         round(electrodomestico.calcular_kwh_electrodomestico_anual() * self.calculadora.costo_kwh))])


def main():
    root = tk.Tk()
    my_gui = GUI(root)
    root.mainloop()


main()
