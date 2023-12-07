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