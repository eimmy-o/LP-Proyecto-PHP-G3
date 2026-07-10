<?php
// Algoritmo de prueba SEMANTICO - Eimmy Ochoa
// Escenario: Sistema de trackeo de lecturas (El Grimorio)
// Sintacticamente correcto, pero con errores semanticos intencionales
// que deben ser detectados por las reglas de validacion de Eimmy.

/* ---------- DECLARACIONES Y CONTEXTOS CORRECTOS ---------- */

$mangas_tbr = ["One Piece", "Haikyuu", "Boku no Hero"];
$capitulos_leidos = 1050;
$meta_diaria = 5;

// Uso de funcion: los parametros $leidos y $meta nacen inicializados aqui
function calcularProgreso($leidos, $meta) {
    $dias_estimados = $leidos / $meta;
    return $dias_estimados;
}

$progreso_actual = calcularProgreso($capitulos_leidos, $meta_diaria);

/* ---------- REGLA 1: Variables no inicializadas ---------- */

// ERROR SEMANTICO: La variable $capitulos_totales jamas fue declarada
$porcentaje = ($capitulos_leidos / $capitulos_totales) * 100;

// ERROR SEMANTICO: La variable $estado_lectura jamas fue declarada
if ($estado_lectura == "Completado") {
    echo "Felicidades, terminaste el manga";
}

/* ---------- REGLA 2: Contexto de estructuras de control (break) ---------- */

// CASO CORRECTO: El break esta correctamente anidado dentro de un ciclo while
$contador = 0;
while ($contador < 5) {
    if ($contador == 3) {
        break; // OK: El analizador sabe que estamos dentro de un bucle
    }
    $contador = $contador + 1;
}

// CASO INCORRECTO: El break esta suelto en una estructura que no es de repeticion
if ($progreso_actual > 100) {
    echo "El progreso es muy bueno";
    
    // ERROR SEMANTICO: Un if no es un ciclo, el analizador debe atrapar este break
    break; 
} else {
    echo "Sigue leyendo";
}
?>