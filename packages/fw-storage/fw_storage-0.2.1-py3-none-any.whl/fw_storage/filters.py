"""Storage filter module."""
# pylint: disable=too-few-public-methods
import abc
import datetime
import operator
import re
import typing as t

from fw_utils import parse_hrsize

from .fileinfo import FileInfo

__all__ = ["Filter", "ExpressionFilter"]

Filters = t.Optional[t.List[str]]


class BaseFilter(abc.ABC):
    """Base filter class defining the filter interface."""

    @abc.abstractmethod
    def match(self, value: FileInfo) -> bool:
        """Return True if the filter matches the file info."""


class Filter(BaseFilter):
    """Storage filter supporting multiple include- and exclude filters."""

    def __init__(
        self,
        include: Filters = None,
        exclude: Filters = None,
        factory: t.Optional[t.Dict[str, t.Type["ExpressionFilter"]]] = None,
    ) -> None:
        """Initialize include- and exclude storage filters from expressions.

        Custom filter {key: class} mapping may be provided with factory.
        """
        self.include = [parse_expression(expr, factory) for expr in (include or [])]
        self.exclude = [parse_expression(expr, factory) for expr in (exclude or [])]

    # pylint: disable=arguments-differ
    def match(self, value: t.Any, types: Filters = None) -> bool:
        """Return whether value matches all includes but none of the excludes.

        If types is not None, apply only filters of the given types.
        """
        include = self.include
        exclude = self.exclude
        if types:
            include = [filt for filt in include if filt.key in types]
            exclude = [filt for filt in exclude if filt.key in types]
        include_match = (i.match(value) for i in include)
        exclude_match = (e.match(value) for e in exclude)
        return all(include_match) and not any(exclude_match)

    def __repr__(self) -> str:
        """Return string representation of the storage filter."""
        cls_name = self.__class__.__name__
        include = ",".join(f"'{filt}'" for filt in self.include)
        exclude = ",".join(f"'{filt}'" for filt in self.exclude)
        return f"{cls_name}(include=[{include}], exclude=[{exclude}])"


class ExpressionFilter(BaseFilter):
    """Expression filter tied to a key, operator and value."""

    def __init__(self, key: str, op: str, value: str) -> None:
        """Initialize an expression filter."""
        if not re.match(fr"^{self.operator_re}$", op):
            raise ValueError(f"Invalid op: {op} (expected {self.operator_re})")
        self.key = key
        self.op = op
        self.value = value

    def __repr__(self) -> str:
        """Return the filter's string representation."""
        cls_name = self.__class__.__name__
        cls_args = self.key, self.op, self.value
        return f"{cls_name}{cls_args!r}"

    def __str__(self) -> str:
        """Return human-readable stringification (the original expression)."""
        return f"{self.key}{self.op}{self.value}"

    @property
    def operator_re(self) -> str:
        """Return regex of allowed operators."""
        return "|".join(OPERATORS)


def parse_expression(
    expression: str,
    factory: t.Optional[t.Dict[str, t.Type[ExpressionFilter]]] = None,
) -> ExpressionFilter:
    """Parse and return filter from expression string (factory)."""
    types = TYPES.copy()
    types.update(factory or {})
    filter_re = fr"^({'|'.join(sorted(types))})({'|'.join(OPERATORS)})(.*)$"
    match = re.match(filter_re, expression)
    if not match:
        raise ValueError(f"Invalid filter: {expression} (expected {filter_re})")
    key, op, value = match.groups()
    return types[key](key, op, value)  # type: ignore


class PathFilter(ExpressionFilter):
    """Storage file path filter."""

    operator_re = r"=~|!~"

    def __init__(self, key: str, op: str, value: str) -> None:
        """Initialize path filter from a regex pattern."""
        super().__init__(key, op, value)
        try:
            self.pattern = re.compile(value)
        except re.error as exc:
            raise ValueError(f"Invalid pattern: {value} - {exc}") from exc

    def match(self, value: t.Union[str, FileInfo]) -> bool:
        """Match the path with the filter's regex pattern."""
        path = value if isinstance(value, str) else value.path
        return OPERATORS[self.op](path, self.pattern)


class SizeFilter(ExpressionFilter):
    """Storage file size filter."""

    operator_re = r"<=|>=|!=|<>|<|>|="

    def __init__(self, key: str, op: str, value: str) -> None:
        """Initialize size filter from a human-readable size."""
        super().__init__(key, op, value)
        self.size = parse_hrsize(value)

    def match(self, value: t.Union[int, FileInfo]) -> bool:
        """Compare the file size to the filter value."""
        size = value if isinstance(value, int) else value.size
        return OPERATORS[self.op](size, self.size)


class TimeFilter(ExpressionFilter):
    """Storage file created- and modified time filter."""

    operator_re = r"<=|>=|!=|<>|<|>|="
    timestamp_re = (
        r"(?P<year>\d\d\d\d)([-_/]?"
        r"(?P<month>\d\d)([-_/]?"
        r"(?P<day>\d\d)([-_/T ]?"
        r"(?P<hour>\d\d)([-_:]?"
        r"(?P<minute>\d\d)([-_:]?"
        r"(?P<second>\d\d)?)?)?)?)?)?"
    )

    def __init__(self, key: str, op: str, value: str) -> None:
        """Initialize time filter from an iso-format timestamp."""
        super().__init__(key, op, value)
        match = re.match(self.timestamp_re, value)
        if not match:
            raise ValueError(f"Invalid time: {value} (expected YYYY-MM-DD HH:MM:SS)")
        self.time = "".join(part or "" for part in match.groupdict().values())

    def match(self, value: t.Union[int, FileInfo]) -> bool:
        """Compare the file time to the filter value."""
        timestamp = value if isinstance(value, int) else getattr(value, self.key)
        time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y%m%d%H%M%S")
        return OPERATORS[self.op](time[: len(self.time)], self.time)


def eq_tilde(value: str, pattern: t.Pattern) -> bool:
    """Return True if the regex pattern matches the value."""
    return bool(pattern.search(value))


def ne_tilde(value: str, pattern: t.Pattern) -> bool:
    """Return True if the regex pattern does not match the value."""
    return not eq_tilde(value, pattern)


TYPES = {
    "path": PathFilter,
    "size": SizeFilter,
    "created": TimeFilter,
    "modified": TimeFilter,
}

OPERATORS = {
    "=~": eq_tilde,
    "!~": ne_tilde,
    "<=": operator.le,
    ">=": operator.ge,
    "!=": operator.ne,
    "<>": operator.ne,
    "=": operator.eq,
    "<": operator.lt,
    ">": operator.gt,
}
