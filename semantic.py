# ==========================================
# ANALIZADOR SEMANTICO
# ==========================================
# Modulo que valida la logica del codigo PHP una vez que el analizador
# sintactico confirma que la estructura es correcta. Se apoya en "hooks"
# semanticos colocados dentro de las reglas gramaticales del parser, que
# van entregando descriptores con el TIPO inferido de cada expresion y
# registrando las constantes y variables declaradas.
#
# Cada integrante define sus reglas semanticas como metodos de la clase
# AnalizadorSemantico, delimitados con marcadores INICIO/FIN APORTE.

from datetime import datetime
import os


class AnalizadorSemantico:
    """Mantiene las tablas de simbolos y acumula errores/advertencias."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.errores = []          # errores semanticos (rompen la logica)
        self.advertencias = []     # advertencias (codigo sospechoso)
        self.tabla_constantes = {} # nombre -> {'tipo', 'lineno'}
        self.tabla_variables = {}  # nombre -> {'tipo', 'lineno'}
        self.nivel_ciclo = 0       # control para los break/continue 
        self.tabla_funciones = {}  # nombre -> {'min', 'max', 'lineno'} (Juliana)
        self.pila_retorno = []         # pila de banderas 'tiene return' (Juliana)
    # ================================================================
    # --- INICIO APORTE DIEGO PARRALES --- #
    #   Inferencia de tipos + Regla 1 (constantes) + Regla 2 (operaciones).
    #   Los metodos descriptor_token y registrar_variable son infraestructura
    #   compartida (la usan tambien los hooks que apoyan a las demas reglas).
    # ================================================================

    # ----------------------------------------------------------------
    # Inferencia de tipos: traduce el tipo de token a un tipo semantico
    # ----------------------------------------------------------------
    def descriptor_token(self, tipo_token, valor, lineno):
        """Construye el descriptor {tipo, valor, lineno} de un atomo."""
        if tipo_token == 'ENTERO':
            tipo = 'entero'
        elif tipo_token == 'FLOTANTE':
            tipo = 'flotante'
        elif tipo_token == 'CADENA':
            tipo = 'cadena'
        elif tipo_token == 'BOOLEANO':
            tipo = 'booleano'
        elif tipo_token == 'VARIABLE':
            # El tipo de una variable es el que se le asigno previamente.
            info = self.tabla_variables.get(valor)
            tipo = info['tipo'] if info else 'desconocido'
        elif tipo_token == 'ID':
            # Un identificador puede ser el nombre de una constante.
            info = self.tabla_constantes.get(valor)
            tipo = info['tipo'] if info else 'desconocido'
        else:
            tipo = 'desconocido'
        return {'tipo': tipo, 'valor': valor, 'lineno': lineno}

    # ----------------------------------------------------------------
    # REGLA 1: Constantes no reasignables
    # ----------------------------------------------------------------
    def registrar_constante(self, nombre_desc, valor_desc, lineno):
        # El nombre llega como literal de cadena (incluye comillas): "PI"
        nombre = str(nombre_desc.get('valor', '')).strip('"')
        if nombre in self.tabla_constantes:
            linea_original = self.tabla_constantes[nombre]['lineno']
            self.errores.append(
                f"Error Semantico (linea {lineno}): la constante '{nombre}' ya "
                f"fue definida en la linea {linea_original} y no puede ser "
                f"redefinida ni sobrescrita."
            )
        else:
            self.tabla_constantes[nombre] = {
                'tipo': valor_desc.get('tipo', 'desconocido'),
                'lineno': lineno,
            }

    # ----------------------------------------------------------------
    # Registro de variables (alimenta la inferencia de tipos)
    # ----------------------------------------------------------------
    def registrar_variable(self, nombre, valor_desc, lineno):
        tipo = valor_desc.get('tipo', 'desconocido') if isinstance(valor_desc, dict) else 'desconocido'
        self.tabla_variables[nombre] = {'tipo': tipo, 'lineno': lineno}

    # ----------------------------------------------------------------
    # REGLA 2: Operaciones permitidas (concatenacion / aritmetica)
    # ----------------------------------------------------------------
    def verificar_operacion(self, operador, izq, der, lineno):
        """Valida una operacion binaria y devuelve el descriptor resultante."""
        tipos_numericos = {'entero', 'flotante'}
        t_izq = izq.get('tipo', 'desconocido') if isinstance(izq, dict) else 'desconocido'
        t_der = der.get('tipo', 'desconocido') if isinstance(der, dict) else 'desconocido'

        aritmeticos = {'+', '-', '*', '/', '%'}

        if operador in aritmeticos:
            # Advertencia si se intenta operar aritmeticamente con una cadena pura.
            if t_izq == 'cadena' or t_der == 'cadena':
                self.advertencias.append(
                    f"Advertencia Semantica (linea {lineno}): se usa el operador "
                    f"aritmetico '{operador}' con una cadena; para unir texto use "
                    f"el operador de concatenacion '.'."
                )
            tipo_resultado = 'flotante' if 'flotante' in (t_izq, t_der) else 'entero'

        elif operador == '.':
            # La concatenacion es el operador correcto para texto.
            # Se advierte si se usa entre dos numeros puros (probable error logico).
            if t_izq in tipos_numericos and t_der in tipos_numericos:
                self.advertencias.append(
                    f"Advertencia Semantica (linea {lineno}): se concatenan dos "
                    f"valores numericos con '.'; verifique si en realidad deseaba "
                    f"una operacion aritmetica."
                )
            tipo_resultado = 'cadena'
        else:
            tipo_resultado = 'desconocido'

        return {'tipo': tipo_resultado, 'valor': None, 'lineno': lineno}

    # --- FIN APORTE DIEGO PARRALES --- #


    # ================================================================
    # --- INICIO APORTE EIMMY OCHOA --- #
    #   Reglas semanticas pendientes:
    #     1. Identificadores: validar que una variable este inicializada antes
    #        de usarse en el lado derecho de una asignacion.
    #     2. Estructuras de control: break/continue solo dentro de un ciclo o
    #        switch.
    # ================================================================

    # REGLA 1: Verificar que la variable existe antes de usarse
    def verificar_variable_inicializada(self, nombre, lineno):
        # Buscamos en variables y constantes 
        if nombre not in self.tabla_variables and nombre not in self.tabla_constantes:
            self.errores.append(
                f"Error Semantico (linea {lineno}): La variable '{nombre}' "
                f"no ha sido inicializada antes de su uso."
            )
        # Retornamos el descriptor de tipo 
        tipo = self.tabla_variables.get(nombre, {}).get('tipo', 'desconocido')
        return {'tipo': tipo, 'valor': nombre, 'lineno': lineno}

    # REGLA 2: Contexto de estructuras de control (break)
    def entrar_ciclo(self):
        self.nivel_ciclo += 1

    def salir_ciclo(self):
        self.nivel_ciclo -= 1

    def verificar_break(self, lineno):
        if self.nivel_ciclo == 0:
            self.errores.append(
                f"Error Semantico (linea {lineno}): Sentencia 'break' "
                f"fuera de un contexto valido (ciclo o switch)."
            )

    # --- FIN APORTE EIMMY OCHOA --- #


    # ================================================================
    # --- INICIO APORTE JULIANA BURGOS --- #
    #   Reglas semanticas:
    #     1. Llamada de funciones: la cantidad de argumentos debe coincidir con
    #        los parametros declarados.
    #     2. Retorno en funciones: si una funcion se asigna a una variable debe
    #        contener obligatoriamente un return.
    # ================================================================

    # ----------------------------------------------------------------
    # REGLA 1: Llamada de funciones (cantidad de argumentos vs parametros)
    # ----------------------------------------------------------------
    # El parser llama a registrar_funcion(...) cuando reduce una declaracion
    # de funcion (function_retorno / definicion_funcion_default), indicando
    # cuantos parametros son obligatorios (minimo) y cuantos admite en total
    # (maximo, contando los que tienen valor por defecto).
    def registrar_funcion(self, nombre, minimo, maximo, lineno):
        if nombre in self.tabla_funciones:
            linea_original = self.tabla_funciones[nombre]['lineno']
            self.errores.append(
                f"Error Semantico (linea {lineno}): la funcion '{nombre}' ya "
                f"fue declarada en la linea {linea_original}."
            )
            return
        self.tabla_funciones[nombre] = {
            'min': minimo,
            'max': maximo,
            'lineno': lineno,
        }

    # El parser llama a este metodo cuando reduce una llamada a funcion
    # (ID '(' argumentos ')'), enviando el numero de argumentos detectados.
    def verificar_llamada_funcion(self, nombre, num_argumentos, lineno):
        info = self.tabla_funciones.get(nombre)
        if info is None:
            # Funcion no declarada por el usuario (puede ser nativa de PHP,
            # p. ej. readline(), fgets(), intval(), etc.): no se valida,
            # ya que el proyecto solo modela las funciones definidas en el
            # propio script.
            return

        minimo, maximo = info['min'], info['max']
        if num_argumentos < minimo or num_argumentos > maximo:
            if minimo == maximo:
                esperado = f"{minimo}"
            else:
                esperado = f"entre {minimo} y {maximo}"
            self.errores.append(
                f"Error Semantico (linea {lineno}): la funcion '{nombre}' "
                f"espera {esperado} argumento(s) y se enviaron "
                f"{num_argumentos}."
            )

    # ----------------------------------------------------------------
    # REGLA 2: Retorno obligatorio en funciones asignadas a variables
    #          (closures / funciones anonimas)
    # ----------------------------------------------------------------
    # Se usa una pila porque los closures pueden anidarse (un closure
    # definido dentro de otro). Cada vez que el parser entra al cuerpo de
    # un closure, se apila una bandera en False; si dentro del cuerpo se
    # encuentra un 'return', la bandera del closure mas interno se marca
    # en True; al cerrar el closure se desapila y se valida.
    def entrar_funcion(self):
        self.pila_retorno.append(False)

    def registrar_return(self):
        if self.pila_retorno:
            self.pila_retorno[-1] = True

    def verificar_retorno_closure(self, nombre_variable, lineno):
        tiene_return = self.pila_retorno.pop() if self.pila_retorno else False
        if not tiene_return:
            self.errores.append(
                f"Error Semantico (linea {lineno}): la funcion anonima "
                f"asignada a la variable '{nombre_variable}' debe contener "
                f"obligatoriamente la instruccion 'return'."
            )
    

    # --- FIN APORTE JULIANA BURGOS --- #


    # ----------------------------------------------------------------
    # Generacion del log de resultados (nucleo comun)
    # ----------------------------------------------------------------
    def generar_log(self, ruta_archivo, usuario_git):
        fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
        nombre_log = f"semantico-{usuario_git}-{fecha_hora}.txt"

        if not os.path.exists('logs'):
            os.makedirs('logs')

        ruta_log = os.path.join('logs', nombre_log)

        with open(ruta_log, 'w', encoding='utf-8') as f:
            f.write("=== RESULTADO DEL ANALISIS SEMANTICO ===\n\n")
            f.write(f"Archivo analizado: {ruta_archivo}\n")
            f.write(f"Usuario Git: {usuario_git}\n\n")

            f.write(f"ERRORES SEMANTICOS ENCONTRADOS ({len(self.errores)}):\n")
            if self.errores:
                for e in self.errores:
                    f.write("  - " + e + "\n")
            else:
                f.write("  (ninguno)\n")

            f.write(f"\nADVERTENCIAS SEMANTICAS ({len(self.advertencias)}):\n")
            if self.advertencias:
                for a in self.advertencias:
                    f.write("  - " + a + "\n")
            else:
                f.write("  (ninguna)\n")

            if not self.errores and not self.advertencias:
                f.write("\nAnalisis completado: el codigo es semanticamente correcto.\n")

        return ruta_log


# Instancia global usada por los hooks semanticos del parser.
analizador_semantico = AnalizadorSemantico()


def test_semantico(ruta_archivo, usuario_git):
    """Ejecuta el analisis semantico sobre un archivo PHP y genera el log."""
    # Imports diferidos para evitar dependencia circular con parser.py.
    # Se usa SIEMPRE la instancia del modulo 'semantic' (la misma que usan los
    # hooks del parser), incluso si este archivo se ejecuta como '__main__'.
    import semantic
    from parser import parser, lexer

    analizador = semantic.analizador_semantico
    analizador.reset()

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = archivo.read()

    lexer.lineno = 1
    if hasattr(lexer, 'log_errores'):
        lexer.log_errores = []

    # Al parsear, los hooks semanticos van llenando las tablas y listas.
    parser.parse(data, lexer=lexer)

    ruta_log = analizador.generar_log(ruta_archivo, usuario_git)

    print(f"Analisis semantico completado: "
          f"{len(analizador.errores)} error(es), "
          f"{len(analizador.advertencias)} advertencia(s). "
          f"Log: {ruta_log}")


if __name__ == '__main__':
    # Algoritmo de prueba semantico (Diego): constantes redefinidas y
    # operaciones aritmeticas/concatenacion con tipos incorrectos.
    #test_semantico('pruebas/algoritmo_semantico_diego.php', 'raydan90s')
    #test_semantico('pruebas/algoritmo_semantico_eimmy.php', 'eimmy-o')
    test_semantico('pruebas/algoritmo_semantico_juliana.php', 'juzjuz10')
