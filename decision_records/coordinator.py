from DecisionRecords.decision_record import DecisionRecord
from typing import Dict, Any
from datetime import datetime, timezone
import json
from pathlib import Path

class DecisionCoordinator:
    """
    Central routing and governance coordinator for OpsForge.
    Routes decisions by type and enforces governance touchpoints.
    """
    
    def __init__(self):
        self.audit_log = Path("logs/coordinator_audit.json")
        self.audit_log.parent.mkdir(exist_ok=True)

    def route_decision(self, record: DecisionRecord) -> Dict[str, Any]:
        """Main entry point: classify, route, govern, and audit."""
        decision_type = getattr(record, 'decision_type', 'GENERAL').upper()
        
        # Governance touchpoint 1: Log incoming decision
        self._log_audit(record, "RECEIVED", f"Type: {decision_type}")
        
        # Route based on type
        if decision_type == "ESCALATION":
            result = self._handle_escalation(record)
        elif decision_type == "BLOCKED":
            result = self._handle_blocked(record)
        elif decision_type == "PATTERN":
            result = self._handle_pattern(record)
        else:
            result = self._handle_general(record)
        
        # Governance touchpoint 2: Final audit
        self._log_audit(record, "ROUTED", f"Path: {result['path']}, Status: {result['status']}")
        
        return result

    def _handle_escalation(self, record: DecisionRecord):
        return {
            "path": "Escalation Handler",
            "action": "Immediate human review + notification",
            "priority": "HIGH",
            "status": "Routed to Human",
            "requires_approval": True
        }

    def _handle_blocked(self, record: DecisionRecord):
        return {
            "path": "Blocked Issue Handler",
            "action": "Trigger learning loop + dependency analysis",
            "priority": "MEDIUM",
            "status": "Routed to Learning Loop",
            "requires_approval": False
        }

    def _handle_pattern(self, record: DecisionRecord):
        return {
            "path": "Pattern Recognition",
            "action": "Run full pattern detector",
            "priority": "MEDIUM",
            "status": "Routed to Pattern Detector",
            "requires_approval": False
        }

    def _handle_general(self, record: DecisionRecord):
        return {
            "path": "Standard Processing",
            "action": "Normal governance flow",
            "priority": "LOW",
            "status": "Routed to General Handler",
            "requires_approval": False
        }

    def _log_audit(self, record: DecisionRecord, event: str, details: str):
        """Simple persistent audit log"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision_id": record.decision_id,
            "event": event,
            "details": details
        }
        try:
            if self.audit_log.exists():
                with open(self.audit_log) as f:
                    logs = json.load(f)
            else:
                logs = []
            logs.append(entry)
            with open(self.audit_log, "w") as f:
                json.dump(logs, f, indent=2)
        except:
            pass  # Fail silently for now

# Quick test
if __name__ == "__main__":
    from DecisionRecords.decision_record import create_test_closed_decision
    c = DecisionCoordinator()
    record = create_test_closed_decision()
    print(c.route_decision(record))
