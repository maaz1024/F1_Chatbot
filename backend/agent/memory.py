class Memory:
    history = []

    @classmethod
    def append(cls, msg):
        cls.history.append(msg)

    @classmethod
    def get(cls):
        return "\n".join(cls.history)
