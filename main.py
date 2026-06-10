import csv
import os

from post import Post
from usuario import Usuario
from indice_invertido import IndiceInvertidoPosts, IndiceInvertidoUsuarios
from utils import limpiar_texto, limpiar_consulta

posts = []
indice_posts = IndiceInvertidoPosts()
indice_usuarios = IndiceInvertidoUsuarios()

#cargar dataset
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

#buscar post
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


def mostrar_menu():
    print("=" * 50)
    print(" Sistema de Busqueda - Red Social (Tweets)")
    print("=" * 50)
    print(" 1. Buscar posts por termino(s)")
    print(" 2. Buscar contactos de un usuario")
    print(" 3. Ver likes de un post")
    print(" 4. Salir")
    print("=" * 50)


if __name__ == "__main__":

    if not cargar_dataset("Tweets.csv"):
        exit(1)

    cargar_amigos("amigos.csv")
    cargar_likes("likes.csv")

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
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.\n")
