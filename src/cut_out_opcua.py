
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
        6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008, 6009, 6010, 6011, 6012, 6013, 6014,
        6015, 6016, 6017, 6018, 6019, 6020, 6021, 6022, 6023, 6024, 6025, 6026,
        6027, 6028, 6029, 6030, 6031, 6032, 6033, 6034, 6035, 6036, 6037, 6038, 6039,
        6040, 6041, 6042, 6043, 6044, 6045, 6046, 6047, 6048, 6049, 6050, 6052, 6053, 6054, 6055,
        6056, 6057, 6058, 6059, 6060, 6061, 6062, 6063, 6064, 6065, 6066, 6067,
        6068, 6069, 6070, 6071, 6072, 6073, 6074, 6075, 6076, 6077, 6078, 6079,
        6080, 6081, 6082, 6083, 6084, 6085, 6086, 6087, 6088, 6089, 6090, 6091,
        6092, 6093, 6094, 6095, 6096, 6097, 6098, 6099, 6100, 6101, 6102, 6103,
        6104, 6105, 6106, 6107, 6108, 6109, 6110, 6111, 6112, 6113, 6114, 6115,
        6116, 6117, 6118, 6119, 6120, 6121, 6122, 6123, 6124, 6125, 6126, 6127,
        6128, 6129, 6130, 6131, 6132, 6133, 6134, 6135, 6136, 6137, 6138, 6139,
        6140, 6141, 6142, 6143, 6144, 6145, 6146, 6147, 6148, 6149, 6150, 6151,
        6152, 6153, 6154, 6155, 6156, 6157, 6158, 6159, 6160, 6161, 6162, 6163,
        6164, 6165, 6166, 6167, 6168, 6169, 6170, 6171
    ]

amount_of_node_ids = len(node_ids)

j = 0
i = 0
while j < 5:
    values = get_values()
    while i < amount_of_node_ids:
        current_id = node_ids[i]
        print(current_id)
        current_value = values[current_id]
        print(current_value)
        p = influxdb_client.Point(f"value{node_ids[i]}").tag("printer_id", "MK3S").field("Wattage", current_value)
        write_api.write(bucket=bucket, org=org, record=p)
        i = i + 1
    time.sleep(2)
    print(f"iteration {j+1} of 5 done")
    j = j + 1
    i = 0
    