# ==========================================
# INTERFAZ GRAFICA DE USUARIO (GUI)
# ==========================================
# Interfaz visual para el analizador de PHP. Reutiliza los modulos
# lexer.py, parser.py y semantic.py sin modificarlos: los importa y ejecuta
# sobre el codigo escrito en el editor.
#
# Ejecutar con:  python gui.py
#
# --- APORTE JULIANA BURGOS --- #

import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# Modulos de analisis del proyecto
import lexer as modulo_lexer
import parser as modulo_parser
import semantic as modulo_semantic


# ==========================================
# 1. TEMA VISUAL
# ==========================================
class Tema:
    # Superficies
    FONDO      = "#11131a"   # fondo de la ventana
    BARRA      = "#171a23"   # cabecera y barra de estado
    PANEL      = "#1c1f2a"   # tarjetas / encabezados de panel
    EDITOR     = "#151823"   # fondo del editor y de las consolas
    GUTTER     = "#171a23"   # margen de numeros de linea
    BORDE      = "#262b3a"

    # Texto
    TEXTO      = "#e6e9f0"
    TENUE      = "#767d92"
    APAGADO    = "#4b5266"

    # Marca
    ACENTO     = "#7c5cff"   # violeta principal
    ACENTO_ALT = "#9d86ff"   # hover del violeta

    # Semaforo
    OK         = "#3ddc97"
    ERROR      = "#ff5c7c"
    AVISO      = "#ffc857"
    INFO       = "#5ccfe6"

    # Realces del editor
    LINEA_ACTUAL = "#1d2130"
    LINEA_ERROR  = "#3a1d2a"

    # Sintaxis PHP
    S_COMENTARIO = "#5a6178"
    S_CADENA     = "#ffd479"
    S_NUMERO     = "#c792ea"
    S_PALABRA    = "#ff6ac1"
    S_VARIABLE   = "#5ccfe6"
    S_FUNCION    = "#82d982"
    S_ETIQUETA   = "#ff9f5c"


FUENTE_CODIGO = ("Consolas", 11)
FUENTE_CONSOLA = ("Consolas", 10)
FUENTE_UI     = ("Segoe UI", 10)
FUENTE_UI_NEG = ("Segoe UI", 10, "bold")

# Usuarios de git de cada integrante (para nombrar los logs igual que en consola)
INTEGRANTES = {
    "Eimmy Ochoa":    "eimmy-o",
    "Diego Parrales": "raydan90s",
    "Juliana Burgos": "juzjuz10",
}

# Palabras reservadas de PHP que reconoce el lexer (para el resaltado)
PALABRAS_RESERVADAS = (
    "if", "else", "echo", "function", "return", "true", "false",
    "switch", "case", "default", "break", "while", "for", "define",
    "foreach", "as", "class", "public", "private", "protected",
    "static", "new",
)

CODIGO_EJEMPLO = '''<?php

// Constante de impuesto
define("IVA", 0.15);

$nombre = "Juliana";
$edad = 22;

if ($edad >= 18) {
    echo "Mayor de edad";
} else {
    echo "Menor de edad";
}

function calcularTotal($precio, $cantidad) {
    return $precio * $cantidad;
}

$total = calcularTotal(10, 3);
echo $total;

?>'''


# ==========================================
# 2. EJECUCION DE LOS ANALIZADORES
# ==========================================
# Cada funcion recibe el codigo como texto y devuelve un diccionario con el
# resultado. No escriben archivos: el guardado del log se hace aparte.

def _reiniciar_lexer():
    """Deja el lexer limpio antes de cada analisis."""
    modulo_lexer.lexer.lineno = 1
    modulo_lexer.lexer.log_errores = []


def _linea_del_mensaje(mensaje):
    """Extrae el primer numero de linea que aparece en un mensaje de error."""
    coincidencia = re.search(r'linea (\d+)', mensaje)
    return int(coincidencia.group(1)) if coincidencia else 0


def analizar_lexico(codigo):
    """Recorre el codigo y devuelve la lista de tokens y de errores lexicos."""
    _reiniciar_lexer()
    modulo_lexer.lexer.input(codigo)

    tokens = []
    while True:
        tok = modulo_lexer.lexer.token()
        if not tok:
            break
        tokens.append((tok.lineno, tok.type, tok.value))

    errores = list(getattr(modulo_lexer.lexer, 'log_errores', []))
    return {'tokens': tokens, 'errores': errores}


def analizar_sintactico(codigo):
    """Ejecuta el parser y devuelve los errores sintacticos encontrados."""
    _reiniciar_lexer()
    modulo_parser.errores_sintacticos = []

    # El parser tambien dispara los hooks semanticos, por eso se reinicia
    # el analizador semantico para no arrastrar resultados de una corrida previa.
    modulo_semantic.analizador_semantico.reset()

    try:
        modulo_parser.parser.parse(codigo, lexer=modulo_lexer.lexer)
    except Exception as e:
        modulo_parser.errores_sintacticos.append(f"Error interno del parser: {e}")

    errores_lexicos = list(getattr(modulo_lexer.lexer, 'log_errores', []))
    return {
        'errores': list(modulo_parser.errores_sintacticos),
        'errores_lexicos': errores_lexicos,
    }


