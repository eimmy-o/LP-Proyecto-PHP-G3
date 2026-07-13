<?php

// Prueba de estructura foreach y arrays
$numeros = [1,2,3,4];
foreach ($numeros as $numero) {
    echo $numero;
}

// definicion de clase con propiedades 

class Carro {

    public $marca = "Toyota";

    private $modelo = "Corolla";

}

$auto = new Carro();

echo $auto->marca;

 
// Funcion anonima para multiplicar dos numeros
$multiplicar = function($x, $y) {
    return $x * $y;
};
// Variable estatica dentro de una funcion
static $contador = 0;
$contador = $contador + 1;


echo $multiplicar(3, 4);
echo $contador;


?>