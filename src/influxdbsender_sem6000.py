import configparser
import asyncio
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from sem6000_controller import socket


bucket = "FDM_Printer"
url = "https://westeurope-1.azure.cloud2.influxdata.com"
org = "maier.markus@gmx.ch"
token = "g_qCFMT_wIN0Mw8KYhEwbzlXv7PhNITUNO0LO36vN5qY9qrjYZJjIgXXXGV-nyORIzPnlOG6DjfRhGW5D9i3iA=="

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
current_time = time.time()

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("value6172").tag("printer_id", "MK3S").field("Wattage", socket.power)

write_api.write(bucket=bucket, org=org, record=p)