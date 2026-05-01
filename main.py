# main.py
# ─────────────────────────────────────────────────────────────
# MAIN: Punto de entrada del sistema de gestión de red social.
#
# Este archivo coordina todo el sistema:
#   1. Carga el dataset de tweets (Tweets.csv)
#   2. Carga las relaciones de amistad (amigos.csv)
#   3. Construye ambos índices invertidos en memoria
#   4. Ofrece un menú interactivo de búsqueda
#
# Estructuras que se construyen al iniciar:
#   - posts[]              → lista Python de objetos Post
#   - indice_posts         → IndiceInvertidoPosts (término → posts)
#   - indice_usuarios      → IndiceInvertidoUsuarios (usuario → contactos)
# ─────────────────────────────────────────────────────────────

import csv
import os

from post import Post
from usuario import Usuario
from indice_invertido import IndiceInvertidoPosts, IndiceInvertidoUsuarios
from utils import limpiar_texto, limpiar_consulta

# ─────────────────────────────────────────────
# Estructuras globales en memoria
# ─────────────────────────────────────────────

posts = []
# Lista Python que almacena todos los objetos Post cargados desde el CSV.
# El índice de esta lista corresponde al post_id.
# Ejemplo: posts[42] → objeto Post del tweet número 42

indice_posts = IndiceInvertidoPosts()
# Índice invertido que mapea términos a posts.
# Ejemplo: "delayed" → ListaEnlazada([203, 45, 10])

indice_usuarios = IndiceInvertidoUsuarios()
# Índice invertido que mapea usuarios a sus contactos.
# Ejemplo: "cairdin" → ListaEnlazada(["yvonnalynn", "jnardino"])


