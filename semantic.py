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
#
# --- REGLAS SEMANTICAS - DIEGO PARRALES (raydan90s) ---
#   1. Asignacion de tipo (Constantes): una constante definida con define()
#      NO puede ser redefinida ni sobrescrita en lineas posteriores.
#   2. Operaciones permitidas: el operador de concatenacion (.) debe usarse
#      de forma logica y se emite una ADVERTENCIA si se intenta usar un
#      operador aritmetico (+, -, *, /, %) con una cadena pura.
# ==========================================

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

    # (pendiente: definir aqui los metodos de las reglas de Eimmy)

    # --- FIN APORTE EIMMY OCHOA --- #


    # ================================================================
    # --- INICIO APORTE JULIANA BURGOS --- #
    #   Reglas semanticas pendientes:
    #     1. Llamada de funciones: la cantidad de argumentos debe coincidir con
    #        los parametros declarados.
    #     2. Retorno en funciones: si una funcion se asigna a una variable debe
    #        contener obligatoriamente un return.
    # ================================================================

    # (pendiente: definir aqui los metodos de las reglas de Juliana)

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
    test_semantico('pruebas/algoritmo_semantico_diego.php', 'raydan90s')
