"""Data ingress functions."""
import logging

import numpy as np
from pandas import DataFrame, isna, to_datetime

from vespr_model_deployment_utils.config import (
    CategoricalMissingActions,
    CategoricalOOBActions,
    CommonActions,
    ContinuousOOBActions,
    Seconds_In,
    SupportedDatetimeOutput,
    Transformers,
    VariableType,
)

logger = logging.getLogger(__name__)


def transformed_ndarray_to_df(X, column_transformer, categorical_columns, continuous_columns):
    """
    Build dataframe from ndarray output of transformer.

    :param X: ndarray, output of transformer
    :param column_transformer: transformer object
    :param categorical_columns: list of columns
    :param continuous_columns: list of columns
    :return: df
    """
    columns = []
    for transformer in column_transformer.transformers_:
        if not transformer[0] == Transformers.DROP_TRANSFORMERS:
            columns += transformer[2]
    df = DataFrame(data=X, columns=columns)
    df[categorical_columns] = df[categorical_columns].astype(str)
    df[continuous_columns] = df[continuous_columns].astype(float)
    return df


def drop_rows(df, column_info, drop_row_info):
    """
    Drop missing samples.

    :param df: DataFrame: input dataframe - pandas
    :param column_info: DataFrame: column information related to df
    :param drop_row_info: required information for formatting dataset
    :return: df, DataFrame, input dataframe - pandas
    """
    logger.info("Dropping rows from dataset...")
    logger.info("Finding columns with DROP_SAMPLE for missing data")
    drop_missing = column_info.loc[column_info["missing_value_action"] == CommonActions.DROP_SAMPLE]
    logger.info(f"Columns for processing missing_value_action = {drop_missing['name']}")

    for ft in drop_missing["name"]:
        issues = df[ft].isna()
        df = df.drop(df[issues].index, axis=0)

    logger.info("Finding columns with DROP_SAMPLE for out of bounds action")
    drop_boundaries = column_info[column_info["apply_bounds"]]
    logger.info(f"Columns for processing missing_value_action = {drop_boundaries['name']}")
    for i in drop_boundaries.index:
        ft = drop_boundaries["name"][i]
        if drop_row_info[ft]["oob_action"] == CommonActions.DROP_SAMPLE:
            bounds = drop_row_info[ft]["bounds"]
            if drop_boundaries["data_type"][i] == VariableType.CONTINUOUS:
                issues = df.loc[
                    ~df[ft].between(
                        bounds["min"],
                        bounds["max"],
                        inclusive=True,
                    )
                ]
            elif drop_boundaries["data_type"][i] == VariableType.CATEGORICAL:
                issues = df.loc[~df[ft].isin(bounds["levels"])]

            else:
                raise ValueError(f"Unknown datatype {drop_boundaries['data_type'][i]}")

            df = df.drop(issues.index, axis=0)
    logger.info("Exiting row dropping")
    return df


def feature_encoder(df, columns, data_type):
    """
    Encode features as given type.

    :param df: DataFrame: input dataframe - pandas
    :param categorical_columns: list of categorical samples
    :return: dataframe
    """
    logger.info("Beginning string encoding of categorical features")
    for column in columns:
        df.loc[~df[column].isna(), column] = df.loc[~df[column].isna(), column].astype(data_type)
    logger.info("Completed...")
    return df


