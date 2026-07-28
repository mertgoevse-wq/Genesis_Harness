class RuntimeEvents:
    def emit(self, event_name: str, payload: dict):
        return {"event": event_name, "payload": payload}
