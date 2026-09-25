from predictors import baseline_prediction


def test_baseline_marks_all_criteria_as_compliant_for_valid_story():
    story = "Como usuario registrado quiero restablecer mi contraseña para recuperar el acceso a mi cuenta."

    prediction = baseline_prediction(story)

    assert all(value == 1 for value in prediction.values())
    assert set(prediction.keys()) == {
        "independent",
        "negotiable",
        "valuable",
        "estimable",
        "small",
        "testable",
    }


def test_baseline_marks_all_criteria_as_non_compliant_when_ambiguous():
    story = "Como usuario quiero una interfaz rápida y amigable para tener una experiencia óptima."

    prediction = baseline_prediction(story)

    assert all(value == 0 for value in prediction.values())


def test_baseline_marks_all_criteria_as_non_compliant_when_structure_is_invalid():
    story = "Quiero un botón para exportar el reporte."

    prediction = baseline_prediction(story)

    assert all(value == 0 for value in prediction.values())
