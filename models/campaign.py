class Campaign:
    def __init__(
        self,
        product,
        audience,
        goal,
        key_message,
        channels
    ):
        self.product = product
        self.audience = audience
        self.goal = goal
        self.key_message = key_message
        self.channels = channels