import time

class EventBus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def publish(self, event_type: str, data: dict):
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "data": data
        }
        for sub in self.subscribers:
            try:
                sub(event)
            except Exception:
                pass
        return event
