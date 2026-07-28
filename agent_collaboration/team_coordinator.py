class TeamCoordinator:
    def __init__(self):
        self.context = {}

    def handoff_task(self, sender: str, receiver: str, task_data: dict) -> dict:
        self.context[f"{sender}_to_{receiver}"] = task_data
        return {"status": "HANDOFF_SUCCESSFUL", "sender": sender, "receiver": receiver}
