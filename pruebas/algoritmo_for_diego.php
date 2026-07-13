<?php
// Prueba del bucle for - Diego Parrales
// Cubre las tres formas del paso: $i++, $i--, $i += n

// for clasico con incremento
$suma = 0;
for ($i = 0; $i < 10; $i++) {
    $suma += $i;
}
echo $suma;

// for con decremento
for ($j = 5; $j > 0; $j--) {
    echo $j;
}

// for con asignacion compuesta como paso
for ($k = 0; $k <= 100; $k += 10) {
    echo $k;
}

// for con break (valida el contexto de ciclo de Eimmy)
for ($n = 0; $n < 3; $n++) {
    if ($n == 2) {
        break;
    }
    echo $n;
}

// incremento como sentencia independiente
$contador = 0;
$contador++;
echo $contador;
?>
