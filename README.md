# Analizador Léxico, Sintáctico y Semántico en PHP

**Materia:** Lenguajes de Programación  
**Institución:** Escuela Superior Politécnica del Litoral (ESPOL)  
**Facultad:** FIEC  
**Profesor:** Msc. Rodrigo Saraguro Bravo  

---

## Librerías necesarias para probar el proyecto

| Librería | Versión | ¿Hay que instalarla? | Uso en el proyecto |
|---|---|---|---|
| **Python** | 3.8 o superior | Sí, es el intérprete base | Lenguaje en el que están escritos los tres analizadores |
| **PLY** (Python Lex-Yacc) | 3.11 o superior | **Sí**, con `pip` | Módulos `lex` (analizador léxico) y `yacc` (analizador sintáctico) |
| **Tkinter** | — | **No**, viene incluida en Python | Interfaz gráfica de usuario (`gui.py`) |

### Instalación

La única dependencia externa es **PLY**. Se instala con:

```bash
pip install -r requirements.txt
```

O directamente:

```bash
pip install ply
```

> **Nota:** Tkinter forma parte de la librería estándar de Python en Windows y
> macOS, por lo que no requiere instalación. En algunas distribuciones de Linux
> se instala aparte con `sudo apt install python3-tk`.

### Ejecución

La forma recomendada de probar el proyecto es a través de la **interfaz gráfica**,
que ejecuta los tres analizadores sobre el código y muestra los errores con su
número de línea:

```bash
python gui.py
```

También se puede ejecutar cada analizador por separado desde la consola:

```bash
python lexer.py      # análisis léxico
python parser.py     # análisis sintáctico
python semantic.py   # análisis semántico
```

En ambos casos los resultados se guardan como archivos de texto en la carpeta `logs/`.

---

## Integrantes

