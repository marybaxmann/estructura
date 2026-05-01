# usuario.py
# ─────────────────────────────────────────────────────────────
# USUARIO: Modela un perfil de usuario de la red social.
#
# Cada usuario tiene:
#   - Un nombre de usuario (ej: "cairdin")
#   - Una lista enlazada propia de contactos/amigos
#
# Los contactos se gestionan con ListaEnlazada, cumpliendo
# el requisito de memoria dinámica de la rúbrica:
#   "habrá una lista enlazada con sus contactos"
# ─────────────────────────────────────────────────────────────

from lista_enlazada import ListaEnlazada

class Usuario:
    def __init__(self, nombre):
        # Constructor del Usuario.
        # Ejemplo: u = Usuario("cairdin")

        self.nombre = nombre
        # Nombre de usuario tal como aparece en el CSV.
        # Ejemplo: "cairdin", "southwestair"

        self.contactos = ListaEnlazada()
        # Lista enlazada propia que almacena los nombres
        # de los contactos/amigos de este usuario.
        # Ejemplo: [yvonnalynn] → [jnardino] → None

    def agregar_contacto(self, nombre_contacto):
        # Agrega un contacto a la lista del usuario.
        # Verifica primero que no esté duplicado.
        # Si ya existe, no lo vuelve a insertar.

        if not self.contactos.existe(nombre_contacto):
            self.contactos.insertar(nombre_contacto)

    def tiene_contacto(self, nombre_contacto):
        # Verifica si un usuario específico es contacto de este perfil.
        # Retorna True o False.
        # Complejidad: O(n) — recorre la lista de contactos.

        return self.contactos.existe(nombre_contacto)

    def mostrar_contactos(self):
        # Imprime todos los contactos del usuario en pantalla.
        # Si no tiene contactos, muestra un mensaje informativo.

        print(f"Contactos de @{self.nombre}:")
        if self.contactos.esta_vacia():
            print("  (sin contactos registrados)")
        else:
            self.contactos.mostrar()