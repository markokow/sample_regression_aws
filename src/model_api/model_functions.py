import pandas as pd
import numpy as np
from typing import Dict, Union, List

from .model_utils import load_model
from .constants import BASE_DIR


def classify_match(
    match_dict: Dict, sales_data: str, df_request: pd.Series
) -> pd.Series:
    """Match the input sales data to the corresponding dictionary key values to perform one hot encoding.

    The categorical parameter is set to 1 based in sales input data. the rest of the input dictionary key is zero.

    :param match_dict: Dictionary containing sales data key and corresponding feature values
    :type match_dict: Dict
    :param sales_data: actual input sales data based on corresponding dictionary inputs
    :type sales_data: str
    :param df_request: model input dataframe
    :type df_request: pd.Series
    :return: reshaped model input dataframe
    :rtype: pd.Series
    """
    value_match = match_dict[sales_data]
    df_request[match_dict.values()] = 0
    df_request[value_match] = 1

    return df_request


def compute_duration(
    current_date: pd.Series, start_date: pd.Series, freq: str
) -> Union[float, int]:
    """Calculate the number of months/weeks between the current date based on sales data and the start date of the event (e.g Opening of competition, Promo2 opening)

    :param current_date: current date based on sales data. either Month Year or Week Year
    :type current_date: pd.Series
    :param start_date: Actual start date of specific event
    :type start_date: pd.Series
    :param freq: period frequency. Either in months or weeks
    :type freq: str
    :return: reshaped model input dataframe
    :rtype: Union[float, int]
    """
    if freq == "M":
        divisor = 12
    elif freq == "W":
        divisor = 52
    else:
        divisor = 1

    current_date = current_date.values
    start_date = start_date.values

    if np.all(start_date == 0):
        duration = 0
    else:
        duration = (current_date[0] - start_date[0]) / divisor + (
            current_date[1] - start_date[1]
        )

    return np.maximum(duration, 0) * divisor


def scale_inputs(
    df_to_scale: pd.Series, feature_list: List, scaler_type: str
) -> pd.Series:
    """Perform feature scaling, either MinMax or StandardScaler, based on the fitted train dataset.

    :param df_to_scale: feature values to be scaled based on model input
    :type df_to_scale: pd.Series
    :param feature_list: list of features to be scaled
    :type feature_list: List
    :param scaler_type: scaling type, either standardscaling or minmax
    :type scaler_type: str
    :return: scaled model input dataframe.
    :rtype: pd.Series
    """
    scaled_df = df_to_scale.copy()
    if scaler_type == "minmax":
        scaler = load_model(BASE_DIR / "models" / "transform_minmax.pkl")
    else:
        scaler = load_model(BASE_DIR / "models" / "transform_std.pkl")

    to_scale = df_to_scale[feature_list].to_frame().T
    scaled_df.loc[feature_list] = scaler.transform(to_scale)[0]

    return scaled_df
