
#imports
import os
import time
from octoprintbroker import get_values
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

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
            6049, 6050, 6052, 6095, 6096, 6097, 6098, 6099, 6100, 6101, 6102, 6103,
        ]

amount_of_node_ids = len(node_ids)

j = 0
i = 0
while j < 5:
    values = get_values()
    # Update the value of the manufacturer node
    node_values = {
        6005: (str(values['jobFileName'])),                      #Current Print Job Name
        6007: (ua.LocalizedText(Text=str(CurrentProductionState), Locale="en"), ua.VariantType.LocalizedText),  #Current State
        6022: (values['temperatureAActual'],ua.VariantType.Double), #Ambient Temperature
        6025: (values['jobEstimatedPrintTime'], ua.VariantType.Double),         #Estimated Print Time
        6029: (values['progressPrintTimeLeft'], ua.VariantType.Double),
        6030: (values['jobFilamentLength'], ua.VariantType.Double),             #Estimated Filament Length             
        6033: ('Additive manufacturing machine', ua.VariantType.String),        #Device Class
        6034: (values['currentToolTemperatureActual'], ua.VariantType.Double),  #Extruder Temperature
        6037: (values['jobFilamentVolume'], ua.VariantType.Double),             #Estimated Filament Volume
        6041: ('EMO 9 F24/N 47.3895819 E 8.5134454', ua.VariantType.String),    #Device Location
        6042: (values['progressCompletion'], ua.VariantType.Double),
        6046: (values['currentBedTemperatureActual'], ua.VariantType.Double),   #Bed Temperature
        6049: (ua.LocalizedText(Text='MK3S+', Locale="en"), ua.VariantType.LocalizedText),  #device Model
        6050: ('2022-1', ua.VariantType.String),                                            #Product Code
        6052: (values['temperatureATarget'], ua.VariantType.Double),
        6095: (str(values['selectedSpoolName']), ua.VariantType.String),                #Selected Spool Name
        6096: (values['selectedSpoolCost'], ua.VariantType.Double),                     #Selected Spool Cost
        6097: (values['selectedSpoolProfileDensity'], ua.VariantType.Double),           #Selected Spool Density
        6098: (values['selectedSpoolProfileDiameter'], ua.VariantType.Double),          #Selected Spool Diameter
        6099: (str(values['selectedSpoolProfileMaterial']), ua.VariantType.String),     #Selected Spool Material
        6100: (str(values['selectedSpoolProfileVendor']), ua.VariantType.String),       #Selected Spool Vendor
        6101: (values['selectedSpoolTempOffset'], ua.VariantType.Double),               #Selected Spool Temperature Offset
        6102: (values['selectedSpoolUsed'], ua.VariantType.Double),                     #Selected Spool Used
        6103: (values['selectedSpoolWeight'], ua.VariantType.Double),                   #Selected Spool Weight
    }


    while i < amount_of_node_ids:
        current_id = node_ids[i]
        print(current_id)
        current_value = node_values[current_id]
        print(current_value)
        p = influxdb_client.Point(f"value{node_ids[i]}").tag("printer_id", "MK3S").field("Wattage", current_value)
        write_api.write(bucket=bucket, org=org, record=p)
        i = i + 1
    time.sleep(2)
    print(f"iteration {j+1} of 5 done")
    j = j + 1
    i = 0
    
