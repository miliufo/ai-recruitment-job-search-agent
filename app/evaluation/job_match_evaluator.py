import json
from pathlib import Path
from statistics import mean
from typing import Any, Optional

from app.models.candidate import Candidate
from app.graph.recruitment_graph import recruitment_graph


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVALUATION_DATASET = (
    PROJECT_ROOT / "data" / "evaluation" / "job_match_cases.json"
)


def load_evaluation_cases() -> list[dict[str, Any]]:
    with open(EVALUATION_DATASET, "r", encoding="utf-8") as file:
        return json.load(file)


def recall_at_k(
    predicted_job_ids: list[str],
    relevant_job_ids: list[str],
    k: int,
) -> float:
    if not relevant_job_ids:
        return 0.0

    predicted = set(predicted_job_ids[:k])
    relevant = set(relevant_job_ids)

    return len(predicted & relevant) / len(relevant)


def hit_at_k(
    predicted_job_ids: list[str],
    expected_top_jobs: list[str],
    k: int,
) -> float:
    predicted = set(predicted_job_ids[:k])
    expected = set(expected_top_jobs)

    return 1.0 if predicted & expected else 0.0


def reciprocal_rank(
    predicted_job_ids: list[str],
    expected_top_jobs: list[str],
) -> float:
    expected = set(expected_top_jobs)

    for rank, job_id in enumerate(predicted_job_ids, start=1):
        if job_id in expected:
            return 1.0 / rank

    return 0.0


def recommendation_accuracy(
    ranked_matches: list[dict[str, Any]],
    expected_recommendations: dict[str, list[str]],
) -> Optional[float]:
    if not expected_recommendations:
        return None

    predictions = {}

    for item in ranked_matches:
        job = item["job"]
        match = item["match"]

        predictions[job.job_id] = match.recommendation

    correct = 0
    evaluated = 0

    for job_id, accepted_values in expected_recommendations.items():
        if job_id not in predictions:
            continue

        evaluated += 1

        if predictions[job_id] in accepted_values:
            correct += 1

    if evaluated == 0:
        return 0.0

    return correct / evaluated


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    candidate = Candidate(**case["candidate"])

    initial_state = {
        "candidate": candidate
    }

    result = recruitment_graph.invoke(initial_state)

    ranked_matches = result.get("ranked_matches", [])

    predicted_job_ids = [
        item["job"].job_id
        for item in ranked_matches
    ]

    recall_3 = recall_at_k(
        predicted_job_ids,
        case["expected_relevant_jobs"],
        3,
    )

    hit_1 = hit_at_k(
        predicted_job_ids,
        case["expected_top_jobs"],
        1,
    )

    mrr = reciprocal_rank(
        predicted_job_ids,
        case["expected_top_jobs"],
    )

    recommendation_acc = recommendation_accuracy(
        ranked_matches,
        case.get("expected_recommendations", {}),
    )

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "candidate_id": candidate.candidate_id,
        "predicted_job_ids": predicted_job_ids,
        "recall_at_3": round(recall_3, 4),
        "hit_at_1": round(hit_1, 4),
        "reciprocal_rank": round(mrr, 4),
        "recommendation_accuracy": (
            round(recommendation_acc, 4)
            if recommendation_acc is not None
            else None
        ),
        "jobs_retrieved": result.get("jobs_retrieved", 0),
        "jobs_evaluated": result.get("jobs_evaluated", 0),
        "failed_matches": len(result.get("failed_matches", [])),
    }


def run_evaluation() -> dict[str, Any]:
    cases = load_evaluation_cases()

    results = []

    for case in cases:
        print(
            f"Evaluating {case['case_id']} - {case['name']}..."
        )

        try:
            result = evaluate_case(case)
            results.append(result)

        except Exception as exc:
            results.append(
                {
                    "case_id": case["case_id"],
                    "name": case["name"],
                    "error": str(exc),
                }
            )

    successful_results = [
        result
        for result in results
        if "error" not in result
    ]

    if not successful_results:
        return {
            "cases_total": len(cases),
            "cases_successful": 0,
            "cases_failed": len(cases),
            "metrics": {},
            "results": results,
        }

    recommendation_scores = [
        result["recommendation_accuracy"]
        for result in successful_results
        if result["recommendation_accuracy"] is not None
    ]

    metrics = {
        "mean_recall_at_3": round(
            mean(
                result["recall_at_3"]
                for result in successful_results
            ),
            4,
        ),
        "hit_rate_at_1": round(
            mean(
                result["hit_at_1"]
                for result in successful_results
            ),
            4,
        ),
        "mean_reciprocal_rank": round(
            mean(
                result["reciprocal_rank"]
                for result in successful_results
            ),
            4,
        ),
        "recommendation_accuracy": (
            round(mean(recommendation_scores), 4)
            if recommendation_scores
            else None
        ),
    }

    return {
        "cases_total": len(cases),
        "cases_successful": len(successful_results),
        "cases_failed": len(cases) - len(successful_results),
        "metrics": metrics,
        "results": results,
    }


if __name__ == "__main__":
    evaluation = run_evaluation()

    print()
    print("=" * 60)
    print("AI RECRUITMENT AGENT — EVALUATION RESULTS")
    print("=" * 60)

    print(
        json.dumps(
            evaluation,
            indent=2,
            default=str,
        )
    )