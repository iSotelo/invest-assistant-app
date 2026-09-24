import re
from functools import lru_cache

import spacy

SPACY_MODEL_NAME = "es_core_news_sm"

AMBIGUOUS_WORDS = {
    "rápido",
    "fácil",
    "amigable",
    "óptimo",
    "eficiente",
    "intuitivo",
    "robusto",
    "flexible",
    "escalable",
    "sencillo",
}

STORY_PATTERN = re.compile(
    r"como\s+(?P<rol>.+?)\s+quiero\s+(?P<accion>.+?)\s+para\s+(?P<beneficio>.+)",
    re.IGNORECASE | re.DOTALL,
)


@lru_cache(maxsize=1)
def _load_nlp():
    return spacy.load(SPACY_MODEL_NAME)


def _extract_parts(story_text: str) -> dict[str, str | None]:
    match = STORY_PATTERN.search(story_text)
    if not match:
        return {"rol": None, "accion": None, "beneficio": None}
    return {
        "rol": match.group("rol").strip(" .,"),
        "accion": match.group("accion").strip(" .,"),
        "beneficio": match.group("beneficio").strip(" .,"),
    }


def _detect_ambiguities(story_text: str) -> list[str]:
    nlp = _load_nlp()
    doc = nlp(story_text.lower())
    found = {token.lemma_ for token in doc if token.lemma_ in AMBIGUOUS_WORDS}
    return sorted(found)


def _detect_syntax_errors(parts: dict[str, str | None]) -> list[str]:
    errors = []
    if not parts["rol"]:
        errors.append("No se identificó la cláusula de Rol ('Como...').")
    if not parts["accion"]:
        errors.append("No se identificó la cláusula de Acción ('quiero...').")
    if not parts["beneficio"]:
        errors.append("No se identificó la cláusula de Beneficio ('para...').")
    return errors


def analyze_story_structure(story_text: str) -> dict:
    """Valida la estructura sintáctica Como/Quiero/Para y detecta ambigüedades léxicas."""
    parts = _extract_parts(story_text)
    errores_sintacticos = _detect_syntax_errors(parts)

    return {
        "estructura_correcta": len(errores_sintacticos) == 0,
        "partes_detectadas": parts,
        "ambiguedades_detectadas": _detect_ambiguities(story_text),
        "errores_sintacticos": errores_sintacticos,
    }
