import pandas as pd
import pytest


from ..model_api.model_functions import compute_duration, scale_inputs, classify_match

from ..model_api.constants import (
    STATE_HOLIDAYS,
    STORE_TYPE,
    ASSORT_TYPE,
    ORDINAL_FEATURES,
    NUMERICAL_FEATURES,
    PROMO_TWO_WEEKYEAR,
    COMPET_OPEN_MONTHYEAR,
    BASE_DIR,
)

from ..model_api.model_pipeline import (
    reshape_inputs_pipeline,
    model_prediction_pipeline,
)

from pandas.testing import assert_series_equal
from numpy.testing import assert_almost_equal


@pytest.mark.parametrize(
    "sales_data, match_dict, expected_results",
    [
        (
            "0",
            STATE_HOLIDAYS,
            {
                "no_holiday": 1,
                "public_holiday": 0,
                "easter_holiday": 0,
                "christmas": 0,
            },
        ),
        ("a", ASSORT_TYPE, {"basic": 1, "extra": 0, "extended": 0}),
        (
            "c",
            STORE_TYPE,
            {
                "store_type_a": 0,
                "store_type_b": 0,
                "store_type_c": 1,
                "store_type_d": 0,
            },
        ),
    ],
)
def test_classify_match(sales_data, match_dict, expected_results):
    df_request = pd.Series(index=match_dict.values())
    results = classify_match(match_dict, sales_data, df_request)
    exp_results = pd.Series(expected_results)

    assert_series_equal(
        results,
        exp_results,
        check_dtype=False,
        check_index_type=False,
        check_names=False,
    )


@pytest.mark.parametrize(
    "current_date, start_date, freq, expected_results",
    [
        (
            {
                "Month": 1,
                "Year": 2015,
            },
            dict(zip(COMPET_OPEN_MONTHYEAR, [12, 2011])),
            "M",
            37,
        ),
        (
            {
                "Month": 51,
                "Year": 2015,
            },
            dict(zip(COMPET_OPEN_MONTHYEAR, [7, 2011])),
            "W",
            252,
        ),
        (
            {
                "Week": 1,
                "Year": 2013,
            },
            dict(zip(PROMO_TWO_WEEKYEAR, [5, 2014])),
            "W",
            0,
        ),
        (
            {
                "Week": 1,
                "Year": 2013,
            },
            dict(zip(PROMO_TWO_WEEKYEAR, [0, 0])),
            "M",
            0,
        ),
    ],
)
def test_compute_duration(current_date, start_date, freq, expected_results):
    current_df = pd.Series(current_date)
    start_df = pd.Series(start_date)
    result = compute_duration(current_df, start_df, freq)
    assert_almost_equal(result, expected_results)


@pytest.mark.parametrize(
    "df_vals, feature_list, scaler_type, expected_results",
    [
        (
            {"Store": 33, "Year": 2013, "Week": 27, "Month": 7, "DayOfWeek": 6},
            ORDINAL_FEATURES,
            "minmax",
            {
                "Store": 0.02872531418312388,
                "Year": 0.0,
                "Week": 0.5098039215686274,
                "Month": 0.5454545454545454,
                "DayOfWeek": 0.8333333333333334,
            },
        ),
        (
            {
                "Customers": 603,
                "CompetitionDistance": 1680,
                "CompetitionOpenSinceDuration": 112,
                "Promo2SinceDuration": 0,
            },
            NUMERICAL_FEATURES,
            "standard",
            {
                "Customers": -0.06786970568702155,
                "CompetitionDistance": -0.48495409395015204,
                "CompetitionOpenSinceDuration": 1.0972063300371866,
                "Promo2SinceDuration": -0.6770057837989922,
            },
        ),
    ],
)
def test_scale_inputs(df_vals, feature_list, scaler_type, expected_results):
    df_to_scale = pd.Series(df_vals)
    results = scale_inputs(df_to_scale, feature_list, scaler_type)
    exp_results = pd.Series(expected_results)

    assert_series_equal(
        results,
        exp_results,
        check_dtype=False,
        check_index_type=False,
        check_names=False,
    )


