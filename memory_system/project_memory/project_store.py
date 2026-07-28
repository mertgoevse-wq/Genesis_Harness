class ProjectStore:
    def __init__(self):
        self.timeline = []

    def record_milestone(self, phase: str, details: dict):
        self.timeline.append({"phase": phase, "details": details})
        return len(self.timeline)
