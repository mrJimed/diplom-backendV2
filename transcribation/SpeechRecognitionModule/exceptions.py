class NoSilenceFoundError(Exception):
    """Исключение выбрасывается, если в аудио длительное время нет участков тишины."""

    def __init__(self):
        msg = "Cannot split on silence."
        super().__init__(msg)
