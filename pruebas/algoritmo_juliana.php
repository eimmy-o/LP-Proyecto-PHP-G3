<?php

// Prueba de estructura foreach y arrays
$frutas = ["manzana", "pera", "uva", "sandia"];
$precios = ["manzana" => 1.50, "pera" => 0.75, "uva" => 2.00];

foreach ($frutas as $fruta) {
    echo $fruta;
}

foreach ($precios as $nombre => $precio) {
    echo $nombre;
    echo $precio;
}

// definicion de clase con propiedades y metodo

class Carro {

    public $marca = "Toyota";

    private $modelo = "Corolla";

    protected $anio = 2024;
}


 
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