import ply.lex as lex
from datetime import datetime
import os

# ==========================================
# 1. LISTA DE TOKENS 
# ==========================================
tokens = [
    # --- EIMMY OCHOA --- #
    'VARIABLE', 'ENTERO', 'BOOLEANO', 'CADENA',
    'ASIGNACION', 'IGUALDAD', 'SUMA',
    'IF', 'ELSE', 'ELSEIF', 'ECHO', 'FUNCTION', 'RETURN',
    'LLAVE_IZQ', 'LLAVE_DER', 'PAR_IZQ', 'PAR_DER',
    'COR_IZQ', 'COR_DER', 'PUNTO_COMA', 'COMA',
    'ID', 'APERTURA_PHP', 'CIERRE_PHP',

    # --- DIEGO PARRALES --- #
    'FLOTANTE',
    'SWITCH', 'CASE', 'DEFAULT', 'BREAK', 'WHILE', 'FOR',
    'DEFINE',
    'FLECHA', 'CONCATENACION', 'DOS_PUNTOS',
    'RESTA', 'MULTIPLICACION', 'DIVISION', 'MODULO',
    'IGUALDAD_ESTRICTA', 'DESIGUALDAD',
    'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL',
    'AND', 'OR', 'NOT', 'SUMA_ASIG',
    'INCREMENTO', 'DECREMENTO',

    # --- JULIANA BURGOS --- #
    'FOREACH', 'AS', 'CLASS',
    'PUBLIC', 'PRIVATE', 'PROTECTED',
    'STATIC', 'NEW', 'OBJETO_OP'

]

# ==========================================
# 2. EXPRESIONES REGULARES 
# ==========================================

# --- INICIO APORTE EIMMY OCHOA --- #

# inicio y cierre de archivo php
t_APERTURA_PHP = r'<\?php'
t_CIERRE_PHP   = r'\?>'

# palabras reservadas
reservadas_eimmy = {
    'if': 'IF',
    'else': 'ELSE',
    'elseif': 'ELSEIF',   # PHP admite 'elseif' junto y 'else if' separado
    'echo': 'ECHO',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'true': 'BOOLEANO',
    'false': 'BOOLEANO'
}

# palabras reservadas - Diego Parrales
reservadas_diego = {
    'switch':  'SWITCH',
    'case':    'CASE',
    'default': 'DEFAULT',
    'break':   'BREAK',
    'while':   'WHILE',
    'for':     'FOR',
    'define':  'DEFINE',
}

# palabras reservadar - Juliana Burgos
reservadas_juliana = { 
    'foreach'   : 'FOREACH',
    'as'        : 'AS',
    'class'     : 'CLASS',
    'public'    : 'PUBLIC',
    'private'   : 'PRIVATE',
    'protected' : 'PROTECTED',
    'static'    : 'STATIC',
    'new'       : 'NEW',
}

# delimitadores 
t_LLAVE_IZQ  = r'\{'
t_LLAVE_DER  = r'\}'
t_PAR_IZQ    = r'\('
t_PAR_DER    = r'\)'
t_COR_IZQ    = r'\['
t_COR_DER    = r'\]'
t_PUNTO_COMA = r';'
t_COMA       = r','

# operadores 
t_IGUALDAD   = r'=='  
t_ASIGNACION = r'='
t_SUMA       = r'\+'

# --- Tipos de datos --- # 
# cadenas
t_CADENA = r'\"[^\"]*\"'

# flotantes - Diego Parrales
def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# enteros
def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# variables
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# identificador para palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    todas_reservadas = {**reservadas_eimmy, **reservadas_diego,**reservadas_juliana}
    t.type = todas_reservadas.get(t.value, 'ID')
    return t

# --- FIN APORTE EIMMY OCHOA --- #



# --- INICIO APORTE DIEGO PARRALES --- #

# ignorar espacios en blanco y tabulaciones
t_ignore = ' \t\r'

