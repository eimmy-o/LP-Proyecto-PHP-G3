<?php
// Asignacion simple de variables primitivas y expresiones matematicas
$estado_activo = true;
$capitulos_leidos = 450;
$capitulos_totales = 1100;
$dias_lectura = 15;

// Arreglo indexado 
$grimorio_tbr = ["One Piece", "Haikyuu", "Boku no Hero"];

// Funcion clasica con retorno y logica interna
function calcularVelocidad($leidos, $dias) { 
    $promedio = $leidos / $dias; 
    return $promedio; 
}

// Llamada a la funcion y asignacion a una variable nueva
$velocidad_actual = calcularVelocidad($capitulos_leidos, $dias_lectura);

// Estructura if-else anidada con condiciones booleanas y relacionales compuestas
if ($capitulos_leidos == $capitulos_totales) { 
    echo "Lectura finalizada"; 
} else { 
    if ($velocidad_actual >= 20 && $estado_activo == true) {
        echo "Buen ritmo de lectura";
    } else {
        echo "Debes leer mas rapido";
    }
}
?>