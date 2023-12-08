import pandas as pd


def read_registration_dynamic_by_country() -> pd.DataFrame:
    df_columns = {
        "country": "category",
        "date": str,
        "new_registration_count": float
    }

    df_registration_dynamic_by_country = pd.read_csv(
        "registration_dynamic_by_country.csv",
        usecols = df_columns.keys(),
        dtype = df_columns,
        sep = ",",
        parse_dates = [
            "date"
        ]
    )

    return df_registration_dynamic_by_country


def read_first_deposits_dynamic_by_country() -> pd.DataFrame:
    df_columns = {
        "country": "category",
        "date": str,
        "first_deposit_count": float
    }

    df_first_deposits_dynamic_by_country = pd.read_csv(
        "first_deposits_dynamic_by_country.csv",
        usecols = df_columns.keys(),
        dtype = df_columns,
        sep = ",",
        parse_dates = [
            "date"
        ]
    )

    return df_first_deposits_dynamic_by_country


def read_conversion_from_regist_to_deposit() -> pd.DataFrame:
    df_columns = {
        "country": "category",
        "date": str,
        "new_customers_count": float,
        "new_customers_with_deposit_count": float,
        "conversion, %": float
    }

    df_conversion_from_regist_to_deposit = pd.read_csv(
        "conversion_from_regist_to_deposit.csv",
        usecols = df_columns.keys(),
        dtype = df_columns,
        sep = ",",
        parse_dates = [
            "date"
        ]
    )

    return df_conversion_from_regist_to_deposit