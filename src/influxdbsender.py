import asyncio
import influxdb_client
import configparser
import logging
import time

from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from opcuaclient import get_values

config = configparser.ConfigParser()
config.read('config.ini')

url = config.get('influxDb', 'url')
token = config.get('influxDb', 'token')
org = config.get('influxDb', 'org')
bucket = config.get('influxDb', 'bucketName')
printer_id = config.get('Printer', 'id')

MAX_RETRIES = 5
RANGES = [
    range(6001, 6013),
    range(6015, 6033),
    range(6034, 6041),
    range(6042, 6049),
    range(6052, 6172),
]

# Dictionary to store the last sent value for each key
last_sent_values = {}
# Time when the last data was sent
last_sent_time = None

async def fetch_values():
    for attempt in range(MAX_RETRIES):
        try:
            return await get_values()
        except asyncio.exceptions.TimeoutError:
            print(f"Connection attempt {attempt + 1} failed. Retrying...")
            await asyncio.sleep(2)
    else:
        logging.error(f"Could not establish connection after {MAX_RETRIES} attempts.")
        return None

def prepare_data_dict(values):
    data = {}
    for r in RANGES:
        for i in r:
            key = f"value{i}"
            data[key] = {
                "printer_id": printer_id,
                "unit": "nounit",  # to do right
                "value": values.get(key),
            }

    return data

async def main():
    global last_sent_values, last_sent_time

    # Set up InfluxDB client
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    # Define the write api
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    while True:
        print("______________prepare values to send____________")

        values = await fetch_values()
        if values is None:  # if the connection could not be established, try again
            continue

        data = prepare_data_dict(values)

        # Get current time
        current_time = time.time()

        # Create a variable to store the points to send
        points_to_send = []

        for key, value in data.items():
            # Check if data has changed or 3 minutes have passed
            if last_sent_values.get(key) != value or last_sent_time is None or current_time - last_sent_time >= 180:
                points_to_send.append(Point(key).tag("printer_id", value["printer_id"]).field(value["unit"], value["value"]))
                # Update the last sent value for the key
                last_sent_values[key] = value

        if points_to_send:
            write_api.write(bucket=bucket, org=org, record=points_to_send)
            print("__________________values sent!__________________")

            # Update the last sent time
            last_sent_time = current_time

        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
