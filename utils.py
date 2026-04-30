# utils.py
import re

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
    texto = texto.lower()
    texto = re.sub(r'http\S+|www\S+', '', texto)
    texto = re.sub(r'@\w+', '', texto)
    texto = re.sub(r'#', '', texto)
    texto = re.sub(r'[^a-z ]', ' ', texto)
    palabras = texto.split()
    return [p for p in palabras if p not in STOPWORDS and len(p) > 2]

def limpiar_consulta(consulta):
    return limpiar_texto(consulta)