from pathlib import Path

STATE_HOLIDAYS = {
    "0": "no_holiday",
    "a": "public_holiday",
    "b": "easter_holiday",
    "c": "christmas",
}
STORE_TYPE = {
    "a": "store_type_a",
    "b": "store_type_b",
    "c": "store_type_c",
    "d": "store_type_d",
}
ASSORT_TYPE = {"a": "basic", "b": "extra", "c": "extended"}

PROMO_INTERVAL_LIST = [
    "No_Promo",
    "Jan,Apr,Jul,Oct",
    "Feb,May,Aug,Nov",
    "Mar,Jun,Sept,Dec",
]

ORDINAL_FEATURES = ["Store", "Year", "Week", "Month", "DayOfWeek"]
NUMERICAL_FEATURES = [
    "Customers",
    "CompetitionDistance",
    "CompetitionOpenSinceDuration",
    "Promo2SinceDuration",
]

PROMO_TWO_WEEKYEAR = ["Promo2SinceWeek", "Promo2SinceYear"]
COMPET_OPEN_MONTHYEAR = ["CompetitionOpenSinceMonth", "CompetitionOpenSinceYear"]

BASE_DIR = Path(__file__).resolve(strict=True).parents[2]
