# usuario.py
from lista_enlazada import ListaEnlazada

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.contactos = ListaEnlazada()

    def agregar_contacto(self, nombre_contacto):
        if not self.contactos.existe(nombre_contacto):
            self.contactos.insertar(nombre_contacto)

    def tiene_contacto(self, nombre_contacto):
        return self.contactos.existe(nombre_contacto)

    def mostrar_contactos(self):
        print(f"Contactos de @{self.nombre}:")
        if self.contactos.esta_vacia():
            print("  (sin contactos registrados)")
        else:
            self.contactos.mostrar()