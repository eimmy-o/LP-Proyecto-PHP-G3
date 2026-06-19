import ply.yacc as yacc
from lexer import tokens 
from datetime import datetime
import os

# ==========================================
# 1. REGLAS GENERALES Y ESTRUCTURA BASE
# ==========================================

# REGLA PADRE 
def p_programa(p):
    '''programa : declaraciones'''
    pass

def p_declaraciones(p):
    '''declaraciones : declaracion
                     | declaracion declaraciones'''
    pass


def p_declaracion(p):
    '''declaracion : APERTURA_PHP 
                   | CIERRE_PHP''' 
    pass


# ==========================================
# 2. REGLAS SINTÁCTICAS 
# ==========================================

# --- INICIO APORTE EIMMY OCHOA --- #


# --- FIN APORTE EIMMY OCHOA --- #


# --- INICIO APORTE DIEGO PARRALES --- #


# --- FIN APORTE DIEGO PARRALES --- #


# --- INICIO APORTE JULIANA BURGOS --- #


# --- FIN APORTE JULIANA BURGOS --- #


# ==========================================
# 3. MANEJO DE ERRORES SINTÁCTICOS Y LOGS
# ==========================================
errores_sintacticos = []

def p_error(p):
    global errores_sintacticos
    if p:
        mensaje = f"Error de Sintaxis: Se esperaba otra estructura, pero se encontro '{p.value}' (tipo {p.type}) en la linea {p.lineno}"
    else:
        mensaje = "Error de Sintaxis: Fin de archivo inesperado"
    
    print(mensaje)
    errores_sintacticos.append(mensaje)

# Construimos el parser
parser = yacc.yacc()

def test_sintactico(ruta_archivo, usuario_git):
    global errores_sintacticos
    errores_sintacticos = [] # Limpiar errores previos por cada test
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = archivo.read()
    
    # Analizamos el código
    parser.parse(data)
    
    # Generar log
    fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
    nombre_log = f"sintactico-{usuario_git}-{fecha_hora}.txt"
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    ruta_log = os.path.join('logs', nombre_log)
    
    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("=== RESULTADO DEL ANALISIS SINTACTICO ===\n\n")
        if len(errores_sintacticos) == 0:
            f.write("Analisis completado: 0 errores de sintaxis.\nEl codigo PHP esta escrito correctamente segun la gramatica definida.\n")
        else:
            f.write("ERRORES SINTACTICOS ENCONTRADOS:\n")
            for error in errores_sintacticos:
                f.write(error + "\n")
                
    print(f"Test completado. Log generado en: {ruta_log}")

# --- PUNTO DE EJECUCIÓN ---
if __name__ == '__main__':
    #test_sintactico('pruebas/algoritmo_eimmy.php', 'eimmy-o')
    pass