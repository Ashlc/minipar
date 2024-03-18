class Token:
    def __init__(self, token_type, value=None, position=None):
        self.type = token_type  # Type of the token (e.g., keyword, identifier, operator)
        self.value = value      # Value of the token (e.g., the actual keyword, identifier name, or operator symbol)
        self.position = position  # Position of the token in the source code (e.g., line number, column number)

    def __repr__(self):
        return f"Token({self.type}, {self.value})"