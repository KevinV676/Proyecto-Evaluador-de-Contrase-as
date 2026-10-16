#------------Librerías-----------#
import tkinter as tk
from tkinter import ttk, messagebox

#-----------Funciones del programa (main.py)-----------#
from main import (
    verificar_contrasena,
    calcular_entropia,
    clasificar_entropia,
    cracking_time,
    generar_contrasena_sugerida,
    LONGITUD_MINIMA,
    LONGITUD_SUGERIDA,
)

#-----------Constantes-----------#
BITS_BARRA_MAX = 100  # con esta entropía la barra se llena al 100 %

COLORES = {
    "Muy Débil": "#d32f2f",
    "Débil": "#f57c00",
    "Media": "#fbc02d",
    "Fuerte": "#388e3c",
    "Muy Fuerte": "#1b5e20",
}

ESCALA_ENTROPIA = (
    ("Menos de 28 bits", "Muy Débil"),
    ("28 a 35 bits", "Débil"),
    ("36 a 59 bits", "Media"),
    ("60 a 127 bits", "Fuerte"),
    ("128 bits o más", "Muy Fuerte"),
)


#-----------Utilidades-----------#
def formatear_tiempo(años):
    """Convierte años a un texto legible."""
    if años < 1e-6:
        return "Inmediato"
    if años < 1:
        dias = años * 365
        if dias < 1:
            return "Menos de 1 día"
        return f"{dias:.2f} días"
    if años < 1000:
        return f"{años:.2f} años"
    if años < 1e6:
        return f"{años / 1000:.2f} mil años"
    return f"{años:.2e} años"


