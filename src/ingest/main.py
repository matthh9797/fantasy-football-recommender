from pathlib import Path
from helpers.io import dict_from_yaml
from ingest.steps import download, dict_to_dataframe, upload


# Parameters
key_file = 'data-science-on-gcp-323609-5874d2e62a8d.json'
downloads_path = str(Path.home() / "Downloads")
key_path = f"{Path.home()}/Downloads/{key_file}"
bq_config = {
    "key_path": key_path
}
config = dict_from_yaml('ingest/config.yaml')


# Steps
bootstrip_dict = download(config['fantasy_football_api']['endpoint'])
# elements_df, element_types_df, teams_df = dict_to_dataframe(json, keys)
df_dict = dict_to_dataframe(bootstrip_dict, config['fantasy_football_api']['tables'])

bq_config = {
    "key_path": key_path
}

upload(bq_config, config['bigquery']['dest_dataset_id'], df_dict)