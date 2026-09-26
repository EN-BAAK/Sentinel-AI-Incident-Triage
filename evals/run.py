from app.services.triage import triage_incident
from evals.cases import EVAL_CASES


def run_evaluation() -> None:
    passed = 0

    for case in EVAL_CASES:
        report = triage_incident(case.incident)

        expected_found = all(
            expected in report.hypotheses
            for expected in case.expected_hypotheses
        )

        forbidden_absent = all(
            forbidden not in report.hypotheses
            for forbidden in case.forbidden_hypotheses
        )

        success = expected_found and forbidden_absent

        if success:
            passed += 1

        status = "PASS" if success else "FAIL"

        print(
            f"{status} | {case.name} | "
            f"expected={case.expected_hypotheses} | "
            f"forbidden={case.forbidden_hypotheses} | "
            f"actual={report.hypotheses}"
        )

    total = len(EVAL_CASES)
    score = passed / total

    print()
    print(f"Passed: {passed}/{total}")
    print(f"Success rate: {score:.2%}")


if __name__ == "__main__":
    run_evaluation()