<?php
// Prueba de condicionales encadenados y anidamiento
// Cubre: if simple, else if separado, elseif junto, if dentro de if,
//        for dentro de for y for dentro de else.

$nota = 7;

// Cadena con 'else if' separado
if ($nota >= 9) {
    echo "Sobresaliente";
} else if ($nota >= 7) {
    echo "Aprobado";
} else {
    echo "Reprobado";
}

// Cadena con 'elseif' junto (ambas formas son PHP valido)
$dia = 3;
if ($dia == 1) {
    echo "Lunes";
} elseif ($dia == 2) {
    echo "Martes";
} elseif ($dia == 3) {
    echo "Miercoles";
} else {
    echo "Otro dia";
}

// if anidado dentro de otro if
$edad = 25;
$tieneDni = true;
if ($edad >= 18) {
    if ($tieneDni) {
        echo "Puede votar";
    }
}

// for anidado dentro de otro for (tabla de multiplicar)
for ($i = 1; $i <= 3; $i++) {
    for ($j = 1; $j <= 3; $j++) {
        echo $i * $j;
    }
}

// for dentro de un else, con break
if ($nota < 0) {
    echo "Nota invalida";
} else {
    for ($k = 0; $k < 5; $k++) {
        if ($k == 3) {
            break;
        }
        echo $k;
    }
}
?>
