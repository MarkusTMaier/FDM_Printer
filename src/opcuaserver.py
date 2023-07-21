
# Imports
import os
import asyncio
import logging
import time
import random
import configparser
import struct
from datetime import datetime
from asyncua import Server, ua
from asyncua.common.ua_utils import value_to_datavalue
from octoprintbroker import get_values
from opcua.ua import NodeId
from typing import List

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

build_date = datetime(2023, 4, 2, 10, 00)
time_value = None


async def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    database_uri = config.get('opcUa', 'uri')
    database_serialNumber = config.get('opcUa', 'serialNumber')
    database_manufacturer = config.get('opcUa', 'manufacturer')
    database_umatiServerName = config.get('opcUa', 'umatiServerName')
    database_serverUrl = config.get('opcUa', 'url')

    time_value = time.time()
    print("Start setup...")
    # Serversetup
    server = Server()
    server.name = database_umatiServerName
    await server.init()
    await server.set_build_info(
        product_uri=database_uri,
        product_name=database_umatiServerName,
        manufacturer_name=database_manufacturer,
        software_version="alpha",
        build_number=database_serialNumber,
        build_date=build_date,
    )

    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
    ])
    server.set_security_IDs([
        "Anonymous",
    ])
    server.set_endpoint(database_serverUrl)

    print(f"Setup done! {time.time() - time_value}s")

    ##################################################################################################################

    async def import_xml_file(server, base_dir: str, filename: str, namespace_url: str):
        try:
            await server.import_xml(os.path.join(base_dir, "nodeset", filename))
        except Exception as e:
            print(e)
        return await server.get_namespace_index(namespace_url)

    xml_files_and_namespaces = [
        ("Opc.Ua.Di.NodeSet2.xml", "http://opcfoundation.org/UA/DI/"),
        ("Opc.Ua.Machinery.NodeSet2.xml", "http://opcfoundation.org/UA/Machinery/"),
        ("Opc.Ua.SurfaceTechnology.NodeSet2.xml", "http://opcfoundation.org/UA/SurfaceTechnology/"),
        ("Opc.Ua.Ijt.Tightening.NodeSet2.xml", "http://opcfoundation.org/UA/IJT/"),
        ("Opc.Ua.Robotics.NodeSet2.xml", "http://opcfoundation.org/UA/Robotics/"),
        ("Opc.Ua.IA.NodeSet2.xml", "http://opcfoundation.org/UA/IA/"),
        ("Opc.Ua.MachineTool.Nodeset2.xml", "http://opcfoundation.org/UA/MachineTool/"),
    ]

    indices = []

    time_value = time.time()
    print("Importing companion spec. XML...")

    for file, namespace in xml_files_and_namespaces:
        index = await import_xml_file(server, BASE_DIR, file, namespace)
        indices.append(index)

    di_idx, ma_idx, st_idx, ijt_idx, rob_idx, ia_idx, mt_idx = indices

    ##################################################################################################################
    print(f"Import done! {time.time() - time_value}s")

    time_value = time.time()
    print("Importing models...")

    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "newdigitaltwin.xml"))
    except Exception as e:
        print(e)

    print(f"Import done! {time.time() - time_value}s")

    ##################################################################################################################

    time_value = time.time()
    print("Create TypeDefinitions from XML...")
    # Load TypeDefinitions    
    await server.load_data_type_definitions()
    print(f"TypeDefinitions created!  {time.time() - time_value}s")

    print("Starting Server...")
    async with server:
        print(f"Server is now running!")

        # calling function that updates nodes in a parallel task
        await variableupdater(server)


