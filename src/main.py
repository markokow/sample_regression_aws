from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import pandas as pd

from typing import Dict, Union

from model_api.constants import STATE_HOLIDAYS, BASE_DIR

from pandas._libs.tslibs.parsing import DateParseError

from model_api.model_functions import classify_match
from model_api.model_pipeline import reshape_inputs_pipeline, model_prediction_pipeline


app = FastAPI()


class SalesData(BaseModel):
    """Standard input entry format and data type of incoming JSON POST requests"""

    Store: int
    DayOfWeek: int
    Date: str
    Customers: int
    Open: int
    Promo: int
    StateHoliday: str
    SchoolHoliday: int


class PredictionOut(BaseModel):
    """Standard format and data type of predicted output"""

    sales: float


@app.post("/predict", response_model=PredictionOut)
async def process_data(sales_data: SalesData) -> Dict[str, float]:
    """Predict the sales based on incoming JSON response values.

    This function will process the incoming POST request, validate the entry, clean/reshape the inputs into corresponding model features, and predict the sales output based on the trained model.

    :param sales_data: JSON response input
    :type sales_data: StoreData
    :return: predicted sales data
    :rtype: Dict[str, float]
    """
    df = pd.read_csv(BASE_DIR / "data" / "processed_data.csv", nrows=1).drop(
        ["Id", "Sales"], axis=1
    )
    df_request = pd.Series(index=df.columns)
    sales_data = await pre_check_data_entry(sales_data)
    df_request["Store"] = sales_data.Store
    df_request["DayOfWeek"] = sales_data.DayOfWeek
    df_request["Customers"] = sales_data.Customers
    df_request["Open"] = sales_data.Open
    df_request["Promo"] = sales_data.Promo
    df_request["SchoolHoliday"] = sales_data.SchoolHoliday
    df_request["Date"] = sales_data.Date
    df_request = classify_match(
        STATE_HOLIDAYS,
        sales_data.StateHoliday,
        df_request,
    )

    reshaped_inputs = reshape_inputs_pipeline(df_request)
    sales = model_prediction_pipeline(reshaped_inputs=reshaped_inputs)

    return {"sales": sales}


async def pre_check_data_entry(sales_data: SalesData) -> SalesData:
    """Check the validity of the sales data entry.

    :param sales_data: JSON response input
    :type sales_data: SalesData
    :return: validated model input
    :rtype: SalesData
    """
    sales_data = await check_store_entry(sales_data)
    sales_data = await check_week_day_entry(sales_data)
    sales_data = await check_customer_entry(sales_data)
    sales_data = await check_binary_entry(sales_data, sales_data.Open, "Open")
    sales_data = await check_binary_entry(sales_data, sales_data.Promo, "Promo")
    sales_data = await check_binary_entry(sales_data, sales_data.Promo, "SchoolHoliday")
    sales_data = await check_date_period(sales_data)
    sales_data = await check_stateholidays(sales_data)

    return sales_data


async def check_stateholidays(sales_data: SalesData) -> SalesData:
    """Validate if the StateHolidays entry has correct inputs.

    Checks if the StateHoliday entry has values of 0, a, b, c based on the specification.

    :param sales_data: JSON response input
    :type sales_data: SalesData
    :raises HTTPException: incorrect StateHoliday entry error
    :return: validated StateHolidays input
    :rtype: SalesData
    """
    if sales_data.StateHoliday not in list(STATE_HOLIDAYS.keys()):
        raise HTTPException(status_code=422, detail="incorrect StateHoliday entry")
    return sales_data


async def check_date_period(sales_data: SalesData) -> SalesData:
    """Validate if the Date entry is of valid format.

    Checks if the entry can be converted into date format.

    :param sales_data: JSON response input
    :type sales_data: SalesData
    :raises HTTPException: incorrect Date entry error
    :return: validated Date input
    :rtype: SalesData
    """
    try:
        pd.Period(sales_data.Date)
    except DateParseError:
        raise HTTPException(status_code=422, detail="incorrect Date entry")

    return sales_data


async def check_binary_entry(
    sales_data: SalesData, entry: Union[int, float], params: str
) -> SalesData:
    """Validate if the entry is binary. Either 1 or 0 only.

    :param sales_data: JSON response input
    :type sales_data: SalesData
    :param entry: binary categorical values
    :type entry: Union[int, float]
    :param params: binary categorical features
    :type params: str
    :raises HTTPException: entry must be binary error
    :return: validated binary input
    :rtype: SalesData
    """
    if entry not in range(2):
        raise HTTPException(status_code=422, detail=f"{params} entry must be binary")

    return sales_data


async def check_customer_entry(sales_data: SalesData) -> SalesData:
    """Check if the number of customer is not negative.

    :param sales_data: JSON response input
    :type sales_data: SalesData
    :raises HTTPException: Number of customers must be greater than or equal to 0
    :return: Validated Customer input
    :rtype: SalesData
    """
    if sales_data.Customers < 0:
        raise HTTPException(
            status_code=422,
            detail="Number of customers must be greater than or equal to 0",
        )

    return sales_data


async def check_week_day_entry(sales_data: SalesData) -> SalesData:
    """Checks if DayofWeek is between 1 to 7, corresponding to Sunday to Saturday.

    :param sales_data: JSON response input
    :type sales_data: SalesData
    :raises HTTPException: Number of days in a week should be between 1 to 7
    :return: Validated DayofWeek input
    :rtype: SalesData
    """
    if sales_data.DayOfWeek not in range(1, 8):
        raise HTTPException(
            status_code=422, detail="Number of days in a week should be between 1 to 7"
        )

    return sales_data


async def check_store_entry(sales_data: SalesData) -> SalesData:
    """Checks if the Store entry is within the store.csv information.

    :param sales_data: JSON response input
    :type sales_data: SalesData
    :raises HTTPException: Store Number is not on the list
    :return: Validated Store input
    :rtype: SalesData
    """
    df_store_info = pd.read_csv(
        BASE_DIR / "data" / "raw" / "store.csv", usecols=["Store"]
    ).drop_duplicates()
    store_list = df_store_info["Store"].to_list()
    if sales_data.Store not in store_list:
        raise HTTPException(
            status_code=422,
            detail=f"Store number must be from {store_list[0]} to {store_list[-1]}",
        )

    return sales_data
