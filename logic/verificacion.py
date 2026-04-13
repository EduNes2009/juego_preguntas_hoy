# logic/verificacion.py
import unicodedata
from rapidfuzz import fuzz

def normalizar(texto):
    texto = texto.lower().strip()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto

def es_respuesta_correcta(respuesta_correcta, respuesta_usuario, umbral=80):
    correcta_norm = normalizar(respuesta_correcta)
    usuario_norm = normalizar(respuesta_usuario)
    score = fuzz.ratio(correcta_norm, usuario_norm)
    
    es_correcta = score >= umbral
    return es_correcta, score