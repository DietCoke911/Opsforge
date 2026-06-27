class Pattern6_Formulaic:
    def detect(self, text):
        if any(word in text.lower() for word in ["therefore", "additionally", "in conclusion", "it is important"]):
            return {"name": "Formulaic Structure", "score_contribution": 18, "evidence": ["Repetitive procedural language"]}
        return None

class Pattern7_CompoundAmplification:
    def detect(self, text):
        if "high dependency" in text.lower() and "blocked" in text.lower():
            return {"name": "Compound Amplification", "score_contribution": 22, "evidence": ["Multiple degrading signals"]}
        return None

class Pattern8_RepeatRecurring:
    def detect(self, text):
        if "Still Blocked" in text:
            return {"name": "Repeat Recurring Issue", "score_contribution": 20, "evidence": ["Recurring blocked outcome"]}
        return None

class Pattern9_IgnoredSignals:
    def detect(self, text):
        if "ignored" in text.lower():
            return {"name": "Ignored Signals", "score_contribution": 15, "evidence": ["Unaddressed signals detected"]}
        return None

class PatternDetector:
    def __init__(self):
        self.patterns = [
            Pattern6_Formulaic(),
            Pattern7_CompoundAmplification(),
            Pattern8_RepeatRecurring(),
            Pattern9_IgnoredSignals(),
        ]

    def detect(self, text):
        results = []
        for pattern in self.patterns:
            result = pattern.detect(text)
            if result:
                results.append(result)
        average_score = sum(r.get("score_contribution", 0) for r in results) / len(results) if results else 0.0
        return {
            "results": results,
            "average_score": round(average_score, 1),
            "patterns_detected": len(results)
        }
