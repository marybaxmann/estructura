# Proyecto Estructuras de Datos — Red Social (Tweets)
## Objetivo del proyecto

Implementar un sistema de búsqueda textual basado en índices invertidos utilizando listas enlazadas y memoria dinámica, simulando funcionalidades básicas de una red social.

## Dataset utilizado

Se utilizó el dataset “Twitter US Airline Sentiment”, compuesto por aproximadamente 14 mil tweets relacionados con aerolíneas estadounidenses.

Además, se generaron archivos adicionales (`amigos.csv` y `likes.csv`) para simular relaciones sociales y reacciones entre usuarios.

## Requisitos
- Python 3.8 o superior
- No requiere librerías externas

## Ejecución
```bash
python main.py
```
El programa busca automáticamente los archivos `Tweets.csv`, `amigos.csv` y `likes.csv`
en el mismo directorio.


## Estructura del proyecto
| Archivo | Descripción |
|---|---|
| `nodo.py` | Clase `Nodo`: unidad básica de la lista enlazada (dato + puntero siguiente) |
| `lista_enlazada.py` | Clase `ListaEnlazada`: lista simple con cabeza, insertar, existe, eliminar, vaciar |
| `post.py` | Clase `Post`: almacena id, texto, autor y lista de likes (ListaEnlazada) |
| `usuario.py` | Clase `Usuario`: almacena nombre y lista de contactos (ListaEnlazada) |
| `indice_invertido.py` | `IndiceInvertidoPosts`: vocabulario → ListaEnlazada de post_ids. `IndiceInvertidoUsuarios`: nombre → Usuario con ListaEnlazada de contactos |
| `utils.py` | `limpiar_texto`: normaliza, elimina URLs/@mentions, filtra stopwords. `cargar_stopwords`: lee stopwords.csv |
| `main.py` | Punto de entrada: carga dataset, amigos y likes; menú interactivo |

## Estructuras de datos implementadas
- **Lista enlazada simple** (`ListaEnlazada` + `Nodo`): inserción O(1) al inicio, sin recorrer la estructura,  búsqueda O(n), eliminación O(n).
- **Índice Invertido de Posts**: diccionario Python donde cada clave es un término y el valor es una `ListaEnlazada` de `post_id`.
- **Índice Invertido de Usuarios**: diccionario Python donde cada clave es un nombre de usuario y el valor es un objeto `Usuario` con una `ListaEnlazada` de contactos.

## Funciones principales
| Función | Archivo | Descripción |
|---|---|---|
| `cargar_dataset(ruta)` | main.py | Lee Tweets.csv, construye índices |
| `cargar_amigos(ruta)` | main.py | Carga relaciones usuario↔usuario desde amigos.csv |
| `cargar_likes(ruta)` | main.py | Asocia likes a posts desde likes.csv |
| `buscar_posts_por_termino()` | main.py | Búsqueda simple o intersección de términos en el índice |
| `buscar_contactos_usuario()` | main.py | Lista contactos de un usuario desde el índice de usuarios |
| `buscar_likes_de_post()` | main.py | Muestra likes y usuarios que los dieron para un post_id |
| `ListaEnlazada.insertar(dato)` | lista_enlazada.py | Inserta al inicio en O(1) |
| `ListaEnlazada.existe(dato)` | lista_enlazada.py | Recorrido lineal O(n) para evitar duplicados |
| `IndiceInvertidoPosts.buscar_multiples(palabras)` | indice_invertido.py | Intersección de listas de posteo para búsqueda AND |
| `limpiar_texto(texto)` | utils.py | Convierte texto a minúsculas, elimina ruido textual y filtra stopwords. |
