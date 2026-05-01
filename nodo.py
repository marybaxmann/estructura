# nodo.py
# ─────────────────────────────────────────────────────────────
# NODO: Unidad básica de la Lista Enlazada
#
# Un Nodo es como una "caja" que almacena dos cosas:
#   1. Un DATO: el valor que queremos guardar
#   2. Una REFERENCIA: un puntero al siguiente nodo de la cadena
#
# Ejemplo visual de cómo se encadenan los nodos:
#
#   [dato: 42 | siguiente:──→] [dato: 7 | siguiente:──→] [dato: 1 | siguiente: None]
#
# Cuando "siguiente" es None, significa que es el último nodo.
#
# En este proyecto, el DATO puede ser:
#   - Un número entero → ID de un post (ej: 42)
#   - Un string       → nombre de usuario (ej: "cairdin")
# ─────────────────────────────────────────────────────────────

class Nodo:
    def __init__(self, dato):
        # Constructor del Nodo.
        # Se ejecuta automáticamente al crear un objeto Nodo.
        # Ejemplo de uso: n = Nodo(42)

        self.dato = dato
        # "dato" almacena el valor que queremos guardar en este nodo.
        # Puede ser cualquier tipo: int, string, etc.
        # Ejemplo: si indexamos el post número 42, self.dato = 42

        self.siguiente = None
        # "siguiente" es una referencia al próximo nodo en la cadena.
        # Por defecto es None, indicando que este nodo no tiene sucesor.
        # Cuando se inserta en la lista, se actualiza para apuntar
        # al nodo que estaba antes en el tope.
        #
        # Ejemplo:
        #   antes de insertar: self.siguiente = None
        #   después de insertar: self.siguiente = <Nodo con dato 7>