| Nombre | GitHub |
|---|---|
| Eimmy Ochoa Morán | [@eimmy-o](https://github.com/eimmy-o) |
| Diego Parrales Villacreses | [@raydan90s](https://github.com/raydan90s) |
| Juliana Burgos Panta | [@juzjuz10](https://github.com/juzjuz10) |

---

## Descripción

Sistema que procesa código fuente escrito en PHP y realiza análisis **léxico**, **sintáctico** y **semántico**, implementado en Python usando la librería **PLY (Python Lex-Yacc)**.

## Analizador Léxico (`lexer.py`)

Para ejecutarlo desde consola, edita la línea al final de `lexer.py` indicando el archivo PHP a analizar y el nombre del desarrollador:

```python
analizar_archivo('pruebas/algoritmo_nombre.php', 'NombreDesarrollador')
```

Luego ejecuta:

```bash
python lexer.py
```

El resultado se guarda automáticamente en la carpeta `logs/` con el formato:  
`lexico-NombreApellido-DD-MM-YYYY-HHhMM.txt`

## Estructura del proyecto

```
LP-Proyecto-PHP-G3/
├── gui.py                      # Interfaz gráfica (Tkinter)
├── lexer.py                    # Analizador léxico (PLY - lex)
├── parser.py                   # Analizador sintáctico (PLY - yacc)
├── semantic.py                 # Analizador semántico
├── requirements.txt            # Dependencias (ply)
├── pruebas/
│   ├── algoritmo_eimmy.php     # Algoritmo de prueba - Eimmy Ochoa
│   ├── algoritmo_diego.php     # Algoritmo de prueba - Diego Parrales
│   └── algoritmo_juliana.php   # Algoritmo de prueba - Juliana Burgos
└── logs/                       # Logs generados por los analizadores
```

## Tokens implementados

### Eimmy Ochoa
| Token | Descripción | Ejemplo |
|---|---|---|
| `VARIABLE` | Variable PHP | `$nombre` |
| `ENTERO` | Número entero | `25` |
| `BOOLEANO` | Valor booleano | `true`, `false` |
| `CADENA` | Cadena de texto | `"Hola"` |
| `ASIGNACION` | Operador `=` | `$x = 5` |
| `IGUALDAD` | Operador `==` | `$a == $b` |
| `SUMA` | Operador `+` | `$a + $b` |
| `IF`, `ELSE` | Estructura if-else | `if (...) { } else { }` |
| `ECHO` | Impresión | `echo "texto"` |
| `FUNCTION`, `RETURN` | Funciones | `function f() { return x; }` |
| `APERTURA_PHP`, `CIERRE_PHP` | Delimitadores PHP | `<?php`, `?>` |

### Diego Parrales
| Token | Descripción | Ejemplo |
|---|---|---|
| `FLOTANTE` | Número flotante | `3.1416`, `0.12` |
| `DEFINE` | Declaración de constante | `define("PI", 3.14)` |
| `SWITCH`, `CASE`, `DEFAULT`, `BREAK` | Estructura switch | `switch ($x) { case 1: ... }` |
| `WHILE`, `FOR` | Bucles | `while ($i < 3) { }` |
| `FLECHA` | Operador `=>` (arreglo asociativo) | `["clave" => "valor"]` |
| `CONCATENACION` | Operador `.` | `"Hola" . $nombre` |
| `IGUALDAD_ESTRICTA` | Operador `===` | `$a === $b` |
| `MAYOR_IGUAL`, `MENOR_IGUAL` | Comparación | `>=`, `<=` |
| `DESIGUALDAD` | Operador `!=` | `$a != $b` |
| `MAYOR`, `MENOR` | Comparación | `>`, `<` |
| `AND`, `OR`, `NOT` | Lógicos | `&&`, `\|\|`, `!` |
| `RESTA`, `MULTIPLICACION`, `DIVISION`, `MODULO` | Aritméticos | `-`, `*`, `/`, `%` |
| `SUMA_ASIG` | Asignación compuesta | `+=` |
| `INCREMENTO`, `DECREMENTO` | Incremento / decremento | `$i++`, `$i--` |
| `DOS_PUNTOS` | Separador `case` | `:` |

### Juliana Burgos
| Token | Descripción | Ejemplo |
|---|---|---|
| `FOREACH`, `AS` | Bucle para recorrer arrays u objetos | `foreach ($array as $valor) { ... }` |
| `CLASS` | Declaración de clase | `class Persona { ... }` |
| `PUBLIC`, `PRIVATE`, `PROTECTED` | Modificadores de visibilidad de propiedades y métodos | `public $nombre; private $edad; protected function mostrar();` |
| `STATIC` | Propiedades o métodos estáticos (no requieren instancia) | `public static $contador = 0;` |
| `NEW` | Creación de objetos | `$obj = new Persona();` |
| `OBJETO_OP` | Operador de objeto `->` | `$obj->metodo(); $obj->propiedad;` |


## Analizador Sintáctico (`parser.py`)

Construido con el módulo **yacc** de PLY sobre los tokens del léxico. Para probarlo:

```bash
python parser.py
```

Genera un log en `logs/` con el formato `sintactico-usuarioGit-DDMMYYYY-HHhMM.txt`.

### Reglas sintácticas — Diego Parrales

| Categoría | Regla / Estructura |
|---|---|
| **Transversales** | Expresiones aritméticas y de concatenación con 1+ operadores (con precedencia), condiciones booleanas con 1+ conectores lógicos (`&&`, `\|\|`), impresión (`echo`) |
| **Asignación** | Asignación con expresiones/condiciones y asignación compuesta (`+=`) |
| **Entrada por teclado** | `readline()` / `fgets(STDIN)` (reconocidas como llamada a función) |
| **Estructura de datos** | Arreglo asociativo `["clave" => valor]` |
| **Estructura de control** | `switch` / `case` / `default` (+ `while` de apoyo) |
| **Bucle `for`** | `for ($i = 0; $i < 10; $i++) { }` — el paso admite `$i++`, `$i--`, `$i += n` y `$i = expr`. Incremento como sentencia: `$contador++;` |
| **Tipo de función** | Función con parámetros por defecto `function f($x = "v") { }` |
| **Constantes** | `define("NOMBRE", valor)` |

Archivo de prueba del bucle: `pruebas/algoritmo_for_diego.php` (0 errores sintácticos
y 0 semánticos; incluye un `break` dentro del `for` para validar el contexto de ciclo).

## Analizador Semántico (`semantic.py`)

Valida la lógica del código una vez que el sintáctico confirma la estructura. Se
implementa mediante *hooks* semánticos dentro de las reglas del parser, que
infieren el **tipo** de cada expresión y registran constantes y variables en
tablas de símbolos. Para probarlo:

```bash
python semantic.py
```

Genera un log en `logs/` con el formato `semantico-usuarioGit-DDMMYYYY-HHhMM.txt`,
separando **errores** (rompen la lógica) de **advertencias** (código sospechoso).

### Reglas semánticas — Diego Parrales

| # | Regla | Descripción |
|---|---|---|
| 1 | **Constantes no reasignables** | Una constante definida con `define("X", ...)` no puede ser redefinida ni sobrescrita; un segundo `define` con el mismo nombre genera un **error semántico**. |
| 2 | **Operaciones permitidas** | Verifica el uso lógico de los operadores: advierte si se usa un operador aritmético (`+`, `-`, `*`, `/`, `%`) con una **cadena pura**, y si se usa la concatenación (`.`) entre **dos números** (probable error lógico). |

Archivo de prueba: `pruebas/algoritmo_semantico_diego.php` (sintácticamente
correcto, con 1 error y 3 advertencias semánticas a propósito).

## Interfaz Gráfica (GUI)

Interfaz de escritorio construida con **Tkinter** (incluida en la librería estándar
de Python, no requiere instalación adicional). Se ejecuta con:

```bash
python gui.py
```

La ventana integra los tres analizadores sin modificarlos: importa `lexer.py`,
`parser.py` y `semantic.py` y los ejecuta sobre el código escrito en el editor.

| Elemento | Descripción |
|---|---|
| **Editor** | Área de código PHP con numeración de líneas. Permite escribir directamente o abrir un archivo `.php`. |
| **Botones** | `▶ Analizar todo` (ejecuta los tres analizadores), `Abrir .php`, `Guardar código`, `Guardar log` y `Limpiar`. Atajos: `F5`, `Ctrl+O`, `Ctrl+S`, `Ctrl+L`. |
| **Pestañas de resultados** | Salida de cada analizador (tokens reconocidos, errores de sintaxis, errores y advertencias semánticas) y la **tabla de símbolos** con variables, constantes y funciones. |
| **Tabla de errores** | Lista todos los errores con su **número de línea** y su tipo. Doble clic sobre un error salta a esa línea del editor, que además queda resaltada. |
| **Selector de integrante** | Define el usuario de Git con el que se nombra el log generado desde la interfaz. |

Los logs generados desde la GUI se guardan en `logs/` con el mismo formato de
nombre que los generados por consola.

## Fases del Proyecto

- [x] **Analizador Léxico** — Eimmy Ochoa, Diego Parrales, Juliana Burgos
- [x] **Analizador Sintáctico** — Eimmy Ochoa, Diego Parrales, Juliana Burgos
- [x] **Analizador Semántico** — Eimmy Ochoa, Diego Parrales, Juliana Burgos
- [x] **Interfaz Gráfica (GUI)** — Juliana Burgos
