class SessionNotInitialisedError(Exception):
    def __init__(self):
        msg = """
        Session not initialised! Ensure that MiddlewareDB has been initialised before
        attempting database access.
        """

        super().__init__(msg)
