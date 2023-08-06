"""Utility functions."""
import datetime as dt
import typing as t

import dateutil.parser as dt_parser


def parse_datetime(value: str, pattern: t.Optional[str] = None) -> dt.datetime:
    """Return datetime object from a timestamp string."""
    try:
        if pattern:
            return dt.datetime.strptime(value, pattern)
        return dt_parser.parse(value)
    except (ValueError, dt_parser.ParserError) as exc:  # type: ignore
        msg = f"Cannot parse timestamp {value!r} (pattern: {pattern!r})"
        raise ValueError(msg) from exc
