from google.cloud import bigquery
import os
import json

data_name = "others"
table_name = "digitalocean"
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{BASE_DIR}/key.json"
client = bigquery.Client()


# Batch insert configuration
BATCH_SIZE = 1000  # Number of rows to insert per batch


def insert_rows_wit_convert(rows, datatable):
    print("Data insert to " + datatable)
    if not isinstance(rows, (list, tuple)) or not all(
        isinstance(row, dict) for row in rows
    ):
        raise TypeError("rows argument should be a sequence of dicts")

    table_id = f"profound-surge-368421.{datatable}.digitalocean"

    errors = client.insert_rows_json(table_id, rows)  # Make an API request
    if errors == []:
        print("New rows have been added")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def insert_rows_no_convert(rows, datatable):
    print("Panjang data: " + str(len(rows)))
    print("Data insert to " + datatable)
    if not isinstance(rows, (list, tuple)) or not all(
        isinstance(row, dict) for row in rows
    ):
        raise TypeError("rows argument should be a sequence of dicts")

    table_id = f"profound-surge-368421.{datatable}.digitalocean"
    errors = client.insert_rows_json(table_id, rows)  # Make an API request
    if errors == []:
        print("New rows have been added before conversion")
    else:
        print("Attempting to convert store_type to int and retrying...")

        # Convert store_type to int
        convert_store_type_to_int(rows)

        # Retry the insertion
        errors = client.insert_rows_json(table_id, rows)  # Make another API request
        if errors == []:
            print("New rows have been added after conversion")
        else:
            print("Encountered errors while inserting rows")


def convert_store_type_to_int(data):
    for item in data:
        store_type = item.get("store_type")
        # cange to int 0 or 1
        int1 = 1
        int0 = 0

        if item.get("store_type") == True:
            item["store_type"] = int1
        elif item.get("store_type") == False:
            item["store_type"] = int0

    return data


def batch_insert_rows(rows):
    errors = client.insert_rows_json(table_id, rows)  # Make an API request.
    if errors == []:
        print("New rows have been added")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    data = read_json_file("all_data_output.json")
    data = convert_store_type_to_int(data)

    # Split the data into smaller chunks
    chunks = [data[i : i + BATCH_SIZE] for i in range(0, len(data), BATCH_SIZE)]

    for chunk in chunks:
        batch_insert_rows(chunk)
# # perawatan kecantikan
# data_name   = 'beauty'
# table_name  = 'digitalocean'

# # Cesssa & quotidien salad
# data_name   = 'others'
# table_name  = 'digitalocean'