#---------- INTERFAZ ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Verificador de contraseñas")
        self.geometry("500x760")
        self.resizable(False, False)

        self.var_contrasena = tk.StringVar()
        self.var_mostrar = tk.BooleanVar(value=False)
        self.var_longitud = tk.IntVar(value=LONGITUD_SUGERIDA)
        self.var_generada = tk.StringVar()

        self.configurar_estilos()
        self.crear_menu()
        self.crear_widgets()

        # Evalúa en tiempo real mientras se escribe
        self.var_contrasena.trace_add("write", lambda *_: self.al_verificar())

    #---------- Estilos ----------
    def configurar_estilos(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")  # permite cambiar el color de la barra
        except tk.TclError:
            pass
        for nombre, color in COLORES.items():
            estilo.configure(
                f"{nombre}.Horizontal.TProgressbar",
                background=color,
                troughcolor="#e0e0e0",
                thickness=18,
            )
        estilo.configure("Neutro.Horizontal.TProgressbar",
                         background="#9e9e9e", troughcolor="#e0e0e0", thickness=18)

    #---------- Menú ----------
    def crear_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Limpiar", command=self.al_limpiar)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.destroy)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        entropia_menu = tk.Menu(menubar, tearoff=0)
        entropia_menu.add_command(label="Ver escala de entropía",
                                  command=self.mostrar_escala_entropia)
        menubar.add_cascade(label="Entropía", menu=entropia_menu)

        generar_menu = tk.Menu(menubar, tearoff=0)
        generar_menu.add_command(label="Generar contraseña",
                                 command=self.al_generar)
        menubar.add_cascade(label="Generar", menu=generar_menu)

    #---------- Widgets ----------
    def crear_widgets(self):
        marco = ttk.Frame(self, padding=16)
        marco.pack(fill="both", expand=True)

        # Título
        ttk.Label(marco, text="Verificador de contraseñas",
                  font=("Segoe UI", 14, "bold")).pack(anchor="w")

        # Entrada de contraseña
        ttk.Label(marco, text="Contraseña:").pack(anchor="w", pady=(12, 2))
        self.entrada = ttk.Entry(marco, textvariable=self.var_contrasena, show="•")
        self.entrada.pack(fill="x")
        self.entrada.focus()
        self.entrada.bind("<Return>", lambda e: self.al_verificar())

        ttk.Checkbutton(marco, text="Mostrar contraseña",
                        variable=self.var_mostrar,
                        command=self.alternar_visibilidad).pack(anchor="w", pady=4)

        # Botones
        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=8)
        self.btn_verificar = ttk.Button(botones, text="Verificar",
                                        command=self.al_verificar)
        self.btn_verificar.pack(side="left")
        ttk.Button(botones, text="Limpiar",
                   command=self.al_limpiar).pack(side="left", padx=6)
        ttk.Button(botones, text="Salir", command=self.destroy).pack(side="right")

        # Resultado
        self.lbl_resultado = ttk.Label(marco, text="", font=("Segoe UI", 12, "bold"))
        self.lbl_resultado.pack(anchor="w", pady=(8, 2))

        self.barra = ttk.Progressbar(marco, orient="horizontal", mode="determinate",
                                     maximum=BITS_BARRA_MAX,
                                     style="Neutro.Horizontal.TProgressbar")
        self.barra.pack(fill="x")

        self.lbl_entropia = ttk.Label(marco, text="")
        self.lbl_entropia.pack(anchor="w", pady=(4, 0))

        # Problemas
        ttk.Label(marco, text="Problemas encontrados:",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.txt_problemas = self.crear_texto(marco, alto=5)

        # Recomendaciones
        ttk.Label(marco, text="Recomendaciones:",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8, 2))
        self.txt_recomendaciones = self.crear_texto(marco, alto=5)

        # Tiempos de crackeo
        ttk.Label(marco, text="Tiempo estimado para crackearla:",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8, 2))
        self.txt_tiempos = self.crear_texto(marco, alto=4)

        # Generador
        gen = ttk.LabelFrame(marco, text="Generar contraseña", padding=8)
        gen.pack(fill="x", pady=(12, 0))

        fila = ttk.Frame(gen)
        fila.pack(fill="x")
        ttk.Label(fila, text="Longitud:").pack(side="left")
        ttk.Spinbox(fila, from_=LONGITUD_MINIMA, to=64, width=5,
                    textvariable=self.var_longitud).pack(side="left", padx=6)
        ttk.Button(fila, text="Generar", command=self.al_generar).pack(side="left")
        ttk.Button(fila, text="Copiar", command=self.al_copiar).pack(side="left", padx=6)
        ttk.Button(fila, text="Usar",
                   command=self.al_usar_generada).pack(side="left")

        ttk.Entry(gen, textvariable=self.var_generada, state="readonly",
                  font=("Consolas", 10)).pack(fill="x", pady=(8, 0))

    def crear_texto(self, padre, alto):
        """Crea un cuadro de texto de solo lectura con scroll."""
        contenedor = ttk.Frame(padre)
        contenedor.pack(fill="x")
        txt = tk.Text(contenedor, height=alto, wrap="word", state="disabled",
                      relief="solid", borderwidth=1, font=("Segoe UI", 9))
        scroll = ttk.Scrollbar(contenedor, command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)
        txt.pack(side="left", fill="x", expand=True)
        scroll.pack(side="right", fill="y")
        return txt

    #------------Funciones-----------
    def escribir(self, widget, texto):
        """Reemplaza el contenido de un Text de solo lectura."""
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", texto)
        widget.config(state="disabled")

    def alternar_visibilidad(self):
        self.entrada.config(show="" if self.var_mostrar.get() else "•")

    def al_verificar(self):
        contrasena = self.var_contrasena.get()
        if not contrasena:
            self.limpiar_resultados()
            return

        problemas = verificar_contrasena(contrasena)
        bits = calcular_entropia(contrasena)
        clasificacion = clasificar_entropia(bits)

        # Clasificación y barra
        self.lbl_resultado.config(text=f"Clasificación: {clasificacion}",
                                  foreground=COLORES[clasificacion])
        self.barra.config(style=f"{clasificacion}.Horizontal.TProgressbar")
        self.barra["value"] = min(bits, BITS_BARRA_MAX)
        self.lbl_entropia.config(text=f"Entropía: {bits:.2f} bits")

        # Problemas y recomendaciones
        if problemas:
            self.escribir(self.txt_problemas,
                          "\n".join(f"• {p}" for p, _ in problemas))
            self.escribir(self.txt_recomendaciones,
                          "\n".join(f"• {r}" for _, r in problemas))
        else:
            self.escribir(self.txt_problemas, "Ninguno.")
            self.escribir(self.txt_recomendaciones,
                          "La contraseña cumple con todos los criterios de seguridad.")

        # Tiempos de crackeo
        self.escribir(self.txt_tiempos, self.texto_tiempos(bits))

    def texto_tiempos(self, bits):
        if bits > 1000:  # 2 ** bits desbordaría un float
            return "Prácticamente imposible de crackear por fuerza bruta."
        resultados = cracking_time(bits)
        if isinstance(resultados, str):  # entropía 0 -> "Inmediato"
            return resultados
        return "\n".join(f"• {desc}: {formatear_tiempo(años)}"
                         for desc, años in resultados)

    def limpiar_resultados(self):
        self.lbl_resultado.config(text="")
        self.lbl_entropia.config(text="")
        self.barra.config(style="Neutro.Horizontal.TProgressbar")
        self.barra["value"] = 0
        self.escribir(self.txt_problemas, "")
        self.escribir(self.txt_recomendaciones, "")
        self.escribir(self.txt_tiempos, "")

    def al_limpiar(self):
        self.var_contrasena.set("")
        self.var_generada.set("")
        self.limpiar_resultados()
        self.entrada.focus()

    #---------- Generador ----------
    def al_generar(self):
        try:
            longitud = int(self.var_longitud.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("Longitud no válida",
                                 "Introduce un número entero válido.")
            return
        if longitud < LONGITUD_MINIMA:
            messagebox.showwarning(
                "Longitud muy corta",
                f"La longitud mínima es de {LONGITUD_MINIMA} caracteres.")
            return
        self.var_generada.set(generar_contrasena_sugerida(longitud))

    def al_copiar(self):
        texto = self.var_generada.get()
        if not texto:
            messagebox.showinfo("Copiar", "Primero genera una contraseña.")
            return
        self.clipboard_clear()
        self.clipboard_append(texto)
        messagebox.showinfo("Copiar", "Contraseña copiada al portapapeles.")

    def al_usar_generada(self):
        texto = self.var_generada.get()
        if texto:
            self.var_contrasena.set(texto)

    #---------- Escala de entropía ----------
    def mostrar_escala_entropia(self):
        ventana = tk.Toplevel(self)
        ventana.title("Escala de entropía")
        ventana.geometry("320x240")
        ventana.resizable(False, False)
        ventana.transient(self)

        marco = ttk.Frame(ventana, padding=16)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="Escala de entropía",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

        for rango, nombre in ESCALA_ENTROPIA:
            fila = ttk.Frame(marco)
            fila.pack(fill="x", pady=3)
            tk.Label(fila, width=2, background=COLORES[nombre]).pack(side="left")
            ttk.Label(fila, text=f"  {nombre}: {rango}").pack(side="left")

        ttk.Button(marco, text="Cerrar", command=ventana.destroy).pack(pady=(14, 0))


if __name__ == "__main__":
    App().mainloop()



