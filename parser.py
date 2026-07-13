import ply.yacc as yacc
from lexer import tokens, lexer
from datetime import datetime
import os

# Analizador semantico (Diego Parrales): el parser invoca sus "hooks" para
# inferir tipos, registrar constantes/variables y validar las operaciones.
from semantic import analizador_semantico

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
                   | for_sentencia
                   | incremento_sentencia
                   | definicion_funcion_default
                   | llamada_sentencia
                   | break_sentencia
                   | foreach_sentencia
                   | clase
                   | instanciacion_objeto
                   | variable_estatica
                   | closure'''
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
    # Hook semantico (Diego): registra el tipo de la variable para que la
    # inferencia de tipos pueda validar operaciones posteriores con ella.
    analizador_semantico.registrar_variable(p[1], p[3], p.lineno(1))

# Estructura de datos: Arreglo indexado
def p_arreglo_indexado(p):
    '''arreglo_indexado : VARIABLE ASIGNACION COR_IZQ lista_valores COR_DER PUNTO_COMA'''
    pass

def p_lista_valores(p):
    '''lista_valores : valor_primitivo
                     | lista_valores COMA valor_primitivo
                     | empty'''
    pass

# Estructura de control: Condicional if / else if / elseif / else
# Se separa la cabecera del if ('if_bloque') de lo que puede venir despues
# ('cola_condicional'). Como la cola puede volver a contener un if completo,
# la regla es recursiva y admite cadenas de cualquier longitud:
#   if (..) {..} else if (..) {..} elseif (..) {..} else {..}
def p_estructura_if_else(p):
    '''estructura_if_else : if_bloque cola_condicional'''
    pass

def p_if_bloque(p):
    '''if_bloque : IF PAR_IZQ condicion PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER'''
    pass

def p_cola_condicional(p):
    '''cola_condicional : empty
                        | ELSE LLAVE_IZQ bloque_codigo LLAVE_DER
                        | ELSE estructura_if_else
                        | ELSEIF PAR_IZQ condicion PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER cola_condicional'''
    pass

# Definición de funciones: Función clásica con retorno
def p_funcion_retorno(p):
    '''funcion_retorno : FUNCTION ID PAR_IZQ parametros PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER'''
    cantidad = p[4] if isinstance(p[4], int) else 0  #verifica que la cantidad parametros retornada sea un int
    analizador_semantico.registrar_funcion(p[2], cantidad, cantidad, p.lineno(2)) # guarda la funcion, la cantidad max, y min de parametros y la linea de la funcion)

def p_parametros(p):
    '''parametros : VARIABLE
                  | parametros COMA VARIABLE
                  | empty'''
    if len(p) == 2 and p[1] is not None: # primer argumento
        analizador_semantico.registrar_variable(p[1], {'tipo': 'parametro'}, p.lineno(1)) # guarda la variable, y la linea que se encuentra
        p[0] = 1
    elif len(p) > 2:
        analizador_semantico.registrar_variable(p[3], {'tipo': 'parametro'}, p.lineno(3))
        p[0] = p[1] + 1 # acumulativo 
    else:
        p[0] = 0 # caso que no tenga argumentos
def p_return_statement(p):
    '''return_statement : RETURN expresion PUNTO_COMA'''
    analizador_semantico.registrar_return()

def p_valor_primitivo(p):
    '''valor_primitivo : ENTERO
                       | CADENA
                       | BOOLEANO
                       | VARIABLE'''
    if p.slice[1].type == 'VARIABLE':
        # Hook Regla 1: Validamos si existe (eimmy)
        p[0] = analizador_semantico.verificar_variable_inicializada(p[1], p.lineno(1))
    else:
        # Si es un número o texto, usamos el descriptor de Diego
        p[0] = analizador_semantico.descriptor_token(p.slice[1].type, p[1], p.lineno(1))

def p_bloque_codigo(p):
    '''bloque_codigo : declaracion
                     | bloque_codigo declaracion
                     | empty'''
    pass

def p_empty(p):
    '''empty :'''
    pass

# Marcadores para controlar el contexto de los ciclos (Para la regla del break)
def p_marcador_entrar_ciclo(p):
    '''marcador_entrar_ciclo : empty'''
    analizador_semantico.entrar_ciclo()

def p_marcador_salir_ciclo(p):
    '''marcador_salir_ciclo : empty'''
    analizador_semantico.salir_ciclo()

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
    # REGLA SEMANTICA 2 (Diego): valida que la concatenacion (.) y los
    # operadores aritmeticos se usen con tipos coherentes. p[2] es el simbolo
    # del operador ('+', '.', '*', etc.).
    p[0] = analizador_semantico.verificar_operacion(p[2], p[1], p[3], p.lineno(2))

# Comparaciones (relacionales y de igualdad)
def p_expresion_comparacion(p):
    '''expresion : expresion IGUALDAD expresion
                 | expresion IGUALDAD_ESTRICTA expresion
                 | expresion DESIGUALDAD expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion'''
    # El resultado de una comparacion siempre es booleano.
    p[0] = {'tipo': 'booleano', 'valor': None, 'lineno': p.lineno(2)}

# Conectores logicos (&&, ||)
def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = {'tipo': 'booleano', 'valor': None, 'lineno': p.lineno(2)}

# Negacion logica y signo negativo
def p_expresion_not(p):
    '''expresion : NOT expresion'''
    p[0] = {'tipo': 'booleano', 'valor': None, 'lineno': p.lineno(1)}

def p_expresion_unaria(p):
    '''expresion : RESTA expresion %prec UMINUS'''
    # Un signo negativo conserva el tipo numerico del operando.
    p[0] = p[2] if isinstance(p[2], dict) else {'tipo': 'desconocido', 'valor': None, 'lineno': p.lineno(1)}

# Expresion entre parentesis
def p_expresion_agrupada(p):
    '''expresion : PAR_IZQ expresion PAR_DER'''
    p[0] = p[2]   # el tipo es el de la expresion interna

# Una llamada a funcion tambien es una expresion (resultado)
def p_expresion_llamada(p):
    '''expresion : llamada_funcion'''
    # No se infiere el tipo de retorno de una funcion: queda como desconocido.
    p[0] = {'tipo': 'desconocido', 'valor': None, 'lineno': p.lineno(1)}

# Atomos: valores primitivos (Eimmy) + flotante + identificadores/constantes
def p_expresion_valor(p):
    '''expresion : valor_primitivo
                 | FLOTANTE
                 | ID'''
    # Hook semantico (Diego): propaga el descriptor de tipo hacia arriba.
    if isinstance(p[1], dict):
        p[0] = p[1]                       # ya viene como descriptor (valor_primitivo)
    else:
        p[0] = analizador_semantico.descriptor_token(p.slice[1].type, p[1], p.lineno(1))


# =====================================================================
# 2.2 LECTURA DE DATOS POR TECLADO
#     En PHP la entrada por consola se hace con readline() o fgets(STDIN).
#     Ambas encajan en 'llamada_funcion' (ID '(' argumentos ')'), por lo que
#     no necesita una regla propia. Ej:  $nombre = readline();
# =====================================================================
 ##Se modifico la funcion para aceptar los clouser(Juliana)

def p_llamada_funcion(p):
    '''llamada_funcion : ID PAR_IZQ argumentos PAR_DER
                       | ID PAR_IZQ PAR_DER
                       | VARIABLE PAR_IZQ argumentos PAR_DER  
                       | VARIABLE PAR_IZQ PAR_DER
                       '''
    if p.slice[1].type == 'ID':
        num_argumentos = p[3] if len(p) == 5 else 0
        analizador_semantico.verificar_llamada_funcion(p[1], num_argumentos, p.lineno(1))
   

def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''
    if len(p) == 2:
        p[0] = 1
    else:
        p[0] = p[1] + 1

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
    '''switch_sentencia : SWITCH PAR_IZQ expresion PAR_DER LLAVE_IZQ marcador_entrar_ciclo lista_casos marcador_salir_ciclo LLAVE_DER'''
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
    # Hook Regla 2: Validamos el break (eimmy)
    analizador_semantico.verificar_break(p.lineno(1))

# Estructura de control de apoyo: while
def p_while_sentencia(p):
    '''while_sentencia : WHILE PAR_IZQ expresion PAR_DER LLAVE_IZQ marcador_entrar_ciclo bloque_codigo marcador_salir_ciclo LLAVE_DER'''
    pass

# Asignacion compuesta (+=), usada tipicamente dentro de bucles
def p_asignacion_compuesta(p):
    '''asignacion_compuesta : VARIABLE SUMA_ASIG expresion PUNTO_COMA'''
    pass


# =====================================================================
# 2.4.b ESTRUCTURA DE CONTROL: bucle for
#     for ($i = 0; $i < 10; $i++) { ... }
#     La cabecera tiene 3 partes separadas por ';':
#       - inicializacion: reutiliza 'asignacion_simple', que ya incluye el ';'
#       - condicion: una 'expresion' booleana, seguida de su ';'
#       - paso: 'actualizacion_for' (sin ';', porque va pegado al ')')
#     Los marcadores de ciclo habilitan el uso de 'break' dentro del cuerpo.
# =====================================================================
def p_for_sentencia(p):
    '''for_sentencia : FOR PAR_IZQ asignacion_simple expresion PUNTO_COMA actualizacion_for PAR_DER LLAVE_IZQ marcador_entrar_ciclo bloque_codigo marcador_salir_ciclo LLAVE_DER'''
    pass

# Paso del bucle: admite $i++, $i--, $i += n  y  $i = expresion
def p_actualizacion_for(p):
    '''actualizacion_for : VARIABLE INCREMENTO
                         | VARIABLE DECREMENTO
                         | VARIABLE SUMA_ASIG expresion
                         | VARIABLE ASIGNACION expresion'''
    pass

# Incremento/decremento como sentencia independiente: $contador++;
def p_incremento_sentencia(p):
    '''incremento_sentencia : VARIABLE INCREMENTO PUNTO_COMA
                            | VARIABLE DECREMENTO PUNTO_COMA'''
    pass


# =====================================================================
# 2.5 DECLARACION DE CONSTANTES
# =====================================================================
def p_definicion_constante(p):
    '''definicion_constante : DEFINE PAR_IZQ expresion COMA expresion PAR_DER PUNTO_COMA'''
    # REGLA SEMANTICA 1 (Diego): una constante no puede redefinirse. p[3] es el
    # nombre (cadena) y p[5] el valor asignado.
    analizador_semantico.registrar_constante(p[3], p[5], p.lineno(1))


# =====================================================================
# 2.6 TIPO DE FUNCION OBLIGATORIO: funcion con parametros por defecto
#     function saludar($nombre = "Invitado") { ... }
# =====================================================================
def p_definicion_funcion_default(p):
    '''definicion_funcion_default : FUNCTION ID PAR_IZQ parametros_def PAR_DER LLAVE_IZQ bloque_codigo LLAVE_DER'''

    lista_defaults = p[4] if isinstance(p[4], list) else []
    minimo = sum(1 for tiene_default in lista_defaults if not tiene_default) # solo cuenta los argumentos obligatorios
    maximo = len(lista_defaults)
    analizador_semantico.registrar_funcion(p[2], minimo, maximo, p.lineno(2))

# Lista de parametros que admite valores por defecto (al menos uno con '=')
def p_parametros_def(p):
    '''parametros_def : parametro_def
                      | parametros_def COMA parametro_def'''
    if len(p) == 2:  #si la función solo tiene un parametro obligatorio
        p[0] = [p[1]]  
    else:
        p[0] = p[1] + [p[3]]

def p_parametro_def(p):
    '''parametro_def : VARIABLE
                     | VARIABLE ASIGNACION expresion'''
    tiene_default = (len(p) == 4)
    # El parametro queda registrado en la tabla de simbolos, para que al usarlo
    # dentro del cuerpo no se reporte como "no inicializado". Si tiene valor por
    # defecto se hereda su tipo ($x = "hola" -> cadena); si no, queda generico.
    descriptor = p[3] if tiene_default and isinstance(p[3], dict) else {'tipo': 'parametro'}
    analizador_semantico.registrar_variable(p[1], descriptor, p.lineno(1))
    p[0] = tiene_default

# --- FIN APORTE DIEGO PARRALES --- #


# --- INICIO APORTE JULIANA BURGOS --- #
#   (reglas de Juliana: foreach, clases/objetos y closures)

 # Variabale estatica 
def p_variable_estatica(p):
    '''
    variable_estatica : STATIC VARIABLE ASIGNACION expresion PUNTO_COMA
    '''
    pass

# Definición de for each

def p_foreach(p):
    '''
    foreach_sentencia : FOREACH PAR_IZQ VARIABLE AS VARIABLE PAR_DER LLAVE_IZQ marcador_entrar_ciclo bloque_codigo marcador_salir_ciclo LLAVE_DER
    '''
    pass

# Definicion de clases 
def p_marcador_entrar_funcion(p):
    '''marcador_entrar_funcion : empty'''
    analizador_semantico.entrar_funcion()

def p_clase(p):
    '''
    clase : CLASS ID LLAVE_IZQ miembros_clase LLAVE_DER
    '''
    pass


def p_miembros_clase(p):
    '''
    miembros_clase : miembro_clase
                    | miembros_clase miembro_clase
    '''
    pass

def p_miembro_clase(p):
    '''
    miembro_clase : modificador VARIABLE PUNTO_COMA
                  | modificador VARIABLE ASIGNACION expresion PUNTO_COMA
    '''
    pass

def p_modificador(p):
    '''
    modificador : PUBLIC
                | PRIVATE
                | PROTECTED
    '''
    pass

#Instanciar Objetos
def p_instanciacion_objeto(p):
    '''
    instanciacion_objeto : VARIABLE ASIGNACION NEW ID PAR_IZQ PAR_DER PUNTO_COMA
    '''
    pass

# Acceso a atributos 
def p_expresion_objeto(p):
    '''expresion : VARIABLE OBJETO_OP ID'''
    pass

# clousers
def p_closure(p):
    '''
    closure : VARIABLE ASIGNACION FUNCTION PAR_IZQ parametros PAR_DER LLAVE_IZQ marcador_entrar_funcion bloque_codigo LLAVE_DER PUNTO_COMA
    '''
    analizador_semantico.verificar_retorno_closure(p[1], p.lineno(1))
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
    #test_sintactico('pruebas/algoritmo_diego.php', 'raydan90s')
    test_sintactico('pruebas/algoritmo_juliana.php', 'juzjuz10')
    #test_sintactico('pruebas/algoritmo_eimmy.php', 'eimmy-o')
    
