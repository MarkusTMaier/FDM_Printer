import configparser
import asyncio
import time
from influxdb_client import InfluxDBClient

url = "https://westeurope-1.azure.cloud2.influxdata.com"
org = "maier.markus@gmx.ch"
token = "g_qCFMT_wIN0Mw8KYhEwbzlXv7PhNITUNO0LO36vN5qY9qrjYZJjIgXXXGV-nyORIzPnlOG6DjfRhGW5D9i3iA=="

client = InfluxDBClient(url=url, token=token, org=org)

bucket = "FDM_Printer"

current_time = time.time()

data = [
    {
        "measurement": "value6172",
        "tags": {"printer_id": "MK3S"},
        "time": (current_time),
        "fields": {
            "Wattage": 5.0
        }
    }
]

write_api = client.write_api(write_options=WriteOptions(bucket=bucket))
write_api.write(bucket=bucket, org=org, record=data)

client.close()
