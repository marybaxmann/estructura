"""
Casos de prueba - Entrega II (Grafo y Algoritmo de Grados de Conexion).

Este script construye el grafo de contactos a partir del dataset real del
proyecto y ejecuta el algoritmo de grados de conexion (BFS) sobre AL MENOS
3 usuarios distintos, verificando automaticamente mediante aserciones que:

  1. El usuario raiz NUNCA aparece en sus propios niveles de contactos.
  2. No existen duplicados DENTRO de un mismo nivel.
  3. No existen duplicados ENTRE niveles (un mismo contacto no puede
     aparecer simultaneamente en 1°, 2° y/o 3° grado).
  4. Los contactos de cada grado se pueden listar de forma ordenada.

Ejecutar con:  python test_entrega2.py
"""

from main import (
    cargar_dataset,
    cargar_amigos,
    construir_grafo_contactos,
    grafo_contactos,
)


def verificar_grados_conexion(usuario_raiz, grado_maximo=3):
    print("=" * 60)
    print(f"CASO DE PRUEBA: usuario raiz = @{usuario_raiz}")
    print("=" * 60)

    niveles = grafo_contactos.grados_conexion(usuario_raiz, grado_maximo)

    assert niveles is not None, f"El usuario @{usuario_raiz} deberia existir en el grafo"

    conjuntos_por_grado = {}
    for grado in range(1, grado_maximo + 1):
        lista = niveles[grado]
        contactos = lista.obtener_todos()

        # 2) Sin duplicados dentro del mismo nivel
        assert len(contactos) == len(set(contactos)), \
            f"Hay duplicados dentro del nivel {grado}° grado"

        # 1) El usuario raiz no debe aparecer en sus propios niveles
        assert usuario_raiz not in contactos, \
            f"El usuario raiz @{usuario_raiz} no deberia aparecer en su propio nivel {grado}"

        conjuntos_por_grado[grado] = set(contactos)

        contactos_ordenados = sorted(contactos)
        print(f"\n  Contactos de {grado}° grado ({len(contactos_ordenados)}):")
        for nombre in contactos_ordenados:
            print(f"    - @{nombre}")

    # 3) Sin duplicados ENTRE niveles (interseccion vacia entre todos los pares)
    for g1 in range(1, grado_maximo + 1):
        for g2 in range(g1 + 1, grado_maximo + 1):
            interseccion = conjuntos_por_grado[g1] & conjuntos_por_grado[g2]
            assert not interseccion, (
                f"Se encontraron usuarios duplicados entre el nivel {g1}° y "
                f"{g2}° grado: {interseccion}"
            )

    print(f"\n[OK] Caso de prueba @{usuario_raiz} verificado correctamente "
          f"(sin duplicados, sin auto-referencias, niveles bien separados).\n")


if __name__ == "__main__":
    cargar_dataset("Tweets.csv")
    cargar_amigos("amigos.csv")
    construir_grafo_contactos()

    # --- Al menos 3 usuarios distintos, como exige el enunciado ---
    usuarios_de_prueba = ["cairdin", "jetbluenews", "kbosspotter"]

    for usuario in usuarios_de_prueba:
        verificar_grados_conexion(usuario, grado_maximo=3)

    # Caso adicional: usuario inexistente (debe manejarse sin error)
    print("=" * 60)
    print("CASO DE PRUEBA: usuario inexistente")
    print("=" * 60)
    resultado = grafo_contactos.grados_conexion("usuario_que_no_existe_123")
    assert resultado is None, "Un usuario inexistente debe retornar None"
    print("[OK] Usuario inexistente manejado correctamente (retorna None).\n")

    print("=" * 60)
    print("TODOS LOS CASOS DE PRUEBA PASARON CORRECTAMENTE")
    print("=" * 60)
