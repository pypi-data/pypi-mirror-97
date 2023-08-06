"""Enums and constants used to integrate with VESPR."""
from enum import Enum


class SupportedDatetimeOutput:
    """Class to hold supported datetime formats."""

    CATEGORICAL_REFERENCE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    class Categorical(str, Enum):
        """Supported Categorical Datetime formats."""

        DAY_OF_WEEK = "day of week"
        DAY_OF_MONTH = "day of month"
        DAY_OF_YEAR = "day of year"
        SEASON_OF_YEAR = "season of year"
        QUARTER_OF_YEAR = "quarter of year"
        MONTH_OF_YEAR = "month of year"
        YEAR = "year"

    class Continuous(str, Enum):
        """Supported Continuous Datetime formats."""

        SECONDS = "seconds"
        MINUTES = "minutes"
        HOURS = "hours"
        DAYS = "days"
        WEEKS = "weeks"
        YEARS = "years"


Seconds_In = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400, "weeks": 604800, "years": 31449600}


class VariableType(str, Enum):
    """Supported variable types post data ingress."""

    CONTINUOUS = "continuous"
    CATEGORICAL = "categorical"


class CommonActions(str, Enum):
    """Actions that are common across all missing and out of bounds sample cases."""

    DROP_SAMPLE = "drop sample"


class ContinuousMissingActions(str, Enum):
    """Supported actions for missing continuous data."""

    FILL_MEAN = "fill mean"
    FILL_MEDIAN = "fill median"
    DROP_SAMPLE = CommonActions.DROP_SAMPLE.value


class ContinuousOOBActions(str, Enum):
    """Supported actions for out of bounds data."""

    CLIP = "clip"
    REPLACE_MEAN = "replace mean"
    REPLACE_MEDIAN = "replace median"
    DROP_SAMPLE = CommonActions.DROP_SAMPLE.value


class CategoricalMissingActions(str, Enum):
    """Supported actions for missing continuous data."""

    FILL_MAX_COUNT = "fill most common"
    FILL_UNKNOWN = "fill <unknown>"
    DROP_SAMPLE = CommonActions.DROP_SAMPLE.value


class CategoricalOOBActions(str, Enum):
    """Supported actions for out of bounds data."""

    REPLACE_MAX_COUNT = "replace most common"
    REPLACE_UNKNOWN = "replace <unknown>"
    DROP_SAMPLE = CommonActions.DROP_SAMPLE.value


class Transformers(str, Enum):
    DROP_TRANSFORMERS = "drop_transformers"
