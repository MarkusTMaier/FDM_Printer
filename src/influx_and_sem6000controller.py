import time
from sem6000_library import SEMSocket
import bluepy
import configparser
import asyncio
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


PW = "0000"
MYMAC = '6C:79:B8:60:5F:9D'  #MAC adress of the Voltcraft SEM6000 device, Raspberry Pi MAC: E4:5F:01:80:F2:2E
socket = None

bucket = "FDM_Printer"
url = "https://westeurope-1.azure.cloud2.influxdata.com"
org = "maier.markus@gmx.ch"
token = "g_qCFMT_wIN0Mw8KYhEwbzlXv7PhNITUNO0LO36vN5qY9qrjYZJjIgXXXGV-nyORIzPnlOG6DjfRhGW5D9i3iA=="

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    time.sleep(1)
    try:
        if socket == None:
            print("Connecting... ", end="")
            socket = SEMSocket(MYMAC)
            print("Success!")
            print("You're now connected to: {} (Icon: {})".format(socket.name, socket.icons[0]))
            if socket.login(PW) and socket.authenticated:
                print("Login successful!")
                socket.getSynConfig()
        socket.getStatus()
        wattage = socket.power

        p = influxdb_client.Point("value6172").tag("printer_id", "MK3S").field("Wattage", wattage)
        write_api.write(bucket=bucket, org=org, record=p)

    except (SEMSocket.NotConnectedException, BrokenPipeError):
        print("Restarting...")
        if socket != None:
            socket.disconnect()
            socket = None
