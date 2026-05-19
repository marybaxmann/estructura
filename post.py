# post.py
from lista_enlazada import ListaEnlazada

class Post:
    def __init__(self, post_id, texto, autor):
        self.post_id = post_id
        self.texto = texto
        self.autor = autor
        self.likes = ListaEnlazada()

    def agregar_like(self, nombre_usuario):
        if not self.likes.existe(nombre_usuario):
            self.likes.insertar(nombre_usuario)

    def obtener_likes(self):
        return self.likes.tamanio

    def mostrar(self):
        print(f"  [Post {self.post_id}] @{self.autor}: {self.texto[:100]}...")
        print(f"  Likes: {self.obtener_likes()}")

        if not self.likes.esta_vacia():
            self.mostrar_likes()
        
    def mostrar_likes(self):
        print(f"  Usuarios que dieron like ({self.likes.tamanio}):")
        if self.likes.esta_vacia():
            print("   (sin likes)")
        else:
            self.likes.mostrar()