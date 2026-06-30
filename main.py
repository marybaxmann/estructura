import csv
import os

from post import Post
from usuario import Usuario
from indice_invertido import IndiceInvertidoPosts, IndiceInvertidoUsuarios
from utils import limpiar_texto, limpiar_consulta
from grafo import Grafo
from tabla_hash import TablaHash, calcular_tamanio_tabla

posts = []
indice_posts = IndiceInvertidoPosts()
indice_usuarios = IndiceInvertidoUsuarios()

# Entrega II: grafo de contactos (no dirigido), construido sobre el indice de usuarios
grafo_contactos = Grafo()

# Entrega III: tabla hash de frecuencia de terminos (se instancia tras conocer N)
tabla_frecuencia = None


# ---------------------------------------------------------------------
# Carga de datos (Entrega I, sin cambios en su logica)
# ---------------------------------------------------------------------
def cargar_dataset(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"[ERROR] No se encontró el archivo: {ruta_csv}")
        return False

    print(f"Cargando dataset desde '{ruta_csv}'...")

    with open(ruta_csv, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for i, fila in enumerate(lector):
            texto     = fila.get("text", "").strip()
            autor     = fila.get("name", f"user_{i}").strip().lower()

            if not texto:
                continue

            post = Post(post_id=i, texto=texto, autor=autor)
            posts.append(post)

            indice_usuarios.agregar_usuario(autor)

            palabras = limpiar_texto(texto)
            for palabra in palabras:
                indice_posts.agregar(palabra, i)

    print(f"Dataset cargado: {len(posts)} posts | "
          f"{indice_posts.total_terminos()} términos  | "
          f"{indice_usuarios.total_usuarios()} usuarios")
    return True


def cargar_amigos(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"[AVISO] No se encontró archivo de amigos: {ruta_csv}")
        return

    with open(ruta_csv, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            usuario = fila["usuario"].strip().lower()
            amigo = fila["amigo"].strip().lower()
            indice_usuarios.agregar_contacto(usuario, amigo)

    print("Amigos cargados correctamente.")


def cargar_likes(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"[AVISO] No se encontró archivo de likes: {ruta_csv}")
        return

    with open(ruta_csv, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            post_id = int(fila["post_id"].strip())
            usuario = fila["usuario"].strip().lower()
            if post_id < len(posts):
                posts[post_id].agregar_like(usuario)

    print("Likes cargados correctamente.")


# ---------------------------------------------------------------------
# Entrega II: construccion del grafo de contactos a partir del Indice
# Invertido de Usuarios (Entrega I)
# ---------------------------------------------------------------------
def construir_grafo_contactos():
    print("Construyendo grafo de contactos (no dirigido) desde el Indice "
          "Invertido de Usuarios...")
    grafo_contactos.construir_desde_indice(indice_usuarios, mostrar_reporte=True)
    print(f"Grafo construido: {grafo_contactos.total_usuarios()} vertices | "
          f"{grafo_contactos.total_aristas()} aristas.")


# ---------------------------------------------------------------------
# Entrega III: construccion de la tabla hash de frecuencia de terminos,
# a partir del vocabulario obtenido en el Indice Invertido de Posts.
# ---------------------------------------------------------------------
def construir_tabla_hash():
    global tabla_frecuencia

    n_vocabulario = indice_posts.total_terminos()
    tamanio_m = calcular_tamanio_tabla(n_vocabulario)
    tabla_frecuencia = TablaHash(tamanio_m)

    print(f"Construyendo tabla hash (N={n_vocabulario}, M={tamanio_m})...")

    # Se recorren nuevamente los posts para contar CADA aparicion (con
    # repeticiones) de cada termino en el dataset, ya que el indice
    # invertido de Entrega I solo registra apariciones unicas por post.
    for post in posts:
        palabras = limpiar_texto(post.texto)
        for palabra in palabras:
            tabla_frecuencia.insertar_o_incrementar(palabra)

    tabla_frecuencia.mostrar_estadisticas(n_vocabulario)


# ---------------------------------------------------------------------
# Entrega I: busquedas existentes
# ---------------------------------------------------------------------
def buscar_posts_por_termino():
    consulta = input("Ingresa término(s) a buscar (separados por espacio): ").strip()

    if not consulta:
        print("Consulta vacía.")
        return

    terminos = limpiar_consulta(consulta)

    if not terminos:
        print("La consulta solo contiene stop words.")
        return

    print(f"Buscando posts con: {terminos}")

    if len(terminos) == 1:
        lista = indice_posts.buscar(terminos[0])

        if lista is None:
            print(f"No se encontraron posts con '{terminos[0]}'.")
            return

        ids_encontrados = lista

    else:
        ids_encontrados = indice_posts.buscar_multiples(terminos)

        if ids_encontrados.esta_vacia():
            print("No se encontraron posts con todos esos términos.")
            return

    print("\nPosts encontrados. Mostrando máximo 10:\n")

    contador = 0
    actual = ids_encontrados.cabeza

    while actual is not None and contador < 10:
        post_id = actual.dato
        posts[post_id].mostrar()
        actual = actual.siguiente
        contador += 1

    print()


def buscar_contactos_usuario():
    nombre = input("Ingresa el nombre de usuario (sin @): ").strip().lower()
    if not nombre:
        return

    lista_contactos = indice_usuarios.buscar_contactos(nombre)

    if lista_contactos is None:
        print(f"El usuario '@{nombre}' no está registrado.")
        print("Algunos usuarios registrados:")
        contador = 0
        for usuario_clave in indice_usuarios.indice:
            if contador >= 5:
                break
            print(f"  - @{usuario_clave}")
            contador += 1
        print()
        return

    if lista_contactos.esta_vacia():
        print(f"@{nombre} no tiene contactos registrados.")
        return

    print(f"\nContactos de @{nombre}:")
    lista_contactos.mostrar()
    print()


def buscar_likes_de_post():
    entrada = input("Ingresa el ID del post: ").strip()
    if not entrada.isdigit():
        print("ID inválido.")
        return
    post_id = int(entrada)
    if post_id < 0 or post_id >= len(posts):
        print(f"No existe un post con ID {post_id}.")
        return
    post = posts[post_id]
    post.mostrar()
    post.mostrar_likes()
    print()


# ---------------------------------------------------------------------
# Entrega II: consulta de grados de conexion (BFS)
# ---------------------------------------------------------------------
def consultar_grados_conexion():
    nombre = input("Ingresa el nombre de usuario raiz (sin @): ").strip().lower()
    if not nombre:
        return

    if not grafo_contactos.existe_usuario(nombre):
        print(f"El usuario '@{nombre}' no existe en el grafo de contactos.")
        return

    grafo_contactos.mostrar_grados_conexion(nombre, grado_maximo=3)


# ---------------------------------------------------------------------
# Entrega III: consultas sobre la tabla hash
# ---------------------------------------------------------------------
def consultar_frecuencia_termino():
    termino = input("Ingresa el termino a consultar: ").strip().lower()
    if not termino:
        return

    frecuencia = tabla_frecuencia.buscar(termino)
    if frecuencia == 0:
        print(f"El termino '{termino}' no aparece en el dataset (o es stopword).")
    else:
        print(f"El termino '{termino}' aparece {frecuencia} veces en el dataset.")
    print()


def consultar_top_n():
    entrada = input("¿Cuántos términos quieres ver? (5, 10 o 20): ").strip()
    if not entrada.isdigit():
        print("Valor inválido.")
        return
    n = int(entrada)
    tabla_frecuencia.mostrar_top_n(n)


def mostrar_estadisticas_tabla_hash():
    tabla_frecuencia.mostrar_estadisticas(indice_posts.total_terminos())


# ---------------------------------------------------------------------
# Menu principal
# ---------------------------------------------------------------------
def mostrar_menu():
    print("=" * 60)
    print(" Sistema de Busqueda - Red Social (Tweets)")
    print(" Entregas I, II y III")
    print("=" * 60)
    print(" --- Entrega I: Indices Invertidos ---")
    print(" 1. Buscar posts por termino(s)")
    print(" 2. Buscar contactos directos de un usuario")
    print(" 3. Ver likes de un post")
    print(" --- Entrega II: Grafo y BFS por Grados de Conexion ---")
    print(" 4. Consultar grados de conexion (1°, 2° y 3°) de un usuario")
    print(" --- Entrega III: Tabla Hash de Frecuencia de Terminos ---")
    print(" 5. Consultar frecuencia de un termino")
    print(" 6. Consultar Top-N terminos mas frecuentes")
    print(" 7. Ver estadisticas de la tabla hash (N, M, alpha, colisiones)")
    print(" 8. Salir")
    print("=" * 60)


if __name__ == "__main__":

    if not cargar_dataset("Tweets.csv"):
        exit(1)

    cargar_amigos("amigos.csv")
    cargar_likes("likes.csv")

    # Construcciones requeridas por Entregas II y III, reutilizando lo
    # cargado en la Entrega I
    construir_grafo_contactos()
    construir_tabla_hash()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            buscar_posts_por_termino()
        elif opcion == "2":
            buscar_contactos_usuario()
        elif opcion == "3":
            buscar_likes_de_post()
        elif opcion == "4":
            consultar_grados_conexion()
        elif opcion == "5":
            consultar_frecuencia_termino()
        elif opcion == "6":
            consultar_top_n()
        elif opcion == "7":
            mostrar_estadisticas_tabla_hash()
        elif opcion == "8":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.\n")
