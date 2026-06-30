"""
Casos de prueba - Entrega III (Tabla Hash de Frecuencia de Terminos).

Construye la tabla hash sobre el dataset real del proyecto y verifica
mediante aserciones que:

  1. M es primo y cumple M >= 1.5 * N (dimensionamiento correcto).
  2. La funcion hash djb2 esta correctamente implementada (se contrasta
     contra un calculo de referencia independiente, hecho a mano en este
     mismo script, replicando unicamente la formula del enunciado).
  3. Las frecuencias contadas por la tabla coinciden con un conteo de
     referencia independiente (hecho con un diccionario nativo SOLO para
     fines de verificacion en este script de pruebas; la implementacion
     real de la tabla, en tabla_hash.py, no usa dict en ningun momento).
  4. La consulta Top-N es consistente para N = 5, 10 y 20 (cada resultado
     mas chico es un prefijo del resultado mas grande, y esta ordenado de
     mayor a menor frecuencia).
  5. Las metricas de colisiones (total, largo maximo, largo promedio) son
     coherentes con el contenido real de la tabla.

Ejecutar con:  python test_entrega3.py
"""

from main import cargar_dataset, posts
from utils import limpiar_texto
from tabla_hash import TablaHash, calcular_tamanio_tabla, es_primo


def hash_djb2_referencia(cadena, m):
    """Implementacion de referencia de djb2, escrita de forma independiente
    a TablaHash._hash_djb2, para verificar que ambas coinciden."""
    hash_val = 5381
    for caracter in cadena:
        hash_val = (hash_val * 33 + ord(caracter)) & 0xFFFFFFFF
    return hash_val % m


def verificar_dimensionamiento(n_vocabulario, m):
    print("=" * 60)
    print("CASO DE PRUEBA: Dimensionamiento de la tabla (N, M, alpha)")
    print("=" * 60)

    assert es_primo(m), f"M={m} deberia ser primo"
    assert m >= 1.5 * n_vocabulario, (
        f"M={m} no cumple M >= 1.5*N (1.5*N={1.5*n_vocabulario})"
    )

    alpha = n_vocabulario / m
    assert alpha <= 0.67, f"El factor de carga alpha={alpha:.4f} supera 0.67"

    print(f"  N = {n_vocabulario}")
    print(f"  M = {m}  (primo: OK, M >= 1.5*N: OK)")
    print(f"  alpha = {alpha:.4f}  (<= 0.67: OK)")
    print("[OK] Dimensionamiento correcto.\n")


def verificar_hash_djb2(tabla):
    print("=" * 60)
    print("CASO DE PRUEBA: Funcion hash djb2 vs. implementacion de referencia")
    print("=" * 60)

    terminos_prueba = ["flight", "cancelled", "service", "thanks", "delay", "a", "zz"]
    for termino in terminos_prueba:
        esperado = hash_djb2_referencia(termino, tabla.M)
        obtenido = tabla._hash_djb2(termino)
        assert esperado == obtenido, (
            f"djb2('{termino}') = {obtenido}, se esperaba {esperado}"
        )
        print(f"  hash_djb2('{termino}') = {obtenido}  (coincide con referencia)")

    print("[OK] Funcion hash djb2 verificada correctamente.\n")


def verificar_frecuencias(tabla):
    print("=" * 60)
    print("CASO DE PRUEBA: Frecuencias contadas vs. conteo de referencia")
    print("=" * 60)

    # Conteo de referencia INDEPENDIENTE, solo para esta verificacion
    # (no forma parte de la implementacion real de la tabla hash).
    conteo_referencia = {}
    for post in posts:
        for palabra in limpiar_texto(post.texto):
            conteo_referencia[palabra] = conteo_referencia.get(palabra, 0) + 1

    assert tabla.n_terminos_distintos == len(conteo_referencia), (
        f"La tabla tiene {tabla.n_terminos_distintos} terminos distintos, "
        f"se esperaban {len(conteo_referencia)}"
    )

    terminos_a_verificar = sorted(conteo_referencia, key=conteo_referencia.get, reverse=True)[:15]
    for termino in terminos_a_verificar:
        esperado = conteo_referencia[termino]
        obtenido = tabla.buscar(termino)
        assert obtenido == esperado, (
            f"buscar('{termino}') = {obtenido}, se esperaba {esperado}"
        )
        print(f"  '{termino}': {obtenido} (coincide con conteo de referencia)")

    assert tabla.buscar("palabra_inexistente_xyz") == 0, \
        "Un termino inexistente deberia retornar frecuencia 0"

    print(f"[OK] {len(terminos_a_verificar)} frecuencias verificadas, "
          f"todas coinciden con el conteo de referencia.\n")


