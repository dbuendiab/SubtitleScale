## -*- coding: utf-8 -*-
"""
    Utilidad para realinear los subtítulos de una película de forma lineal
    La idea es tomar el tiempo del primer y último subtítulo del fichero
    de subtítulos y los correspondientes tiempos de los comentarios en la
    película y a partir de ahí hace una interpolación lineal de los tiempos
    corregidos de los subtítulos.
"""
import argparse
import codecs
import sys
from datetime import datetime, timedelta
import time

CRLF = '\r\n'

def procesar_texto(tx):
    """Crear una lista con los subtítulos. Cada elemento de la lista
es una lista con el número, el tiempo de inicio, el tiempo final y el texto"""
    salida = []
    subtitulos = tx.split(CRLF + CRLF)  ## Debe haber una línea vacía entre subtítulos
    for item in subtitulos:
        elementos = item.split(CRLF)    ## Los elementos del subt. están en líneas aparte
        try:
            n = int(elementos[0])
            t = elementos[1].split(' --> ') ## Separador de tiempos en formato SRT
            t1 = procesar_instante(t[0])    ## Conversión a segundos
            t2 = procesar_instante(t[1])
            texto = CRLF.join(elementos[2:])    ## Las líneas del subtítulo se vuelven a unir
            salida.append([n, t1, t2, texto])
        except:
            pass
    return salida

    
def procesar_instante(str_t):
    """Extraer el timestamp de la hora hh:mm:ss,nnn"""
    h = m = s = ms = 0
    tmp = str_t.split(':')
    lentmp = len(tmp)
    if lentmp > 3:
        print('Formato fecha %s incorrecto' % str_t)
        sys.exit()
    elif lentmp == 3:
        h = tmp[0]
        m = tmp[1]
        s = tmp[2]
    elif lentmp == 2:
        m = tmp[0]
        s = tmp[1]
    elif lentmp == 1:
        s = tmp[0]
    else:
        print('Error raro')
        sys.exit()

    s, ms = s.split(',')

    h = int(h)
    m = int(m)
    s = int(s)
    ms = float('0.' + ms)

    return h * 3600 + m * 60 + s + ms


def instante_a_str(ts):
    """Devolver formato hh:mm:ss,nnn a un tiempo en segundos"""
    return str(timedelta(seconds=ts))[:-3].replace('.', ',')    ## 3 decimales sólo, y con (,) en vez de (.)


def procesar(tx, tv0, tv1):
    """Interpolador de tiempos: cálculo de los coeficientes m en y=mx+b"""
    s0 = tx[0][1]   # Tiempo (original) del primer subtitulo
    s1 = tx[-1][1]  # Tiempo (original) del último subtítulo
    n0 = 1          # x del primer elemento
    n1 = len(tx)    # x del último elemento
    
    m_sub = (s1 - s0) / (n1 - n0)   # Cálculo de la m de los subtítulos
    m_vid = (tv1 - tv0) / (n1 - n0) # Cálculo de la m del vídeo
    b_sub = s0                      # Cálculo de la b de los subtítulos
    b_vid = tv0                     # Cálculo de la b del vídeo

    print('s0:', s0)
    print('s1:', s1)
    print('v0:', tv0)
    print('v1:', tv1)

    print('m_sub:', m_sub, 'b_sub:', b_sub)
    print('m_vid:', m_vid, 'b_vid:', b_vid)

    salida = []
    coef = m_vid / m_sub    # Coeficiente de corrección

    # Función interna para conversión de tiempos según los coeficientes anteriores
    def conversion(y1):
        y_vid = coef * (y1 - b_sub) + b_vid
        return y_vid

    # Cálculo y almacenamiento de los nuevos tiempos
    for i, item in enumerate(tx):
        n = i
        t0 = conversion(item[1])
        t1 = conversion(item[2])

        #print (item[1], t0)
        #print(item[2], t1)
        
        texto = item[3]
        
        intervalo = instante_a_str(t0) + ' --> ' + instante_a_str(t1)
        salida.append(CRLF.join([str(n+1), intervalo, texto])+CRLF)

    return salida


def main():
    parser = argparse.ArgumentParser(description='Utilidad para realinear subtítulos')
    parser.add_argument('infile', help='Fichero de subtítulos (extensión .srt)')
    parser.add_argument('v1', help='Tiempo en el vídeo del primer subtítulo (formato hh:mm:ss,nnn)')
    parser.add_argument('v2', help='Tiempo en el vídeo del último subtítulo (formato hh:mm:ss,nnn)')
    args = parser.parse_args()

    try:
        f = codecs.open(args.infile, 'r', encoding='UTF-8')
        texto = f.read()[1:]    ## Quitar el BOM
        f.close()
    except Exception as e:
        print('Error en la apertura del fichero', e)
        sys.exit()

    tx = procesar_texto(texto)
    v1 = procesar_instante(args.v1)
    v2 = procesar_instante(args.v2)
    
    salida = procesar(tx, v1, v2)

    print(salida)

    f = codecs.open(args.infile + '.out', 'w', encoding='UTF-8')
    f.write(CRLF.join(salida))
    f.close()
    
#----------------------------------------------------------------------------
main()