def analizar_semantico(codigo):
    """Ejecuta el parser (que alimenta las tablas) y lee el resultado semantico."""
    resultado_sintactico = analizar_sintactico(codigo)
    analizador = modulo_semantic.analizador_semantico

    return {
        'errores': list(analizador.errores),
        'advertencias': list(analizador.advertencias),
        'variables': dict(analizador.tabla_variables),
        'constantes': dict(analizador.tabla_constantes),
        'funciones': dict(analizador.tabla_funciones),
        'errores_sintacticos': resultado_sintactico['errores'],
    }


def guardar_log(tipo, usuario_git, contenido):
    """Escribe el log en la carpeta logs/ con el mismo formato de nombre
    que usan lexer.py, parser.py y semantic.py."""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    if tipo == 'lexico':
        fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    else:
        fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")

    nombre_log = f"{tipo}-{usuario_git}-{fecha_hora}.txt"
    ruta_log = os.path.join('logs', nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write(contenido)

    return ruta_log


# ==========================================
# 3. WIDGETS REUTILIZABLES
# ==========================================
class Boton(tk.Frame):
    """Boton plano con efecto hover. Se construye sobre un Frame para poder
    controlar el color del borde y el relleno interno."""

    def __init__(self, padre, texto, comando, primario=False, ancho_min=0):
        fondo = Tema.ACENTO if primario else Tema.PANEL
        super().__init__(padre, bg=fondo, highlightthickness=1,
                         highlightbackground=Tema.ACENTO if primario else Tema.BORDE,
                         highlightcolor=Tema.ACENTO if primario else Tema.BORDE)

        self.fondo_normal = fondo
        self.fondo_hover = Tema.ACENTO_ALT if primario else Tema.BORDE
        self.comando = comando

        self.etiqueta = tk.Label(
            self, text=texto, bg=fondo,
            fg="#ffffff" if primario else Tema.TEXTO,
            font=FUENTE_UI_NEG if primario else FUENTE_UI,
            padx=14, pady=7, cursor="hand2",
        )
        if ancho_min:
            self.etiqueta.config(width=ancho_min)
        self.etiqueta.pack(fill="both", expand=True)

        for widget in (self, self.etiqueta):
            widget.bind("<Enter>", self._entrar)
            widget.bind("<Leave>", self._salir)
            widget.bind("<Button-1>", self._click)

    def _entrar(self, _=None):
        self.config(bg=self.fondo_hover)
        self.etiqueta.config(bg=self.fondo_hover)

    def _salir(self, _=None):
        self.config(bg=self.fondo_normal)
        self.etiqueta.config(bg=self.fondo_normal)

    def _click(self, _=None):
        self.comando()


class Separador(tk.Frame):
    """Linea vertical delgada para agrupar botones en la barra."""

    def __init__(self, padre):
        super().__init__(padre, bg=Tema.BORDE, width=1)


# ==========================================
# 4. EDITOR DE CODIGO
# ==========================================
class Margen(tk.Canvas):
    """Canvas lateral: numeros de linea + marcador de las lineas con error."""

    def __init__(self, master, editor, **kwargs):
        super().__init__(master, **kwargs)
        self.editor = editor
        self.lineas_error = set()

    def redibujar(self, *_):
        self.delete("all")
        ancho = self.winfo_width()
        linea_cursor = str(self.editor.index("insert")).split(".")[0]

        indice = self.editor.index("@0,0")
        while True:
            info = self.editor.dlineinfo(indice)
            if info is None:
                break
            y = info[1]
            numero = str(indice).split(".")[0]

            if int(numero) in self.lineas_error:
                color = Tema.ERROR
                self.create_oval(7, y + 6, 13, y + 12, fill=Tema.ERROR, outline="")
            elif numero == linea_cursor:
                color = Tema.TEXTO
            else:
                color = Tema.APAGADO

            self.create_text(ancho - 10, y, anchor="ne", text=numero,
                             font=FUENTE_CODIGO, fill=color)
            indice = self.editor.index(f"{indice}+1line")


class EditorPHP(tk.Frame):
    """Editor con numeracion de lineas, resaltado de sintaxis PHP,
    realce de la linea actual y marcado de las lineas con error."""

    def __init__(self, master, al_cambiar_cursor=None):
        super().__init__(master, bg=Tema.EDITOR, highlightthickness=1,
                         highlightbackground=Tema.BORDE)

        self.al_cambiar_cursor = al_cambiar_cursor
        self._tarea_resaltado = None

        self.scroll = ttk.Scrollbar(self, orient="vertical", style="Fino.Vertical.TScrollbar")
        self.scroll.pack(side="right", fill="y")

        self.texto = tk.Text(
            self, wrap="none", undo=True, maxundo=-1,
            bg=Tema.EDITOR, fg=Tema.TEXTO,
            insertbackground=Tema.ACENTO_ALT, insertwidth=2,
            selectbackground="#3a3f57", selectforeground=Tema.TEXTO,
            font=FUENTE_CODIGO, relief="flat", borderwidth=0,
            padx=12, pady=10, spacing1=2, spacing3=2,
            tabs=("1c",), yscrollcommand=self._al_desplazar,
        )
        self.margen = Margen(self, self.texto, width=54,
                             bg=Tema.GUTTER, highlightthickness=0)
        self.margen.pack(side="left", fill="y")
        self.texto.pack(side="left", fill="both", expand=True)
        self.scroll.config(command=self.texto.yview)

        self._configurar_tags()

        for evento in ("<KeyRelease>", "<ButtonRelease-1>", "<MouseWheel>",
                       "<Configure>", "<<Paste>>", "<<Undo>>", "<<Redo>>"):
            self.texto.bind(evento, self._al_editar, add="+")

    def _configurar_tags(self):
        t = self.texto
        # El realce de linea se configura primero para que quede por debajo
        # de los colores de sintaxis (en Tk gana el tag creado mas tarde).
        t.tag_configure("linea_actual", background=Tema.LINEA_ACTUAL)
        t.tag_configure("linea_error", background=Tema.LINEA_ERROR)

        t.tag_configure("s_variable", foreground=Tema.S_VARIABLE)
        t.tag_configure("s_numero", foreground=Tema.S_NUMERO)
        t.tag_configure("s_funcion", foreground=Tema.S_FUNCION)
        t.tag_configure("s_palabra", foreground=Tema.S_PALABRA)
        t.tag_configure("s_etiqueta", foreground=Tema.S_ETIQUETA, font=("Consolas", 11, "bold"))
        t.tag_configure("s_cadena", foreground=Tema.S_CADENA)
        t.tag_configure("s_comentario", foreground=Tema.S_COMENTARIO, font=("Consolas", 11, "italic"))

    # ------------------------------------------------------------------
    # Resaltado de sintaxis
    # ------------------------------------------------------------------
    # Reglas en orden de prioridad: lo que ya fue coloreado por una regla
    # anterior no vuelve a colorearse (asi un 'if' dentro de una cadena o de
    # un comentario no se pinta como palabra reservada).
    REGLAS = (
        ("s_comentario", r'(?://|\#)[^\n]*|/\*[\s\S]*?\*/'),
        ("s_cadena",     r'"[^"\n]*"'),
        ("s_etiqueta",   r'<\?php|\?>'),
        ("s_variable",   r'\$[a-zA-Z_][a-zA-Z0-9_]*'),
        ("s_palabra",    r'\b(?:' + "|".join(PALABRAS_RESERVADAS) + r')\b'),
        ("s_funcion",    r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*\()'),
        ("s_numero",     r'\b\d+(?:\.\d+)?\b'),
    )

    def _resaltar(self):
        contenido = self.texto.get("1.0", "end-1c")
        for nombre, _ in self.REGLAS:
            self.texto.tag_remove(nombre, "1.0", "end")

        ocupado = []  # rangos (inicio, fin) ya coloreados

        def libre(ini, fin):
            return all(fin <= a or ini >= b for a, b in ocupado)

        for nombre, patron in self.REGLAS:
            for m in re.finditer(patron, contenido):
                ini, fin = m.span()
                if not libre(ini, fin):
                    continue
                ocupado.append((ini, fin))
                self.texto.tag_add(nombre, f"1.0+{ini}c", f"1.0+{fin}c")

    def _realzar_linea_actual(self):
        self.texto.tag_remove("linea_actual", "1.0", "end")
        self.texto.tag_add("linea_actual", "insert linestart", "insert lineend+1c")

    def _al_editar(self, _=None):
        self._realzar_linea_actual()
        self.margen.redibujar()

        if self.al_cambiar_cursor:
            fila, columna = str(self.texto.index("insert")).split(".")
            self.al_cambiar_cursor(int(fila), int(columna) + 1)

        # Se reprograma el resaltado para no recalcularlo en cada pulsacion.
        if self._tarea_resaltado:
            self.after_cancel(self._tarea_resaltado)
        self._tarea_resaltado = self.after(120, self._resaltar)

    def _al_desplazar(self, *args):
        self.scroll.set(*args)
        self.margen.redibujar()

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------
    def obtener_codigo(self):
        return self.texto.get("1.0", "end-1c")

    def establecer_codigo(self, codigo):
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", codigo)
        self.texto.edit_reset()
        self._resaltar()
        self._al_editar()

    def limpiar_marcas(self):
        self.texto.tag_remove("linea_error", "1.0", "end")
        self.margen.lineas_error.clear()
        self.margen.redibujar()

    def marcar_linea(self, numero_linea):
        if numero_linea and numero_linea > 0:
            self.texto.tag_add("linea_error", f"{numero_linea}.0", f"{numero_linea}.end+1c")
            self.margen.lineas_error.add(numero_linea)
            self.margen.redibujar()

    def ir_a_linea(self, numero_linea):
        if numero_linea and numero_linea > 0:
            self.texto.see(f"{numero_linea}.0")
            self.texto.mark_set("insert", f"{numero_linea}.0")
            self.texto.focus_set()
            self._al_editar()

    def total_lineas(self):
        return int(str(self.texto.index("end-1c")).split(".")[0])


# ==========================================
# 5. VENTANA PRINCIPAL
# ==========================================
class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Analizador de PHP  —  Lenguajes de Programación (Grupo 3)")
        self.geometry("1280x800")
        self.minsize(1040, 660)
        self.configure(bg=Tema.FONDO)

        self.ruta_actual = None
        self.ultimo_log = None
        self.conteos = {"lexico": None, "sintactico": None, "semantico": None}

        self._configurar_estilos()
        self._construir_cabecera()
        self._construir_barra_herramientas()
        self._construir_area_central()
        self._construir_barra_estado()
        self._registrar_atajos()

        self.editor.establecer_codigo(CODIGO_EJEMPLO)
        self._estado("Listo. Escriba código PHP o abra un archivo, y ejecute un análisis.", Tema.TENUE)

    # ------------------------------------------------------------------
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure("TNotebook", background=Tema.FONDO, borderwidth=0, tabmargins=(0, 0, 0, 0))
        estilo.configure("TNotebook.Tab", background=Tema.FONDO, foreground=Tema.TENUE,
                         padding=(18, 9), font=FUENTE_UI, borderwidth=0)
        estilo.map("TNotebook.Tab",
                   background=[("selected", Tema.EDITOR)],
                   foreground=[("selected", Tema.TEXTO), ("active", Tema.TEXTO)],
                   expand=[("selected", (0, 0, 0, 0))])

        estilo.configure("Treeview", background=Tema.EDITOR, fieldbackground=Tema.EDITOR,
                         foreground=Tema.TEXTO, rowheight=27, borderwidth=0, font=("Consolas", 10))
        estilo.configure("Treeview.Heading", background=Tema.PANEL, foreground=Tema.TENUE,
                         font=("Segoe UI", 9, "bold"), relief="flat", padding=(8, 6))
        estilo.map("Treeview.Heading", background=[("active", Tema.BORDE)])
        estilo.map("Treeview", background=[("selected", "#2e3550")],
                   foreground=[("selected", Tema.TEXTO)])
        estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        for nombre in ("Fino.Vertical.TScrollbar", "Vertical.TScrollbar"):
            estilo.configure(nombre, background=Tema.BORDE, troughcolor=Tema.EDITOR,
                             bordercolor=Tema.EDITOR, arrowcolor=Tema.TENUE,
                             borderwidth=0, arrowsize=12)
            estilo.map(nombre, background=[("active", Tema.APAGADO)])

        estilo.configure("TCombobox", fieldbackground=Tema.PANEL, background=Tema.PANEL,
                         foreground=Tema.TEXTO, arrowcolor=Tema.TENUE,
                         bordercolor=Tema.BORDE, lightcolor=Tema.PANEL, darkcolor=Tema.PANEL,
                         selectbackground=Tema.PANEL, selectforeground=Tema.TEXTO,
                         padding=(8, 6))
        estilo.map("TCombobox", fieldbackground=[("readonly", Tema.PANEL)])
        self.option_add("*TCombobox*Listbox.background", Tema.PANEL)
        self.option_add("*TCombobox*Listbox.foreground", Tema.TEXTO)
        self.option_add("*TCombobox*Listbox.selectBackground", Tema.ACENTO)
        self.option_add("*TCombobox*Listbox.font", FUENTE_UI)

    # ------------------------------------------------------------------
    def _construir_cabecera(self):
        cabecera = tk.Frame(self, bg=Tema.BARRA, height=64)
        cabecera.pack(side="top", fill="x")
        cabecera.pack_propagate(False)

        tk.Label(cabecera, text="Analizador de PHP", bg=Tema.BARRA, fg=Tema.TEXTO,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=20)

        # Selector de integrante, alineado a la derecha
        der = tk.Frame(cabecera, bg=Tema.BARRA)
        der.pack(side="right", padx=20)
        tk.Label(der, text="Integrante", bg=Tema.BARRA, fg=Tema.TENUE,
                 font=("Segoe UI", 9)).pack(anchor="e")
        self.combo_integrante = ttk.Combobox(der, values=list(INTEGRANTES.keys()),
                                             state="readonly", width=17, font=FUENTE_UI)
        self.combo_integrante.current(2)
        self.combo_integrante.pack(anchor="e", pady=(2, 0))

    # ------------------------------------------------------------------
    def _construir_barra_herramientas(self):
        barra = tk.Frame(self, bg=Tema.FONDO)
        barra.pack(side="top", fill="x", padx=18, pady=(14, 10))

        Boton(barra, "▶  Analizar todo", self.analisis_completo, primario=True).pack(side="left")

        Separador(barra).pack(side="left", fill="y", padx=12, pady=4)

        Boton(barra, "Abrir .php", self.abrir_archivo).pack(side="left", padx=(0, 6))
        Boton(barra, "Guardar código", self.guardar_codigo).pack(side="left")

        # Derecha
        Boton(barra, "Limpiar", self.limpiar_todo).pack(side="right")
        Boton(barra, "Guardar log", self.guardar_log_actual).pack(side="right", padx=(0, 6))

    # ------------------------------------------------------------------
    def _encabezado_panel(self, padre, titulo):
        """Barra superior de una tarjeta: titulo a la izquierda, extras a la derecha."""
        cinta = tk.Frame(padre, bg=Tema.PANEL, height=34)
        cinta.pack(side="top", fill="x")
        cinta.pack_propagate(False)
        tk.Label(cinta, text=titulo, bg=Tema.PANEL, fg=Tema.TENUE,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=12)
        return cinta

    def _construir_area_central(self):
        panel = tk.PanedWindow(self, orient="horizontal", bg=Tema.FONDO,
                               sashwidth=8, sashrelief="flat", borderwidth=0,
                               sashpad=0, opaqueresize=False)
        panel.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        # ---------------- Izquierda: editor ----------------
        izquierda = tk.Frame(panel, bg=Tema.FONDO)
        cinta = self._encabezado_panel(izquierda, "CÓDIGO FUENTE PHP")

        self.etiqueta_archivo = tk.Label(cinta, text="sin título", bg=Tema.PANEL,
                                         fg=Tema.APAGADO, font=("Consolas", 9))
        self.etiqueta_archivo.pack(side="right", padx=12)

        self.editor = EditorPHP(izquierda, al_cambiar_cursor=self._actualizar_posicion)
        self.editor.pack(fill="both", expand=True)
        panel.add(izquierda, minsize=440, width=610, stretch="always")

        # ---------------- Derecha: resultados ----------------
        derecha = tk.Frame(panel, bg=Tema.FONDO)
        panel.add(derecha, minsize=430, stretch="always")

        vertical = tk.PanedWindow(derecha, orient="vertical", bg=Tema.FONDO,
                                  sashwidth=8, sashrelief="flat", borderwidth=0,
                                  opaqueresize=False)
        vertical.pack(fill="both", expand=True)

        # Consolas de salida
        marco_pestanas = tk.Frame(vertical, bg=Tema.EDITOR, highlightthickness=1,
                                  highlightbackground=Tema.BORDE)
        self.pestanas = ttk.Notebook(marco_pestanas)
        self.pestanas.pack(fill="both", expand=True)

        self.salida_lexico     = self._crear_consola("Léxico")
        self.salida_sintactico = self._crear_consola("Sintáctico")
        self.salida_semantico  = self._crear_consola("Semántico")
        self.salida_simbolos   = self._crear_consola("Tabla de símbolos")
        vertical.add(marco_pestanas, minsize=220, height=420, stretch="always")

        # Tabla de errores
        marco_errores = tk.Frame(vertical, bg=Tema.EDITOR, highlightthickness=1,
                                 highlightbackground=Tema.BORDE)
        cinta_err = self._encabezado_panel(marco_errores, "ERRORES DETECTADOS")
        self.etiqueta_conteo = tk.Label(cinta_err, text="", bg=Tema.PANEL, fg=Tema.APAGADO,
                                        font=("Segoe UI", 9))
        self.etiqueta_conteo.pack(side="right", padx=12)

        contenedor = tk.Frame(marco_errores, bg=Tema.EDITOR)
        contenedor.pack(fill="both", expand=True)

        self.tabla = ttk.Treeview(contenedor, columns=("linea", "tipo", "descripcion"),
                                  show="headings", selectmode="browse")
        self.tabla.heading("linea", text="LÍNEA")
        self.tabla.heading("tipo", text="TIPO")
        self.tabla.heading("descripcion", text="DESCRIPCIÓN")
        self.tabla.column("linea", width=64, anchor="center", stretch=False)
        self.tabla.column("tipo", width=118, anchor="w", stretch=False)
        self.tabla.column("descripcion", width=520, anchor="w")

        barra_tabla = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla.yview,
                                    style="Fino.Vertical.TScrollbar")
        self.tabla.configure(yscrollcommand=barra_tabla.set)
        barra_tabla.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)

        self.tabla.tag_configure("lexico", foreground=Tema.ERROR)
        self.tabla.tag_configure("sintactico", foreground=Tema.ERROR)
        self.tabla.tag_configure("semantico", foreground=Tema.ERROR)
        self.tabla.tag_configure("advertencia", foreground=Tema.AVISO)
        self.tabla.tag_configure("vacio", foreground=Tema.APAGADO)

        self.tabla.bind("<Double-1>", self._ir_a_error)
        self.tabla.bind("<Return>", self._ir_a_error)

        vertical.add(marco_errores, minsize=140, height=220)

        self._tabla_vacia()

    def _crear_consola(self, titulo):
        marco = tk.Frame(self.pestanas, bg=Tema.EDITOR)
        self.pestanas.add(marco, text=f"  {titulo}  ")

        barra = ttk.Scrollbar(marco, orient="vertical", style="Fino.Vertical.TScrollbar")
        barra.pack(side="right", fill="y")

        texto = tk.Text(marco, wrap="word", bg=Tema.EDITOR, fg=Tema.TEXTO,
                        font=FUENTE_CONSOLA, relief="flat", borderwidth=0,
                        padx=14, pady=12, spacing1=1, spacing3=1,
                        selectbackground="#3a3f57",
                        yscrollcommand=barra.set, state="disabled")
        texto.pack(side="left", fill="both", expand=True)
        barra.config(command=texto.yview)

        texto.tag_configure("titulo", foreground=Tema.ACENTO_ALT, font=("Consolas", 11, "bold"),
                            spacing1=4, spacing3=6)
        texto.tag_configure("seccion", foreground=Tema.TEXTO, font=("Consolas", 10, "bold"),
                            spacing1=6, spacing3=3)
        texto.tag_configure("ok", foreground=Tema.OK)
        texto.tag_configure("error", foreground=Tema.ERROR)
        texto.tag_configure("advertencia", foreground=Tema.AVISO)
        texto.tag_configure("info", foreground=Tema.INFO)
        texto.tag_configure("tenue", foreground=Tema.APAGADO)
        texto.tag_configure("token", foreground=Tema.S_VARIABLE)
        return texto

    # ------------------------------------------------------------------
    def _construir_barra_estado(self):
        barra = tk.Frame(self, bg=Tema.BARRA, height=30)
        barra.pack(side="bottom", fill="x")
        barra.pack_propagate(False)

        self.punto_estado = tk.Label(barra, text="●", bg=Tema.BARRA, fg=Tema.TENUE,
                                     font=("Segoe UI", 11))
        self.punto_estado.pack(side="left", padx=(16, 6))

        self.etiqueta_estado = tk.Label(barra, text="", bg=Tema.BARRA, fg=Tema.TENUE,
                                        font=FUENTE_UI, anchor="w")
        self.etiqueta_estado.pack(side="left", fill="x", expand=True)

        self.etiqueta_posicion = tk.Label(barra, text="Ln 1, Col 1", bg=Tema.BARRA,
                                          fg=Tema.APAGADO, font=("Consolas", 9))
        self.etiqueta_posicion.pack(side="right", padx=16)

        tk.Label(barra, text="F5 analizar todo  ·  Ctrl+O abrir  ·  Ctrl+L limpiar",
                 bg=Tema.BARRA, fg=Tema.APAGADO, font=("Segoe UI", 8)).pack(side="right", padx=16)

    def _registrar_atajos(self):
        self.bind("<F5>", lambda _: self.analisis_completo())
        self.bind("<Control-o>", lambda _: self.abrir_archivo())
        self.bind("<Control-s>", lambda _: self.guardar_codigo())
        self.bind("<Control-l>", lambda _: self.limpiar_todo())

    def _estado(self, mensaje, color=Tema.TENUE):
        self.etiqueta_estado.config(text=mensaje, fg=color)
        self.punto_estado.config(fg=color)

    def _actualizar_posicion(self, fila, columna):
        self.etiqueta_posicion.config(text=f"Ln {fila}, Col {columna}")

    # ------------------------------------------------------------------
    # Utilidades de escritura en las consolas
    # ------------------------------------------------------------------
    def _escribir(self, widget, texto, tag=None):
        widget.config(state="normal")
        widget.insert("end", texto, tag or "")
        widget.config(state="disabled")
        widget.see("end")

    def _limpiar(self, widget):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.config(state="disabled")

    def _texto_de(self, widget):
        return widget.get("1.0", "end-1c")

    def _resumen(self, widget, etiquetas):
        """Escribe una linea de resumen tipo 'Tokens 77 · Errores 0'."""
        for i, (nombre, valor, tag) in enumerate(etiquetas):
            if i:
                self._escribir(widget, "   ·   ", "tenue")
            self._escribir(widget, f"{nombre} ", "tenue")
            self._escribir(widget, str(valor), tag)
        self._escribir(widget, "\n\n")

    # ------------------------------------------------------------------
    # Tabla de errores
    # ------------------------------------------------------------------
    def _tabla_vacia(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        self.tabla.insert("", "end", values=("", "", "Sin errores que mostrar."), tags=("vacio",))
        self.etiqueta_conteo.config(text="")

    def _limpiar_errores(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        self.editor.limpiar_marcas()
        self.etiqueta_conteo.config(text="")

    def _agregar_error(self, tipo, mensaje, tag=None):
        # Si estaba la fila de marcador de posicion, se retira antes de insertar.
        for fila in self.tabla.get_children():
            if self.tabla.item(fila, "tags")[0] == "vacio":
                self.tabla.delete(fila)

        linea = _linea_del_mensaje(mensaje)
        self.tabla.insert("", "end", values=(linea or "—", tipo, mensaje),
                          tags=(tag or tipo.lower(),))
        self.editor.marcar_linea(linea)
        self._actualizar_conteo()

    def _finalizar_tabla(self):
        """Muestra el marcador de posicion si el analisis no dejo hallazgos."""
        if not self.tabla.get_children():
            self._tabla_vacia()

    def _actualizar_conteo(self):
        filas = self.tabla.get_children()
        if not filas:
            self.etiqueta_conteo.config(text="")
            return
        errores = sum(1 for f in filas if self.tabla.item(f, "tags")[0] != "advertencia")
        avisos = len(filas) - errores
        partes = []
        if errores:
            partes.append(f"{errores} error(es)")
        if avisos:
            partes.append(f"{avisos} advertencia(s)")
        self.etiqueta_conteo.config(text="   ".join(partes) or "")

    def _ir_a_error(self, _evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        linea = self.tabla.item(seleccion[0], "values")[0]
        if str(linea).isdigit():
            self.editor.ir_a_linea(int(linea))

    def _marcar_pestana(self, indice, titulo, cantidad):
        """Anade el conteo de hallazgos al titulo de la pestana."""
        if cantidad is None:
            texto = f"  {titulo}  "
        elif cantidad == 0:
            texto = f"  {titulo}  ✓  "
        else:
            texto = f"  {titulo}  {cantidad}  "
        self.pestanas.tab(indice, text=texto)

    def _codigo_o_aviso(self):
        codigo = self.editor.obtener_codigo().strip()
        if not codigo:
            messagebox.showwarning("Sin código",
                                   "Escriba o abra un archivo PHP antes de analizar.")
            return None
        return codigo

    # ------------------------------------------------------------------
    # 6. ACCIONES DE ANALISIS
    # ------------------------------------------------------------------
    def ejecutar_lexico(self, codigo=None, limpiar=True):
        codigo = codigo or self._codigo_o_aviso()
        if codigo is None:
            return None

        if limpiar:
            self._limpiar_errores()
        self._limpiar(self.salida_lexico)
        self.pestanas.select(0)

        resultado = analizar_lexico(codigo)
        salida = self.salida_lexico
        n_err = len(resultado['errores'])

        self._escribir(salida, "ANÁLISIS LÉXICO\n", "titulo")
        self._resumen(salida, [
            ("Tokens", len(resultado['tokens']), "info"),
            ("Errores", n_err, "error" if n_err else "ok"),
        ])

        self._escribir(salida, "TOKENS RECONOCIDOS\n", "seccion")
        for lineno, tipo, valor in resultado['tokens']:
            self._escribir(salida, f"  {lineno:>4}  ", "tenue")
            self._escribir(salida, f"{tipo:<20}", "token")
            self._escribir(salida, f" {valor!r}\n")

        if n_err:
            self._escribir(salida, "\nERRORES LÉXICOS\n", "seccion")
            for error in resultado['errores']:
                self._escribir(salida, f"  ✗ {error}\n", "error")
                self._agregar_error("Léxico", error, tag="lexico")
            self._estado(f"Análisis léxico: {n_err} error(es) encontrado(s).", Tema.ERROR)
        else:
            self._escribir(salida, "\n  ✓ Sin errores léxicos: todos los caracteres "
                                   "fueron reconocidos.\n", "ok")
            self._estado(f"Análisis léxico correcto · {len(resultado['tokens'])} tokens.", Tema.OK)

        self._finalizar_tabla()
        self._marcar_pestana(0, "Léxico", n_err)
        self.ultimo_log = ("lexico", self._texto_de(salida))
        return resultado

    def ejecutar_sintactico(self, codigo=None, limpiar=True):
        codigo = codigo or self._codigo_o_aviso()
        if codigo is None:
            return None

        if limpiar:
            self._limpiar_errores()
        self._limpiar(self.salida_sintactico)
        self.pestanas.select(1)

        resultado = analizar_sintactico(codigo)
        salida = self.salida_sintactico
        n_err = len(resultado['errores'])

        self._escribir(salida, "ANÁLISIS SINTÁCTICO\n", "titulo")
        self._resumen(salida, [
            ("Errores de sintaxis", n_err, "error" if n_err else "ok"),
        ])

        # Los errores lexicos se reportan primero: impiden un parseo confiable.
        if resultado['errores_lexicos']:
            self._escribir(salida, "ATENCIÓN: el código contiene errores léxicos\n", "seccion")
            for error in resultado['errores_lexicos']:
                self._escribir(salida, f"  ✗ {error}\n", "error")
                self._agregar_error("Léxico", error, tag="lexico")
            self._escribir(salida, "\n")

        if n_err:
            self._escribir(salida, "ERRORES SINTÁCTICOS\n", "seccion")
            for error in resultado['errores']:
                self._escribir(salida, f"  ✗ {error}\n", "error")
                self._agregar_error("Sintáctico", error, tag="sintactico")
            self._estado(f"Análisis sintáctico: {n_err} error(es) encontrado(s).", Tema.ERROR)
        else:
            self._escribir(salida, "  ✓ Análisis completado: 0 errores de sintaxis.\n", "ok")
            self._escribir(salida, "  El código PHP está escrito correctamente según la "
                                   "gramática definida.\n", "tenue")
            self._estado("Análisis sintáctico correcto.", Tema.OK)

        self._finalizar_tabla()
        self._marcar_pestana(1, "Sintáctico", n_err)
        self.ultimo_log = ("sintactico", self._texto_de(salida))
        return resultado

    def ejecutar_semantico(self, codigo=None, limpiar=True):
        codigo = codigo or self._codigo_o_aviso()
        if codigo is None:
            return None

        if limpiar:
            self._limpiar_errores()
        self._limpiar(self.salida_semantico)
        self._limpiar(self.salida_simbolos)
        self.pestanas.select(2)

        resultado = analizar_semantico(codigo)
        salida = self.salida_semantico
        n_err = len(resultado['errores'])
        n_adv = len(resultado['advertencias'])

        self._escribir(salida, "ANÁLISIS SEMÁNTICO\n", "titulo")
        self._resumen(salida, [
            ("Errores", n_err, "error" if n_err else "ok"),
            ("Advertencias", n_adv, "advertencia" if n_adv else "ok"),
        ])

        if resultado['errores_sintacticos']:
            self._escribir(salida, "  ⚠ Hay errores sintácticos; el análisis semántico "
                                   "puede estar incompleto.\n\n", "advertencia")

        self._escribir(salida, f"ERRORES SEMÁNTICOS ({n_err})\n", "seccion")
        if n_err:
            for error in resultado['errores']:
                self._escribir(salida, f"  ✗ {error}\n", "error")
                self._agregar_error("Semántico", error, tag="semantico")
        else:
            self._escribir(salida, "  (ninguno)\n", "tenue")

        self._escribir(salida, f"\nADVERTENCIAS SEMÁNTICAS ({n_adv})\n", "seccion")
        if n_adv:
            for adv in resultado['advertencias']:
                self._escribir(salida, f"  ⚠ {adv}\n", "advertencia")
                self._agregar_error("Advertencia", adv, tag="advertencia")
        else:
            self._escribir(salida, "  (ninguna)\n", "tenue")

        if not n_err and not n_adv:
            self._escribir(salida, "\n  ✓ El código es semánticamente correcto.\n", "ok")
            self._estado("Análisis semántico correcto.", Tema.OK)
        else:
            self._estado(f"Análisis semántico: {n_err} error(es), {n_adv} advertencia(s).",
                         Tema.ERROR if n_err else Tema.AVISO)

        self._mostrar_tabla_simbolos(resultado)
        self._finalizar_tabla()
        self._marcar_pestana(2, "Semántico", n_err + n_adv)
        self.ultimo_log = ("semantico", self._texto_de(salida))
        return resultado

    def _mostrar_tabla_simbolos(self, resultado):
        salida = self.salida_simbolos
        self._escribir(salida, "TABLA DE SÍMBOLOS\n", "titulo")
        self._resumen(salida, [
            ("Constantes", len(resultado['constantes']), "info"),
            ("Variables", len(resultado['variables']), "info"),
            ("Funciones", len(resultado['funciones']), "info"),
        ])

        def bloque(titulo, datos, formato):
            self._escribir(salida, f"{titulo} ({len(datos)})\n", "seccion")
            if not datos:
                self._escribir(salida, "  (ninguna)\n\n", "tenue")
                return
            for nombre, info in datos.items():
                self._escribir(salida, "  " + formato(nombre, info) + "\n")
            self._escribir(salida, "\n")

        bloque("CONSTANTES", resultado['constantes'],
               lambda n, i: f"{n:<22} tipo: {i['tipo']:<12} línea: {i['lineno']}")
        bloque("VARIABLES", resultado['variables'],
               lambda n, i: f"{n:<22} tipo: {i['tipo']:<12} línea: {i['lineno']}")
        bloque("FUNCIONES", resultado['funciones'],
               lambda n, i: f"{n:<22} parámetros: {i['min']}-{i['max']:<6} línea: {i['lineno']}")

    def analisis_completo(self):
        """Ejecuta los tres analizadores en cadena sobre el mismo código."""
        codigo = self._codigo_o_aviso()
        if codigo is None:
            return

        self._limpiar_errores()
        self._estado("Analizando…", Tema.INFO)
        self.update_idletasks()

        lex = self.ejecutar_lexico(codigo, limpiar=False)
        sin = self.ejecutar_sintactico(codigo, limpiar=False)
        sem = self.ejecutar_semantico(codigo, limpiar=False)

        total = len(lex['errores']) + len(sin['errores']) + len(sem['errores'])
        avisos = len(sem['advertencias'])

        # El log del analisis completo agrupa la salida de los tres paneles.
        self.ultimo_log = ("completo", (
            self._texto_de(self.salida_lexico) + "\n\n" +
            self._texto_de(self.salida_sintactico) + "\n\n" +
            self._texto_de(self.salida_semantico)
        ))

        if total == 0 and avisos == 0:
            self.pestanas.select(2)
            self._estado("Análisis completo: el código no presenta errores.", Tema.OK)
        else:
            primera = self.tabla.get_children()
            if primera:
                self.tabla.selection_set(primera[0])
                self.tabla.focus(primera[0])
            self._estado(
                f"Análisis completo: {total} error(es) y {avisos} advertencia(s). "
                f"Doble clic en un error para ir a su línea.",
                Tema.ERROR if total else Tema.AVISO,
            )

    # ------------------------------------------------------------------
    # 7. ARCHIVOS Y LOGS
    # ------------------------------------------------------------------
    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Abrir archivo PHP",
            filetypes=[("Archivos PHP", "*.php"), ("Todos los archivos", "*.*")],
            initialdir="pruebas" if os.path.isdir("pruebas") else ".",
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                self.editor.establecer_codigo(archivo.read())
        except OSError as e:
            messagebox.showerror("Error al abrir", str(e))
            return

        self.ruta_actual = ruta
        self.etiqueta_archivo.config(text=os.path.basename(ruta), fg=Tema.TENUE)
        self._limpiar_errores()
        self._tabla_vacia()
        self._estado(f"Archivo abierto: {ruta}", Tema.INFO)

    def guardar_codigo(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar código PHP", defaultextension=".php",
            filetypes=[("Archivos PHP", "*.php")],
            initialdir="pruebas" if os.path.isdir("pruebas") else ".",
        )
        if not ruta:
            return
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(self.editor.obtener_codigo())
        self.ruta_actual = ruta
        self.etiqueta_archivo.config(text=os.path.basename(ruta), fg=Tema.TENUE)
        self._estado(f"Código guardado en: {ruta}", Tema.OK)

    def guardar_log_actual(self):
        if not self.ultimo_log:
            messagebox.showwarning("Sin resultados",
                                   "Ejecute primero un análisis para poder guardar su log.")
            return

        tipo, contenido = self.ultimo_log
        usuario = INTEGRANTES[self.combo_integrante.get()]

        encabezado = (
            f"Archivo analizado: {self.ruta_actual or '(código escrito en la interfaz)'}\n"
            f"Usuario Git: {usuario}\n"
            f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        )

        ruta_log = guardar_log(tipo, usuario, encabezado + contenido + "\n")
        self._estado(f"Log generado: {ruta_log}", Tema.OK)
        messagebox.showinfo("Log generado", f"Se guardó el log en:\n{ruta_log}")

    def limpiar_todo(self):
        for consola in (self.salida_lexico, self.salida_sintactico,
                        self.salida_semantico, self.salida_simbolos):
            self._limpiar(consola)
        self._limpiar_errores()
        self._tabla_vacia()
        for i, titulo in enumerate(("Léxico", "Sintáctico", "Semántico")):
            self._marcar_pestana(i, titulo, None)
        self.ultimo_log = None
        self._estado("Consola limpiada.", Tema.TENUE)


# ==========================================
# 8. PUNTO DE ENTRADA
# ==========================================
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
