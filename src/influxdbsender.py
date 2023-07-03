import asyncio
import influxdb_client, os, time
import configparser
import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from opcuaclient import get_values

config = configparser.ConfigParser()
config.read('config.ini')
url = config.get('influxDb', 'url')
token = config.get('influxDb', 'token')
org = config.get('influxDb', 'org')

async def main():
    # Set up InfluxDB client
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    bucket = "FDM_Printer"

    # Define the write api
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    while True:
        print("______________prepare values to send____________")
        values = await get_values()
        data = {}

        for i in range(6001, 6013):
            key = f"value{i}"
            data[key] = {
                "printer_id": "MK3S",
                "unit": "nounit",  # to do right
                "value": values[key],
            }
        for i in range(6015, 6033):
            key = f"value{i}"
            data[key] = {
                "printer_id": "MK3S",
                "unit": "nounit",  # to do right
                "value": values[key],
            }
        for i in range(6034, 6041):
            key = f"value{i}"
            data[key] = {
                "printer_id": "MK3S",
                "unit": "nounit",  # to do right
                "value": values[key],
            }
        for i in range(6042, 6049):
            key = f"value{i}"
            data[key] = {
                "printer_id": "MK3S",
                "unit": "nounit",  # to do right
                "value": values[key],
            }
        for i in range(6052, 6172):
            key = f"value{i}"
            data[key] = {
                "printer_id": "MK3S",
                "unit": "nounit",  # to do right
                "value": values[key],
            }

        for key in data:
            point = Point(key) \
                .tag("printer_id", data[key]["printer_id"]) \
                .field(data[key]["unit"], data[key]["value"])
            write_api.write(bucket=bucket, org=org, record=point)
            # time.sleep(1)      # needed??

        print("__________________values sent!__________________")
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
