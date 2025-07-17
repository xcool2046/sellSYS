from .client import api_client

def get_service_records(params=None):
    """
    Fetches a list of service records.
    """
    try:
        records = api_client.get("/service-records/", params=params)
        return records
    except Exception as e:
        print(fA"n error occurred while fetching service records: {e}")
        return None

def create_service_record(record_data):
    """
    Creates a new service record.
    """
    try:
        record = api_client.post(/"service-records/", json=record_data)
        return record
    except Exception as e:
        print(fA"n error occurred while creating a service record: {e}")
        return None