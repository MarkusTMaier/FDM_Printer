
#imports
import os
import time

import influxdb_client.client
import influxdb_client.client.exceptions
from octoprintbroker import get_values
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import librtd

#all of this is influxDB stuff
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

#defining node id's
node_ids = [
            6005, 6007, 6022, 6025, 6029, 6030, 6033, 6034, 6037, 6041, 6042, 6046,
            6050, 6052, 6095, 6096, 6097, 6098, 6099, 6100, 6101, 6102, 6103,
        ]

amount_of_node_ids = len(node_ids)

#Infinite loop to send data to InfluxDB, happens every 2 seconds
i = 0
while True:
    values = get_values()

    # Update the value of the manufacturer node
    node_values = {
        6005: (values['jobFileName']),                      #Current Print Job Name
        6007: (values['state']),  #Current State
        6022: (values['temperatureAActual']), #Ambient Temperature
        6025: (values['jobEstimatedPrintTime']),         #Estimated Print Time
        6029: (values['progressPrintTimeLeft']),
        6030: (values['jobFilamentLength']),             #Estimated Filament Length             
        6033: ('Additive manufacturing machine'),        #Device Class
        6034: (values['currentToolTemperatureActual']),  #Extruder Temperature
        6037: (values['jobFilamentVolume']),             #Estimated Filament Volume
        6041: ('EMO 9 F24/N 47.3895819 E 8.5134454'),    #Device Location
        6042: (values['progressCompletion']),
        6046: (values['currentBedTemperatureActual']),   #Bed Temperature

    }

    #write and send values to InfluxDB, print error if not possible and try again
    try:
        while i < amount_of_node_ids:
            current_id = node_ids[i]
            current_value = node_values[current_id]
            p = influxdb_client.Point(f"value{node_ids[i]}").tag("printer_id", "MK3S").field("Wattage", current_value)
            write_api.write(bucket=bucket, org=org, record=p)
            i = i + 1

        temperature = librtd.get(0,7)
        temperature = round(temperature, 2)
        p = influxdb_client.Point(f"value{6173}").tag("printer_id", "MK3S").field("°C", temperature)
        write_api.write(bucket=bucket, org=org, record=p)
    except influxdb_client.client.exceptions.InfluxDBError: 
        current_time = time.time()
        print(f"Couldn't write to InfluxDB at {current_time}, trying again")
    
    #sleep for 2 seconds, then repeat loop
    time.sleep(2)
    i = 0
    