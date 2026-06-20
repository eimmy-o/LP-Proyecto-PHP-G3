import ply.yacc as yacc
from lexer import tokens, lexer
from datetime import datetime
import os

# ==========================================
# 0. PRECEDENCIA DE OPERADORES (Diego Parrales)
#    De menor (arriba) a mayor (abajo) prioridad. Permite escribir las
#    expresiones de forma recursiva sin ambiguedad (1 o mas operadores).
# ==========================================
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'IGUALDAD', 'IGUALDAD_ESTRICTA', 'DESIGUALDAD'),
    ('nonassoc', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
    ('left', 'CONCATENACION'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('right', 'NOT', 'UMINUS'),
)


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
                   | return_statement
                   | asignacion_compuesta
                   | arreglo_asociativo
                   | definicion_constante
                   | switch_sentencia
                   | while_sentencia
                   | definicion_funcion_default
                   | llamada_sentencia
                   | break_sentencia
                   | foreach_sentencia
                   | clase
                   | variable_estatica
                   | closure'''
    pass
 
 # Variabale estatica 
 def p_variable_estatica(p):
    '''
    variable_estatica : STATIC VARIABLE ASIGNACION expresion PUNTO_COMA
    '''
    pass


# ==========================================
# 2. REGLAS SINTÁCTICAS
# ==========================================

# --- INICIO APORTE EIMMY OCHOA --- #

# Asignación simple de variables primitivas
# NOTA (Diego): se cambio 'valor_primitivo' por 'expresion' para soportar
# asignaciones con expresiones/condiciones (p. ej. $x = $a * 2 + $b;).
# Como 'expresion : valor_primitivo' esta incluida, los casos simples de
# Eimmy siguen funcionando igual.
def p_asignacion_simple(p):
    '''asignacion_simple : VARIABLE ASIGNACION expresion PUNTO_COMA'''
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

# =====================================================================
# 2.1 REGLAS TRANSVERSALES (las que Eimmy dejo declaradas para completar)
#     Expresiones aritmeticas y concatenacion, condiciones (booleanas)
#     con uno o mas operadores/conectores, e impresion.
# =====================================================================

# ---- IMPRESION: echo (la funcion 'print' se reconoce como llamada a funcion) ----
def p_impresion(p):
    '''impresion : ECHO expresion PUNTO_COMA'''
    pass

# ---- CONDICION: una expresion booleana completa (1 o mas conectores logicos) ----
# Se usa en la cabecera del if/while. Al ser 'expresion', admite
# comparaciones encadenadas con && y || , p. ej.  ($a >= 18) && $reg
def p_condicion(p):
    '''condicion : expresion'''
    pass

# ---- EXPRESIONES: definicion recursiva con precedencia (1 o mas operadores) ----

# Aritmeticas y de concatenacion
def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULTIPLICACION expresion
                 | expresion DIVISION expresion
                 | expresion MODULO expresion
                 | expresion CONCATENACION expresion'''
    pass

# Comparaciones (relacionales y de igualdad)
def p_expresion_comparacion(p):
    '''expresion : expresion IGUALDAD expresion
                 | expresion IGUALDAD_ESTRICTA expresion
                 | expresion DESIGUALDAD expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion'''
    pass

# Conectores logicos (&&, ||)
def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    pass

# Negacion logica y signo negativo
def p_expresion_not(p):
    '''expresion : NOT expresion'''
    pass

def p_expresion_unaria(p):
    '''expresion : RESTA expresion %prec UMINUS'''
    pass

# Expresion entre parentesis
def p_expresion_agrupada(p):
    '''expresion : PAR_IZQ expresion PAR_DER'''
    pass

# Una llamada a funcion tambien es una expresion (resultado)
def p_expresion_llamada(p):
    '''expresion : llamada_funcion'''
    pass

# Atomos: valores primitivos (Eimmy) + flotante + identificadores/constantes
def p_expresion_valor(p):
    '''expresion : valor_primitivo
                 | FLOTANTE
                 | ID'''
    pass


# =====================================================================
# 2.2 LECTURA DE DATOS POR TECLADO
#     En PHP la entrada por consola se hace con readline() o fgets(STDIN).
#     Ambas encajan en 'llamada_funcion' (ID '(' argumentos ')'), por lo que
#     no necesita una regla propia. Ej:  $nombre = readline();
# =====================================================================

def p_llamada_funcion(p):
    '''llamada_funcion : ID PAR_IZQ argumentos PAR_DER
                       | ID PAR_IZQ PAR_DER'''
    pass

def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''
    pass

def p_llamada_sentencia(p):
    '''llamada_sentencia : llamada_funcion PUNTO_COMA'''
    pass

def p_arreglo_asociativo(p):
    '''arreglo_asociativo : VARIABLE ASIGNACION COR_IZQ lista_pares COR_DER PUNTO_COMA'''
    pass

def p_lista_pares(p):
    '''lista_pares : par
                   | lista_pares COMA par'''
    pass

def p_par(p):
    '''par : expresion FLECHA expresion'''
    pass


# =====================================================================
# 2.4 ESTRUCTURA DE CONTROL: switch / case / default
# =====================================================================
def p_switch_sentencia(p):
    '''switch_sentencia : SWITCH PAR_IZQ expresion PAR_DER LLAVE_IZQ lista_casos LLAVE_DER'''
    pass

def p_lista_casos(p):
    '''lista_casos : caso
                   | lista_casos caso'''
    pass

def p_caso(p):
    '''caso : CASE expresion DOS_PUNTOS bloque_codigo
            | DEFAULT DOS_PUNTOS bloque_codigo'''
    pass

# break como sentencia (valido dentro de switch y de bucles)
def p_break_sentencia(p):
    '''break_sentencia : BREAK PUNTO_COMA'''
    pass

# Estructura de control de apoyo: while
def p_while_sentencia(p):
    '''while_sentencia : WHILE PAR_IZQ expresion PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER'''
    pass

# Asignacion compuesta (+=), usada tipicamente dentro de bucles
def p_asignacion_compuesta(p):
    '''asignacion_compuesta : VARIABLE SUMA_ASIG expresion PUNTO_COMA'''
    pass


# =====================================================================
# 2.5 DECLARACION DE CONSTANTES
# =====================================================================
def p_definicion_constante(p):
    '''definicion_constante : DEFINE PAR_IZQ expresion COMA expresion PAR_DER PUNTO_COMA'''
    pass


# =====================================================================
# 2.6 TIPO DE FUNCION OBLIGATORIO: funcion con parametros por defecto
#     function saludar($nombre = "Invitado") { ... }
# =====================================================================
def p_definicion_funcion_default(p):
    '''definicion_funcion_default : FUNCTION ID PAR_IZQ parametros_def PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER'''
    pass

# Lista de parametros que admite valores por defecto (al menos uno con '=')
def p_parametros_def(p):
    '''parametros_def : parametro_def
                      | parametros_def COMA parametro_def'''
    pass

def p_parametro_def(p):
    '''parametro_def : VARIABLE
                     | VARIABLE ASIGNACION expresion'''
    pass

# --- FIN APORTE DIEGO PARRALES --- #


# --- INICIO APORTE JULIANA BURGOS --- #
#   (reglas de Juliana: foreach, clases/objetos y closures)


def p_foreach(p):
    '''
    foreach_sentencia : FOREACH PAR_IZQ VARIABLE AS VARIABLE PAR_DER
                        LLAVE_IZQ bloque_codigo LLAVE_DER
    '''
    pass

# Definicion de clases 
def p_clase(p):
    '''
    clase : CLASS ID LLAVE_IZQ miembros_clase LLAVE_DER
    '''
    pass


def p_miembros_clase(p):
    '''
    miembros_clase : miembro_clase
                    | miembros_clase miembro_clase
                    | empty
    '''
    pass

def p_miembro_clase(p):
    '''
    miembro_clase : modificador VARIABLE ASIGNACION expresion PUNTO_COMA
    '''
    pass

def p_modificador(p):
    '''
    modificador : PUBLIC
                | PRIVATE
                | PROTECTED
    '''
    pass


# clousers
def p_closure(p):
    '''
    closure : VARIABLE ASIGNACION FUNCTION
              PAR_IZQ parametros PAR_DER
              LLAVE_IZQ bloque_codigo LLAVE_DER
              PUNTO_COMA
    '''
    pass

# --- FIN APORTE JULIANA BURGOS --- #


# ==========================================
# 3. MANEJO DE ERRORES SINTÁCTICOS Y LOGS
# ==========================================
errores_sintacticos = []

def p_error(p):
    global errores_sintacticos
    if p:
        mensaje = (f"Error de Sintaxis: token inesperado '{p.value}' "
                   f"(tipo {p.type}) en la linea {p.lineno}")
    else:
        mensaje = ("Error de Sintaxis: fin de archivo inesperado "
                   "(posible falta de ';', '}' o '?>')")
    print(mensaje)
    errores_sintacticos.append(mensaje)

# Construimos el parser
parser = yacc.yacc()

def test_sintactico(ruta_archivo, usuario_git):
    global errores_sintacticos
    errores_sintacticos = [] 

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = archivo.read()

    lexer.lineno = 1
    if hasattr(lexer, 'log_errores'):
        lexer.log_errores = []

    parser.parse(data, lexer=lexer)

    fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
    nombre_log = f"sintactico-{usuario_git}-{fecha_hora}.txt"

    if not os.path.exists('logs'):
        os.makedirs('logs')

    ruta_log = os.path.join('logs', nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("=== RESULTADO DEL ANALISIS SINTACTICO ===\n\n")
        f.write(f"Archivo analizado: {ruta_archivo}\n")
        f.write(f"Usuario Git: {usuario_git}\n\n")
        if len(errores_sintacticos) == 0:
            f.write("Analisis completado: 0 errores de sintaxis.\n")
            f.write("El codigo PHP esta escrito correctamente segun la gramatica definida.\n")
        else:
            f.write(f"ERRORES SINTACTICOS ENCONTRADOS ({len(errores_sintacticos)}):\n")
            for error in errores_sintacticos:
                f.write(error + "\n")

    if errores_sintacticos:
        print(f"Test completado con {len(errores_sintacticos)} error(es). Log: {ruta_log}")
    else:
        print(f"Test completado sin errores. Log: {ruta_log}")

if __name__ == '__main__':
    # Algoritmo de prueba (Diego) (constantes, arreglo asociativo, switch,
    # while, funcion con parametros por defecto, expresiones y condiciones).
    test_sintactico('pruebas/algoritmo_diego.php', 'raydan90s')
    