@pytest.mark.parametrize(
    "post_request, expected_results",
    [
        (
            {
                "Store": 872,
                "DayOfWeek": 3,
                "Date": "2014-07-09",
                "Customers": 577,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "0",
                "SchoolHoliday": 1,
            },
            4944.18,
        ),
        (
            {
                "Store": 608,
                "DayOfWeek": 7,
                "Date": "2013-12-01",
                "Customers": 0,
                "Open": 0,
                "Promo": 0,
                "StateHoliday": "0",
                "SchoolHoliday": 0,
            },
            418.3,
        ),
        (
            {
                "Store": 67,
                "DayOfWeek": 6,
                "Date": "2013-11-23",
                "Customers": 619,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "0",
                "SchoolHoliday": 0,
            },
            5155.34,
        ),
        (
            {
                "Store": 788,
                "DayOfWeek": 5,
                "Date": "2015-02-06",
                "Customers": 1600,
                "Open": 1,
                "Promo": 1,
                "StateHoliday": "0",
                "SchoolHoliday": 1,
            },
            13366.42,
        ),
        (
            {
                "Store": 348,
                "DayOfWeek": 1,
                "Date": "2015-01-12",
                "Customers": 821,
                "Open": 1,
                "Promo": 1,
                "StateHoliday": "0",
                "SchoolHoliday": 0,
            },
            8206.98,
        ),
        (
            {
                "Store": 43,
                "DayOfWeek": 7,
                "Date": "2013-12-22",
                "Customers": 0,
                "Open": 0,
                "Promo": 0,
                "StateHoliday": "0",
                "SchoolHoliday": 0,
            },
            921.59,
        ),
        (
            {
                "Store": 947,
                "DayOfWeek": 3,
                "Date": "2013-10-16",
                "Customers": 1153,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "0",
                "SchoolHoliday": 0,
            },
            9138.18,
        ),
        (
            {
                "Store": 260,
                "DayOfWeek": 2,
                "Date": "2015-04-07",
                "Customers": 990,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "0",
                "SchoolHoliday": 1,
            },
            7768.47,
        ),
        (
            {
                "Store": 1099,
                "DayOfWeek": 1,
                "Date": "2015-04-06",
                "Customers": 804,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "b",
                "SchoolHoliday": 1,
            },
            6193.56,
        ),
        (
            {
                "Store": 274,
                "DayOfWeek": 4,
                "Date": "2015-01-01",
                "Customers": 754,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "a",
                "SchoolHoliday": 1,
            },
            -1384.13,
        ),
        (
            {
                "Store": 948,
                "DayOfWeek": 4,
                "Date": "2015-12-25",
                "Customers": 1463,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "c",
                "SchoolHoliday": 1,
            },
            3930.79,
        ),
    ],
)
def test_integration_modelling_pipeline(post_request, expected_results):
    df = pd.read_csv(BASE_DIR / "data" / "processed_data.csv", nrows=1).drop(
        ["Id", "Sales"], axis=1
    )
    df_request = pd.Series(index=df.columns)

    df_request["Store"] = post_request["Store"]
    df_request["DayOfWeek"] = post_request["DayOfWeek"]
    df_request["Customers"] = post_request["Customers"]
    df_request["Open"] = post_request["Open"]
    df_request["Promo"] = post_request["Promo"]
    df_request["SchoolHoliday"] = post_request["SchoolHoliday"]
    df_request["Date"] = post_request["Date"]

    df_request = classify_match(
        STATE_HOLIDAYS, post_request["StateHoliday"], df_request
    )

    reshaped_inputs = reshape_inputs_pipeline(df_request)
    result = model_prediction_pipeline(reshaped_inputs=reshaped_inputs)
    assert_almost_equal(result, expected_results)
