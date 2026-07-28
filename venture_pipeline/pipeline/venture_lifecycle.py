class VentureLifecycle:
    def __init__(self, name: str):
        self.name = name
        self.stage = "DISCOVERY"
    def advance(self):
        stages = ["DISCOVERY", "ANALYSIS", "VALIDATION", "INVESTMENT", "BUILD"]
        idx = stages.index(self.stage)
        if idx + 1 < len(stages):
            self.stage = stages[idx + 1]
        return self.stage
