# lista_enlazada.py
from nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.tope = None
        self.tamanio = 0

    def insertar(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.tamanio += 1

    def existe(self, dato):
        actual = self.tope
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def obtener_todos(self):
        resultado = []
        actual = self.tope
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def mostrar(self):
        actual = self.tope
        while actual is not None:
            print(" -", actual.dato)
            actual = actual.siguiente

    def esta_vacia(self):
        return self.tope is None