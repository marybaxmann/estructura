# Proyecto Estructuras de Datos — Red Social (Tweets)

## Objetivo del proyecto

Implementar un sistema de gestión de red social que integra tres entregas:

- **Entrega I:** Índices Invertidos (de Posts y de Usuarios) implementados sobre listas enlazadas propias.
- **Entrega II:** Grafo no dirigido de contactos, construido sobre el Índice Invertido de Usuarios, con un algoritmo BFS (Breadth-First Search) que obtiene los contactos de 1°, 2° y 3° grado de un usuario raíz.
- **Entrega III:** Tabla Hash propia (función djb2, resolución de colisiones por encadenamiento separado) para contabilizar la frecuencia de aparición de cada término del vocabulario y consultar los términos más frecuentes (Top-N).

## Dataset utilizado

Se utilizó el dataset "Twitter US Airline Sentiment", compuesto por aproximadamente 14.640 tweets relacionados con aerolíneas estadounidenses.

Además, se generaron archivos adicionales (`amigos.csv` y `likes.csv`) para simular relaciones sociales y reacciones entre usuarios.

## Requisitos

- Python 3.8 o superior
- No requiere librerías externas (solo `csv`, `os`, `re` y `collections.deque` de la biblioteca estándar, usado únicamente como cola de apoyo para el algoritmo BFS, conforme lo permite el enunciado de la Entrega II)

## Ejecución

```bash
python main.py
```

El programa busca automáticamente los archivos `Tweets.csv`, `amigos.csv` y `likes.csv` en el mismo directorio. Al iniciar, construye en orden:

1. El índice invertido de posts y de usuarios (Entrega I).
2. El grafo de contactos no dirigido (Entrega II).
3. La tabla hash de frecuencia de términos (Entrega III), reportando en consola N, M, el factor de carga α y las métricas de colisiones.

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `nodo.py` | Clase `Nodo`: unidad básica de la lista enlazada (dato + puntero siguiente) |
| `lista_enlazada.py` | Clase `ListaEnlazada`: lista simple con cabeza, insertar, existe, eliminar, vaciar |
| `post.py` | Clase `Post`: almacena id, texto, autor y lista de likes (ListaEnlazada) |
| `usuario.py` | Clase `Usuario`: almacena nombre y lista de contactos (ListaEnlazada) |
| `indice_invertido.py` | `IndiceInvertidoPosts`: vocabulario → ListaEnlazada de post_ids. `IndiceInvertidoUsuarios`: nombre → Usuario con ListaEnlazada de contactos |
| `utils.py` | `limpiar_texto`: normaliza, elimina URLs/@mentions, filtra stopwords. `cargar_stopwords`: lee stopwords.csv |
| `grafo.py` | **(Entrega II)** Clase `Grafo`: lista de adyacencia no dirigida construida desde el Índice Invertido de Usuarios. Algoritmo `grados_conexion` (BFS) |
| `tabla_hash.py` | **(Entrega III)** Clase `TablaHash`: hash djb2 + encadenamiento separado. Clase `ParTermino` (termino, contador) |
| `main.py` | Punto de entrada: carga dataset, amigos y likes; construye grafo y tabla hash; menú interactivo |
| `test_entrega2.py` | Casos de prueba automatizados de Entrega II (BFS sobre 3 usuarios, valida ausencia de duplicados y auto-referencias) |
| `test_entrega3.py` | Casos de prueba automatizados de Entrega III (dimensionamiento, djb2, frecuencias, Top-N, métricas de colisión) |

## Estructuras de datos implementadas

- **Lista enlazada simple** (`ListaEnlazada` + `Nodo`): inserción O(1) al inicio, búsqueda O(n), eliminación O(n). Reutilizada en TODAS las estructuras del proyecto (índices, grafo y tabla hash).
- **Índice Invertido de Posts**: diccionario Python donde cada clave es un término y el valor es una `ListaEnlazada` de `post_id`.
- **Índice Invertido de Usuarios**: diccionario Python donde cada clave es un nombre de usuario y el valor es un objeto `Usuario` con una `ListaEnlazada` de contactos.
- **Grafo no dirigido** (`Grafo`): diccionario `usuario -> ListaEnlazada` de vecinos (lista de adyacencia). Cada arista se agrega en ambos sentidos y se valida que no existan duplicados ni bucles.
- **Tabla Hash propia** (`TablaHash`): arreglo de tamaño `M`, donde cada celda es una `ListaEnlazada` de objetos `ParTermino`. Las colisiones se resuelven por encadenamiento separado.

