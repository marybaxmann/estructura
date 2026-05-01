# indice_invertido.py
# ─────────────────────────────────────────────────────────────
# ÍNDICE INVERTIDO: Núcleo del sistema de búsqueda.
#
# Contiene DOS clases de índice invertido:
#
#   1. IndiceInvertidoPosts:
#      Mapea palabras → posts donde aparece esa palabra.
#      Funciona como el índice de un libro:
#      en vez de leer los 14.640 tweets uno por uno,
#      se va directo a la entrada de la palabra buscada.
#
#   2. IndiceInvertidoUsuarios:
#      Mapea usuarios → lista de sus contactos/amigos.
#      Permite buscar eficientemente los amigos de un usuario.
#
# Ambos usan:
#   - Un DICCIONARIO Python como estructura de mapa (clave→valor)
#   - LISTAS ENLAZADAS propias como listas de posteo/contactos
#
# Ejemplo visual del IndiceInvertidoPosts:
#
#   vocabulario = {
#     "delayed": [post_203] → [post_45] → [post_10] → None,
#     "flight":  [post_88]  → [post_10] → [post_1]  → None,
#     "cancel":  [post_45]  → [post_88] → None
#   }
#
# Ejemplo visual del IndiceInvertidoUsuarios:
#
#   indice = {
#     "cairdin":  [yvonnalynn] → [jnardino] → None,
#     "jnardino": [cjmcginnis] → [cairdin]  → None
#   }
# ─────────────────────────────────────────────────────────────

from lista_enlazada import ListaEnlazada


# ══════════════════════════════════════════════════════════════
# CLASE 1: Índice Invertido de Posts (término → posts)
# ══════════════════════════════════════════════════════════════
class IndiceInvertidoPosts:
    def __init__(self):
        # Constructor del índice de posts.
        # Inicializa el vocabulario como diccionario vacío.

        self.vocabulario = {}
        # Diccionario Python que actúa como mapa del índice.
        # Clave:  string (palabra/término)
        # Valor:  ListaEnlazada de post_ids (enteros)
        # Ejemplo: {"delayed": ListaEnlazada([203, 45, 10])}

    def agregar(self, palabra, post_id):
        # Asocia una palabra con un post_id en el índice.
        #
        # Proceso:
        #   1. Si la palabra no existe en el vocabulario,
        #      crea una nueva ListaEnlazada para ella.
        #   2. Verifica que el post_id no esté ya en la lista
        #      (evita duplicados).
        #   3. Inserta el post_id en la lista enlazada.
        #
        # Ejemplo:
        #   agregar("delayed", 10) → vocabulario["delayed"] = [10]
        #   agregar("delayed", 45) → vocabulario["delayed"] = [45→10]
        #   agregar("delayed", 10) → no hace nada (duplicado)

        if palabra not in self.vocabulario:
            # Primera vez que aparece esta palabra → crear lista nueva
            self.vocabulario[palabra] = ListaEnlazada()

        if not self.vocabulario[palabra].existe(post_id):
            # Solo insertar si el post_id no está ya en la lista
            self.vocabulario[palabra].insertar(post_id)

    def buscar(self, palabra):
        # Busca una palabra en el vocabulario y retorna
        # su lista enlazada de post_ids.
        #
        # Complejidad: O(1) — acceso directo al diccionario.
        #
        # Retorna:
        #   - ListaEnlazada con los post_ids si la palabra existe
        #   - None si la palabra no está en el vocabulario

        return self.vocabulario.get(palabra, None)

    def buscar_multiples(self, palabras):
        # Busca posts que contengan TODAS las palabras indicadas.
        # Realiza una intersección (AND) entre las listas de cada palabra.
        #
        # Ejemplo:
        #   buscar_multiples(["delayed", "flight"])
        #   → posts que contengan "delayed" Y "flight"
        #
        # Proceso:
        #   1. Obtiene los post_ids de la primera palabra
        #   2. Los convierte a conjunto (set) para intersectar
        #   3. Por cada palabra siguiente, intersecta con su lista
        #   4. Si alguna palabra no existe → resultado vacío
        #
        # Retorna un conjunto (set) de post_ids comunes.

        if not palabras:
            return set()

        # Obtener IDs de la primera palabra como conjunto base
        primera = self.buscar(palabras[0])
        if primera is None:
            return set()  # Si la primera palabra no existe, resultado vacío

        resultado = set(primera.obtener_todos())

        # Intersectar con cada palabra restante
        for palabra in palabras[1:]:
            lista = self.buscar(palabra)
            if lista is None:
                return set()  # Si alguna palabra no existe, intersección vacía
            resultado = resultado & set(lista.obtener_todos())
            # El operador & retorna solo los IDs que están en AMBOS conjuntos

        return resultado

    def total_terminos(self):
        # Retorna la cantidad de términos únicos en el vocabulario.
        # Se usa al mostrar el resumen de carga del dataset.

        return len(self.vocabulario)


# ══════════════════════════════════════════════════════════════
# CLASE 2: Índice Invertido de Usuarios (usuario → contactos)
# ══════════════════════════════════════════════════════════════
class IndiceInvertidoUsuarios:
    def __init__(self):
        # Constructor del índice de usuarios.
        # Inicializa el índice como diccionario vacío.

        self.indice = {}
        # Diccionario Python que actúa como mapa del índice.
        # Clave:  string (nombre de usuario)
        # Valor:  ListaEnlazada de nombres de contactos (strings)
        # Ejemplo: {"cairdin": ListaEnlazada(["yvonnalynn", "jnardino"])}

    def agregar_usuario(self, nombre_usuario):
        # Registra un usuario en el índice si no existe aún.
        # Crea una lista enlazada vacía para sus contactos.
        #
        # Se llama automáticamente al cargar el dataset
        # por cada autor de tweet y cada aerolínea mencionada.

        if nombre_usuario not in self.indice:
            self.indice[nombre_usuario] = ListaEnlazada()

    def agregar_contacto(self, nombre_usuario, nombre_contacto):
        # Agrega nombre_contacto a la lista de contactos de nombre_usuario.
        #
        # Proceso:
        #   1. Si el usuario no existe, lo registra primero
        #   2. Verifica que el contacto no esté duplicado
        #   3. Inserta el contacto en la lista enlazada
        #
        # Ejemplo:
        #   agregar_contacto("cairdin", "jnardino")
        #   → indice["cairdin"] = [jnardino] → None
        #
        #   agregar_contacto("cairdin", "yvonnalynn")
        #   → indice["cairdin"] = [yvonnalynn] → [jnardino] → None

        self.agregar_usuario(nombre_usuario)
        # Garantiza que el usuario exista antes de agregar contacto

        if not self.indice[nombre_usuario].existe(nombre_contacto):
            # Solo insertar si el contacto no está ya en la lista
            self.indice[nombre_usuario].insertar(nombre_contacto)

    def buscar_contactos(self, nombre_usuario):
        # Retorna la lista enlazada de contactos de un usuario.
        #
        # Complejidad: O(1) — acceso directo al diccionario.
        #
        # Retorna:
        #   - ListaEnlazada con los contactos si el usuario existe
        #   - None si el usuario no está registrado

        return self.indice.get(nombre_usuario, None)

    def existe_usuario(self, nombre_usuario):
        # Verifica si un usuario está registrado en el índice.
        # Retorna True o False.
        # Complejidad: O(1)

        return nombre_usuario in self.indice

    def total_usuarios(self):
        # Retorna la cantidad de usuarios únicos registrados.
        # Se usa al mostrar el resumen de carga del dataset.

        return len(self.indice)