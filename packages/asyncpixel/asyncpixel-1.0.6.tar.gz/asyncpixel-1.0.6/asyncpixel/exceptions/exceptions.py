"""Custom Exceptions for asyncpixel."""
import datetime


class RateLimitError(Exception):
    """Exception raised when Hypixel ratelimit is reached."""

    def __init__(self, retry_after: datetime.datetime) -> None:
        """Create error."""
        self.message = (
            "The hypixel API ratelimit was reached, "
            + f"try again at {retry_after.strftime('%H:%M:%S')}."
        )
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return error in readable format.

        Returns:
            str: string version of error.
        """
        return self.message


class ApiNoSuccess(Exception):
    """Exception raised when api has an error."""

    def __init__(
        self,
        source: str,
    ) -> None:
        """Create error."""
        self.message = f"The {source} endpoint encounted an error on the hypixel side."
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return error in readable format.

        Returns:
            str: string version of error.
        """
        return self.message


class InvalidApiKey(Exception):
    """Exception raised when the API key is invalid."""

    def __init__(self) -> None:
        """Create error."""
        self.message = "Entered API key is not valid"
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return error in readable format.

        Returns:
            str: string version of error.
        """
        return self.message
