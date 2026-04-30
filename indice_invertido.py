# indice_invertido.py
from lista_enlazada import ListaEnlazada

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
            return set()
        primera = self.buscar(palabras[0])
        if primera is None:
            return set()
        resultado = set(primera.obtener_todos())
        for palabra in palabras[1:]:
            lista = self.buscar(palabra)
            if lista is None:
                return set()
            resultado = resultado & set(lista.obtener_todos())
        return resultado

    def total_terminos(self):
        return len(self.vocabulario)


class IndiceInvertidoUsuarios:
    def __init__(self):
        self.indice = {}

    def agregar_usuario(self, nombre_usuario):
        if nombre_usuario not in self.indice:
            self.indice[nombre_usuario] = ListaEnlazada()

    def agregar_contacto(self, nombre_usuario, nombre_contacto):
        self.agregar_usuario(nombre_usuario)
        if not self.indice[nombre_usuario].existe(nombre_contacto):
            self.indice[nombre_usuario].insertar(nombre_contacto)

    def buscar_contactos(self, nombre_usuario):
        return self.indice.get(nombre_usuario, None)

    def existe_usuario(self, nombre_usuario):
        return nombre_usuario in self.indice

    def total_usuarios(self):
        return len(self.indice)