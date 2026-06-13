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
    'IF', 'ELSE', 'ECHO', 'FUNCTION', 'RETURN',
    'LLAVE_IZQ', 'LLAVE_DER', 'PAR_IZQ', 'PAR_DER',
    'COR_IZQ', 'COR_DER', 'PUNTO_COMA', 'COMA',
    'ID'

    # --- DIEGO PARRALES --- #
    
    # --- JULIANA BURGOS --- #
    
]

# ==========================================
# 2. EXPRESIONES REGULARES 
# ==========================================

# --- INICIO APORTE EIMMY OCHOA --- #

# palabras reservadas 
reservadas_eimmy = {
    'if': 'IF',
    'else': 'ELSE',
    'echo': 'ECHO',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'true': 'BOOLEANO',  
    'false': 'BOOLEANO'
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
    t.type = reservadas_eimmy.get(t.value, 'ID')    
    return t

# --- FIN APORTE EIMMY OCHOA --- #



# --- INICIO APORTE DIEGO PARRALES --- #


# --- FIN APORTE DIEGO PARRALES --- #



# --- INICIO APORTE JULIANA BURGOS --- #


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

