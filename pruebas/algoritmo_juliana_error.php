<?php

// ====================================================
// ERROR 1: Falta AS en foreach
// Se espera:
// foreach ($usuarios as $usuario)
// ====================================================

foreach ($usuarios $usuario) {

    echo $usuario;

}


// ====================================================
// ERROR 2: Falta ; en atributo de clase
// Se espera:
// public $marca = "Toyota";
// ====================================================

class Carro {

    public $marca = "Toyota"

}


// ====================================================
// ERROR 3: Instanciación incorrecta
// Falta el parentesis de cierre
// Se espera:
// $auto = new Carro();
// ====================================================

$auto = new Carro(;


// ====================================================
// ERROR 4: Operador objeto incompleto
// Se espera:
// echo $auto->marca;
// ====================================================

echo $auto->;


// ====================================================
// ERROR 5: Variable estática sin expresión
// Se espera:
// static $contador = 0;
// ====================================================

function contar() {

    static $contador = ;

}


// ====================================================
// ERROR 6: Closure mal cerrada
// Falta ;
// Se espera:
// };
// ====================================================

$multiplicar = function($x, $y) {

    return $x * $y;

}


// ====================================================
// ERROR 7: Llamada a closure incompleta
// Falta )
// Se espera:
// echo $multiplicar(3, 4);
// ====================================================

echo $multiplicar(3, 4;


?>