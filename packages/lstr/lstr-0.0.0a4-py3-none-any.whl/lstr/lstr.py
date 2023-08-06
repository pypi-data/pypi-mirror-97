from copy import deepcopy
from logging import getLogger
from re import search
from typing import Any, List

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
        self.logger = getLogger("lstr")
        self.logger.debug('Created lstr("%s")', value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, lstr):
            return self.value == other.value and self.locks == other.locks
        if isinstance(other, str):
            return self.value == other
        other_type = type(other).__name__
        raise NotImplementedError(f"Cannot compare lstr with {other_type}.")

    def __len__(self) -> int:
        return len(self.value)

    def __repr__(self) -> str:
        count = len(self)
        column_width = len(str(count)) + 1

        r = ""
        for index in range(len(self)):
            r += str(index).rjust(column_width)

        r += "\n"
        for char in self.value:
            r += char.rjust(column_width)

        r += "\n"
        for index in range(len(self)):
            writeable = self.can_write(index=index, length=1)
            r += (" " if writeable else "^").rjust(column_width)

        return r

    def __str__(self) -> str:
        return self.value

    def can_sub(self, pattern: str, replacement: str) -> bool:
        """
        Determines whether or not all matches of a regular expression can be
        substituted for a replacement.

        Arguments:
            pattern:     Regular expression.
            replacement: String or expression expansion to replace with.

        Returns:
            `True` if all matches of the pattern can be substituted.
        """
        worker = deepcopy(self)
        return worker.sub(pattern=pattern, replacement=replacement, allow_partial=True)

    def can_write(self, index: int, length: int) -> bool:
        """
        Determines whether or not a range can be overwritten.

        Arguments:
            index:  Start index.
            length: Length.

        Returns:
            `True` if the range can be overwritten.
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

    def sub(self, pattern: str, replacement: str, allow_partial: bool = False) -> bool:
        """
        Substitutes matches of a regular expression with a new value.

        Arguments:
            pattern:       Regular expression.

            replacement:   String or expression expansion to replace with.

            allow_partial: If `True` then any matches within locked ranges will
                           be skipped. If `False` then the string will be
                           updated only if all instances can be updated.

        Returns:
            `True` if all substitutions were successful.
        """

        if not allow_partial:
            if not self.can_sub(pattern=pattern, replacement=replacement):
                return False

        changed = False

        while True:
            match = search(pattern, self.value)
            if not match:
                self.logger.debug("No more matches: changed=%s", changed)
                return changed

            write_ok = self.write(
                match.expand(replacement),
                index=match.start(),
                length=match.end() - match.start(),
            )

            if not write_ok:
                return False
            changed = True

    def write(self, value: str, index: int, length: int) -> bool:
        """
        Attempts to overwrite a given range with a new value.

        Arguments:
            value:  String.
            index:  Start index.
            length: Length.

        Returns:
            `True` if the overwrite was permitted, otherwise `False`.
        """
        if not self.can_write(index=index, length=length):
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
