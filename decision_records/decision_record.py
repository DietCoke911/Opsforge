import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import os

DATA_FILE = "opsforge_decisions.json"

@dataclass
class DecisionRecord:
    decision_id: str
    project: str
    context: str
    priority_score: int
    dependency_score: int
    severity_score: int
    actual_outcome: str = ""
    timestamp: str = ""

def save_decision(record: DecisionRecord):
    decisions = load_decisions()
    decisions.append(asdict(record))
    with open(DATA_FILE, "w") as f:
        json.dump(decisions, f, indent=2)

def load_decisions() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def create_test_closed_decision(status: str = "BLOCKED") -> DecisionRecord:
    record = DecisionRecord(
        decision_id=f"TEST-{datetime.now().strftime('%H%M%S')}",
        project="General Operations Project",
        context="High dependency test scenario",
        priority_score=75,
        dependency_score=68,
        severity_score=55,
        actual_outcome=status,
        timestamp=datetime.now().isoformat()
    )
    save_decision(record)
    return record

def learn_from_outcomes() -> Dict[str, Any]:
    decisions = load_decisions()
    if not decisions:
        return {"blocked_count": 0, "recommendation": "No data yet."}

    blocked = [d for d in decisions if d.get("actual_outcome") == "Still Blocked"]
    if not blocked:
        return {"blocked_count": 0, "recommendation": "No blocked outcomes."}

    avg_dep = sum(d.get("dependency_score", 0) for d in blocked) / len(blocked)

    # Tunable threshold
    DEPENDENCY_THRESHOLD = 65   # ← adjust this

    if avg_dep > DEPENDENCY_THRESHOLD:
        return {
            "blocked_count": len(blocked),
            "avg_dependency": round(avg_dep, 1),
            "recommendation": f"Increase w1 (dependency weight) — avg dependency {round(avg_dep,1)} > {DEPENDENCY_THRESHOLD}"
        }
    else:
        return {
            "blocked_count": len(blocked),
            "avg_dependency": round(avg_dep, 1),
            "recommendation": "No weight change recommended yet."
        }

