import pandas as pd
import numpy as np
from .constants import (
    BASE_DIR,
    ASSORT_TYPE,
    PROMO_INTERVAL_LIST,
    STORE_TYPE,
    PROMO_TWO_WEEKYEAR,
    COMPET_OPEN_MONTHYEAR,
    ORDINAL_FEATURES,
    NUMERICAL_FEATURES,
)

from .model_functions import classify_match, compute_duration, scale_inputs

from .model_utils import load_model


def reshape_inputs_pipeline(df_request: pd.Series) -> pd.Series:
    """Reshapes and transforms the sales data input into necessary model features.

    :param df_request: sales data input
    :type df_request: pd.Series
    :return: reshaped model inputs
    :rtype: pd.Series
    """
    df_store_info = pd.read_csv(BASE_DIR / "data" / "raw" / "store.csv")
    df_store_info = df_store_info.drop_duplicates()

    store_mask = df_store_info["Store"] == df_request["Store"]
    store_vals = df_store_info[store_mask].squeeze()

    df_request["CompetitionDistance"] = store_vals["CompetitionDistance"]

    df_request["Promo2"] = store_vals["Promo2"]

    df_request[PROMO_INTERVAL_LIST] = 0

    if store_vals["PromoInterval"] != store_vals["PromoInterval"]:
        df_request["No_Promo"] = 1
    else:
        df_request[store_vals["PromoInterval"]] = 1

    df_request["Date"] = pd.Period(df_request["Date"])
    df_request["Year"] = df_request["Date"].year
    df_request["Month"] = df_request["Date"].month
    df_request["Week"] = df_request["Date"].week
    df_request = df_request.drop("Date")

    week_str = ["Week", "Year"]
    df_request["Promo2SinceDuration"] = compute_duration(
        current_date=df_request[week_str],
        start_date=store_vals[PROMO_TWO_WEEKYEAR].fillna(0.0),
        freq="W",
    )

    month_str = ["Month", "Year"]
    df_request["CompetitionOpenSinceDuration"] = compute_duration(
        current_date=df_request[month_str],
        start_date=store_vals[COMPET_OPEN_MONTHYEAR].fillna(0.0),
        freq="M",
    )

    df_request = classify_match(
        match_dict=ASSORT_TYPE,
        sales_data=store_vals["Assortment"],
        df_request=df_request,
    )
    df_request = classify_match(
        match_dict=STORE_TYPE, sales_data=store_vals["StoreType"], df_request=df_request
    )

    return df_request


def model_prediction_pipeline(reshaped_inputs: pd.Series) -> float:
    """Predict the sales based on the model inputs and trained model.

    :param reshaped_inputs: reshaped model inputs
    :type reshaped_inputs: pd.Series
    :return: predicted sales
    :rtype: float
    """
    scaled_data = scale_inputs(
        df_to_scale=reshaped_inputs, feature_list=ORDINAL_FEATURES, scaler_type="minmax"
    )
    scaled_data = scale_inputs(
        df_to_scale=scaled_data, feature_list=NUMERICAL_FEATURES, scaler_type="standard"
    )

    tuned_model = load_model(BASE_DIR / "models" / "tuned_model.pkl")
    sales = tuned_model.predict(scaled_data.to_frame().T)

    return np.round(sales, 2)
