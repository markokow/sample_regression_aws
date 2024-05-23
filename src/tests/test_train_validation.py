import pytest
import pandas as pd
from pandas._libs.tslibs.parsing import DateParseError

from ..model_api.constants import (
    STATE_HOLIDAYS,
    BASE_DIR,
)


@pytest.fixture(scope="module")
def training_data_input():
    df_train_chunks = pd.read_csv(
        BASE_DIR / "data" / "raw" / "train.csv", iterator=True, chunksize=1000
    )  # csv reading is done in chunks to process large data
    df_train = pd.concat(df_train_chunks, ignore_index=True)

    return df_train


def test_store_entry(training_data_input):
    df_store_info = pd.read_csv(
        BASE_DIR / "data" / "raw" / "store.csv", usecols=["Store"]
    ).drop_duplicates()

    store_list = df_store_info["Store"].to_list()

    mask = (training_data_input["Store"] < store_list[0]) | (
        training_data_input["Store"] > store_list[-1]
    )
    excess_entry = len(training_data_input.loc[mask])

    assert excess_entry == 0


def test_check_stateholidays(training_data_input):
    wrong_entry = 0
    for holidays in training_data_input["StateHoliday"].unique():
        if str(holidays) not in list(STATE_HOLIDAYS.keys()):
            wrong_entry += 1
    assert wrong_entry == 0


def test_check_date_period(training_data_input):
    parse_error = 0
    try:
        pd.Series(training_data_input["Date"].unique()).apply(lambda x: pd.Period(x))
    except DateParseError:
        parse_error = 1

    assert parse_error == 0


def test_check_binary_entry_school_holiday(training_data_input):
    for binary_str in ["SchoolHoliday", "Promo", "Open"]:
        unique_list = list(training_data_input[binary_str].unique())
        unique_list.remove(1)
        unique_list.remove(0)

        deviate_limit = len(unique_list)
        assert deviate_limit == 0


def test_check_customer_entry(training_data_input):
    mask = training_data_input["Customers"] < 0
    negative_entry = len(training_data_input.loc[mask])

    assert negative_entry == 0


def check_week_day_entry(training_data_input):
    not_in_range = 0
    week_list = list(training_data_input["DayOfWeek"].unique())
    for week in week_list:
        if week not in range(1, 8):
            not_in_range += 1

    assert not_in_range == 0
