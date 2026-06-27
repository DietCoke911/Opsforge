class Pattern7_CompoundAmplification:
    def detect(self, text):
        # Placeholder for combined risk signals
        if "high dependency" in text.lower() and "blocked" in text.lower():
            return {"name": "Compound Amplification", "score_contribution": 22, "evidence": ["Multiple degrading signals"]}
        return None
