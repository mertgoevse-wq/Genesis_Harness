class MessageBus:
    def __init__(self):
        self.messages = []

    def publish_message(self, sender: str, receiver: str, payload: dict):
        msg = {"sender": sender, "receiver": receiver, "payload": payload}
        self.messages.append(msg)
        return msg
