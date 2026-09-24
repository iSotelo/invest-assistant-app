from app.services.linguistic_rules import analyze_story_structure


def test_valid_story_structure_is_detected():
    story = "Como usuario registrado quiero restablecer mi contraseña para recuperar el acceso a mi cuenta."

    result = analyze_story_structure(story)

    assert result["estructura_correcta"] is True
    assert result["partes_detectadas"]["rol"] == "usuario registrado"
    assert "restablecer mi contraseña" in result["partes_detectadas"]["accion"]
    assert "recuperar el acceso a mi cuenta" in result["partes_detectadas"]["beneficio"]
    assert result["errores_sintacticos"] == []


def test_incomplete_story_reports_syntax_errors():
    story = "Quiero un botón para exportar el reporte."

    result = analyze_story_structure(story)

    assert result["estructura_correcta"] is False
    assert result["partes_detectadas"]["rol"] is None
    assert len(result["errores_sintacticos"]) >= 1


def test_ambiguous_words_are_detected():
    story = "Como PO quiero una interfaz rápida y amigable para mejorar la experiencia."

    result = analyze_story_structure(story)

    assert "rápido" in result["ambiguedades_detectadas"]
    assert "amigable" in result["ambiguedades_detectadas"]


def test_story_without_ambiguous_words_returns_empty_list():
    story = "Como PO quiero registrar una historia de usuario para iniciar su análisis."

    result = analyze_story_structure(story)

    assert result["ambiguedades_detectadas"] == []
