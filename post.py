# post.py
# ─────────────────────────────────────────────────────────────
# POST: Modela una publicación (tweet) de la red social.
#
# Cada post tiene:
#   - Un ID único (número de fila en el CSV)
#   - El texto original del tweet
#   - El autor (nombre de usuario)
#   - Una lista enlazada de likes (usuarios que dieron like)
#
# Los likes se gestionan con ListaEnlazada propia,
# lo que garantiza que no haya duplicados y que se
# almacene en memoria dinámica según lo pedido en la rúbrica.
# ─────────────────────────────────────────────────────────────

from lista_enlazada import ListaEnlazada

class Post:
    def __init__(self, post_id, texto, autor):
        # Constructor del Post.
        # Se ejecuta al crear un objeto Post.
        # Ejemplo: post = Post(42, "I love flying!", "cairdin")

        self.post_id = post_id
        # Identificador único del post.
        # Corresponde al índice (número de fila) en el CSV.
        # Se usa para recuperar el post desde la lista global "posts[]"

        self.texto = texto
        # Texto original del tweet tal como aparece en el CSV.
        # Ejemplo: "@VirginAmerica I love this airline!"

        self.autor = autor
        # Nombre de usuario del autor del tweet.
        # Ejemplo: "cairdin", "jnardino"

        self.likes = ListaEnlazada()
        # Lista enlazada propia que almacena los nombres de usuarios
        # que dieron like a este post.
        # Se usa ListaEnlazada para cumplir con el requisito de
        # memoria dinámica de la rúbrica.
        # Ejemplo: [yvonnalynn] → [cairdin] → None

    def agregar_like(self, nombre_usuario):
        # Agrega un like de un usuario al post.
        # Primero verifica que el usuario no haya dado like antes (sin duplicados).
        # Si no existe, lo inserta en la lista enlazada de likes.
        if not self.likes.existe(nombre_usuario):
            self.likes.insertar(nombre_usuario)

    def obtener_likes(self):
        # Retorna la cantidad de likes del post.
        # Usa el atributo "tamanio" de ListaEnlazada que se
        # actualiza automáticamente en cada inserción.
        return self.likes.tamanio

    def mostrar(self):
        # Imprime la información del post en pantalla.
        # Muestra solo los primeros 100 caracteres del texto
        # para no saturar la terminal.
        print(f"  [Post {self.post_id}] @{self.autor}: {self.texto[:100]}...")
        print(f"  Likes: {self.obtener_likes()}")