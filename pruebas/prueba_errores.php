<?php
// ==========================================
// ARCHIVO DE PRUEBA: ERRORES PARA INFORME
// ==========================================

// ------------------------------------------
// 1. ERRORES LEXICOS
// (Caracteres invalidos no reconocidos por los patrones del lexer)
// ------------------------------------------
$error_lexico_1 = ~100;
$error_lexico_2 = @;


// ------------------------------------------
// 2. ERRORES SINTACTICOS
// (Violaciones a la gramatica libre de contexto)
// ------------------------------------------

// Error sintactico 1: Falta punto y coma al final de la instruccion
$numero = 42
echo "El numero es: " . $numero;

// Error sintactico 2: Condicion de if sin parentesis (mal formada)
if $numero > 10 {
    echo "Mayor a 10";
}


// ------------------------------------------
// 3. ERRORES SEMANTICOS
// (Logica y coherencia del codigo)
// ------------------------------------------

// Error semantico 1 (Eimmy): Uso de variable NO inicializada previamente
$calculo = $variable_fantasma + 10;

// Error semantico 2 (Eimmy): Uso de break fuera de un ciclo o switch
if ($calculo == 10) {
    break;
}

// Error semantico 3 (Diego): Redefinicion de una constante
define("IMPUESTO", 0.15);
define("IMPUESTO", 0.12);

// Error semantico 4 (Juliana): Invocacion con cantidad incorrecta de argumentos
function multiplicar($a, $b) {
    return $a * $b;
}
multiplicar(5); 

// Error semantico 5 (Juliana): Closure (funcion anonima) sin instruccion return
$operacion = function($valor) {
    $doble = $valor * 2;
};

// Advertencia Semantica (Diego): Operacion aritmetica usando un string (cadena)
$advertencia_cadena = "Hola" + 10;
?>
