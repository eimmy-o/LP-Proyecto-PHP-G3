<?php
// Algoritmo de prueba CON ERRORES sintacticos - Diego Parrales
// Sirve para demostrar que el analizador sintactico detecta y reporta fallos.

// ERROR 1: falta el punto y coma al final de la asignacion
$edad = 25

// ERROR 2: switch sin los dos puntos despues del case
switch ($opcion) {
    case 1
        echo "uno";
        break;
}

// ERROR 3: arreglo asociativo con '=>' incompleto (falta el valor)
$persona = ["nombre" => ];
?>
