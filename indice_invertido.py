# indice_invertido.py
from lista_enlazada import ListaEnlazada
from usuario import Usuario

class IndiceInvertidoPosts:

    def __init__(self):
        self.vocabulario = {}

    def agregar(self, palabra, post_id):

        if palabra not in self.vocabulario:
            self.vocabulario[palabra] = ListaEnlazada()

        if not self.vocabulario[palabra].existe(post_id):
            self.vocabulario[palabra].insertar(post_id)

    def buscar(self, palabra):
        return self.vocabulario.get(palabra, None)

    def buscar_multiples(self, palabras):

        if not palabras:
            return ListaEnlazada()

        resultado = self.buscar(palabras[0])

        if resultado is None:
            return ListaEnlazada()

        for palabra in palabras[1:]:

            lista_actual = self.buscar(palabra)

            if lista_actual is None:
                return ListaEnlazada()

            resultado = self._interseccion(resultado, lista_actual)

            if resultado.esta_vacia():
                return resultado

        return resultado

    def _interseccion(self, lista_a, lista_b):

        resultado = ListaEnlazada()

        actual = lista_a.cabeza

        while actual is not None:

            if lista_b.existe(actual.dato):
                resultado.insertar(actual.dato)

            actual = actual.siguiente

        return resultado

    def total_terminos(self):
        return len(self.vocabulario)


class IndiceInvertidoUsuarios:

    def __init__(self):
        self.indice = {}

    def agregar_usuario(self, nombre_usuario):

        if nombre_usuario not in self.indice:
            self.indice[nombre_usuario] = Usuario(nombre_usuario)

    def agregar_contacto(self, nombre_usuario, nombre_contacto):

        self.agregar_usuario(nombre_usuario)

        usuario = self.indice[nombre_usuario]

        if not usuario.tiene_contacto(nombre_contacto):
            usuario.agregar_contacto(nombre_contacto)

    def buscar_contactos(self, nombre_usuario):

        usuario = self.indice.get(nombre_usuario, None)

        if usuario is None:
            return None

        return usuario.contactos

    def existe_usuario(self, nombre_usuario):
        return nombre_usuario in self.indice

    def total_usuarios(self):
        return len(self.indice)