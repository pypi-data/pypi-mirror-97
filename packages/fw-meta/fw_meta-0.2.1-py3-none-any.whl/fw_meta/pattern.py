"""Flywheel meta pattern class/definitions and utility funtions."""
import re
import typing as t

from memoization import cached

from .fields import is_tmp_field, validate_field
from .utils import parse_datetime

__all__ = ["extract_pattern", "MetaPattern"]


# map of strptime codes to regex strings
STRPTIME_CODE_RE: t.Dict[str, str] = {
    "%a": r"[A-Za-z]+?",
    "%A": r"[A-Za-z]+?",
    "%w": r"\d",
    "%d": r"\d\d",
    "%b": r"[A-Za-z]+?",
    "%B": r"[A-Za-z]+?",
    "%m": r"\d\d",
    "%y": r"\d\d",
    "%Y": r"\d\d\d\d",
    "%H": r"\d\d",
    "%I": r"\d\d",
    "%p": r"[A-Za-z]+?",
    "%M": r"\d\d",
    "%S": r"\d\d",
    "%f": r"\d+?",
    "%z": r"[+-]\d\d\d\d(\d\d(\.\d+?)?)?",
    "%Z": r"[A-Z]*?",
    "%j": r"\d\d\d",
    "%U": r"\d\d",
    "%W": r"\d\d",
    "%c": r".*?",
    "%x": r".*?",
    "%X": r".*?",
    "%%": r"%",
    "%G": r"\d\d\d\d",
    "%u": r"\d",
    "%V": r"\d\d",
}


def extract_pattern(pattern: str, value: str) -> t.Dict[str, str]:
    """Shorthand for using MetaPattern in a single statement."""
    meta_pattern = MetaPattern(pattern)
    return meta_pattern.extract(value)


@cached
class MetaPattern:
    r"""MetaPattern can extract flywheel upload metadata from strings.

    Templates allow defining capture groups within { and } tailored for flywheel
    metadata fields, eg. '{subject.label}' would match any string as the subject
    label field.

    Templates are very similar to python regexes, but it is easire to define groups:
      {group} -> (?P<name>)
      [...]   -> (...)?
      *       -> *?
      +       -> +?

    This implies that you need to escape these characters if you want to use
    the original token: [a-z]+ needs to be defined like this: \[a-z\]+
    Similarly eager match can be achived by escaping * like this: \*

    Regex flags can be specified after `:` like this: "{group}:i"
    Available flags:
      - a: re.ASCII
      - i: re.IGNORECASE
      - s: re.DOTALL

    Timestamp fields (session.timestamp and acquisition.timestamp) are parsed
    via dateutil.parser by default, or with a custom strptime pattern if given:
    '{acquisition.timestamp:%Y%m%d}'

    Examples:
      MetaPattern(r'.\*/{subject}/.*.dcm').extract('foo/bar/subject/1.2.3.dcm')
      >>> {'subject.label': 'subject'}

      MetaPattern(r'[fw://]{group:\[^/\]+}/{project}').extract('foo/bar/baz')
      >>> {'group._id': 'foo', 'project.label': 'bar/baz'}

      MetaPattern('{timestamp:%Y%m%d%H%M%S}(\.\d*)?').extract('19991231235959.99')
      >>> {'acquisition.timestamp': datetime.datetime(1999, 12, 31, 23, 59, 59, 0)}
    """

    def __init__(self, pattern: str) -> None:
        """Parse and compile pattern into a python regex Pattern."""
        self.pattern = pattern
        self.timestamp_formats: t.Dict[str, str] = {}
        regex, flags, self.timestamp_formats = parse_pattern(Tokenizer(pattern))
        self.regex = re.compile(f"^{regex}$", flags=flags)

    def __repr__(self) -> str:
        """Return the canonical string representation of a MetaPattern instance."""
        return f"{self.__class__.__name__}({self.pattern!r})"

    def __str__(self) -> str:
        """Return the string representation of the pattern."""
        return self.pattern

    def extract(
        self, string: str, temp: t.Dict[str, t.Any] = None
    ) -> t.Dict[str, t.Any]:
        """Extract metadata from a string."""
        match = self.regex.match(string)
        if not match:
            return {}
        meta = {}
        for field, value in match.groupdict().items():
            if not value:
                continue
            field = python_id_to_str(field)
            if field.endswith("timestamp"):
                timestamp_format = self.timestamp_formats.get(field)
                value = parse_datetime(value, timestamp_format)  # type: ignore
            if temp is not None and is_tmp_field(field):
                temp[field] = value
            else:
                meta[field] = value
        return meta