## Entrega II — Grafo de Contactos y Algoritmo BFS

### Modelo del grafo

El grafo `G = (V, E)` se construye **directamente a partir del `IndiceInvertidoUsuarios`** de la Entrega I:

- `V`: cada usuario registrado en el índice de usuarios.
- `E`: cada relación de amistad `(usuario, contacto)` del índice se traduce en una arista no dirigida (se agrega en ambos sentidos), validando que no se dupliquen aristas y que no existan bucles (un usuario no puede ser su propio contacto).

Es un **grafo no dirigido** porque la relación de "amistad" en redes sociales (a diferencia de "seguir") se modela como simétrica: si A es amigo de B, B es amigo de A.

### Algoritmo de Grados de Conexión (BFS)

`Grafo.grados_conexion(usuario_raiz, grado_maximo=3)`:

- Recorre el grafo mediante **BFS (Breadth-First Search)**, expandiendo nivel por nivel desde el usuario raíz.
- Usa un `set` de visitados y una `collections.deque` como cola, estructuras de apoyo explícitamente permitidas por el enunciado para implementar BFS (no se usan para representar el grafo ni la red de amigos, que siguen siendo `ListaEnlazada` propia).
- Cada usuario se visita **una sola vez**, por lo que no hay duplicados entre los niveles de 1°, 2° y 3° grado.
- Retorna un diccionario `{1: ListaEnlazada, 2: ListaEnlazada, 3: ListaEnlazada}` con los contactos de cada grado.
- **Complejidad:** O(V + E), ya que cada vértice se encola una vez y cada arista se revisa a lo sumo dos veces (una desde cada extremo), comportamiento estándar de BFS sobre lista de adyacencia.

## Entrega III — Tabla Hash de Frecuencia de Términos

### Función hash

Se utiliza obligatoriamente **djb2** (Daniel J. Bernstein):

```
hash(0) = 5381
hash(i) = hash(i-1) * 33 + c[i]
índice final = hash(termino) mod M
```

Dado que Python utiliza enteros de precisión arbitraria, se trunca el valor a 32 bits en cada iteración (`hash_val &= 0xFFFFFFFF`) para reproducir el comportamiento de overflow natural de C/C++ (`unsigned long`) y Java (`long`).

### Dimensionamiento de la tabla (N, M, α)

- **N** = cantidad de términos únicos del vocabulario, obtenida desde `IndiceInvertidoPosts.total_terminos()` (Entrega I).
- **M** = menor número primo que cumple `M ≥ 1.5 × N` (factor de carga α ≤ 0.67), calculado dinámicamente con `calcular_tamanio_tabla()` en `tabla_hash.py` (usa `math.ceil` sobre `1.5 × N` antes de buscar el primo, para no incumplir la cota por redondeo hacia abajo).
- Con el dataset de tweets usado: **N ≈ 10.817**, lo que da **M = 16.229** (primo, M ≥ 1.5×N) y un factor de carga α ≈ 0.6665.

> Estos valores se recalculan automáticamente si cambia el dataset o el filtrado de stopwords; el programa los reporta en consola al iniciar (ver `TablaHash.mostrar_estadisticas`).

### Resolución de colisiones

Encadenamiento separado: cada celda del arreglo `self.tabla[i]` es una `ListaEnlazada` propia. Al insertar un término:

1. Se calcula su índice con djb2.
2. Se recorre la lista de esa celda buscando si el término ya existe (en cuyo caso solo se incrementa su contador).
3. Si no existe y la celda ya tenía al menos un elemento, se contabiliza como **colisión** y el nuevo término se agrega al inicio de la lista de esa celda.

### Construcción de la tabla

A diferencia del Índice Invertido de Posts (que solo registra apariciones **únicas** por post), la tabla hash de frecuencia cuenta **cada aparición** de cada término en el dataset completo (incluyendo repeticiones dentro de un mismo post), ya que el objetivo es medir frecuencia real de uso del término, no solo en cuántos posts aparece.

