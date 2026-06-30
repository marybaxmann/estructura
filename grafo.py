"""
Entrega II - Grafo de Contactos (no dirigido) y Algoritmo de Grados de Conexión.

El grafo se construye a partir del Indice Invertido de Usuarios (Entrega I),
reutilizando la ListaEnlazada propia para representar la lista de adyacencia
de cada usuario. El recorrido por niveles (grados de conexion) se realiza
mediante BFS (Breadth-First Search), respetando la restriccion de no usar
funciones de bibliotecas que entreguen directamente los grados, distancias
o caminos minimos.
"""

from collections import deque
from lista_enlazada import ListaEnlazada


class Grafo:
    """
    Grafo no dirigido G = (V, E) implementado mediante lista de adyacencia.

    V: usuarios de la red social (claves del diccionario self.adyacencia).
    E: relaciones de amistad, almacenadas como ListaEnlazada propia por nodo.
    """

    def __init__(self):
        # Diccionario: usuario -> ListaEnlazada de usuarios vecinos (amigos directos)
        self.adyacencia = {}

    # ------------------------------------------------------------------
    # Construccion del grafo a partir del Indice Invertido de Usuarios (Entrega I)
    # ------------------------------------------------------------------
    def construir_desde_indice(self, indice_usuarios, mostrar_reporte=True):
        """
        Recorre el IndiceInvertidoUsuarios (Entrega I) y construye la lista
        de adyacencia no dirigida, validando que las relaciones sean simetricas
        (si A es amigo de B, entonces B es amigo de A) y sin aristas duplicadas
        ni bucles (un usuario no es contacto de si mismo).
        """
        # 0) Validar simetria del indice ORIGINAL antes de construir el grafo.
        #    Esto detecta y reporta relaciones unidireccionales presentes en
        #    los datos de origen (p. ej. A->B sin B->A en amigos.csv).
        relaciones_asimetricas = self.validar_simetria(indice_usuarios)
        if mostrar_reporte:
            self._reportar_simetria(relaciones_asimetricas)

        # 1) Crear un vertice para cada usuario registrado en el indice
        for nombre_usuario in indice_usuarios.indice:
            self._asegurar_vertice(nombre_usuario)

        # 2) Agregar las aristas (relaciones de amistad). El grafo resultante
        #    es no dirigido por construccion: agregar_arista() siempre crea
        #    la relacion en ambos sentidos, independientemente de si el dato
        #    de origen era o no simetrico (las asimetrias ya fueron
        #    reportadas en el paso anterior).
        for nombre_usuario, objeto_usuario in indice_usuarios.indice.items():
            contactos = objeto_usuario.contactos.obtener_todos()
            for nombre_contacto in contactos:
                self.agregar_arista(nombre_usuario, nombre_contacto)

        return relaciones_asimetricas

    def validar_simetria(self, indice_usuarios):
        """
        Recorre el IndiceInvertidoUsuarios y detecta relaciones que NO son
        simetricas en los datos de origen, es decir, casos donde A tiene a
        B como contacto pero B no tiene a A (antes de cualquier correccion).

        Retorna una lista de tuplas (A, B) con las relaciones faltantes
        (la relacion inversa que no estaba presente).
        """
        faltantes = []
        for nombre_usuario, objeto_usuario in indice_usuarios.indice.items():
            for nombre_contacto in objeto_usuario.contactos.obtener_todos():
                contacto_objeto = indice_usuarios.indice.get(nombre_contacto)
                tiene_inversa = (
                    contacto_objeto is not None
                    and contacto_objeto.tiene_contacto(nombre_usuario)
                )
                if not tiene_inversa:
                    faltantes.append((nombre_usuario, nombre_contacto))
        return faltantes

    def _reportar_simetria(self, relaciones_asimetricas):
        if not relaciones_asimetricas:
            print("Validacion de simetria: todas las relaciones del indice "
                  "de usuarios son simetricas.")
            return

        print(f"Validacion de simetria: se detectaron "
              f"{len(relaciones_asimetricas)} relacion(es) unidireccional(es) "
              f"en los datos de origen (se corrigen automaticamente al "
              f"construir el grafo no dirigido):")
        for usuario, contacto in relaciones_asimetricas:
            print(f"    @{usuario} -> @{contacto}  (faltaba @{contacto} -> @{usuario})")

    def _asegurar_vertice(self, usuario):
        if usuario not in self.adyacencia:
            self.adyacencia[usuario] = ListaEnlazada()

    def agregar_arista(self, usuario_a, usuario_b):
        """
        Agrega una arista no dirigida entre usuario_a y usuario_b.
        - No se permiten bucles (un usuario no puede ser contacto de si mismo).
        - No se permiten aristas duplicadas (se valida con ListaEnlazada.existe).
        - La relacion se agrega en ambos sentidos (grafo no dirigido).
        """
        if usuario_a == usuario_b:
            return  # evitar bucle

        self._asegurar_vertice(usuario_a)
        self._asegurar_vertice(usuario_b)

        if not self.adyacencia[usuario_a].existe(usuario_b):
            self.adyacencia[usuario_a].insertar(usuario_b)

        if not self.adyacencia[usuario_b].existe(usuario_a):
            self.adyacencia[usuario_b].insertar(usuario_a)

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def existe_usuario(self, usuario):
        return usuario in self.adyacencia

    def total_usuarios(self):
        return len(self.adyacencia)

    def total_aristas(self):
        # Cada arista se cuenta una vez (no dirigida): suma de grados / 2
        suma_grados = sum(lista.tamanio for lista in self.adyacencia.values())
        return suma_grados // 2

    def vecinos(self, usuario):
        return self.adyacencia.get(usuario, None)

    def grado_del_vertice(self, usuario):
        lista = self.adyacencia.get(usuario)
        return lista.tamanio if lista is not None else 0

    # ------------------------------------------------------------------
    # Algoritmo de Grados de Conexion (BFS por niveles)
    # ------------------------------------------------------------------
    def grados_conexion(self, usuario_raiz, grado_maximo=3):
        """
        Dado un usuario raiz u, retorna un diccionario {1: ListaEnlazada,
        2: ListaEnlazada, 3: ListaEnlazada, ...} con los contactos de 1°, 2°
        y 3° grado, sin duplicados entre niveles.

        Se basa en BFS (Breadth-First Search) con control explicito de
        niveles: cada usuario se visita una sola vez (set 'visitados' como
        estructura de apoyo permitida por el enunciado) y se etiqueta con
        su grado de distancia respecto de la raiz en el momento en que se
        descubre, evitando que aparezca en mas de un nivel.

        Retorna None si el usuario raiz no existe en el grafo.
        """
        if usuario_raiz not in self.adyacencia:
            return None

        # Estructuras de apoyo para BFS (permitidas explicitamente por el enunciado)
        visitados = {usuario_raiz}
        cola = deque()
        cola.append((usuario_raiz, 0))

        # Un nivel (ListaEnlazada propia) por cada grado solicitado
        niveles = {grado: ListaEnlazada() for grado in range(1, grado_maximo + 1)}

        while cola:
            usuario_actual, grado_actual = cola.popleft()

            if grado_actual >= grado_maximo:
                # No seguimos expandiendo mas alla del grado maximo solicitado
                continue

            lista_vecinos = self.adyacencia.get(usuario_actual)
            if lista_vecinos is None:
                continue

            for vecino in lista_vecinos.obtener_todos():
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_grado = grado_actual + 1
                    niveles[nuevo_grado].insertar(vecino)
                    cola.append((vecino, nuevo_grado))

        return niveles

    # ------------------------------------------------------------------
    # Presentacion en consola
    # ------------------------------------------------------------------
    def mostrar_grados_conexion(self, usuario_raiz, grado_maximo=3):
        niveles = self.grados_conexion(usuario_raiz, grado_maximo)

        if niveles is None:
            print(f"El usuario '@{usuario_raiz}' no existe en el grafo de contactos.")
            return

        print(f"\nGrados de conexion desde @{usuario_raiz}:")
        for grado in range(1, grado_maximo + 1):
            lista = niveles[grado]
            cantidad = lista.tamanio
            print(f"\n  Contactos de {grado}° grado ({cantidad}):")
            if lista.esta_vacia():
                print("    (ninguno)")
            else:
                for nombre in sorted(lista.obtener_todos()):
                    print(f"    - @{nombre}")
        print()
