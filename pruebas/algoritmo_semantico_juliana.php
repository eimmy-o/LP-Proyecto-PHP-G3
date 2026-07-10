<?php

/* ---------- Declaracion de funciones ---------- */

// Funcion con 2 parametros obligatorios
function sumar($a, $b) {
    return $a + $b;
}

// Funcion con 1 parametro con valor por defecto (0 a 1 argumentos validos)
function saludar($nombre = "Invitado") {
    echo "Hola";
}

/* ---------- REGLA 1: Cantidad de argumentos en la llamada ---------- */

// -- Casos correctos (no generan error) --
$resultado1 = sumar(5, 3);       // OK: 2 argumentos para 2 parametros obligatorios
saludar("Juliana");              // OK: dentro del rango permitido (0 a 1)
saludar();                       // OK: el parametro tiene valor por defecto

// -- Casos incorrectos (ERROR semantico) --
$resultado2 = sumar(5);              // ERROR: faltan argumentos (sumar espera 2)
$resultado3 = sumar(1, 2, 3);        // ERROR: demasiados argumentos (sumar espera 2)
saludar("Juliana", "Extra");         // ERROR: saludar admite maximo 1 argumento

/* ---------- REGLA 2: Return obligatorio en funciones asignadas a variables ---------- */

// CASO CORRECTO: el closure SI contiene la instruccion return
$duplicar = function($x) {
    return $x * 2;
};

// CASO INCORRECTO: el closure NO contiene la instruccion return
// ERROR SEMANTICO: toda funcion anonima asignada a una variable debe
// retornar un valor mediante 'return'.
$imprimirSaludo = function($nombre) {
    echo "Hola";
};

echo $duplicar(4);
?>
