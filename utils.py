# utils.py
# ─────────────────────────────────────────────────────────────
# UTILS: Funciones auxiliares de procesamiento de texto.
#
# Se encarga de:
#   1. Limpiar el texto de los tweets antes de indexarlos
#   2. Filtrar stop words (palabras sin valor semántico)
#   3. Normalizar las consultas del usuario para que sean
#      consistentes con cómo se indexaron los términos
#
# La rúbrica exige filtrar stop words tanto al construir
# el índice como al procesar las consultas del usuario.
# ─────────────────────────────────────────────────────────────

import re

# Lista de stop words en inglés.
# Son palabras muy frecuentes que no aportan valor a la búsqueda:
# artículos, preposiciones, conjunciones, pronombres, etc.
# También incluye términos propios de Twitter: "rt", "amp", "http".
# Al filtrarlas se reduce el tamaño del índice y mejora la precisión.
STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "to", "for", "of", "with", "by",
    "from", "up", "about", "into", "and", "but", "or", "nor", "so", "yet",
    "i", "me", "my", "we", "our", "you", "your", "he", "him", "his",
    "she", "her", "it", "its", "they", "them", "their", "this", "these",
    "those", "who", "which", "what", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "shall", "should", "may", "might", "must", "can", "could",
    "not", "no", "just", "now", "then", "here", "there", "when", "where",
    "how", "all", "more", "some", "only", "very", "as", "also", "get",
    "got", "im", "dont", "cant", "wont", "rt", "amp", "via", "http",
    "https", "co"
}

def limpiar_texto(texto):
    # Limpia y normaliza un texto para indexación o búsqueda.
    #
    # Pasos en orden:
    #   1. Convertir a minúsculas → "Flight" se vuelve "flight"
    #   2. Eliminar URLs → "https://t.co/abc" desaparece
    #   3. Eliminar menciones (@usuario) → "@VirginAmerica" desaparece
    #   4. Eliminar símbolo # → "#delay" se vuelve "delay"
    #   5. Eliminar caracteres no alfabéticos → números, emojis, puntuación
    #   6. Filtrar stop words y palabras muy cortas (menos de 3 letras)
    #
    # Retorna una lista de palabras limpias listas para indexar.
    # Ejemplo:
    #   entrada:  "@VirginAmerica my flight was delayed! #fail"
    #   salida:   ["virginamerica", "flight", "delayed", "fail"]

    texto = texto.lower()
    # Paso 1: minúsculas para uniformidad

    texto = re.sub(r'http\S+|www\S+', '', texto)
    # Paso 2: eliminar URLs completas

    texto = re.sub(r'@\w+', '', texto)
    # Paso 3: eliminar menciones (@usuario)

    texto = re.sub(r'#', '', texto)
    # Paso 4: eliminar símbolo # pero conservar la palabra

    texto = re.sub(r'[^a-z ]', ' ', texto)
    # Paso 5: eliminar todo lo que no sea letra o espacio

    palabras = texto.split()
    return [p for p in palabras if p not in STOPWORDS and len(p) > 2]
    # Paso 6: filtrar stop words y palabras muy cortas


def limpiar_consulta(consulta):
    # Aplica la misma limpieza que limpiar_texto() a las consultas
    # ingresadas por el usuario en el menú.
    #
    # Esto es fundamental para la consistencia:
    # si el índice guardó "delayed" (sin @, sin #, en minúscula),
    # la consulta también debe llegar como "delayed" para encontrar resultados.
    #
    # Ejemplo:
    #   usuario escribe: "Delayed Flight"
    #   después de limpiar: ["delayed", "flight"]
    #   el índice busca exactamente esas palabras → encuentra resultados

    return limpiar_texto(consulta)