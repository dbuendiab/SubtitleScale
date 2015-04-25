# SubtitleScale
Utilidad para reescalar en el tiempo subtítulos en formato SRT, cuando los textos se decalan de forma lineal.

## Concepto
A veces un fichero de subtítulos no está bien sincronizado con la película. Puede que sea un decalaje constante,
en cuyo caso bastaría con añadir el tiempo del desfase a cada comentario para que los subtítulos volvieran a estar
en sincronía, pero a menudo me he encontrado con desfases que van aumentando a lo largo del tiempo, de modo que
lo que al principio eran apenas unas décimas de segundo se convierten a final incluso en minutos de diferencia.

Para arreglar esta falta de sincronismo, hay que añadir (o restar) a cada subtítulo una cantidad de tiempo que 
es proporcional al tiempo transcurrido desde el principio. Este programa toma como parámetros los instantes del 
primer y del último subtítulo, y hace los cálculos para cambiar esos instantes en el fichero SRT para que 
coincidan con los de la película. Además, interpolan los instantes de los demás subtítulos linealmente a partir
de los dos extremos, asumiendo que las variaciones, como dijimos, se producen linealmente.

El programa no dará iguales resultados si los desfases en el sincronismo presentan saltos bruscos. Lo que sí está
garantizado es que el primer y el último subtítulo coincidirán con los instantes de tiempo que se hayan pasado
como parámetros.
