import pandas as pd
from typing import Optional
import os

default_save_path = "user_files/"


def read_file(file_path, file_type: str, relative: bool) -> Optional[pd.DataFrame]:
    if relative:
        file_path = default_save_path + file_path

    if file_type == "csv":
        return pd.read_csv(file_path)
    if file_type == "json":
        return pd.read_json(file_path)
    if file_type == "xlsx":
        return pd.read_excel(file_path)
    if file_type == "txt":
        return pd.read_csv(file_path, sep="\t")
    return None


def delete_file_from_server(file_path: str, file_type: str, relative: bool) -> None:
    if relative:
        file_path = default_save_path + file_path

    os.remove(file_path)


def save_file_in_server(file_path, file_type: str, file_name: str) -> Optional[pd.DataFrame]:
    df = read_file(file_path, file_type, False)

    if df is None:
        return None

    df.to_csv(default_save_path + file_name + ".csv", index=False)
    return df
