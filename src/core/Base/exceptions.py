class BotBlocked(Exception):
    """
    Exception raised when a bot is blocked.
    """

    def __init__(self, message):
        self.message = message