def construct_datetime_features(df, datetime_column_info, datetime_info, renaming):
    """
    Create datetime features.

    :param df: DataFrame: input dataframe - pandas
    :param datetime_info: dict: Custom pydantic model containing processing information
    :param renaming: dict: Dictionary of original and new column names for datetimes
    :param datetime_column_info: DataFrame: column information related to df (datetime info only)
    :return: DataFrame
    """
    to_categorical = datetime_column_info[datetime_column_info["data_type"] == VariableType.CATEGORICAL][
        "name"
    ].to_list()
    logger.info(f"Converting to categorical: {to_categorical}")
    to_continuous = datetime_column_info[datetime_column_info["data_type"] == VariableType.CONTINUOUS]["name"].to_list()
    logger.info(f"Converting to continuous: {to_continuous}")

    for _, column in datetime_column_info.iterrows():
        column_name = column["name"]
        dt_info = datetime_info[renaming[column_name]]
        convert_to = dt_info["convert_to"]
        datetime_format = dt_info["datetime_format"]
        logger.info(f"Processing {column_name}")

        ts = to_datetime(df[renaming[column_name]], errors="coerce", format=datetime_format)

        if column_name in to_categorical:

            if convert_to == SupportedDatetimeOutput.Categorical.DAY_OF_WEEK:
                df[column_name] = [t.isoweekday() if not isna(t) else t for t in ts]

            if convert_to == SupportedDatetimeOutput.Categorical.DAY_OF_MONTH:
                df[column_name] = [t.day if not isna(t) else t for t in ts]

            if convert_to == SupportedDatetimeOutput.Categorical.DAY_OF_YEAR:
                df[column_name] = [t.timetuple().tm_yday if not isna(t) else t for t in ts]

            if (
                convert_to == SupportedDatetimeOutput.Categorical.QUARTER_OF_YEAR
                or convert_to == SupportedDatetimeOutput.Categorical.SEASON_OF_YEAR
            ):
                quarter_of_year = lambda m: ((m % 12) // 3) + 1
                df[column_name] = [quarter_of_year(t.month) if not isna(t) else t for t in ts]

            if convert_to == SupportedDatetimeOutput.Categorical.MONTH_OF_YEAR:
                df[column_name] = [t.month if not isna(t) else None for t in ts]

            if convert_to == SupportedDatetimeOutput.Categorical.YEAR:
                df[column_name] = [t.year if not isna(t) else None for t in ts]

        elif column_name in to_continuous:

            logger.info(f"Processing {column_name} as continuous")
            reference_point = to_datetime(
                dt_info["reference_point"],
                errors="coerce",
                format=SupportedDatetimeOutput.CATEGORICAL_REFERENCE_FORMAT,
            )
            logger.info(f"References point:{reference_point}")
            df[column_name] = [(t.total_seconds() / Seconds_In[convert_to]) for t in (ts - reference_point)]

        df = df.drop(renaming[column_name], axis=1)

    return df


def apply_categorical_bounds(feat, levels, method):
    """
    Handle any values that are not in the expected bounds.

    :param feat: DataSeries, single feature to be processed
    :param bounds: bounds of categorical data
    :param method: how to handle out of bounds data
    :return: feat: DataSeries, pfearocessed feature
    """
    logger.info("Applying categorical bounds")

    issues = ~feat.isin(levels)

    if method == CommonActions.DROP_SAMPLE:
        assert (
            len(feat[issues].value_counts()) <= 1
        ), "No missing values should exist after drop samples has been applied"

    elif method == CategoricalOOBActions.REPLACE_MAX_COUNT:
        feat[issues] = feat[feat.isin(levels)].dropna().max()[0]

    elif method == CategoricalOOBActions.REPLACE_UNKNOWN:
        feat[issues] = "unknown level"

    else:
        raise ValueError(f"Unknown method to handle categorical out of bounds data {method}")

    return feat


def group_values(feat, grouping_info):
    """
    Group values according to groups.

    :param feat: DataSeries, single feature to be processed
    :param grouping_info: pydantic model, levels to be grouped
    :return: feat: DataSeries, processed feature
    """
    logger.info("Applying value grouping...")

    for group in grouping_info:
        new_name = group["group_name"]
        levels = group["grouped_levels"]
        feat[feat.isin(levels)] = new_name

    logger.info("Grouping complete...")
    return feat


def categorical_imputer(feat, method):
    """
    Imputes missing values using according to method.

    designed as a speed up over sklearn's SimpleImputer(strategy="most_frequent")

    :param feat: pd.Series which needs to imputed
    :param method: CategoricalMissingActions
    :return feat: pd.Series
    """
    logger.info("Imputing  categorical feature...")
    excluded = isna(feat)

    if method == CategoricalMissingActions.FILL_MAX_COUNT:
        fill = feat.dropna().max()[0]
    elif method == CategoricalMissingActions.FILL_UNKNOWN:
        fill = "unknown level"
    else:
        raise ValueError(f"Unknown value of method for categorical missing values {method}")

    feat[excluded] = fill
    logger.info("Completed imputing")
    return feat


def apply_continuous_bounds(feat, min_value, max_value, method):
    """
    Clip continuous values.

    :param feat: DataSeries, single feature to be processed
    :param min_value: float, min value for clipping
    :param max_value: float, max value for clipping
    :param method: ContinuousOOBActions, how to handle values outside range, [CLIP, FILL_MEAN, FILL_MEDIAN]
    :return: feat: DataSeries, processed feature
    """
    clip_top_idxs = feat > max_value
    clip_bottom_idxs = feat < min_value

    if method == ContinuousOOBActions.CLIP:
        feat[clip_top_idxs] = max_value
        feat[clip_bottom_idxs] = min_value

    elif method == ContinuousOOBActions.REPLACE_MEAN:
        fill_idxs = np.where(np.logical_and(feat >= min_value, feat <= max_value))[0]
        fill_value = np.mean(feat[fill_idxs])
        fill_idxs = np.where(np.logical_or(feat < min_value, feat > max_value))[0]
        feat[fill_idxs] = fill_value

    elif method == ContinuousOOBActions.REPLACE_MEDIAN:
        fill_idxs = np.where(np.logical_and(feat >= min_value, feat <= max_value))[0]
        fill_value = np.median(feat[fill_idxs])
        fill_idxs = np.where(np.logical_or(feat < min_value, feat > max_value))[0]
        feat[fill_idxs] = fill_value

    elif method == CommonActions.DROP_SAMPLE:
        assert (
            clip_top_idxs.sum() == clip_bottom_idxs.sum() == 0
        ), "There should be no missing values if method was drop sample"

    else:
        raise ValueError(f"Unknown method for handling out of bounds samples: {method}")

    return feat