# comentarios de una linea (// y #) - descartar sin retornar token
def t_COMENTARIO_LINEA(t):
    r'(//|\#)[^\n]*'
    pass

# comentarios de bloque (/* ... */) - descartar y contar saltos de linea
def t_COMENTARIO_BLOQUE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# operadores de comparacion (patrones mas largos primero para correcta precedencia)
t_IGUALDAD_ESTRICTA = r'==='
t_MAYOR_IGUAL       = r'>='
t_MENOR_IGUAL       = r'<='
t_DESIGUALDAD       = r'!='
t_FLECHA            = r'=>'
t_SUMA_ASIG         = r'\+='
t_AND               = r'&&'
t_OR                = r'\|\|'

# incremento y decremento (usados en el paso del bucle for: $i++)
# Sus regex son mas largas que las de SUMA y RESTA, por lo que PLY las evalua
# primero y '$i++' no se lee como '$i + + '.
t_INCREMENTO        = r'\+\+'
t_DECREMENTO        = r'--'

# operadores aritmeticos y de concatenacion
t_RESTA             = r'-'
t_MULTIPLICACION    = r'\*'
t_DIVISION          = r'/'
t_MODULO            = r'%'
t_CONCATENACION     = r'\.'

# operadores de comparacion simples (van despues de los de 2 caracteres)
t_MAYOR             = r'>'
t_MENOR             = r'<'
t_NOT               = r'!'

# delimitador adicional para case/default
t_DOS_PUNTOS        = r':'

# --- FIN APORTE DIEGO PARRALES --- #



# --- INICIO APORTE JULIANA BURGOS --- #
# Operador de acceso a objetos: $auto->marca
# Se define como función para tener prioridad sobre t_RESTA (-) definina por Diego
def t_OBJETO_OP(t):
    r'->'
    return t
# --- FIN APORTE JULIANA BURGOS --- #




# ==========================================
# 3. MANEJO DE ERRORES 
# ==========================================
def t_error(t):
    mensaje = f"Error lexico: Caracter no valido '{t.value[0]}' en la linea {t.lexer.lineno}"
    print(mensaje)
    # Guardamos el error en el log también
    if not hasattr(t.lexer, 'log_errores'):
        t.lexer.log_errores = []
    t.lexer.log_errores.append(mensaje)
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ==========================================
# 4. CONSTRUCCIÓN DEL LEXER Y GENERACIÓN DE LOGS
# ==========================================
lexer = lex.lex()


def analizar_archivo(ruta_archivo, nombre_desarrollador):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = archivo.read()
    
    lexer.input(data)
    
    # contenido del log
    log_content = "=== RESULTADO DEL ANALISIS LEXICO ===\n\n"
    log_content += "TOKENS RECONOCIDOS:\n"
    
    # sacamos los tokens
    while True:
        tok = lexer.token()
        if not tok: 
            break      
        log_content += f"Linea {tok.lineno}: {tok.type} -> '{tok.value}'\n"
    
    # errores por si hay
    if hasattr(lexer, 'log_errores') and lexer.log_errores:
        log_content += "\nERRORES ENCONTRADOS:\n"
        for error in lexer.log_errores:
            log_content += error + "\n"
            
    # archivo de salida
    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"lexico-{nombre_desarrollador}-{fecha_hora}.txt"
    
    # carpeta logs por si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    ruta_log = os.path.join('logs', nombre_log)
    
    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write(log_content)
        
    print(f"Analisis completado. Log generado en: {ruta_log}")


# --- EJECUCIÓN ---
if __name__ == '__main__':
    #analizar_archivo('pruebas/algoritmo_eimmy.php', 'EimmyOchoa')
    #analizar_archivo('pruebas/algoritmo_diego.php', 'DiegoParrales')
    analizar_archivo('pruebas/algoritmo_juliana.php', 'JulianaBurgos')
    pass