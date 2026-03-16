import pandas as pd


def read_data(data_path_25: str, file_name: str):
    try:
        return pd.read_csv(f'{data_path_25}{file_name}')
    except FileNotFoundError:
        print("Error: No se encontro el archivo.")
        return None
    