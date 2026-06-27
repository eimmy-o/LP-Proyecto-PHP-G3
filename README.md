# Analizador Léxico, Sintáctico y Semántico en PHP

**Materia:** Lenguajes de Programación  
**Institución:** Escuela Superior Politécnica del Litoral (ESPOL)  
**Facultad:** FIEC  
**Profesor:** Msc. Rodrigo Saraguro Bravo  

## Integrantes

| Nombre | GitHub |
|---|---|
| Eimmy Ochoa Morán | [@eimmy-o](https://github.com/eimmy-o) |
| Diego Parrales Villacreses | [@raydan90s](https://github.com/raydan90s) |
| Juliana Burgos Panta | [@juzjuz10](https://github.com/juzjuz10) |

---

## Descripción

Sistema que procesa código fuente escrito en PHP y realiza análisis **léxico**, **sintáctico** y **semántico**, implementado en Python usando la librería **PLY (Python Lex-Yacc)**.

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

Edita la línea al final de `lexer.py` indicando el archivo PHP a analizar y el nombre del desarrollador:

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
├── lexer.py                  # Analizador léxico (PLY)
├── requirements.txt          # Dependencias (ply)
├── pruebas/
│   ├── algoritmo_eimmy.php   # Algoritmo de prueba - Eimmy Ochoa
│   └── algoritmo_diego.php   # Algoritmo de prueba - Diego Parrales
│   └── algoritmo_juliana.php   # Algoritmo de prueba - Julianna Burgos
└── logs/                     # Logs generados por el analizador
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
| **Tipo de función** | Función con parámetros por defecto `function f($x = "v") { }` |
| **Constantes** | `define("NOMBRE", valor)` |

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

## Fases del Proyecto

- [x] **Analizador Léxico** — Eimmy Ochoa, Diego Parrales, Juliana Burgos
- [~] **Analizador Sintáctico** — Diego Parrales (transversales + switch, arreglo asociativo, función con defaults). Pendiente: Eimmy, Juliana
- [~] **Analizador Semántico** — Diego Parrales (constantes no reasignables, operaciones permitidas). Pendiente: Eimmy, Juliana
- [ ] Interfaz Gráfica (GUI)
