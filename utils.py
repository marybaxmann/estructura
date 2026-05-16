# utils.py
import re
import csv
import os

def cargar_stopwords(ruta_csv="stopwords.csv"):
    stopwords = set()
    if not os.path.exists(ruta_csv):
        print("[AVISO] No se encontró stopwords.csv")
        return stopwords
    with open(ruta_csv, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            stopwords.add(fila["palabra"].strip().lower())
    return stopwords

STOPWORDS = cargar_stopwords()

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