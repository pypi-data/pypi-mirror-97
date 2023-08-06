import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer

from vespr_model_deployment_utils.config import (
    CategoricalMissingActions,
    CategoricalOOBActions,
    ContinuousOOBActions,
    SupportedDatetimeOutput,
    VariableType,
)
from vespr_model_deployment_utils.data_ingress import (
    apply_categorical_bounds,
    apply_continuous_bounds,
    categorical_imputer,
    construct_datetime_features,
    drop_rows,
    feature_encoder,
    group_values,
    transformed_ndarray_to_df,
)


@pytest.mark.parametrize("convert_to", list(SupportedDatetimeOutput.Categorical))
def test_datetime_feature_construction_categorical(convert_to):
    df = {"test": pd.date_range(start="01/01/1970", end="01/01/1980", freq="M").astype(str).tolist()}
    df["test"][10] = "hello_world"
    df = pd.DataFrame(df)
    datetime_format = "%Y-%m-%d"

    new_feat_name = f"test_{convert_to.value}"
    column_info = pd.DataFrame(
        {
            "name": [new_feat_name],
            "is_datetime": [True],
            "data_type": [VariableType.CATEGORICAL],
        }
    )

    datetime_info = {"test": {"convert_to": convert_to, "datetime_format": datetime_format}}

    renaming = {new_feat_name: "test"}

    solutions = dict()
    solutions["test_day of week"] = [
        6,
        6,
        2,
        4,
        7,
        2,
        5,
        1,
        3,
        6,
        1,
        4,
        7,
        7,
        3,
        5,
        1,
        3,
        6,
        2,
        4,
        7,
        2,
        5,
        1,
        2,
        5,
        7,
        3,
        5,
        1,
        4,
        6,
        2,
        4,
        7,
        3,
        3,
        6,
        1,
        4,
        6,
        2,
        5,
        7,
        3,
        5,
        1,
        4,
        4,
        7,
        2,
        5,
        7,
        3,
        6,
        1,
        4,
        6,
        2,
        5,
        5,
        1,
        3,
        6,
        1,
        4,
        7,
        2,
        5,
        7,
        3,
        6,
        7,
        3,
        5,
        1,
        3,
        6,
        2,
        4,
        7,
        2,
        5,
        1,
        1,
        4,
        6,
        2,
        4,
        7,
        3,
        5,
        1,
        3,
        6,
        2,
        2,
        5,
        7,
        3,
        5,
        1,
        4,
        6,
        2,
        4,
        7,
        3,
        3,
        6,
        1,
        4,
        6,
        2,
        5,
        7,
        3,
        5,
        1,
    ]

    solutions["test_day of month"] = (
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] * 2
        + [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        + [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] * 3
        + [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        + [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] * 3
    )

    solutions["test_day of year"] = [
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        60,
        91,
        121,
        152,
        182,
        213,
        244,
        274,
        305,
        335,
        366,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        60,
        91,
        121,
        152,
        182,
        213,
        244,
        274,
        305,
        335,
        366,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
    ]

    solutions["test_month of year"] = list(range(1, 13)) * 10
    solutions["test_season of year"] = ([1] * 2 + [2] * 3 + [3] * 3 + [4] * 3 + [1]) * 10
    solutions["test_quarter of year"] = ([1] * 2 + [2] * 3 + [3] * 3 + [4] * 3 + [1]) * 10
    solutions["test_year"] = []

    for i in range(10):
        solutions["test_year"] += [1970 + i] * 12

    for column in solutions:
        solutions[column][10] = None

    solutions = pd.DataFrame(solutions)
    df_dt = construct_datetime_features(df, column_info, datetime_info, renaming)

    assert "test" not in df_dt.columns, "test column was not dropped"
    assert new_feat_name in df_dt.columns.to_list(), f"{new_feat_name} was not constructed"
    assert np.all(
        np.equal(
            df_dt.loc[~df_dt[new_feat_name].isna(), new_feat_name].to_list(),
            solutions.loc[~df_dt[new_feat_name].isna(), new_feat_name].to_list(),
        )
    ), f"{new_feat_name} failed"

    assert (df_dt[new_feat_name].isna() == solutions[new_feat_name].isna()).all()


@pytest.mark.parametrize("convert_to", list(SupportedDatetimeOutput.Continuous))
def test_datetime_feature_construction_continuous(convert_to):
    df = {
        "test": pd.date_range(
            start="01/01/1970",
            end="01/01/1980",
            freq="M",
        )
        .astype(str)
        .tolist()
    }

    df["test"][10] = "hello_world"
    df = pd.DataFrame(df)

    new_feat_name = f"test_{convert_to.value}"
    reference_point = "1970-01-01T00:00:00"
    datetime_format = "%Y-%m-%d"
    column_info = pd.DataFrame(
        {
            "name": [new_feat_name],
            "is_datetime": [True],
            "data_type": [VariableType.CONTINUOUS.value],
        }
    )

    dataset_config = {
        "test": {"convert_to": convert_to, "datetime_format": datetime_format, "reference_point": reference_point}
    }

    renaming = {new_feat_name: "test"}

    solutions = dict()
    solutions["seconds"] = np.array(
        [
            2592000,
            5011200,
            7689600,
            10281600,
            12960000,
            15552000,
            18230400,
            20908800,
            23500800,
            26179200,
            np.nan,
            31449600,
            34128000,
            36547200,
            39225600,
            41817600,
            44496000,
            47088000,
            49766400,
            52444800,
            55036800,
            57715200,
            60307200,
            62985600,
            65664000,
            68169600,
            70848000,
            73440000,
            76118400,
            78710400,
            81388800,
            84067200,
            86659200,
            89337600,
            91929600,
            94608000,
            97286400,
            99705600,
            102384000,
            104976000,
            107654400,
            110246400,
            112924800,
            115603200,
            118195200,
            120873600,
            123465600,
            126144000,
            128822400,
            131241600,
            133920000,
            136512000,
            139190400,
            141782400,
            144460800,
            147139200,
            149731200,
            152409600,
            155001600,
            157680000,
            160358400,
            162777600,
            165456000,
            168048000,
            170726400,
            173318400,
            175996800,
            178675200,
            181267200,
            183945600,
            186537600,
            189216000,
            191894400,
            194400000,
            197078400,
            199670400,
            202348800,
            204940800,
            207619200,
            210297600,
            212889600,
            215568000,
            218160000,
            220838400,
            223516800,
            225936000,
            228614400,
            231206400,
            233884800,
            236476800,
            239155200,
            241833600,
            244425600,
            247104000,
            249696000,
            252374400,
            255052800,
            257472000,
            260150400,
            262742400,
            265420800,
            268012800,
            270691200,
            273369600,
            275961600,
            278640000,
            281232000,
            283910400,
            286588800,
            289008000,
            291686400,
            294278400,
            296956800,
            299548800,
            302227200,
            304905600,
            307497600,
            310176000,
            312768000,
            315446400,
        ]
    )

    solutions["minutes"] = solutions["seconds"] / 60
    solutions["hours"] = solutions["minutes"] / 60
    solutions["days"] = solutions["hours"] / 24
    solutions["weeks"] = solutions["days"] / 7
    solutions["years"] = solutions["weeks"] / 52

    df_dt = construct_datetime_features(df, column_info, dataset_config, renaming)

    assert "test" not in df_dt.columns, "test column was not dropped"
    assert new_feat_name in df_dt.columns.to_list(), f"{new_feat_name} was not constructed"
    assert np.all(np.abs(np.nan_to_num(df_dt[new_feat_name] - solutions[convert_to.value.lower()])) < 1e-8)


def test_drop_row():
    df = dict()
    name = "cont_feature"
    df[name] = list(range(-50, 50))
    df = pd.DataFrame(df)

    column_info = dict()
    column_info["name"] = [name]
    column_info["data_type"] = [VariableType.CONTINUOUS.value]

    column_info["is_feature"] = [True]
    column_info["is_target"] = [False]
    column_info["is_protected"] = [False]
    column_info["drop"] = [False]
    column_info["missing_value_action"] = ["drop sample"]
    column_info["apply_bounds"] = [True]
    column_info = pd.DataFrame(column_info)

    row_drop_info = {name: {"oob_action": "drop sample", "bounds": {"min": -25, "max": 24}}}

    df = drop_rows(df, column_info, row_drop_info)

    assert not any(np.isnan(df.to_numpy()))
    solutions = dict()
    solutions[name] = list(range(-25, 25))
    assert all(df[name] == solutions[name])


def test_drop_row_missing():
    df = dict()

    df["feature_cat_fill_missing"] = ([np.nan] * 39) + (["d"] * 61)

    df["feature_cont_fill_missing"] = [np.nan] * 26 + list(range(-24, 25)) + [np.nan] * 25
    df = pd.DataFrame(df)

    column_info = dict()
    column_info["name"] = [
        "feature_cat_fill_missing",
        "feature_cont_fill_missing",
    ]
    column_info["data_type"] = [VariableType.CATEGORICAL.value, VariableType.CONTINUOUS.value]

    column_info["is_feature"] = [True, True]
    column_info["is_target"] = [False, False]
    column_info["is_protected"] = [False, False]
    column_info["drop"] = [False, False]
    column_info["apply_bounds"] = [False, False]
    column_info["missing_value_action"] = [
        "drop sample",
        "drop sample",
    ]
    column_info = pd.DataFrame(column_info)

    dataset_config = {}

    df = drop_rows(df, column_info, dataset_config)

    assert not df.isna().to_numpy().any()

    solutions = dict()
    solutions["feature_cat_fill_missing"] = ["d"] * 36
    solutions["feature_cont_fill_missing"] = list(range(-11, 25))

    assert all(df["feature_cat_fill_missing"] == solutions["feature_cat_fill_missing"])
    assert all(df["feature_cont_fill_missing"] == solutions["feature_cont_fill_missing"])


def test_feature_encoder():
    df = pd.DataFrame(
        [
            {"A": 1, "B": 1.15, "C": "str1"},
            {"A": 2, "B": 12.12, "C": "str2"},
            {"A": 3, "B": 100.1, "C": "str3"},
        ]
    )
    categorical_columns = ["A", "C"]

    encoded_df = feature_encoder(df, categorical_columns, str)
    for col in categorical_columns:
        for val in encoded_df[col].values:
            assert isinstance(val, str)


@pytest.mark.parametrize("method", [CategoricalMissingActions.FILL_UNKNOWN, CategoricalMissingActions.FILL_MAX_COUNT])
def test_categorical_imputer(method):
    x = pd.Series(data=["1", "1", np.nan, "2", "2", "1"])
    x_filled = categorical_imputer(x, method)
    assert pd.isna(x_filled).sum() == 0

    x = pd.Series(data=[np.nan, "A", np.nan, "C", "D"])
    x_filled = categorical_imputer(x, method)
    assert pd.isna(x_filled).sum() == 0

    x = pd.Series(data=["20.9", np.nan, "1.21", "100.85", np.nan])
    x_filled = categorical_imputer(x, method)
    assert pd.isna(x_filled).sum() == 0


def test_group_values():
    x = pd.Series(["a"] + (["b"] * 10) + (["c"] * 39) + (["d"] * 50))
    x_solved = pd.Series((["other"] * 11) + (["c"] * 39) + (["d"] * 50))

    x_result = group_values(x, [{"group_name": "other", "grouped_levels": {"a", "b"}}])
    assert all(x_result == x_solved)


@pytest.mark.parametrize("levels", [["a", "b"], ["a", "b", "c"]])
@pytest.mark.parametrize("method", [CategoricalOOBActions.REPLACE_MAX_COUNT, CategoricalOOBActions.REPLACE_UNKNOWN])
def test_group_small(levels, method):
    x = pd.Series(["a"] + (["b"] * 10) + (["c"] * 39) + (["d"] * 50))

    x_grouped = apply_categorical_bounds(x, levels=levels, method=method)

    if method == CategoricalOOBActions.REPLACE_MAX_COUNT:
        assert set(x_grouped.unique()) == set(levels)

    elif method == CategoricalOOBActions.REPLACE_UNKNOWN:
        assert set(x_grouped.unique()) == set(levels + ["unknown level"])


@pytest.mark.parametrize(
    "method", [ContinuousOOBActions.REPLACE_MEDIAN, ContinuousOOBActions.REPLACE_MEAN, ContinuousOOBActions.CLIP]
)
def test_clip_values(method):
    x = np.array([1.0, 1.0, 1.0, 2.0, 3.0, 4.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 9.0, 9.0])

    min_value = 2
    max_value = 7

    solution = dict()
    solution["clip"] = np.array([2, 2, 2, 2, 3, 4, 4, 5, 6, 7, 7, 7, 7, 7])
    solution["replace mean"] = np.array(
        [
            (31 / 7),
            (31 / 7),
            (31 / 7),
            2,
            3,
            4,
            4,
            5,
            6,
            7,
            (31 / 7),
            (31 / 7),
            (31 / 7),
            (31 / 7),
        ]
    )
    solution["replace median"] = np.array([4, 4, 4, 2, 3, 4, 4, 5, 6, 7, 4, 4, 4, 4])

    x_clipped = apply_continuous_bounds(x, min_value, max_value, method)
    assert all(x_clipped == solution[method.value])


def test_transformed_ndarray_to_df():
    data = pd.DataFrame(
        [
            {"A": 1, "B": 1.15, "C": "str1"},
            {"A": 2, "B": 12.12, "C": "str2"},
            {"A": 3, "B": 100.1, "C": "str3"},
        ]
    )
    categorical_columns = ["C"]
    continuous_columns = ["B"]

    column_transformer = ColumnTransformer(
        [
            ("drop_transformers", "drop", ["A"]),
            ("transformer1", "passthrough", ["B"]),
            ("transformer2", "passthrough", ["C"]),
        ]
    )
    X = column_transformer.fit_transform(data)

    df = transformed_ndarray_to_df(X, column_transformer, categorical_columns, continuous_columns)
    assert isinstance(df, pd.DataFrame)
    for c in ["B", "C"]:
        assert c in df.columns
