from typing import Any


class Lock:
    """
    A locked range of an `lstr`.

    Arguments:
        index:  Start index.
        length: Length.
    """

    def __init__(self, index: int, length: int) -> None:
        self.index = index
        self.length = length

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Lock):
            other_type = type(other).__name__
            raise NotImplementedError(f"Cannot compare Lock with {other_type}.")
        return self.index == other.index and self.length == other.length

    def __repr__(self) -> str:
        return f"Lock: index={self.index}, length={self.length}"

    def is_earlier(self, index: int) -> bool:
        """
        Calculates whether or not the index occurs before the range.

        Arguments:
            index: Index to check.

        Returns:
            `True` if the index occurs before the range, otherwise `False`.
        """
        return index < self.index

    def is_later(self, index: int) -> bool:
        """
        Calculates whether or not the index occurs after the range.

        Arguments:
            index: Index to check.

        Returns:
            `True` if the index occurs after the range, otherwise `False`.
        """
        return index >= self.index + self.length

    def intersects(self, index: int, length: int) -> bool:
        """
        Calculates whether or not the specified range intersects with this
        range.

        Arguments:
            index:  Start index.
            length: Length.

        Returns:
            `True` if the range instersects, otherwise `False`.
        """
        return not (self.is_earlier(index + length - 1) or self.is_later(index))