async def variableupdater(server):
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Retrieve namespace index
    database_uri = config.get('opcUa', 'uri')
    nsindex = await server.get_namespace_index(database_uri)
    # prepare a list of variables to be updated
    node_ids = [
        6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008, 6009, 6010, 6011, 6012,
        6015, 6016, 6017, 6018, 6019, 6020, 6021, 6022, 6023, 6024, 6025, 6026,
        6027, 6028, 6029, 6030, 6031, 6032, 6034, 6035, 6036, 6037, 6038, 6039,
        6040, 6042, 6043, 6044, 6045, 6046, 6047, 6048, 6052, 6053, 6054, 6055,
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

    nodesToUpdate = []
    for i in node_ids:
        node = server.get_node(f"ns={nsindex};i={i}")
        nodesToUpdate.append(node)

    # Loop forever and update the values of the nodes every 2 seconds
    while True:
        values = get_values()
        # Update the value of the manufacturer node
        node_values = {
            6001: (
            ua.LocalizedText(Text=config.get('opcUa', 'manufacturer'), Locale="en"), ua.VariantType.LocalizedText),
            6002: (config.get('opcUa', 'uri'), ua.VariantType.String),
            6003: (config.get('opcUa', 'serialNumber'), ua.VariantType.String),
            6004: (int(config.get('hardcoded', 'operationMode')), ua.VariantType.UInt16),
            6005: (str(values['jobFileName']), ua.VariantType.String),
            6006: (values['numberInList'], ua.VariantType.UInt16),
            6007: (ua.LocalizedText(Text=values['currentStateProduction'], Locale="en"), ua.VariantType.LocalizedText),
            6011: (ua.LocalizedText(Text=str(values['currentStateMonitoring']), Locale="en"), ua.VariantType.LocalizedText),
            6015: (str(values['fileName1']), ua.VariantType.String),
            6016: (str(values['fileType1']), ua.VariantType.String),
            6017: (str(values['fileName9']), ua.VariantType.String),
            6018: (str(values['fileType9']), ua.VariantType.String),
            6019: (str(values['fileName2']), ua.VariantType.String),
            6020: (str(values['fileType2']), ua.VariantType.String),
            6021: (values['progressPrintTime'], ua.VariantType.Double),
            6022: (values['temperatureAActual'],ua.VariantType.Double),
            6023: (str(values['fileName0']), ua.VariantType.String),
            6024: (str(values['fileType0']), ua.VariantType.String),
            6025: (values['jobEstimatedPrintTime'], ua.VariantType.Double),
            6026: (str(values['spoolName7']), ua.VariantType.String),
            6027: (str(values['fileName3']), ua.VariantType.String),
            6028: (str(values['fileType3']), ua.VariantType.String),
            6029: (values['progressPrintTimeLeft'], ua.VariantType.Double),
            6030: (values['jobFilamentLength'], ua.VariantType.Double),
            6031: (str(values['fileName4']), ua.VariantType.String),
            6032: (str(values['fileType4']), ua.VariantType.String),
            6034: (values['currentToolTemperatureActual'], ua.VariantType.Double),
            6035: (str(values['fileName5']), ua.VariantType.String),
            6036: (str(values['fileType5']), ua.VariantType.String),
            6037: (values['jobFilamentVolume'], ua.VariantType.Double),
            6038: (str(values['stateError']), ua.VariantType.String),
            6039: (str(values['fileName6']), ua.VariantType.String),
            6040: (str(values['fileType6']), ua.VariantType.String),
            6042: (values['progressCompletion'], ua.VariantType.Double),
            6043: (str(values['fileName7']), ua.VariantType.String),
            6044: (str(values['fileType7']), ua.VariantType.String),
            6045: (str(values['spoolName8']), ua.VariantType.String),
            6046: (values['currentBedTemperatureActual'], ua.VariantType.Double),
            6047: (str(values['fileName8']), ua.VariantType.String),
            6048: (str(values['fileType8']), ua.VariantType.String),
            6052: (values['temperatureATarget'], ua.VariantType.Double),
            6053: (str(values['spoolName9']), ua.VariantType.String),
            6054: (values['spoolCost1'], ua.VariantType.Double),
            6055: (values['currentBedTemperatureTarget'], ua.VariantType.Double),
            6056: (values['spoolProfileDensity1'], ua.VariantType.Double),
            6057: (values['spoolProfileDiameter1'], ua.VariantType.Double),
            6058: (values['currentToolTemperatureTarget'], ua.VariantType.Double),
            6059: (str(values['spoolProfileMaterial1']), ua.VariantType.String),
            6060: (values['spoolTempOffset1'], ua.VariantType.Double),
            6061: (values['temperatureAOffset'], ua.VariantType.Double),
            6062: (values['spoolUsed1'] , ua.VariantType.Double),
            6063: (str(values['spoolProfileVendor1']), ua.VariantType.String),
            6064: (values['currentBedTemperatureOffset'], ua.VariantType.Double),
            6065: (values['spoolWeight1'], ua.VariantType.Double),
            6066: (values['spoolCost2'], ua.VariantType.Double),
            6067: (values['currentToolTemperatureOffset'], ua.VariantType.Double),
            6068: (values['printerProfileAxeESpeed'], ua.VariantType.Double),
            6069: (values['printerProfileAxeXSpeed'], ua.VariantType.Double),
            6070: (values['printerProfileAxeYSpeed'], ua.VariantType.Double),
            6071: (values['printerProfileAxeZSpeed'], ua.VariantType.Double),
            6072: (values['spoolProfileDensity2'], ua.VariantType.Double),
            6073: (values['spoolProfileDiameter2'], ua.VariantType.Double),
            6074: (values['printerProfileExtruderDefaultExtrusionLength'], ua.VariantType.Double),
            6075: (str(values['spoolProfileMaterial2']), ua.VariantType.String),
            6076: (values['spoolTempOffset2'], ua.VariantType.Double),
            6077: (values['printerProfileExtruderNozzleDiameter'], ua.VariantType.Double),
            6078: (values['spoolUsed2'], ua.VariantType.Double),
            6079: (str(values['spoolProfileVendor2']), ua.VariantType.String),
            6080: (values['printerProfileExtruderOffsetX'], ua.VariantType.Double),
            6081: (values['spoolWeight2'], ua.VariantType.Double),
            6082: (values['spoolCost3'], ua.VariantType.Double),
            6083: (values['printerProfileExtruderOffsetY'], ua.VariantType.Double),
            6084: (values['printerProfileVolumeCustom_boxX_min'], ua.VariantType.Double),
            6085: (values['printerProfileVolumeCustom_boxX_max'], ua.VariantType.Double),
            6086: (values['printerProfileVolumeCustom_boxY_max'], ua.VariantType.Double),
            6087: (values['printerProfileVolumeCustom_boxY_min'], ua.VariantType.Double),
            6088: (values['printerProfileVolumeCustom_boxZ_max'], ua.VariantType.Double),
            6089: (values['printerProfileVolumeCustom_boxZ_min'], ua.VariantType.Double),
            6090: (values['printerProfileVolumeWidth'], ua.VariantType.Double),
            6091: (values['printerProfileVolumeDepth'], ua.VariantType.Double),
            6092: (values['printerProfileVolumeHeight'], ua.VariantType.Double),
            6093: (values['spoolProfileDensity3'], ua.VariantType.Double),
            6094: (values['spoolProfileDiameter3'], ua.VariantType.Double),
            6095: (str(values['selectedSpoolName']), ua.VariantType.String),
            6096: (values['selectedSpoolCost'], ua.VariantType.Double),
            6097: (values['selectedSpoolProfileDensity'], ua.VariantType.Double),
            6098: (values['selectedSpoolProfileDiameter'], ua.VariantType.Double),
            6099: (str(values['selectedSpoolProfileMaterial']), ua.VariantType.String),
            6100: (str(values['selectedSpoolProfileVendor']), ua.VariantType.String),
            6101: (values['selectedSpoolTempOffset'], ua.VariantType.Double),
            6102: (values['selectedSpoolUsed'], ua.VariantType.Double),
            6103: (values['selectedSpoolWeight'], ua.VariantType.Double),
            6104: (str(values['spoolProfileMaterial3']), ua.VariantType.String),
            6105: (values['spoolTempOffset3'], ua.VariantType.Double),
            6106: (str(values['spoolName0']), ua.VariantType.String),
            6107: (values['spoolCost0'], ua.VariantType.Double),
            6108: (values['spoolProfileDensity0'], ua.VariantType.Double),
            6109: (values['spoolProfileDiameter0'], ua.VariantType.Double),
            6110: (str(values['spoolProfileMaterial0']), ua.VariantType.String),
            6111: (values['spoolTempOffset0'], ua.VariantType.Double),
            6112: (values['spoolUsed0'], ua.VariantType.Double),
            6113: (str(values['spoolProfileVendor0']), ua.VariantType.String),
            6114: (values['spoolWeight0'], ua.VariantType.Double),
            6115: (values['spoolUsed3'], ua.VariantType.Double),
            6116: (str(values['spoolProfileVendor3']), ua.VariantType.String),
            6117: (str(values['spoolName1']), ua.VariantType.String),
            6118: (values['spoolWeight3'], ua.VariantType.Double),
            6119: (values['spoolCost4'], ua.VariantType.Double),
            6120: (str(values['spoolName2']), ua.VariantType.String),
            6121: (values['spoolProfileDensity4'], ua.VariantType.Double),
            6122: (values['spoolProfileDiameter4'], ua.VariantType.Double),
            6123: (str(values['spoolName3']), ua.VariantType.String),
            6124: (str(values['spoolProfileMaterial4']), ua.VariantType.String),
            6125: (values['spoolTempOffset4'], ua.VariantType.Double),
            6126: (str(values['spoolName4']), ua.VariantType.String),
            6127: (values['spoolUsed4'] , ua.VariantType.Double),
            6128: (str(values['spoolProfileVendor4']), ua.VariantType.String),
            6129: (str(values['spoolName5']), ua.VariantType.String),
            6130: (values['spoolWeight4'] , ua.VariantType.Double),
            6131: (values['spoolCost5'] , ua.VariantType.Double),
            6132: (str(values['spoolName6']), ua.VariantType.String),
            6133: (values['spoolProfileDensity5'], ua.VariantType.Double),
            6134: (values['spoolProfileDiameter5'], ua.VariantType.Double),
            6135: (str(values['spoolProfileMaterial5']), ua.VariantType.String),
            6136: (values['spoolTempOffset5'], ua.VariantType.Double),
            6137: (values['spoolUsed5'], ua.VariantType.Double),
            6138: (str(values['spoolProfileVendor5']), ua.VariantType.String),
            6139: (values['spoolWeight5'], ua.VariantType.Double),
            6140: (values['spoolCost6'], ua.VariantType.Double),
            6141: (values['spoolProfileDensity6'], ua.VariantType.Double),
            6142: (values['spoolProfileDiameter6'], ua.VariantType.Double),
            6143: (str(values['spoolProfileMaterial6']), ua.VariantType.String),
            6144: (values['spoolTempOffset6'], ua.VariantType.Double),
            6145: (values['spoolCost7'] , ua.VariantType.Double),
            6146: (values['spoolProfileDensity7'], ua.VariantType.Double),
            6147: (values['spoolProfileDiameter7'], ua.VariantType.Double),
            6148: (str(values['spoolProfileMaterial7']), ua.VariantType.String),
            6149: (values['spoolTempOffset7'], ua.VariantType.Double),
            6150: (values['spoolCost8'], ua.VariantType.Double),
            6151: (values['spoolProfileDensity8'], ua.VariantType.Double),
            6152: (values['spoolProfileDiameter8'], ua.VariantType.Double),
            6153: (str(values['spoolProfileMaterial8']), ua.VariantType.String),
            6154: (values['spoolTempOffset8'], ua.VariantType.Double),
            6155: (values['spoolCost9'], ua.VariantType.Double),
            6156: (values['spoolProfileDensity9'], ua.VariantType.Double),
            6157: (values['spoolProfileDiameter9'], ua.VariantType.Double),
            6158: (str(values['spoolProfileMaterial9']), ua.VariantType.String),
            6159: (values['spoolTempOffset9'], ua.VariantType.Double),
            6160: (values['spoolUsed6'], ua.VariantType.Double),
            6161: (str(values['spoolProfileVendor6']), ua.VariantType.String),
            6162: (values['spoolWeight6'], ua.VariantType.Double),
            6163: (values['spoolUsed7'], ua.VariantType.Double),
            6164: (str(values['spoolProfileVendor7']), ua.VariantType.String),
            6165: (values['spoolWeight7'], ua.VariantType.Double),
            6166: (values['spoolUsed8'], ua.VariantType.Double),
            6167: (str(values['spoolProfileVendor8']), ua.VariantType.String),
            6168: (values['spoolWeight8'], ua.VariantType.Double),
            6169: (values['spoolUsed9'], ua.VariantType.Double),
            6170: (str(values['spoolProfileVendor9']), ua.VariantType.String),
            6171: (values['spoolWeight9'], ua.VariantType.Double)
        }

        for node in nodesToUpdate:
            if node.nodeid.Identifier in node_values:
                value, variant_type = node_values[node.nodeid.Identifier]
                if variant_type == ua.VariantType.Double:
                    if value is None:
                        value = 0.0
                    value = float(value)
                val = ua.Variant(Value=value, VariantType=variant_type)
                await node.write_value(val)
            else:
                print(f"Skipping link node {node.nodeid}")
        await asyncio.sleep(1)


# Start Server
if __name__ == "__main__":
    asyncio.run(main())
