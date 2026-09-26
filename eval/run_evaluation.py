"""Script de evaluacion experimental del MVP (Capitulo 6).

Compara el sistema hibrido (spaCy + LLM) contra un baseline solo-reglas,
usando el dataset anotado en dataset.py, y calcula matriz de confusion,
Precision, Recall y F1-score por criterio INVEST, mas promedios macro/micro.

Uso:
    python eval/run_evaluation.py                  # sistema hibrido (llama a OpenAI)
    python eval/run_evaluation.py --baseline-only   # solo baseline, sin llamadas a OpenAI
    python eval/run_evaluation.py --concurrency 10  # controlar llamadas simultaneas al LLM (default 5)

Requiere OPENAI_API_KEY configurada en .env para el modo hibrido.
"""

import argparse
import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from dotenv import load_dotenv
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

from app.services.llm_engine import INVEST_CRITERIA
from dataset import DATASET
from predictors import baseline_prediction, hybrid_prediction

load_dotenv()


def _collect_baseline_predictions() -> tuple[dict[str, list[int]], dict[str, list[int]]]:
    y_true: dict[str, list[int]] = {c: [] for c in INVEST_CRITERIA}
    y_pred: dict[str, list[int]] = {c: [] for c in INVEST_CRITERIA}

    for item in DATASET:
        prediction = baseline_prediction(item["story_text"])
        for criterion in INVEST_CRITERIA:
            y_true[criterion].append(item["ground_truth"][criterion])
            y_pred[criterion].append(prediction[criterion])

    return y_true, y_pred


async def _collect_hybrid_predictions(concurrency: int = 5) -> tuple[dict[str, list[int]], dict[str, list[int]]]:
    """Ejecuta las llamadas al LLM en paralelo (hasta `concurrency` simultaneas)
    dentro de un unico event loop. El paralelismo reduce el tiempo TOTAL del
    batch (no la latencia de una peticion individual); un semaforo evita
    disparar las 30 llamadas de golpe y saturar el rate limit de OpenAI."""
    semaphore = asyncio.Semaphore(concurrency)
    completed = 0
    lock = asyncio.Lock()

    async def _predict_one(item: dict) -> tuple[str, dict[str, int]]:
        nonlocal completed
        async with semaphore:
            prediction = await hybrid_prediction(item["story_text"], item["project_context"])
        async with lock:
            completed += 1
            print(f"  [{completed}/{len(DATASET)}] Completado {item['id']}", flush=True)
        return item["id"], prediction

    results = await asyncio.gather(*(_predict_one(item) for item in DATASET))
    predictions_by_id = dict(results)

    y_true: dict[str, list[int]] = {c: [] for c in INVEST_CRITERIA}
    y_pred: dict[str, list[int]] = {c: [] for c in INVEST_CRITERIA}

    for item in DATASET:
        prediction = predictions_by_id[item["id"]]
        for criterion in INVEST_CRITERIA:
            y_true[criterion].append(item["ground_truth"][criterion])
            y_pred[criterion].append(prediction[criterion])

    return y_true, y_pred


def _print_criterion_report(criterion: str, y_true: list[int], y_pred: list[int]) -> dict[str, float]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"\n  {criterion.upper()}")
    print(f"    Matriz de confusión -> VP: {tp}  FP: {fp}  VN: {tn}  FN: {fn}")
    print(f"    Precision: {precision:.3f}  Recall: {recall:.3f}  F1: {f1:.3f}")

    return {"precision": precision, "recall": recall, "f1": f1}


def _print_summary(label: str, y_true: dict[str, list[int]], y_pred: dict[str, list[int]]) -> dict[str, float]:
    print(f"\n{'=' * 60}\nRESULTADOS: {label}\n{'=' * 60}")

    per_criterion_scores = []
    all_true: list[int] = []
    all_pred: list[int] = []

    for criterion in INVEST_CRITERIA:
        scores = _print_criterion_report(criterion, y_true[criterion], y_pred[criterion])
        per_criterion_scores.append(scores)
        all_true.extend(y_true[criterion])
        all_pred.extend(y_pred[criterion])

    macro_f1 = sum(s["f1"] for s in per_criterion_scores) / len(per_criterion_scores)
    macro_precision = sum(s["precision"] for s in per_criterion_scores) / len(per_criterion_scores)
    macro_recall = sum(s["recall"] for s in per_criterion_scores) / len(per_criterion_scores)

    micro_precision = precision_score(all_true, all_pred, zero_division=0)
    micro_recall = recall_score(all_true, all_pred, zero_division=0)
    micro_f1 = f1_score(all_true, all_pred, zero_division=0)

    print(f"\n  PROMEDIO MACRO -> Precision: {macro_precision:.3f}  Recall: {macro_recall:.3f}  F1: {macro_f1:.3f}")
    print(f"  PROMEDIO MICRO -> Precision: {micro_precision:.3f}  Recall: {micro_recall:.3f}  F1: {micro_f1:.3f}")

    return {"macro_f1": macro_f1, "macro_precision": macro_precision, "macro_recall": macro_recall}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline-only",
        action="store_true",
        help="Solo evalúa el baseline solo-reglas, sin llamar al LLM (más rápido, sin costo de API).",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Número máximo de llamadas simultáneas al LLM en el modo híbrido (default: 5).",
    )
    args = parser.parse_args()

    print(f"Dataset: {len(DATASET)} historias de usuario.")
    print("NOTA: el ground_truth de dataset.py es ilustrativo, no proviene de expertos reales todavía.")

    start = time.time()
    baseline_true, baseline_pred = _collect_baseline_predictions()
    baseline_summary = _print_summary("BASELINE (solo reglas spaCy)", baseline_true, baseline_pred)
    print(f"\n  Tiempo total baseline: {time.time() - start:.1f}s")

    if not args.baseline_only:
        start = time.time()
        hybrid_true, hybrid_pred = asyncio.run(_collect_hybrid_predictions(concurrency=args.concurrency))
        hybrid_summary = _print_summary("SISTEMA HÍBRIDO (spaCy + LLM)", hybrid_true, hybrid_pred)
        elapsed = time.time() - start
        print(f"\n  Tiempo total híbrido: {elapsed:.1f}s ({elapsed / len(DATASET):.1f}s por historia)")

        print(f"\n{'=' * 60}\nCOMPARACIÓN FINAL\n{'=' * 60}")
        print(f"  F1 macro baseline: {baseline_summary['macro_f1']:.3f}")
        print(f"  F1 macro híbrido:  {hybrid_summary['macro_f1']:.3f}")
        delta = hybrid_summary["macro_f1"] - baseline_summary["macro_f1"]
        print(f"  Mejora del híbrido sobre el baseline: {delta:+.3f}")


if __name__ == "__main__":
    main()
