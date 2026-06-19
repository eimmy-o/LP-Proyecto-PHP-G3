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


# Aquí se agruparán todas las sentencias válidas de PHP (aportes de eimmy, diego y juliana)
def p_declaracion(p):
    '''declaracion : APERTURA_PHP 
                   | CIERRE_PHP
                   | asignacion_simple
                   | arreglo_indexado
                   | estructura_if_else
                   | funcion_retorno
                   | impresion
                   | return_statement''' 
    pass


# ==========================================
# 2. REGLAS SINTÁCTICAS 
# ==========================================

# --- INICIO APORTE EIMMY OCHOA --- #

# Asignación simple de variables primitivas
def p_asignacion_simple(p):
    '''asignacion_simple : VARIABLE ASIGNACION valor_primitivo PUNTO_COMA'''
    pass

# Estructura de datos: Arreglo indexado
def p_arreglo_indexado(p):
    '''arreglo_indexado : VARIABLE ASIGNACION COR_IZQ lista_valores COR_DER PUNTO_COMA'''
    pass

def p_lista_valores(p):
    '''lista_valores : valor_primitivo
                     | lista_valores COMA valor_primitivo
                     | empty'''
    pass

# Estructura de control: Condicional if-else
def p_estructura_if_else(p):
    '''estructura_if_else : IF PAR_IZQ condicion PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER
                          | IF PAR_IZQ condicion PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER ELSE LLAVE_IZQ bloque_codigo LLAVE_DER'''
    pass

# Definición de funciones: Función clásica con retorno
def p_funcion_retorno(p):
    '''funcion_retorno : FUNCTION ID PAR_IZQ parametros PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER'''
    pass

def p_parametros(p):
    '''parametros : VARIABLE
                  | parametros COMA VARIABLE
                  | empty'''
    pass

def p_return_statement(p):
    '''return_statement : RETURN expresion PUNTO_COMA'''
    pass

def p_valor_primitivo(p):
    '''valor_primitivo : ENTERO
                       | CADENA
                       | BOOLEANO
                       | VARIABLE'''
    pass

def p_bloque_codigo(p):
    '''bloque_codigo : declaracion
                     | bloque_codigo declaracion
                     | empty'''
    pass

def p_empty(p):
    '''empty :'''
    pass

# --- FIN APORTE EIMMY OCHOA --- #


# --- INICIO APORTE DIEGO PARRALES --- #

# necesito estas reglas para mi parte, ahi las completas estan solo declaradas para hacer mis prubeas (eimmy)
# son tus reglas transversales (matemáticas, condiciones e impresión)
def p_condicion(p):
    '''condicion : valor_primitivo IGUALDAD valor_primitivo'''
    pass

def p_expresion(p):
    '''expresion : valor_primitivo SUMA valor_primitivo'''
    pass
    
def p_impresion(p):
    '''impresion : ECHO valor_primitivo PUNTO_COMA'''
    pass

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