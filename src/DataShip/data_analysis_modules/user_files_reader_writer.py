import pandas as pd
from typing import Optional
import os

# constant value for the default save path of the files in the server
DEFAULT_SAVE_PATH = "user_files/"


def read_file(file_path, file_type: str, relative: bool) -> Optional[pd.DataFrame]:
    """This function reads a file from the user or the server.

    Args:
        file_path (_type_): name of the file to read.
        file_type (str): extension of the file to read.
        relative (bool): if the file is in the server or in the user system.

    Returns:
        Optional[pd.DataFrame]: dataframe of the file.
    """

    if relative:
        file_path = DEFAULT_SAVE_PATH + file_path

    if file_type == "csv":
        return pd.read_csv(file_path)
    if file_type == "json":
        return pd.read_json(file_path)
    if file_type == "xlsx":
        return pd.read_excel(file_path)
    if file_type == "txt":
        return pd.read_csv(file_path, sep="\t")
    return None


def delete_file_from_server(file_path, file_type: str, relative: bool) -> None:
    """This function deletes a file from the server.

    Args:
        file_path (str): name of the file to delete.
        file_type (str): extension of the file to delete.
        relative (bool): if the file is in the server or in the user system.
    """

    if relative:
        file_path = DEFAULT_SAVE_PATH + file_path

    os.remove(file_path)


def save_file_in_server(
    file_path, file_type: str, file_name: str
) -> Optional[pd.DataFrame]:
    """This function saves a file in the server.

    Args:
        file_path (str): name of the file to save.
        file_type (str): extension of the file to save.
        file_name (str): name of the file to save.

    Returns:
        Optional[pd.DataFrame]: dataframe of the file.
    """

    df = read_file(file_path, file_type, False)

    if df is None:
        return None

    f_path = DEFAULT_SAVE_PATH + file_name + "." + file_type
    if file_type == "csv":
        df.to_csv(f_path, index=False)
    elif file_type == "json":
        df.to_json(f_path, orient="records")
    elif file_type == "xlsx":
        df.to_excel(f_path, index=False)
    elif file_type == "txt":
        df.to_csv(f_path, index=False, sep="\t")
    return df
