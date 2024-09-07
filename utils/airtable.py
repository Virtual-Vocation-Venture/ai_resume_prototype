from pyairtable import Api
from requests import HTTPError


def initialize_airtable_client(
    api_key: str
) -> Api:
    """
    Creates an Airtable client given an API key.
    """
    try:
        return Api(api_key)
    except HTTPError as e:
        print(f"Encountered an error while initializing Airtable client.")
        print(f"Error: {e}")


def create_airtable_record(
    client: Api,
    table_id: str,
    data: dict,
    base_id: str
) -> None:
    """
    Adds a record to an Airtable table given a client and table id. If base_id is not provided, it will default to the environment variable.
    """
    try:
        table = client.table(base_id, table_id)
        result = table.create(data)
        
        if result:
            print(f"Created record in Airtable table {table_id}.")
        else: 
            raise ValueError("Failed to create record in Airtable table.")
    except HTTPError as e:
        print(f"Encountered an error while creating Airtable record.")
        print(f"Error: {e}")
    except ValueError as e:
        print(f"No record created in Airtable table.")
        print(f"Error: {e}")
