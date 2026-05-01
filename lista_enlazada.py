# lista_enlazada.py
# ─────────────────────────────────────────────────────────────
# LISTA ENLAZADA: Estructura dinámica de datos implementada
# íntegramente por los estudiantes (sin usar listas de Python).
#
# Es una cadena de Nodos conectados entre sí:
#   tope → [dato|sig→] → [dato|sig→] → [dato|None]
#
# En este proyecto se usa para:
#   1. Listas de posteo: guardar IDs de posts por palabra
#   2. Listas de contactos: guardar amigos de cada usuario
#   3. Listas de likes: guardar usuarios que dieron like
#
# La inserción siempre es al INICIO de la lista (tope),
# lo que garantiza complejidad O(1).
# ─────────────────────────────────────────────────────────────

from nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        # Constructor de la lista enlazada.
        # Inicializa una lista vacía.

        self.tope = None
        # Referencia al primer nodo (cabeza) de la lista.
        # None significa que la lista está vacía.

        self.tamanio = 0
        # Contador de elementos en la lista.
        # Se incrementa en cada inserción exitosa.

    def insertar(self, dato):
        # Inserta un nuevo dato AL INICIO de la lista.
        # Complejidad: O(1) — siempre inserta al tope, sin recorrer.
        #
        # Proceso:
        #   1. Crea un nuevo Nodo con el dato
        #   2. El nuevo nodo apunta al antiguo tope
        #   3. El tope ahora es el nuevo nodo
        #
        # Ejemplo (insertando 3 → 7 → 42):
        #   después de insertar 3:  tope→[3|None]
        #   después de insertar 7:  tope→[7|→3]→[3|None]
        #   después de insertar 42: tope→[42|→7]→[7|→3]→[3|None]

        nuevo = Nodo(dato)           # Crear nueva caja con el dato
        nuevo.siguiente = self.tope  # Conectar al nodo anterior
        self.tope = nuevo            # Actualizar el tope
        self.tamanio += 1            # Incrementar contador

    def existe(self, dato):
        # Verifica si un dato ya existe en la lista.
        # Complejidad: O(n) — recorre nodo por nodo hasta encontrarlo.
        #
        # Se usa para evitar duplicados al insertar
        # post_ids o nombres de usuario.
        #
        # Retorna True si el dato existe, False si no.

        actual = self.tope           # Comenzar desde el primer nodo
        while actual is not None:    # Mientras haya nodos por recorrer
            if actual.dato == dato:  # Si el dato coincide
                return True          # Lo encontró → existe
            actual = actual.siguiente  # Avanzar al siguiente nodo
        return False                 # Recorrió toda la lista sin encontrarlo

    def obtener_todos(self):
        # Recorre la lista y retorna todos los datos como lista Python.
        # Se usa para hacer intersecciones en búsquedas de múltiples términos.
        # Complejidad: O(n)

        resultado = []
        actual = self.tope
        while actual is not None:
            resultado.append(actual.dato)  # Agregar dato a la lista Python
            actual = actual.siguiente
        return resultado

    def mostrar(self):
        # Recorre e imprime todos los elementos de la lista.
        # Se usa al mostrar contactos de un usuario en el menú.
        # Complejidad: O(n)

        actual = self.tope
        while actual is not None:
            print(" -", actual.dato)
            actual = actual.siguiente

    def esta_vacia(self):
        # Retorna True si la lista no tiene elementos.
        # Complejidad: O(1) — solo verifica si tope es None.

        return self.tope is None