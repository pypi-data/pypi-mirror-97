"""Config module."""
# pylint: disable=too-few-public-methods
import pytz
import tzlocal
from pydantic import BaseSettings, Field, validator


class Config(BaseSettings):
    """Meta extractor config."""

    class Config:
        """Enable env vars with prefix `FW_META_`."""

        env_prefix = "fw_meta_"

    # timezone to use when parsing datetimes
    # use tzlocal.reload_localzone to suppress tzlocal caching
    timezone: pytz.BaseTzInfo = Field(default_factory=tzlocal.reload_localzone)

    @validator("timezone", pre=True)
    @classmethod
    def validate_timezone(cls, val):
        """Load timezone using pytz if val is a string."""
        if isinstance(val, str):
            return pytz.timezone(val)
        return val


CONFIG = Config()