def verificar_top_n(tabla):
    print("=" * 60)
    print("CASO DE PRUEBA: Consulta Top-N (N = 5, 10, 20)")
    print("=" * 60)

    top_5 = tabla.top_n(5)
    top_10 = tabla.top_n(10)
    top_20 = tabla.top_n(20)

    assert len(top_5) == 5
    assert len(top_10) == 10
    assert len(top_20) == 20

    # Cada top mas chico debe ser un prefijo exacto del top mas grande
    assert top_10[:5] == top_5, "Top-5 deberia ser un prefijo de Top-10"
    assert top_20[:10] == top_10, "Top-10 deberia ser un prefijo de Top-20"

    # Cada lista debe estar ordenada de mayor a menor frecuencia
    for resultado, n in ((top_5, 5), (top_10, 10), (top_20, 20)):
        frecuencias = [contador for _, contador in resultado]
        assert frecuencias == sorted(frecuencias, reverse=True), \
            f"Top-{n} no esta ordenado de mayor a menor"

    print("  Top-5 :", top_5)
    print("  Top-10:", top_10)
    print("  Top-20:", top_20)
    print("[OK] Top-N consistente y ordenado correctamente para N=5,10,20.\n")


def verificar_metricas_colisiones(tabla):
    print("=" * 60)
    print("CASO DE PRUEBA: Metricas de colisiones")
    print("=" * 60)

    colisiones, largo_max, largo_prom = tabla.estadisticas_colisiones()

    # Verificacion independiente recorriendo la tabla directamente
    largo_max_esperado = max(lista.tamanio for lista in tabla.tabla)
    celdas_ocupadas = [lista.tamanio for lista in tabla.tabla if lista.tamanio > 0]
    largo_prom_esperado = sum(celdas_ocupadas) / len(celdas_ocupadas)

    assert largo_max == largo_max_esperado, \
        f"Largo maximo {largo_max} != esperado {largo_max_esperado}"
    assert abs(largo_prom - largo_prom_esperado) < 1e-9, \
        f"Largo promedio {largo_prom} != esperado {largo_prom_esperado}"
    assert colisiones >= 0
    assert colisiones <= tabla.n_terminos_distintos, \
        "El numero de colisiones no puede superar el numero de terminos insertados"

    print(f"  Total colisiones      : {colisiones}")
    print(f"  Largo maximo de cadena: {largo_max}")
    print(f"  Largo promedio cadena : {largo_prom:.4f}")
    print("[OK] Metricas de colisiones verificadas correctamente.\n")


if __name__ == "__main__":
    cargar_dataset("Tweets.csv")

    from indice_invertido import IndiceInvertidoPosts
    indice_posts_local = IndiceInvertidoPosts()
    for post in posts:
        for palabra in limpiar_texto(post.texto):
            indice_posts_local.agregar(palabra, post.post_id)

    n_vocabulario = indice_posts_local.total_terminos()
    m = calcular_tamanio_tabla(n_vocabulario)

    verificar_dimensionamiento(n_vocabulario, m)

    tabla = TablaHash(m)
    for post in posts:
        for palabra in limpiar_texto(post.texto):
            tabla.insertar_o_incrementar(palabra)

    verificar_hash_djb2(tabla)
    verificar_frecuencias(tabla)
    verificar_top_n(tabla)
    verificar_metricas_colisiones(tabla)

    print("=" * 60)
    print("TODOS LOS CASOS DE PRUEBA DE LA ENTREGA III PASARON CORRECTAMENTE")
    print("=" * 60)
