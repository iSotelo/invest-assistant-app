from export_utils import build_csv_report

FAKE_RESULT = {
    "score": 85,
    "degraded": False,
    "invest_results": {
        "independent": {"score": 5, "justificacion": "ok", "sugerencia": "ninguna"},
        "historia_mejorada": "Como PO quiero X para Y (mejorada)",
    },
}


def test_build_csv_report_includes_score_and_invest_criteria():
    csv_content = build_csv_report("Como PO quiero X para Y", FAKE_RESULT)

    assert "Como PO quiero X para Y" in csv_content
    assert "85" in csv_content
    assert "independent" in csv_content
    assert "Como PO quiero X para Y (mejorada)" in csv_content


def test_build_csv_report_handles_missing_invest_results():
    result_without_invest = {"score": 40, "degraded": True, "invest_results": None}

    csv_content = build_csv_report("Historia incompleta", result_without_invest)

    assert "Historia incompleta" in csv_content
    assert "40" in csv_content