### Métricas reportadas

Al finalizar la construcción, el programa reporta (`TablaHash.mostrar_estadisticas`):

- N (vocabulario) y M (tamaño de tabla).
- Factor de carga α = N / M.
- Número total de colisiones.
- Largo máximo de cadena (peor caso de encadenamiento).
- Largo promedio de cadena (sobre celdas ocupadas).

### Consulta Top-N

`TablaHash.top_n(n)` recorre todas las celdas de la tabla, recopila los pares `(término, contador)` y los ordena de mayor a menor frecuencia, devolviendo los primeros `n`. Se probó parametrizado para N = 5, 10 y 20 desde el menú interactivo.

## Funciones principales

| Función | Archivo | Descripción |
|---|---|---|
| `cargar_dataset(ruta)` | main.py | Lee Tweets.csv, construye índices invertidos (Entrega I) |
| `cargar_amigos(ruta)` | main.py | Carga relaciones usuario↔usuario desde amigos.csv |
| `cargar_likes(ruta)` | main.py | Asocia likes a posts desde likes.csv |
| `construir_grafo_contactos()` | main.py | Construye el grafo no dirigido a partir del índice de usuarios (Entrega II) |
| `construir_tabla_hash()` | main.py | Calcula N y M, construye la tabla hash y cuenta frecuencias (Entrega III) |
| `buscar_posts_por_termino()` | main.py | Búsqueda simple o intersección de términos en el índice |
| `buscar_contactos_usuario()` | main.py | Lista contactos **directos** (1° grado) de un usuario desde el índice de usuarios |
| `buscar_likes_de_post()` | main.py | Muestra likes y usuarios que los dieron para un post_id |
| `consultar_grados_conexion()` | main.py | Pide un usuario raíz y muestra sus contactos de 1°, 2° y 3° grado (BFS) |
| `consultar_frecuencia_termino()` | main.py | Consulta cuántas veces aparece un término en el dataset |
| `consultar_top_n()` | main.py | Muestra los N términos más frecuentes (N parametrizable: 5, 10, 20, etc.) |
| `Grafo.construir_desde_indice(indice_usuarios)` | grafo.py | Construye la lista de adyacencia no dirigida desde el Índice Invertido de Usuarios |
| `Grafo.grados_conexion(raiz, grado_maximo)` | grafo.py | BFS por niveles; retorna contactos de 1°, 2° y 3° grado sin duplicados |
| `TablaHash._hash_djb2(cadena)` | tabla_hash.py | Implementación de la función hash djb2 truncada a 32 bits |
| `TablaHash.insertar_o_incrementar(termino)` | tabla_hash.py | Inserta un término nuevo o incrementa su contador; resuelve colisiones por encadenamiento |
| `TablaHash.top_n(n)` | tabla_hash.py | Retorna los N términos más frecuentes ordenados de mayor a menor |
| `TablaHash.estadisticas_colisiones()` | tabla_hash.py | Retorna total de colisiones, largo máximo y largo promedio de cadena |
| `ListaEnlazada.insertar(dato)` | lista_enlazada.py | Inserta al inicio en O(1) |
| `ListaEnlazada.existe(dato)` | lista_enlazada.py | Recorrido lineal O(n) para evitar duplicados |
| `IndiceInvertidoPosts.buscar_multiples(palabras)` | indice_invertido.py | Intersección de listas de posteo para búsqueda AND |
| `limpiar_texto(texto)` | utils.py | Convierte texto a minúsculas, elimina ruido textual y filtra stopwords |

## Gestión de memoria dinámica

Todas las estructuras (índices, grafo y tabla hash) se construyen sobre la `ListaEnlazada` propia de la Entrega I, evitando el uso de estructuras hash o de grafos provistas por el lenguaje (`dict`/`HashMap` solo se usan como contenedor externo de alto nivel para ubicar la `ListaEnlazada` correspondiente a cada clave —usuario o término—, nunca para resolver colisiones ni almacenar las relaciones en sí). La eliminación de nodos (`ListaEnlazada.eliminar`/`vaciar`) libera explícitamente las referencias de los nodos removidos.
