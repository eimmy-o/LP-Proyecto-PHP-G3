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

class Persona {
    public $nombre;   // Propiedad pública

    // Constructor
    public function __construct($nombre) {
        $this->nombre = $nombre;
    }

    // Método público
    public function saludar() {
        return "Hola, mi nombre es " . $this->nombre;
    }
}

// Instancia de la clase
$persona = new Persona("Juliana");
// Llamada al método
echo $persona->saludar();

 
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