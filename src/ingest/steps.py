from pathlib import Path
import pandas as pd
from google.cloud import bigquery

from apis.fantasy_premier_league import get_fantasy_api_data
from helpers.gcp import GcpConnector


def download(endpoint: str) -> dict:
    """
    Download data from fantasy.premierleague api
    @param endpoint prefix for the api
    @return json output of api call
    """
    print(f"Downloading data from fantasy.premierleague api on endpoint: {endpoint}")
    return get_fantasy_api_data(endpoint)


def dict_to_dataframe(json: dict, keys: list) -> pd.DataFrame:
    """ 
    Extract sections from json and convert to dataframe
    @param json json output of fantasy.premierleague api call
    @param keys list of keys to convert to dataframes
    @return dictionary of dataframes 
    """
    df_dict = {}
    for key in keys:
        df_dict[key] = pd.DataFrame(json[key])
    return df_dict


def upload(bq_config, dataset_id, df_dict):

    gcp_connector = GcpConnector(bq_config)

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    dataset_ref = gcp_connector.client.dataset(dataset_id)
    for dataframe_name, dataframe in df_dict.items():
        table_ref = dataset_ref.table(dataframe_name)
        gcp_connector.upload_dataframe_to_table(dataframe, table_ref, job_config)