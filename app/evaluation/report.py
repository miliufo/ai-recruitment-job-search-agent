import json
from pathlib import Path
from datetime import datetime, timezone

from app.evaluation.job_match_evaluator import run_evaluation


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = PROJECT_ROOT / "data" / "evaluation" / "evaluation_report.json"


def generate_evaluation_report() -> dict:
    evaluation = run_evaluation()
    metrics = evaluation.get("metrics", {})

    report = {
        "evaluation_summary": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "cases_total": evaluation.get("cases_total", 0),
            "cases_successful": evaluation.get("cases_successful", 0),
            "cases_failed": evaluation.get("cases_failed", 0),
        },
        "metrics": {
            "mean_recall_at_3": metrics.get("mean_recall_at_3", 0),
            "hit_rate_at_1": metrics.get("hit_rate_at_1", 0),
            "mean_reciprocal_rank": metrics.get(
                "mean_reciprocal_rank", 0
            ),
            "recommendation_accuracy": metrics.get(
                "recommendation_accuracy", 0
            ),
        },
        "results": evaluation.get("results", []),
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

    return report


if __name__ == "__main__":
    report = generate_evaluation_report()

    print()
    print("=== AI RECRUITMENT EVALUATION REPORT ===")
    print(
        f"Cases: "
        f"{report['evaluation_summary']['cases_successful']}/"
        f"{report['evaluation_summary']['cases_total']} successful"
    )

    metrics = report["metrics"]

    print(f"Recall@3: {metrics['mean_recall_at_3']:.2%}")
    print(f"Hit Rate@1: {metrics['hit_rate_at_1']:.2%}")
    print(
        f"Mean Reciprocal Rank: "
        f"{metrics['mean_reciprocal_rank']:.2%}"
    )
    print(
        f"Recommendation Accuracy: "
        f"{metrics['recommendation_accuracy']:.2%}"
    )

    print()
    print(f"Report saved to: {REPORT_PATH}")