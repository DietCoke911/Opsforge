from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
import json
from pathlib import Path
from decision_records.coordinator import DecisionCoordinator

DECISIONS_FILE = Path("opsforge_decisions.json")

@dataclass
class DecisionRecord:
    decision_id: str
    project: str
    context: str
    priority_score: int
    dependency_score: int
    severity_score: int
    decision_type: str = "GENERAL"   # NEW: Enables routing
    actual_outcome: str = "Pending"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self):
        return asdict(self)

def save_decision(record: DecisionRecord):
    decisions = load_decisions()
    decisions.append(record.to_dict())
    with open(DECISIONS_FILE, "w") as f:
        json.dump(decisions, f, indent=2)

def load_decisions():
    if not DECISIONS_FILE.exists():
        return []
    with open(DECISIONS_FILE) as f:
        return json.load(f)

def create_test_closed_decision(decision_type="BLOCKED"):
    record = DecisionRecord(
        decision_id=f"TEST-{datetime.now().strftime('%H%M%S')}",
        project="General Operations Project",
        context="High dependency scenario",
        priority_score=75,
        dependency_score=68,
        severity_score=72,
        decision_type=decision_type,
        actual_outcome="Still Blocked"
    )
    save_decision(record)
    return record

def learn_from_outcomes():
    decisions = load_decisions()
    blocked = [d for d in decisions if d.get("actual_outcome") == "Still Blocked"]
    
    if not blocked:
        return {"message": "No blocked outcomes to learn from yet", "recommendation": "Run more test cycles"}

    avg_dep = sum(d.get("dependency_score", 0) for d in blocked) / len(blocked)
    DEPENDENCY_THRESHOLD = 55
    ADJUST_AMOUNT = 6

    if avg_dep > DEPENDENCY_THRESHOLD:
        rec = f"Increase w1 (Dependency) by {ADJUST_AMOUNT} points. Current avg_dep = {avg_dep:.1f}"
    else:
        rec = "Current weights appear stable"

    return {
        "blocked_count": len(blocked),
        "avg_dependency": round(avg_dep, 1),
        "recommendation": rec
    }

# Quick test with coordinator
if __name__ == "__main__":
    c = DecisionCoordinator()
    record = create_test_closed_decision("BLOCKED")
    print("Coordinator routing:")
    print(c.route_decision(record))
    print("\nLearning loop:")
    print(learn_from_outcomes())
