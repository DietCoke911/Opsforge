class Pattern6_Formulaic:
    def detect(self, text):
        # Simple placeholder for formulaic/rigid patterns
        if len(text.split()) > 50 and any(word in text.lower() for word in ["therefore", "additionally", "in conclusion"]):
            return {"name": "Formulaic Structure", "score_contribution": 18, "evidence": ["Repetitive procedural language"]}
        return None
