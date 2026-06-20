<?php
// Algoritmo de prueba - Diego Parrales
// Demuestra: constantes, switch, arreglos asociativos, funciones con parametros por defecto

/* Declaracion de constantes mediante define */
define("PI", 3.1416);
define("TASA_IVA", 0.15);

// Arreglo asociativo
$persona = ["nombre" => "Juan", "edad" => 30, "activo" => true];

// Funcion con parametro por defecto y concatenacion
function saludar($nombre = "Invitado") {
    echo "Hola " . $nombre;
}

// Funcion con operadores aritmeticos
function calcularTotal($precio = 0.0) {
    $impuesto = $precio * 0.15;
    return $precio + $impuesto;
}

// Estructura de control switch
$opcion = 2;
switch ($opcion) {
    case 1:
        echo "Opcion uno";
        break;
    case 2:
        echo "Opcion dos";
        break;
    default:
        echo "Opcion desconocida";
}

// Operadores de comparacion
$edad = 25;
$esMayor = $edad >= 18;
$noEsNulo = $edad != 0;
$esExacto = $opcion === 2;

// Operadores logicos
$tieneDni = true;
$esMayorYTieneDni = $esMayor && $tieneDni;
$esVipOAdmin = false || $tieneDni;

// Bucle while con suma-asignacion
$contador = 0;
while ($contador < 3) {
    $contador += 1;
}

// Llamadas a funciones
saludar("Diego");
saludar();

// Ingreso de datos por teclado
$nombre = readline();
$linea = fgets(STDIN);
echo $nombre;
?>
