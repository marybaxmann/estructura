"""
Entrega III - Tabla Hash de Frecuencia de Terminos.

Implementacion propia de una tabla hash con funcion hash djb2 (Daniel J.
Bernstein) y resolucion de colisiones mediante encadenamiento separado,
usando la ListaEnlazada propia (Entrega I) en cada celda del arreglo.

No se utiliza dict, collections.Counter, HashMap ni ninguna estructura
hash provista por el lenguaje: toda la logica de indexacion, colision y
encadenamiento esta implementada manualmente.
"""

import math

from lista_enlazada import ListaEnlazada


class ParTermino:
    """
    Entrada almacenada dentro de cada celda (lista enlazada) de la tabla.
    Guarda el termino y su contador de frecuencia (numero de apariciones
    en el dataset).
    """

    def __init__(self, termino):
        self.termino = termino
        self.contador = 1

    def __eq__(self, otro):
        # Permite que ListaEnlazada.existe(...) compare por termino
        if isinstance(otro, ParTermino):
            return self.termino == otro.termino
        return self.termino == otro

    def __repr__(self):
        return f"({self.termino}: {self.contador})"


def es_primo(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def siguiente_primo(n):
    """Retorna el menor numero primo mayor o igual a n."""
    candidato = max(2, math.ceil(n))
    while not es_primo(candidato):
        candidato += 1
    return candidato


def calcular_tamanio_tabla(n_vocabulario, factor_carga_maximo=0.67):
    """
    Calcula M (tamanio de la tabla) como el menor primo que cumple
    M >= 1.5 * N, segun lo solicitado en el enunciado (factor de carga
    alpha <= 0.67 equivale a M >= N / 0.67 ~ 1.5 * N).

    Se usa math.ceil (no truncamiento) sobre 1.5 * N antes de buscar el
    primo, para garantizar que la cota M >= 1.5 * N nunca quede por
    debajo del minimo exigido por redondeo hacia abajo.
    """
    minimo_requerido = 1.5 * n_vocabulario
    return siguiente_primo(minimo_requerido)


class TablaHash:
    """
    Tabla hash propia con resolucion de colisiones por encadenamiento
    separado. Cada celda del arreglo es una ListaEnlazada propia que
    contiene objetos ParTermino (termino, contador).
    """

    def __init__(self, tamanio_m):
        self.M = tamanio_m
        self.tabla = [ListaEnlazada() for _ in range(self.M)]
        self.n_terminos_distintos = 0   # cantidad de claves distintas insertadas
        self.total_colisiones = 0       # veces que una insercion cayo en una celda ya ocupada

    # ------------------------------------------------------------------
    # Funcion Hash djb2 (obligatoria segun enunciado)
    # ------------------------------------------------------------------
    def _hash_djb2(self, cadena):
        """
        hash(0) = 5381
        hash(i) = hash(i-1) * 33 + c[i]
        Se trunca a 32 bits en cada iteracion (hash_val &= 0xFFFFFFFF) para
        reproducir el comportamiento natural de overflow de C/C++ (unsigned
        long) y Java (long), ya que Python maneja enteros de precision
        arbitraria.
        """
        hash_val = 5381
        for caracter in cadena:
            hash_val = (hash_val * 33 + ord(caracter)) & 0xFFFFFFFF
        return hash_val % self.M

    # ------------------------------------------------------------------
    # Insercion / actualizacion de frecuencia
    # ------------------------------------------------------------------
    def insertar_o_incrementar(self, termino):
        """
        Si el termino ya existe en la tabla, incrementa su contador en 1.
        Si no existe, lo inserta con contador = 1. Las colisiones se
        resuelven mediante encadenamiento separado (lista enlazada propia
        en la celda correspondiente).
        """
        indice = self._hash_djb2(termino)
        lista_celda = self.tabla[indice]

        # Buscar manualmente en la lista de la celda (encadenamiento)
        actual = lista_celda.cabeza
        while actual is not None:
            if actual.dato.termino == termino:
                actual.dato.contador += 1
                return
            actual = actual.siguiente

        # No existia: si la celda ya tenia al menos un elemento, es colision
        if not lista_celda.esta_vacia():
            self.total_colisiones += 1

        lista_celda.insertar(ParTermino(termino))
        self.n_terminos_distintos += 1

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def buscar(self, termino):
        """Retorna el contador (frecuencia) del termino, o 0 si no existe."""
        indice = self._hash_djb2(termino)
        actual = self.tabla[indice].cabeza
        while actual is not None:
            if actual.dato.termino == termino:
                return actual.dato.contador
            actual = actual.siguiente
        return 0

    def top_n(self, n=10):
        """
        Retorna una lista (python list, solo como contenedor de salida) de
        tuplas (termino, contador) con los N terminos mas frecuentes,
        ordenados de mayor a menor frecuencia. En caso de empate en la
        frecuencia, se ordena alfabeticamente para que el resultado sea
        determinista y reproducible.
        """
        todos = []
        for lista_celda in self.tabla:
            actual = lista_celda.cabeza
            while actual is not None:
                todos.append((actual.dato.termino, actual.dato.contador))
                actual = actual.siguiente

        todos.sort(key=lambda par: (-par[1], par[0]))
        return todos[:n]

    # ------------------------------------------------------------------
    # Metricas / estadisticas de la tabla
    # ------------------------------------------------------------------
    def factor_carga(self):
        return self.n_terminos_distintos / self.M

    def estadisticas_colisiones(self):
        """
        Retorna (total_colisiones, largo_maximo_cadena, largo_promedio_cadena).
        El largo promedio se calcula solo sobre las celdas ocupadas.
        """
        largo_maximo = 0
        suma_largos = 0
        celdas_ocupadas = 0

        for lista_celda in self.tabla:
            largo = lista_celda.tamanio
            if largo > 0:
                celdas_ocupadas += 1
                suma_largos += largo
            if largo > largo_maximo:
                largo_maximo = largo

        largo_promedio = (suma_largos / celdas_ocupadas) if celdas_ocupadas > 0 else 0.0
        return self.total_colisiones, largo_maximo, largo_promedio

    def mostrar_estadisticas(self, n_vocabulario=None):
        colisiones, largo_max, largo_prom = self.estadisticas_colisiones()
        print("\nEstadisticas de la Tabla Hash:")
        if n_vocabulario is not None:
            print(f"  N (vocabulario)        : {n_vocabulario}")
        print(f"  M (tamanio tabla)       : {self.M}")
        print(f"  Terminos distintos      : {self.n_terminos_distintos}")
        print(f"  Factor de carga (alpha) : {self.factor_carga():.4f}")
        print(f"  Total de colisiones     : {colisiones}")
        print(f"  Largo maximo de cadena  : {largo_max}")
        print(f"  Largo promedio de cadena: {largo_prom:.4f}")
        print()

    def mostrar_top_n(self, n=10):
        resultados = self.top_n(n)
        print(f"\nTop-{n} terminos mas frecuentes:")
        if not resultados:
            print("  (tabla vacia)")
        else:
            for posicion, (termino, contador) in enumerate(resultados, start=1):
                print(f"  {posicion:>2}. {termino:<20} {contador}")
        print()
