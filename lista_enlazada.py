from nodo import Nodo

class ListaEnlazada:

    def __init__(self):
        self.cabeza = None
        self.tamanio = 0
#insertar
    def insertar(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio += 1
#existe
    def existe(self, dato):
        actual = self.cabeza

        while actual is not None:

            if actual.dato == dato:
                return True

            actual = actual.siguiente

        return False

    def obtener_todos(self):
        resultado = []

        actual = self.cabeza

        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente

        return resultado

    def mostrar(self):

        actual = self.cabeza

        while actual is not None:
            print(" -", actual.dato)
            actual = actual.siguiente

    def esta_vacia(self):
        return self.cabeza is None

#eliminar
    def eliminar(self, dato):

        if self.cabeza is None:
            return False

        # eliminar cabeza
        if self.cabeza.dato == dato:

            temp = self.cabeza
            self.cabeza = self.cabeza.siguiente

            del temp

            self.tamanio -= 1
            return True

        anterior = self.cabeza

        while anterior.siguiente is not None:

            if anterior.siguiente.dato == dato:

                temp = anterior.siguiente

                anterior.siguiente = temp.siguiente

                del temp

                self.tamanio -= 1
                return True

            anterior = anterior.siguiente

        return False
#vaciar
    def vaciar(self):

        while self.cabeza is not None:

            temp = self.cabeza

            self.cabeza = self.cabeza.siguiente

            del temp

        self.tamanio = 0