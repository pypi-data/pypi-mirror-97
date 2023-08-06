from typing import List

from lstr.lock import Lock


class lstr:
    """
    A partially lockable string.

    Arguments:
        value: String value.
        locks: Ranges to lock. Further locks can be added via `lock()`.
    """

    def __init__(self, value: str, locks: List[Lock] = []) -> None:
        self.value = value
        self.locks = locks

    def __str__(self) -> str:
        return self.value

    def can_replace(self, index: int, length: int) -> bool:
        """
        Calculates whether or not the given range of this string can be
        replaced.

        Arguments:
            index:  Start index.
            length: Length.

        Returns:
            `True` if the range can be replaced, otherwise `False`.
        """
        if index < 0 or length < 0 or index + length > len(self.value):
            return False
        for lock in self.locks:
            if lock.intersects(index=index, length=length):
                return False
        return True

    def lock(self, index: int, length: int) -> None:
        """
        Locks a range of the string.

        Arguments:
            index:  Start index.
            length: Length.
        """
        self.locks.append(Lock(index=index, length=length))

    def replace(self, value: str, index: int, length: int) -> bool:
        """
        Attempts to replace a given range with a new value.

        Arguments:
            value:  Replacement string.
            index:  Start index.
            length: Length.

        Returns:
            `True` if the replacement was permitted, otherwise `False`.
        """
        if not self.can_replace(index=index, length=length):
            return False
        self.value = self.value[0:index] + value + self.value[index + length :]
        if distance := len(value) - length:
            self.shift_locks(index=index, distance=distance)
        return True

    def shift_locks(self, index: int, distance: int) -> None:
        """
        Shifts all the locks affected by a change at a given index by a given
        distance.

        Arguments:
            index:    Affected index.
            distance: Distance. Negative distances shift to the left.
        """
        for lock in [lock for lock in self.locks if lock.index >= index]:
            lock.index += distance
