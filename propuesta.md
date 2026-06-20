# Propuesta de Proyecto Parcial
## Implementación de un Analizador Léxico, Sintáctico y Semántico en Go

**Facultad de Ingeniería en Electricidad y Computación**

**Presentado por:** Grupo #3

- Juliana Burgos Panta — juliburg@espol.edu.ec
- Eimmy Ochoa Morán — eimvocho@espol.edu.ec
- Diego Parrales Villacreses — dxparral@espol.edu.ec

**Professor:** Msc. Rodrigo Saraguro Bravo

Guayaquil – Ecuador | 2026 - 2027

---

## Contenido

1. [Introducción](#1-introducción)
2. [Objetivos del Proyecto](#2-objetivos-del-proyecto)
3. [Analizador Léxico](#3-analizador-léxico)
4. [Analizador Sintáctico](#4-analizador-sintáctico)
5. [Analizador Semántico](#5-analizador-semántico)
6. [Plan de Implementación](#6-plan-de-implementación)
7. [Diseño Preliminar](#7-diseño-preliminar)
8. [Referencias](#8-referencias)

---

## 1. Introducción

El presente proyecto se centra en el lenguaje de programación PHP (Hypertext Preprocessor), un lenguaje de código abierto muy popular y de uso general, especialmente adecuado para el desarrollo web y que puede ser incrustado en HTML. PHP es un lenguaje interpretado y de tipado dinámico, lo que le otorga una curva de aprendizaje sumamente accesible, permitiendo a los nuevos desarrolladores crear aplicaciones funcionales de manera rápida. A nivel de diseño de sintaxis, comparte muchas similitudes con C y Java, utilizando llaves para definir bloques de código y punto y coma para finalizar instrucciones.

Una de las mayores fortalezas de PHP es su extensa y activa comunidad, siendo el motor detrás de la gran mayoría de los sitios web dinámicos en internet, incluyendo gestores de contenido robustos como WordPress. Sus tipos de aplicaciones principales abarcan desde simples páginas web dinámicas hasta complejos sistemas de comercio electrónico, APIs RESTful y aplicaciones empresariales a gran escala, gracias a frameworks modernos como Laravel y Symfony.

Para la construcción de los analizadores léxico y sintáctico del proyecto, se empleará la herramienta PLY (Python Lex-Yacc), una implementación en Python puro de las clásicas herramientas de compilación Lex y Yacc. PLY permite definir reglas léxicas mediante expresiones regulares (módulo `lex.py`) y reglas gramaticales mediante funciones y docstrings (módulo `yacc.py`). El uso de PLY facilita el análisis de lenguajes libres de contexto empleando el algoritmo LALR(1), lo que resulta ideal para modelar e interpretar la estructura de PHP y emitir reportes detallados en caso de detectar construcciones inválidas.

---

## 2. Objetivos del Proyecto

### Objetivo General

- Desarrollar un sistema integrador que procese código fuente escrito en PHP y realice un análisis léxico, sintáctico y semántico, utilizando las herramientas proporcionadas por la librería PLY en Python para validar la correcta estructura y lógica de los programas.

### Objetivos Específicos

- Implementar un analizador léxico que identifique, clasifique y devuelva de manera precisa los tokens válidos tales como palabras reservadas, operadores, variables, delimitadores y capture los errores léxicos del código PHP.
- Construir un analizador sintáctico que evalúe el orden secuencial de los tokens según la gramática libre de contexto de PHP, emitiendo mensajes de error personalizados en caso de violaciones sintácticas.
- Desarrollar un analizador semántico que valide la coherencia del código, incluyendo la existencia de identificadores previos a su uso y la correcta utilización de estructuras lógicas.

---

## 3. Analizador Léxico

### Descripción General

El analizador léxico examinará la cadena de caracteres de entrada del código PHP y la dividirá en componentes léxicos básicos denominados tokens. Su funcionalidad mínima asegura la correcta extracción de palabras reservadas, operadores, símbolos y variables, ignorando espacios en blanco y comentarios. Al detectar un lexema que no coincide con ningún patrón de PHP, el sistema devolverá un error léxico personalizado indicando el carácter no reconocido y su número de línea.

### Componentes Principales

| Categoría | Descripción / Patrón | Ejemplos en PHP |
|---|---|---|
| **Variables** | Comienzan obligatoriamente con el signo de dólar (`$`), seguido de una letra o guión bajo, y luego cualquier combinación de letras, números o guiones bajos. Son sensibles a mayúsculas y minúsculas. | `$nombre`, `$_edad`, `$valor1` |
| **Tipos de datos** | Primitivos: Enteros (int), Flotantes (float), Cadenas (string), Booleanos (bool). Estructurados: Arreglos tradicionales y asociativos (array). | `42`, `3.14`, `"Hola"`, `true`, `[1, 2]` |
| **Operadores** | Aritméticos (`+`, `-`, `*`, `/`, `%`), Asignación (`=`, `+=`), Comparación (`==`, `===`, `!=`, `>`), Lógicos (`&&`, `\|\|`, `!`), y de Concatenación (`.`). | `$a + $b`, `$a === $b`, `$cadena1 . $cadena2` |
| **Palabras Reservadas** | Palabras de uso exclusivo del lenguaje. | `if`, `else`, `echo`, `while`, `function`, `return`, `array` |
| **Comentarios** | Una línea (`//` o `#`) y de múltiples líneas (`/* ... */`). | `// Comentario`, `/* Bloque */` |
| **Delimitadores** | Símbolos de agrupación y terminación. Llaves, paréntesis, punto y coma, comas, y las etiquetas de apertura y cierre de PHP. | `<?php`, `?>`, `{`, `}`, `;`, `(`, `)` |

---

## 4. Analizador Sintáctico

### Descripción General

El analizador sintáctico recibe la secuencia de tokens generada y comprueba si forman expresiones y sentencias gramaticalmente correctas para PHP. El diseño de sintaxis de PHP es bastante flexible, pero exige rigor en el uso del punto y coma al final de cada instrucción y en el encapsulamiento de bloques con llaves. En caso de no cumplir con la gramática, se reportará un error indicando:

> `"Error de Sintaxis: Se esperaba X pero se encontró Y en la línea Z"`

### Reglas Gramaticales y Ejemplos

#### Declaración de Variables

- *Eimmy Ochoa* — Asignación simple de variables primitivas:
  ```php
  $edad = 25;
  ```
- *Diego Parrales* — Declaración de constantes mediante la función `define`:
  ```php
  define("PI", 3.1416);
  ```
- *Juliana Burgos* — Asignación de variables estáticas dentro del alcance de funciones:
  ```php
  static $contador = 0;
  ```

#### Expresiones Aritméticas y Booleanas

- Aritmética (Precedencia estándar):
  ```php
  $total = ($precio * $cantidad) + $impuesto;
  ```
- Booleana:
  ```php
  $esMayor = ($edad >= 18) && $estaRegistrado;
  ```

#### Estructuras de Control

- *Eimmy Ochoa* — `if-else`:
  ```php
  if ($estado == true) { echo "Activo"; } else { echo "Inactivo"; }
  ```
- *Diego Parrales* — `switch`:
  ```php
  switch ($opcion) { case 1: echo "Uno"; break; default: echo "Nada"; }
  ```
- *Juliana Burgos* — `foreach` (específico de PHP):
  ```php
  foreach ($usuarios as $usuario) { echo $usuario; }
  ```

#### Estructuras de Datos

- *Eimmy Ochoa* — Arreglo indexado:
  ```php
  $colores = ["Rojo", "Verde", "Azul"];
  ```
- *Diego Parrales* — Arreglo asociativo:
  ```php
  $persona = ["nombre" => "Juan", "edad" => 30];
  ```
- *Juliana Burgos* — Definición de Clases/Objetos:
  ```php
  class Carro { public $marca = "Toyota"; }
  ```

#### Declaraciones de Funciones

- *Eimmy Ochoa* — Función clásica con retorno:
  ```php
  function sumar($a, $b) { return $a + $b; }
  ```
- *Diego Parrales* — Función con parámetros por defecto:
  ```php
  function saludar($nombre = "Invitado") { echo "Hola " . $nombre; }
  ```
- *Juliana Burgos* — Funciones anónimas / Closures:
  ```php
  $multiplicar = function($x, $y) { return $x * $y; };
  ```

#### Impresión de datos

```php
echo "Hola Mundo";
print($variable);
```

---

## 5. Analizador Semántico

### Descripción General

Valida la lógica del código y el significado de las operaciones, incluso si son gramaticalmente correctas. Verificará cosas clave del comportamiento de los scripts PHP.

### Reglas Semánticas

#### Integrante Eimmy Ochoa

- **Identificadores:** Regla para validar que una variable haya sido inicializada antes de participar en una operación del lado derecho de una asignación (evita errores en tiempo de ejecución).
- **Estructuras de Control:** Validación de que las sentencias `break` o `continue` se encuentren estrictamente dentro del contexto de un ciclo (`while`, `for`, `foreach`) o un `switch`.

#### Integrante Diego Parrales

- **Asignación de tipo (Constantes):** Regla para asegurar que una constante no pueda ser reasignada o sobrescrita en líneas posteriores.
- **Operaciones permitidas:** Verificación estricta de que el operador de concatenación (`.`) se utilice de forma lógica, y emitir advertencias si se intenta sumar con una cadena pura.

#### Integrante Juliana Burgos

- **Llamada de funciones:** Verificación de que la cantidad de argumentos enviados en la llamada a una función coincida con los parámetros requeridos.
- **Retorno en funciones:** Asegurar que si una función se asigna a una variable, esta posea obligatoriamente la instrucción `return`.

---

## 6. Plan de Implementación

### Herramientas de desarrollo y test

| Herramienta | Descripción |
|---|---|
| **Python 3.x** | Lenguaje base para desarrollar los analizadores empleando paradigma orientado a objetos. |
| **PLY (Python Lex-Yacc)** | Módulos `lex.py` y `yacc.py` para construir el escáner y el parser de la gramática de PHP. |
| **VS Code** | Entorno de Desarrollo Integrado para la codificación y pruebas en tiempo real. |
| **GitHub** | Control de versiones para gestión de avances y repositorios del equipo. |
| **Tkinter / CustomTkinter** | Librería de Python para diseñar e integrar la Interfaz Gráfica de Usuario (GUI). |

### Recursos Humanos

Se ha dividido la carga de desarrollo de manera equitativa. La construcción de los patrones léxicos ha sido asignada a Eimmy, siendo una etapa introductoria ideal para establecer las bases. La gramática y el árbol sintáctico serán de Diego, y las validaciones lógicas e interfaz gráfica recaen en Juliana.

| Desarrollador | Usuario GitHub | Analizador | Funcionalidad / Responsabilidad |
|---|---|---|---|
| Eimmy Ochoa | eimmy-o | Léxico | Identificación de tokens, patrones regex, delimitadores, palabras clave y manejo de errores léxicos. |
| Diego Parrales | raydan90s | Sintáctico | Reglas gramaticales (BNF), precedencia de operadores, y control de errores sintácticos. |
| Juliana Burgos | — | Semántico y GUI | Tabla de símbolos, validación de reglas de contexto y creación de la interfaz de usuario gráfica. |

---

## 7. Diseño Preliminar

El proyecto integrará una GUI (Interfaz Gráfica de Usuario) desarrollada en Python para brindar una experiencia amigable e interactiva.

### Funcionalidades de la GUI

- **Panel izquierdo/superior:** Un editor de texto simple con numeración de líneas donde el usuario ingresará el código PHP.
- **Botones de acción:** "Ejecutar Análisis Completo", "Analizar Léxico", "Limpiar Consola".
- **Panel inferior/derecho de resultados:** Áreas de texto estilo consola donde se imprimirán los logs generados, detallando los tokens encontrados, reglas validadas y resaltando los errores.

> *[img del prototipo — pendiente]*

---

## 8. Referencias

- [1] The PHP Group. "PHP: Hypertext Preprocessor". Accedido en 2026. [En línea]. Disponible: https://www.php.net/
- [2] D. Beazley. "PLY (Python Lex-Yacc)". Accedido en 2026. [En línea]. Disponible: https://www.dabeaz.com/ply/ply.html