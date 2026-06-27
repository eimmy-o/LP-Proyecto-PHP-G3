<?php
// Algoritmo de prueba SEMANTICO - Diego Parrales (raydan90s)
// Sintacticamente correcto, pero con errores/advertencias semanticas que
// deben ser detectados por las dos reglas semanticas de Diego.

/* ---------- REGLA 1: Constantes no reasignables ---------- */
define("PI", 3.1416);
define("TASA_IVA", 0.15);
define("PI", 3.14);            // ERROR: la constante 'PI' ya fue definida

/* ---------- Declaracion de variables (inferencia de tipos) ---------- */
$base = 100;                   // entero
$precio = 9.99;                // flotante
$nombre = "Diego";             // cadena

/* ---------- REGLA 2: Operaciones permitidas ---------- */

// Casos correctos (no generan advertencias)
$total = $base + 50;           // OK: suma entre numeros
$conImpuesto = $precio * 0.15; // OK: multiplicacion entre numeros
$saludo = "Hola " . $nombre;   // OK: concatenacion de cadenas

// Casos sospechosos (generan ADVERTENCIA)
$malo1 = "Edad: " + 30;        // ADVERTENCIA: aritmetica '+' con una cadena
$malo2 = $nombre + 10;         // ADVERTENCIA: aritmetica '+' con variable cadena
$malo3 = 10 . 20;              // ADVERTENCIA: concatenacion de dos numeros

echo $saludo;
?>
