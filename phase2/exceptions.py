class PreferenceValidationError(Exception):
    """Raised when user preferences fail validation."""
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors))