# ══════════════════════════════════════════════════════════════
# FUNCIÓN: cargar_dataset
# ══════════════════════════════════════════════════════════════
def cargar_dataset(ruta_csv):
    # Lee el archivo CSV del dataset de Twitter Airline Sentiment
    # y construye ambos índices invertidos en memoria.
    #
    # Por cada fila del CSV:
    #   1. Extrae texto, autor y aerolínea
    #   2. Crea un objeto Post y lo agrega a posts[]
    #   3. Registra el autor en el índice de usuarios
    #   4. Registra la aerolínea como contacto del autor
    #   5. Limpia el texto y agrega cada palabra al índice de posts
    #
    # Retorna True si cargó correctamente, False si no encontró el archivo.

    if not os.path.exists(ruta_csv):
        # Verificar que el archivo exista antes de intentar abrirlo
        print(f"[ERROR] No se encontró el archivo: {ruta_csv}")
        return False

    print(f"Cargando dataset desde '{ruta_csv}'...")

    with open(ruta_csv, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        # DictReader lee cada fila como un diccionario
        # donde las claves son los nombres de las columnas del CSV

        for i, fila in enumerate(lector):
            # i = número de fila (será el post_id)
            # fila = diccionario con los datos del tweet

            texto = fila.get("text", "").strip()
            # Texto original del tweet
            # Ejemplo: "@VirginAmerica my flight was delayed!"

            autor = fila.get("name", f"user_{i}").strip()
            # Nombre de usuario del autor
            # Si no existe la columna "name", usa "user_i" como respaldo

            aerolinea = fila.get("airline", "").strip()
            # Aerolínea mencionada en el tweet
            # Ejemplo: "Virgin America", "United"

            if not texto:
                continue
                # Saltar filas sin texto

            # ── Crear y almacenar el Post ──
            post = Post(post_id=i, texto=texto, autor=autor)
            posts.append(post)
            # Ahora posts[i] contiene este tweet

            # ── Registrar autor en índice de usuarios ──
            indice_usuarios.agregar_usuario(autor)

            # ── Registrar aerolínea como contacto del autor ──
            # Simula la relación social: el usuario interactuó con la aerolínea
            if aerolinea:
                indice_usuarios.agregar_contacto(autor, aerolinea)
                indice_usuarios.agregar_usuario(aerolinea)

            # ── Indexar palabras del tweet en el índice de posts ──
            palabras = limpiar_texto(texto)
            # limpiar_texto elimina URLs, menciones, stop words, etc.
            # Ejemplo: ["flight", "delayed", "virginamerica"]

            for palabra in palabras:
                indice_posts.agregar(palabra, i)
                # Asocia cada palabra con el ID de este tweet

    print(f"Dataset cargado: {len(posts)} posts | {indice_posts.total_terminos()} términos únicos | {indice_usuarios.total_usuarios()} usuarios")
    return True


# ══════════════════════════════════════════════════════════════
# FUNCIÓN: cargar_amigos
# ══════════════════════════════════════════════════════════════
def cargar_amigos(ruta_csv):
    # Lee el archivo amigos.csv y registra las relaciones de amistad
    # en el índice invertido de usuarios.
    #
    # El archivo tiene dos columnas:
    #   - usuario: el usuario al que se le agrega el contacto
    #   - amigo:   el contacto que se agrega
    #
    # Ejemplo de fila: cairdin,jnardino
    # → agrega "jnardino" a la lista de contactos de "cairdin"
    #
    # Si el archivo no existe, muestra un aviso y continúa.

    if not os.path.exists(ruta_csv):
        print(f"[AVISO] No se encontró archivo de amigos: {ruta_csv}")
        return

    with open(ruta_csv, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            usuario = fila["usuario"].strip().lower()
            # Normalizar a minúsculas para consistencia con el índice

            amigo = fila["amigo"].strip().lower()
            # Normalizar a minúsculas para consistencia con el índice

            indice_usuarios.agregar_contacto(usuario, amigo)
            # Agrega el amigo a la lista enlazada del usuario

    print("Amigos cargados correctamente.")


# ══════════════════════════════════════════════════════════════
# FUNCIÓN: buscar_posts_por_termino
# ══════════════════════════════════════════════════════════════
def buscar_posts_por_termino():
    # Solicita al usuario uno o más términos de búsqueda
    # y muestra los posts que los contienen.
    #
    # Si se ingresa UN término:
    #   → busca directamente en el índice → O(1)
    #   → recorre la lista enlazada de ese término
    #
    # Si se ingresan MÚLTIPLES términos:
    #   → realiza intersección AND entre las listas
    #   → solo muestra posts que contengan TODOS los términos
    #
    # Muestra máximo 10 resultados.

    consulta = input("Ingresa término(s) a buscar (separados por espacio): ").strip()
    if not consulta:
        print("Consulta vacía.")
        return

    terminos = limpiar_consulta(consulta)
    # Aplica la misma limpieza que al indexar para garantizar
    # que la búsqueda sea consistente con el índice

    if not terminos:
        print("La consulta solo contiene stop words.")
        return

    print(f"Buscando posts con: {terminos}")

    if len(terminos) == 1:
        # Búsqueda simple: un solo término
        lista = indice_posts.buscar(terminos[0])
        if lista is None:
            print(f"No se encontraron posts con '{terminos[0]}'.")
            return
        ids_encontrados = lista.obtener_todos()
    else:
        # Búsqueda múltiple: intersección AND de varios términos
        ids_encontrados = indice_posts.buscar_multiples(terminos)
        if not ids_encontrados:
            print("No se encontraron posts con todos esos términos.")
            return

    print(f"\n{len(ids_encontrados)} post(s) encontrado(s). Mostrando máximo 10:\n")
    for contador, post_id in enumerate(ids_encontrados):
        if contador >= 10:
            break
            # Limitar a 10 resultados para no saturar la terminal
        posts[post_id].mostrar()
        # Recupera el post por su ID y lo muestra
    print()


# ══════════════════════════════════════════════════════════════
# FUNCIÓN: buscar_contactos_usuario
# ══════════════════════════════════════════════════════════════
def buscar_contactos_usuario():
    # Solicita un nombre de usuario y muestra su lista de contactos
    # almacenada en el índice invertido de usuarios.
    #
    # Accede directamente al diccionario del índice → O(1)
    # Luego recorre la lista enlazada de contactos → O(k)
    # donde k = cantidad de contactos del usuario

    nombre = input("Ingresa el nombre de usuario (sin @): ").strip().lower()
    if not nombre:
        return

    lista_contactos = indice_usuarios.buscar_contactos(nombre)
    # Busca la lista enlazada de contactos de ese usuario

    if lista_contactos is None:
        print(f"El usuario '@{nombre}' no está registrado.")
        return

    if lista_contactos.esta_vacia():
        print(f"@{nombre} no tiene contactos registrados.")
        return

    print(f"\nContactos de @{nombre}:")
    lista_contactos.mostrar()
    # Recorre e imprime cada nodo de la lista enlazada
    print()


# ══════════════════════════════════════════════════════════════
# FUNCIÓN: mostrar_menu
# ══════════════════════════════════════════════════════════════
def mostrar_menu():
    # Imprime el menú principal del sistema en la terminal.

    print("=" * 50)
    print("  Sistema de Busqueda - Red Social (Tweets)")
    print("=" * 50)
    print("  1. Buscar posts por termino(s)")
    print("  2. Buscar contactos de un usuario")
    print("  3. Salir")
    print("=" * 50)


# ══════════════════════════════════════════════════════════════
# PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Punto de entrada del programa.
    # Solo se ejecuta cuando se corre directamente con: python main.py

    if not cargar_dataset("Tweets.csv"):
        exit(1)
        # Si no se pudo cargar el dataset, terminar el programa

    cargar_amigos("amigos.csv")
    # Cargar relaciones de amistad desde archivo externo

    while True:
        # Bucle principal del menú — se repite hasta que el usuario elija salir
        mostrar_menu()
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            buscar_posts_por_termino()
        elif opcion == "2":
            buscar_contactos_usuario()
        elif opcion == "3":
            print("Programa finalizado.")
            break
            # Salir del bucle y terminar el programa
        else:
            print("Opción inválida.\n")