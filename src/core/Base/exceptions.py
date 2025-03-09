class BotBlocked(Exception):
    """
    Exception raised when a bot is blocked.
    """

    def __init__(self, message):
        self.message = message


class MessageFormatterError(Exception):
    """
    The exception raised when errors occur in the MessageFormatter.
    """

    def __init__(self, message):
        self.message = message