def parse_pattern(source, level=0) -> t.Tuple[str, int, t.Dict[str, str]]:
    r"""Parse our custom regex syntax and convert to a valid python regex.

    Validates that group names are valid Flywheel meta field names.

    Reads regex options defined at the end of source after a ':' character.
    Top level ':' character needs to be escaped if want to use as a literal.

    Converts and stores timestamp formats defined for Flywheel timestamp meta
    fields.

    Conversion examples:
      {group}        -> (?P<group__2e___id>.*?)
      []             -> ()?
      *              -> .*?
      \*             -> .*
      {timestamp:%Y} -> (?P<acquisition__2e__timestamp>\d\d\d\d)
      group          -> (?P<group__2e___id>.*?)
    """
    # pylint: disable=too-many-branches,too-many-statements
    regex = ""
    timestamp_formats = dict()
    flags = 0

    while char := source.next:
        if char in "]}":
            break
        source.set_next()

        if char[0] == "\\":
            if char[1] in "[]{}*+:":
                # our special characters, remove the escape char
                regex += char[1]
            else:
                # keep evrything as is
                regex += char
        elif char == "[":
            # simplified optional group syntax
            sub_re, _, sub_ts_formats = parse_pattern(source, level=level + 1)
            timestamp_formats.update(sub_ts_formats)
            if not source.match("]"):
                raise ValueError("missing ], unterminated pattern")
            regex += fr"({sub_re})?"
        elif char == "{":
            # custom named group definition
            field = source.get_until(":}")
            if not field:
                raise ValueError("missing group name")
            field = validate_field(field)
            if source.next == ":":
                source.set_next()
                sub_re, _, sub_ts_formats = parse_pattern(source, level=level + 1)
                timestamp_formats.update(sub_ts_formats)
                if field.endswith("timestamp") and sub_re:
                    # treat sub regex pattern as a timestamp format
                    # store strptime pattern and translate to regex
                    timestamp_formats[field] = sub_re
                    sub_re = strptime_to_regex(sub_re)
            else:
                sub_re = ".*?"
            if not source.match("}"):
                raise ValueError("missing }, unterminated pattern")
            regex += fr"(?P<{str_to_python_id(field)}>{sub_re})"
        elif char in "*+":
            # default to lazy match
            regex += f"{char}?"
        elif char == ":" and level == 0:
            # handle regex options
            options = source.get_until(None)
            if not set(options).issubset(set("ais")):
                raise ValueError(f"Invalid pattern options {options!r}")
            if "a" in options:
                flags |= re.ASCII
            if "i" in options:
                flags |= re.IGNORECASE
            if "s" in options:
                flags |= re.DOTALL
        else:
            # keep everything else as is
            regex += char
    if level == 0:
        try:
            # shorthand notation
            field = validate_field(regex)
            regex = fr"(?P<{str_to_python_id(field)}>.*?)"
        except ValueError:
            pass
    return regex, flags, timestamp_formats


class Tokenizer:
    """Simple tokenizer class to help parsing patterns."""

    def __init__(self, string: str):
        self.string = string
        self.index = 0
        self.next: t.Optional[str] = None
        self.set_next()

    def set_next(self) -> None:
        """Find a set upcoming token."""
        index = self.index
        try:
            char = self.string[index]
        except IndexError:
            self.next = None
            return

        if char == "\\":
            index += 1
            try:
                char += self.string[index]
            except IndexError as exc:
                raise ValueError("Pattern ending with backslash") from exc

        self.index = index + 1
        self.next = char

    def get_until(self, terminals: t.Optional[str]) -> str:
        """Get until terminal character or until the end.

        Multiple terminal characters can be defined.
        """
        result = ""
        while self.next:
            if terminals and self.next in terminals:
                break
            result += self.next
            self.set_next()
        return result

    def match(self, char: str) -> bool:
        """Check character match and set next one if match."""
        if char == self.next:
            self.set_next()
            return True
        return False


def strptime_to_regex(pattern: str) -> str:
    """Convert an strptime pattern to a matching regex string."""
    regex, lastpos = "", 0
    for match in re.finditer(r"%.", pattern):
        # track non-capture prefix and postfix around match group
        start, end = match.span()
        pre, post = match.string[lastpos:start], match.string[end:]
        lastpos = end
        # translate strptime format code to regex
        code = match.group()
        code_re = STRPTIME_CODE_RE.get(code)
        if code_re is None:
            raise ValueError(f"Invalid strptime code {code!r} in {pattern!r}")
        regex = f"{regex}{pre}{code_re}"
    regex = f"{regex}{post}"
    return regex


def str_to_python_id(raw_string: str) -> str:
    """Convert any string to a valid python identifier in a reversible way."""

    def char_to_hex(match: t.Match) -> str:
        return f"__{ord(match.group(0)):02x}__"

    return re.sub(r"[^a-z0-9_]{1}", char_to_hex, raw_string)


def python_id_to_str(python_id: str) -> str:
    """Convert a python identifier back to the original/normal string."""

    def hex_to_char(match: t.Match) -> str:
        return chr(int(match.group(1), 16))

    return re.sub(r"__([a-f0-9]{2})__", hex_to_char, python_id)
