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

## Uso

`python SubtitleScale.py <input file .SRT> <first time hh:mm:ss,nnn> <last time hh:mm:ss,nnn>`

### Parámetros
- *input file*: Fichero de subtítulos a procesar, en formato .SRT
- *first time*: Instante de tiempo en el vídeo correspondiente al inicio del primer subtítulo
- *last time*: Instante de tiempo en el vídeo correspondiente al inicio del último subtítulo

Para determinar los tiempos, localizar en el fichero SRT el primer y el último subtítulo, y a continuación
examinar el vídeo para determinar los tiempos que corresponden realmente a dichos subtítulos. Una vez 
determinados esos tiempos, pasar el fichero y los dos tiempos como parámetros del programa.

El programa genera un fichero con el mismo nombre del fichero SRT, aunque añade la extensión .out al mismo.

## Problemas y singularidades
- El programa se ha hecho en Python 3. No se ha comprobado su funcionamiento con Python 2.
- El programa se hizo para Windows. El separador de líneas es CRLF = '\r\n'. Para Linux posiblemente deba ser '\n' a secas, pero no está probado.
- Los ficheros SRT usados estaban codificados con UTF-8. Esto implica un carácter de BOM al principio que hemos quitado sin contemplaciones eliminando el primer carácter del texto. Una codificación ANSI posiblemente no precise esta acción. En todo caso, estaba más allá de nuestras pretensiones verificar la codificación (o la existencia) del fichero entrante, y el caso UTF-8 era lo bastante general para los acentos y las eñes del español. Y no cuesta mucho abrir el SRT con Notepad y guardarlo como formato UTF-8, en todo caso.
- 
## Posibles mejoras
- Parámetro -out para proporcionar un nombre al fichero de salida
- Gestión más sofisticada de la codificación y existencia del fichero de entrada
