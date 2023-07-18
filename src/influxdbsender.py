import asyncio
import influxdb_client
import configparser
import logging

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

async def fetch_values():
    for attempt in range(MAX_RETRIES):
        try:
            return await get_values()
        except asyncio.exceptions.TimeoutError:
            print(f"Connection attempt {attempt + 1} failed. Retrying...")
            await asyncio.sleep(2)
    else:
        logging.error(f"Could not establish connection after {MAX_RETRIES} attempts.")
        return None  # Or choose your error handling method here

def make_points(values):
    data = {}
    for r in RANGES:
        for i in r:
            key = f"value{i}"
            data[key] = {
                "printer_id": printer_id,
                "unit": "nounit",  # to do right
                "value": values.get(key),
            }

    return [Point(key).tag("printer_id", data[key]["printer_id"]).field(data[key]["unit"], data[key]["value"]) for key in data]

async def main():
    # Set up InfluxDB client
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    # Define the write api
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    while True:
        print("______________prepare values to send____________")

        values = await fetch_values()
        if values is None:  # if the connection could not be established, try again
            continue

        points = make_points(values)
        for point in points:
            write_api.write(bucket=bucket, org=org, record=point)

        print("__________________values sent!__________________")

if __name__ == "__main__":
    asyncio.run(main())
