import csv
import io


def build_csv_report(story_text: str, result: dict) -> str:
    """Construye el contenido CSV del reporte de validación para exportar (HU-05)."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["historia_original", "score", "degraded"])
    writer.writerow([story_text, result["score"], result.get("degraded", False)])
    writer.writerow([])

    invest_results = result.get("invest_results") or {}
    if invest_results:
        writer.writerow(["criterio", "score", "justificacion", "sugerencia"])
        for criterio, valores in invest_results.items():
            if criterio == "historia_mejorada":
                continue
            writer.writerow([criterio, valores["score"], valores["justificacion"], valores["sugerencia"]])
        writer.writerow([])
        writer.writerow(["historia_mejorada", invest_results.get("historia_mejorada", "")])

    return buffer.getvalue()
