# Copyright 2020-2021 (c) Andreas Heine, AFOTEK Anlagen für Oberflächentechnik GmbH
# Copyright 2021 (c) Fabian Beitler, konzeptpark GmbH
# Copyright 2021 (c) Moritz Walker, ISW University of Stuttagart (for umati and VDW e.V.)
# Copyright 2021 (c) Goetz Goerisch, VDW - Verein Deutscher Werkzeugmaschinenfabriken e.V.

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

    time_value = time.time()
    print("Importing companion spec. XML...")

    # Import Opc.Ua.Di.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Di.NodeSet2.xml"))
    except Exception as e:
        print(e)

    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")

    # Import Opc.Ua.Machinery.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Machinery.NodeSet2.xml"))
    except Exception as e:
        print(e)

    ma_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Machinery/")

    # Import Opc.Ua.SurfaceTechnology.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.SurfaceTechnology.NodeSet2.xml"))
    except Exception as e:
        print(e)

    st_idx = await server.get_namespace_index("http://opcfoundation.org/UA/SurfaceTechnology/")

    # Import Opc.Ua.Ijt.Tightening.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Ijt.Tightening.NodeSet2.xml"))
    except Exception as e:
        print(e)

    ijt_idx = await server.get_namespace_index("http://opcfoundation.org/UA/IJT/")

    # Import Opc.Ua.Robotics.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Robotics.NodeSet2.xml"))
    except Exception as e:
        print(e)

    rob_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Robotics/")

    # Import Opc.Ua.Ia.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.IA.NodeSet2.xml"))
    except Exception as e:
        print(e)

    ia_idx = await server.get_namespace_index("http://opcfoundation.org/UA/IA/")

    # Import Opc.Ua.MachineTool.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.MachineTool.Nodeset2.xml"))
    except Exception as e:
        print(e)

    mt_idx = await server.get_namespace_index("http://opcfoundation.org/UA/MachineTool/")

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
    nodesToUpdate = [
        server.get_node(f"ns={nsindex};i=6001"),
        server.get_node(f"ns={nsindex};i=6002"),
        server.get_node(f"ns={nsindex};i=6003"),
        server.get_node(f"ns={nsindex};i=6004"),
        server.get_node(f"ns={nsindex};i=6005"),
        server.get_node(f"ns={nsindex};i=6006"),
        server.get_node(f"ns={nsindex};i=6007"),
        server.get_node(f"ns={nsindex};i=6008"),
        server.get_node(f"ns={nsindex};i=6009"),
        server.get_node(f"ns={nsindex};i=6010"),
        server.get_node(f"ns={nsindex};i=6011"),
        server.get_node(f"ns={nsindex};i=6012"),

        server.get_node(f"ns={nsindex};i=6015"),
        server.get_node(f"ns={nsindex};i=6016"),
        server.get_node(f"ns={nsindex};i=6017"),
        server.get_node(f"ns={nsindex};i=6018"),
        server.get_node(f"ns={nsindex};i=6019"),
        server.get_node(f"ns={nsindex};i=6020"),
        server.get_node(f"ns={nsindex};i=6021"),
        server.get_node(f"ns={nsindex};i=6022"),
        server.get_node(f"ns={nsindex};i=6023"),
        server.get_node(f"ns={nsindex};i=6024"),
        server.get_node(f"ns={nsindex};i=6025"),
        server.get_node(f"ns={nsindex};i=6026"),
        server.get_node(f"ns={nsindex};i=6027"),
        server.get_node(f"ns={nsindex};i=6028"),
        server.get_node(f"ns={nsindex};i=6029"),
        server.get_node(f"ns={nsindex};i=6030"),
        server.get_node(f"ns={nsindex};i=6031"),
        server.get_node(f"ns={nsindex};i=6032"),

        server.get_node(f"ns={nsindex};i=6034"),
        server.get_node(f"ns={nsindex};i=6035"),
        server.get_node(f"ns={nsindex};i=6036"),
        server.get_node(f"ns={nsindex};i=6037"),
        server.get_node(f"ns={nsindex};i=6038"),
        server.get_node(f"ns={nsindex};i=6039"),
        server.get_node(f"ns={nsindex};i=6040"),

        server.get_node(f"ns={nsindex};i=6042"),
        server.get_node(f"ns={nsindex};i=6043"),
        server.get_node(f"ns={nsindex};i=6044"),
        server.get_node(f"ns={nsindex};i=6045"),
        server.get_node(f"ns={nsindex};i=6046"),
        server.get_node(f"ns={nsindex};i=6047"),
        server.get_node(f"ns={nsindex};i=6048"),

        server.get_node(f"ns={nsindex};i=6052"),
        server.get_node(f"ns={nsindex};i=6053"),
        server.get_node(f"ns={nsindex};i=6054"),
        server.get_node(f"ns={nsindex};i=6055"),
        server.get_node(f"ns={nsindex};i=6056"),
        server.get_node(f"ns={nsindex};i=6057"),
        server.get_node(f"ns={nsindex};i=6058"),
        server.get_node(f"ns={nsindex};i=6059"),
        server.get_node(f"ns={nsindex};i=6060"),
        server.get_node(f"ns={nsindex};i=6061"),
        server.get_node(f"ns={nsindex};i=6062"),
        server.get_node(f"ns={nsindex};i=6063"),
        server.get_node(f"ns={nsindex};i=6064"),
        server.get_node(f"ns={nsindex};i=6065"),
        server.get_node(f"ns={nsindex};i=6066"),
        server.get_node(f"ns={nsindex};i=6067"),
        server.get_node(f"ns={nsindex};i=6068"),
        server.get_node(f"ns={nsindex};i=6069"),
        server.get_node(f"ns={nsindex};i=6070"),
        server.get_node(f"ns={nsindex};i=6071"),
        server.get_node(f"ns={nsindex};i=6072"),
        server.get_node(f"ns={nsindex};i=6073"),
        server.get_node(f"ns={nsindex};i=6074"),
        server.get_node(f"ns={nsindex};i=6075"),
        server.get_node(f"ns={nsindex};i=6076"),
        server.get_node(f"ns={nsindex};i=6077"),
        server.get_node(f"ns={nsindex};i=6078"),
        server.get_node(f"ns={nsindex};i=6079"),
        server.get_node(f"ns={nsindex};i=6080"),
        server.get_node(f"ns={nsindex};i=6081"),
        server.get_node(f"ns={nsindex};i=6082"),
        server.get_node(f"ns={nsindex};i=6083"),
        server.get_node(f"ns={nsindex};i=6084"),
        server.get_node(f"ns={nsindex};i=6085"),
        server.get_node(f"ns={nsindex};i=6086"),
        server.get_node(f"ns={nsindex};i=6087"),
        server.get_node(f"ns={nsindex};i=6088"),
        server.get_node(f"ns={nsindex};i=6089"),
        server.get_node(f"ns={nsindex};i=6090"),
        server.get_node(f"ns={nsindex};i=6091"),
        server.get_node(f"ns={nsindex};i=6092"),
        server.get_node(f"ns={nsindex};i=6093"),
        server.get_node(f"ns={nsindex};i=6094"),
        server.get_node(f"ns={nsindex};i=6095"),
        server.get_node(f"ns={nsindex};i=6096"),
        server.get_node(f"ns={nsindex};i=6097"),
        server.get_node(f"ns={nsindex};i=6098"),
        server.get_node(f"ns={nsindex};i=6099"),
        server.get_node(f"ns={nsindex};i=6100"),
        server.get_node(f"ns={nsindex};i=6101"),
        server.get_node(f"ns={nsindex};i=6102"),
        server.get_node(f"ns={nsindex};i=6103"),
        server.get_node(f"ns={nsindex};i=6104"),
        server.get_node(f"ns={nsindex};i=6105"),
        server.get_node(f"ns={nsindex};i=6106"),
        server.get_node(f"ns={nsindex};i=6107"),
        server.get_node(f"ns={nsindex};i=6108"),
        server.get_node(f"ns={nsindex};i=6109"),
        server.get_node(f"ns={nsindex};i=6110"),
        server.get_node(f"ns={nsindex};i=6111"),
        server.get_node(f"ns={nsindex};i=6112"),
        server.get_node(f"ns={nsindex};i=6113"),
        server.get_node(f"ns={nsindex};i=6114"),
        server.get_node(f"ns={nsindex};i=6115"),
        server.get_node(f"ns={nsindex};i=6116"),
        server.get_node(f"ns={nsindex};i=6117"),
        server.get_node(f"ns={nsindex};i=6118"),
        server.get_node(f"ns={nsindex};i=6119"),
        server.get_node(f"ns={nsindex};i=6120"),
        server.get_node(f"ns={nsindex};i=6121"),
        server.get_node(f"ns={nsindex};i=6122"),
        server.get_node(f"ns={nsindex};i=6123"),
        server.get_node(f"ns={nsindex};i=6124"),
        server.get_node(f"ns={nsindex};i=6125"),
        server.get_node(f"ns={nsindex};i=6126"),
        server.get_node(f"ns={nsindex};i=6127"),
        server.get_node(f"ns={nsindex};i=6128"),
        server.get_node(f"ns={nsindex};i=6129"),
        server.get_node(f"ns={nsindex};i=6130"),
        server.get_node(f"ns={nsindex};i=6131"),
        server.get_node(f"ns={nsindex};i=6132"),
        server.get_node(f"ns={nsindex};i=6133"),
        server.get_node(f"ns={nsindex};i=6134"),
        server.get_node(f"ns={nsindex};i=6135"),
        server.get_node(f"ns={nsindex};i=6136"),
        server.get_node(f"ns={nsindex};i=6137"),
        server.get_node(f"ns={nsindex};i=6138"),
        server.get_node(f"ns={nsindex};i=6139"),
        server.get_node(f"ns={nsindex};i=6140"),
        server.get_node(f"ns={nsindex};i=6141"),
        server.get_node(f"ns={nsindex};i=6142"),
        server.get_node(f"ns={nsindex};i=6143"),
        server.get_node(f"ns={nsindex};i=6144"),
        server.get_node(f"ns={nsindex};i=6145"),
        server.get_node(f"ns={nsindex};i=6146"),
        server.get_node(f"ns={nsindex};i=6147"),
        server.get_node(f"ns={nsindex};i=6148"),
        server.get_node(f"ns={nsindex};i=6149"),
        server.get_node(f"ns={nsindex};i=6150"),
        server.get_node(f"ns={nsindex};i=6151"),
        server.get_node(f"ns={nsindex};i=6152"),
        server.get_node(f"ns={nsindex};i=6153"),
        server.get_node(f"ns={nsindex};i=6154"),
        server.get_node(f"ns={nsindex};i=6155"),
        server.get_node(f"ns={nsindex};i=6156"),
        server.get_node(f"ns={nsindex};i=6157"),
        server.get_node(f"ns={nsindex};i=6158"),
        server.get_node(f"ns={nsindex};i=6159"),
        server.get_node(f"ns={nsindex};i=6160"),
        server.get_node(f"ns={nsindex};i=6161"),
        server.get_node(f"ns={nsindex};i=6162"),
        server.get_node(f"ns={nsindex};i=6163"),
        server.get_node(f"ns={nsindex};i=6164"),
        server.get_node(f"ns={nsindex};i=6165"),
        server.get_node(f"ns={nsindex};i=6166"),
        server.get_node(f"ns={nsindex};i=6167"),
        server.get_node(f"ns={nsindex};i=6168"),
        server.get_node(f"ns={nsindex};i=6169"),
        server.get_node(f"ns={nsindex};i=6170"),
        server.get_node(f"ns={nsindex};i=6171"),
    ]

    # Loop forever and update the values of the nodes every 2 seconds
    while True:
        values = get_values()
        for node in nodesToUpdate:
            if node.nodeid.Identifier == 6001:
                # Update the value of the manufacturer node
                database_manufacturer = config.get('opcUa', 'manufacturer')
                val = ua.Variant(Value=ua.LocalizedText(Text=database_manufacturer, Locale="en"),
                                 VariantType=ua.VariantType.LocalizedText)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6002:
                # Update the value of the productInstanceUri node
                database_uri = config.get('opcUa', 'uri')
                val = ua.Variant(Value=database_uri, VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6003:
                # Update the value of the serialNumber node
                database_serialNumber = config.get('opcUa', 'serialNumber')
                val = ua.Variant(Value=database_serialNumber, VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6004:
                # Update the value of the operationMode node
                database_operationMode = int(config.get('hardcoded', 'operationMode'))
                val = ua.Variant(Value=database_operationMode, VariantType=ua.VariantType.UInt16)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6005:
                # Update the value of the Name node
                val = ua.Variant(Value=str(values['jobFileName']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6006:
                # Update the value of the NumberInList node
                val = ua.Variant(Value=values['numberInList'], VariantType=ua.VariantType.UInt16)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6007:
                # Update the value of the CurrentState Production node
                state = (values['currentStateProduction'])
                val = ua.Variant(Value=ua.LocalizedText(Text=state, Locale="en"),
                                 VariantType=ua.VariantType.LocalizedText)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6008:
                # Update the value of the Production currentState Id node //?
                pass
            elif node.nodeid.Identifier == 6009:
                # Update the value of the Number node
                pass
            elif node.nodeid.Identifier == 6010:
                # Update the value of the NodeVersion node // Optional!
                pass
            elif node.nodeid.Identifier == 6011:
                # Update the value of the currentState monitoring node
                currentState = str(values['currentStateMonitoring'])
                val = ua.Variant(Value=ua.LocalizedText(Text=currentState, Locale="en"),
                                 VariantType=ua.VariantType.LocalizedText)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6012:
                # Update the value of the Monitoring currentState Id node //?
                pass
            elif node.nodeid.Identifier == 6015:
                # Update the value of the fileName1 node
                val = ua.Variant(Value=str(values['fileName1']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6016:
                # Update the value of the fileType1 node
                val = ua.Variant(Value=str(values['fileType1']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6017:
                # Update the value of the fileName9 node
                val = ua.Variant(Value=str(values['fileName9']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6018:
                # Update the value of the fileType9 node
                val = ua.Variant(Value=str(values['fileType9']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6019:
                # Update the value of the fileName2 node
                val = ua.Variant(Value=str(values['fileName2']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6020:
                # Update the value of the fileType2 node
                val = ua.Variant(Value=str(values['fileType2']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6021:
                # Update the value of the progressPrintTime node
                value = float(values['progressPrintTime']) if values['progressPrintTime'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6022:
                # Update the value of the TemperatureAmbient node
                value = float(values['temperatureAActual']) if values['temperatureAActual'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6023:
                # Update the value of the fileName0 node
                val = ua.Variant(Value=str(values['fileName0']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6024:
                # Update the value of the fileType0 node
                val = ua.Variant(Value=str(values['fileType0']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6025:
                # Update the value of the jobEstimatedPrintTime node
                value = float(values['jobEstimatedPrintTime']) if values['jobEstimatedPrintTime'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6026:
                # Update the value of the Spool7 node
                val = ua.Variant(Value=str(values['spoolName7']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6027:
                # Update the value of the fileName3 node
                val = ua.Variant(Value=str(values['fileName3']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6028:
                # Update the value of the fileType3 node
                val = ua.Variant(Value=str(values['fileType3']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6029:
                # Update the value of the progressPrintTimeLeft node
                value = float(values['progressPrintTimeLeft']) if values['progressPrintTimeLeft'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6030:
                # Update the value of the jobFilamentLength node
                value = float(values['jobFilamentLength']) if values['jobFilamentLength'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6031:
                # Update the value of the fileName4 node
                val = ua.Variant(Value=str(values['fileName4']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6032:
                # Update the value of the fileType4 node
                val = ua.Variant(Value=str(values['fileType4']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6034:
                # Update the value of the currentToolTemperatureActual node
                value = float(values['currentToolTemperatureActual']) if values['currentToolTemperatureActual'] is not \
                                                                         None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6035:
                # Update the value of the fileName5 node
                val = ua.Variant(Value=str(values['fileName5']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6036:
                # Update the value of the fileType5 node
                val = ua.Variant(Value=str(values['fileType5']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6037:
                # Update the value of the jobFilamentVolume node
                value = float(values['jobFilamentVolume']) if values['jobFilamentVolume'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6038:
                # Update the value of the Error node
                val = ua.Variant(Value=str(values['stateError']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6039:
                # Update the value of the fileName6 node
                val = ua.Variant(Value=str(values['fileName6']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6040:
                # Update the value of the fileType6 node
                val = ua.Variant(Value=str(values['fileType6']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6042:
                # Update the value of the ProgressCompletion node
                value = float(values['progressCompletion']) if values['progressCompletion'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6043:
                # Update the value of the fileName7 node
                val = ua.Variant(Value=str(values['fileName7']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6044:
                # Update the value of the fileType7 node
                val = ua.Variant(Value=str(values['fileType7']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6045:
                # Update the value of the Spool8 node
                val = ua.Variant(Value=str(values['spoolName8']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6046:
                # Update the value of the currentBedTemperatureActual node
                value = float(values['currentBedTemperatureActual']) if values['currentBedTemperatureActual'] is \
                                                                        not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6047:
                # Update the value of the fileName8 node
                val = ua.Variant(Value=str(values['fileName8']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6048:
                # Update the value of the fileType8 node
                val = ua.Variant(Value=str(values['fileType8']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6052:
                # Update the value of the temperatureATarget node
                value = float(values['temperatureATarget']) if values['temperatureATarget'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6053:
                # Update the value of the Spool9 node
                val = ua.Variant(Value=str(values['spoolName9']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6054:
                # Update the value of the Spool1 Cost node
                value = float(values['spoolCost1']) if values['spoolCost1'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6055:
                # Update the value of the currentBedTemperatureTarget node
                value = float(values['currentBedTemperatureTarget']) if values['currentBedTemperatureTarget'] is \
                                                                        not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6056:
                # Update the value of the Spool1 Density node
                value = float(values['spoolProfileDensity1']) if values['spoolProfileDensity1'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6057:
                # Update the value of the Spool1 Diameter node
                value = float(values['spoolProfileDiameter1']) if values['spoolProfileDiameter1'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6058:
                # Update the value of the currentToolTemperatureTarget node
                value = float(values['currentToolTemperatureTarget']) if values['currentToolTemperatureTarget'] is\
                                                                         not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6059:
                # Update the value of the Spool1 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial1']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6060:
                # Update the value of the Spool1 Temperature Offset node
                value = float(values['spoolTempOffset1']) if values['spoolTempOffset1'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6061:
                # Update the value of the TemperatureAOffset node
                value = float(values['temperatureAOffset']) if values['temperatureAOffset'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6062:
                # Update the value of the Spool1 Used node
                value = float(values['spoolUsed1']) if values['spoolUsed1'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6063:
                # Update the value of the Spool1 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor1']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6064:
                # Update the value of the currentBedTemperatureOffset node
                value = float(values['currentBedTemperatureOffset']) if values['currentBedTemperatureOffset'] is \
                                                                        not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6065:
                # Update the value of the Spool1 Weight node
                value = float(values['spoolWeight1']) if values['spoolWeight1'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6066:
                # Update the value of the Spool2 Cost node
                value = float(values['spoolCost2']) if values['spoolCost2'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6067:
                # Update the value of the currentToolTemperatureOffset node
                value = float(values['currentToolTemperatureOffset']) if values['currentToolTemperatureOffset'] is \
                                                                         not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6068:
                # Update the value of the Extruder Speed node
                value = float(values['printerProfileAxeESpeed']) if values['printerProfileAxeESpeed'] is not \
                                                                    None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6069:
                # Update the value of the AxisX Speed node
                value = float(values['printerProfileAxeXSpeed']) if values['printerProfileAxeXSpeed'] is not \
                                                                    None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6070:
                # Update the value of the AxisY Speed node
                value = float(values['printerProfileAxeYSpeed']) if values['printerProfileAxeYSpeed'] is not\
                                                                    None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6071:
                # Update the value of the AxisZ Speed node
                value = float(values['printerProfileAxeZSpeed']) if values['printerProfileAxeZSpeed'] is not None \
                    else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6072:
                # Update the value of the Spool2 Density node
                value = float(values['spoolProfileDensity2']) if values['spoolProfileDensity2'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6073:
                # Update the value of the Spool2 Diameter node
                value = float(values['spoolProfileDiameter2']) if values['spoolProfileDiameter2'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6074:
                # Update the value of the Default Extrusion Length node
                value = float(values['printerProfileExtruderDefaultExtrusionLength']) if\
                    values['printerProfileExtruderDefaultExtrusionLength'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6075:
                # Update the value of the Spool2 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial2']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6076:
                # Update the value of the Spool2 Temperature Offset node
                value = float(values['spoolTempOffset2']) if values['spoolTempOffset2'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6077:
                # Update the value of the Nozzle Diameter node
                value = float(values['printerProfileExtruderNozzleDiameter']) if \
                    values['printerProfileExtruderNozzleDiameter'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6078:
                # Update the value of the Spool2 Used node
                value = float(values['spoolUsed2']) if values['spoolUsed2'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6079:
                # Update the value of the Spool2 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor2']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6080:
                # Update the value of the Nozzle OffsetX node
                value = float(values['printerProfileExtruderOffsetX']) if values['printerProfileExtruderOffsetX'] \
                                                                          is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6081:
                # Update the value of the Spool2 Weight node
                value = float(values['spoolWeight2']) if values['spoolWeight2'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6082:
                # Update the value of the Spool3 Cost node
                value = float(values['spoolCost3']) if values['spoolCost3'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6083:
                # Update the value of the Nozzle OffsetY node
                value = float(values['printerProfileExtruderOffsetY']) if values['printerProfileExtruderOffsetY'] \
                                                                          is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6084:
                # Update the value of the AxisX Min node
                value = float(values['printerProfileVolumeCustom_boxX_min']) if \
                    values['printerProfileVolumeCustom_boxX_min'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6085:
                # Update the value of the AxisX Max node
                value = float(values['printerProfileVolumeCustom_boxX_max']) if\
                    values['printerProfileVolumeCustom_boxX_max'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6086:
                # Update the value of the AxisY Max node
                value = float(values['printerProfileVolumeCustom_boxY_max']) if\
                    values['printerProfileVolumeCustom_boxY_max'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6087:
                # Update the value of the AxisY Min node
                value = float(values['printerProfileVolumeCustom_boxY_min']) if \
                    values['printerProfileVolumeCustom_boxY_min'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6088:
                # Update the value of the AxisZ Max node
                value = float(values['printerProfileVolumeCustom_boxZ_max']) if \
                    values['printerProfileVolumeCustom_boxZ_max'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6089:
                # Update the value of the AxisZ Min node
                value = float(values['printerProfileVolumeCustom_boxZ_min']) if \
                    values['printerProfileVolumeCustom_boxZ_min'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6090:
                # Update the value of the AxisX Length node
                value = float(values['printerProfileVolumeWidth']) if values['printerProfileVolumeWidth'] is not \
                                                                      None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6091:
                # Update the value of the AxisY Length node
                value = float(values['printerProfileVolumeDepth']) if values['printerProfileVolumeDepth'] is not \
                                                                      None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6092:
                # Update the value of the AxisZ Length node
                value = float(values['printerProfileVolumeHeight']) if values['printerProfileVolumeHeight'] is not \
                                                                       None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6093:
                # Update the value of the Spool3 Density node
                value = float(values['spoolProfileDensity3']) if values['spoolProfileDensity3'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6094:
                # Update the value of the Spool3 Diameter node
                value = float(values['spoolProfileDiameter3']) if values['spoolProfileDiameter3'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6095:
                # Update the value of the selectedSpoolName node
                val = ua.Variant(Value=str(values['selectedSpoolName']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6096:
                # Update the value of the selectedSpoolCost node
                value = float(values['selectedSpoolCost']) if values['selectedSpoolCost'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6097:
                # Update the value of the SpoolSelected Density node
                value = float(values['selectedSpoolProfileDensity']) if values['selectedSpoolProfileDensity'] is not\
                                                                        None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6098:
                # Update the value of the SpoolSelected Diameter node
                value = float(values['selectedSpoolProfileDiameter']) if values['selectedSpoolProfileDiameter'] is \
                                                                         not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6099:
                # Update the value of the SpoolSelected Material node
                val = ua.Variant(Value=str(values['selectedSpoolProfileMaterial']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6100:
                # Update the value of the selectedSpoolProfileVendor node
                val = ua.Variant(Value=str(values['selectedSpoolProfileVendor']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6101:
                # Update the value of the selectedSpoolTempOffset node
                value = float(values['selectedSpoolTempOffset']) if values['selectedSpoolTempOffset'] is not None\
                    else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6102:
                # Update the value of the selectedSpoolUsed node
                value = float(values['selectedSpoolUsed']) if values['selectedSpoolUsed'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6103:
                # Update the value of the selectedSpoolWeight node
                value = float(values['selectedSpoolWeight']) if values['selectedSpoolWeight'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6104:
                # Update the value of the Spool3 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial3']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6105:
                # Update the value of the Spool3 Temperature Offset node
                value = float(values['spoolTempOffset3']) if values['spoolTempOffset3'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6106:
                # Update the value of the Spool0 node
                val = ua.Variant(Value=str(values['spoolName0']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6107:
                # Update the value of the Spool0 Cost node
                value = float(values['spoolCost0']) if values['spoolCost0'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6108:
                # Update the value of the Spool0 Density node
                value = float(values['spoolProfileDensity0']) if values['spoolProfileDensity0'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6109:
                # Update the value of the Spool0 Diameter node
                value = float(values['spoolProfileDiameter0']) if values['spoolProfileDiameter0'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6110:
                # Update the value of the Spool0 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial0']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6111:
                # Update the value of the Spool0 Temperature Offset node
                value = float(values['spoolTempOffset0']) if values['spoolTempOffset0'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6112:
                # Update the value of the Spool0 Used node
                value = float(values['spoolUsed0']) if values['spoolUsed0'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6113:
                # Update the value of the Spool0 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor0']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6114:
                # Update the value of the Spool0 Weight node
                value = float(values['spoolWeight0']) if values['spoolWeight0'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6115:
                # Update the value of the Spool3 Used node
                value = float(values['spoolUsed3']) if values['spoolUsed3'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6116:
                # Update the value of the Spool3 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor3']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6117:
                # Update the value of the Spool1 node
                val = ua.Variant(Value=str(values['spoolName1']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6118:
                # Update the value of the Spool3 Weight node
                value = float(values['spoolWeight3']) if values['spoolWeight3'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6119:
                # Update the value of the Spool4 Cost node
                value = float(values['spoolCost4']) if values['spoolCost4'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6120:
                # Update the value of the Spool2 node
                val = ua.Variant(Value=str(values['spoolName2']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6121:
                # Update the value of the Spool4 Density node
                value = float(values['spoolProfileDensity4']) if values['spoolProfileDensity4'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6122:
                # Update the value of the Spool4 Diameter node
                value = float(values['spoolProfileDiameter4']) if values['spoolProfileDiameter4'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6123:
                # Update the value of the Spool3 node
                val = ua.Variant(Value=str(values['spoolName3']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6124:
                # Update the value of the Spool4 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial4']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6125:
                # Update the value of the Spool4 Temperature Offset node
                value = float(values['spoolTempOffset4']) if values['spoolTempOffset4'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6126:
                # Update the value of the Spool4 node
                val = ua.Variant(Value=str(values['spoolName4']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6127:
                # Update the value of the Spool4 Used node
                value = float(values['spoolUsed4']) if values['spoolUsed4'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6128:
                # Update the value of the Spool4 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor4']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6129:
                # Update the value of the Spool5 node
                val = ua.Variant(Value=str(values['spoolName5']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6130:
                # Update the value of the Spool4 Weight node
                value = float(values['spoolWeight4']) if values['spoolWeight4'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6131:
                # Update the value of the Spool5 Cost node
                value = float(values['spoolCost5']) if values['spoolCost5'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6132:
                # Update the value of the Spool6 node
                val = ua.Variant(Value=str(values['spoolName6']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6133:
                # Update the value of the Spool5 Density node
                value = float(values['spoolProfileDensity5']) if values['spoolProfileDensity5'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6134:
                # Update the value of the Spool5 Diameter node
                value = float(values['spoolProfileDiameter5']) if values['spoolProfileDiameter5'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6135:
                # Update the value of the Spool5 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial5']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6136:
                # Update the value of the Spool5 Temperature Offset node
                value = float(values['spoolTempOffset5']) if values['spoolTempOffset5'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6137:
                # Update the value of the Spool5 Used node
                value = float(values['spoolUsed5']) if values['spoolUsed5'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6138:
                # Update the value of the Spool5 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor5']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6139:
                # Update the value of the Spool5 Weight node
                value = float(values['spoolWeight5']) if values['spoolWeight5'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6140:
                # Update the value of the Spool6 Cost node
                value = float(values['spoolCost6']) if values['spoolCost6'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6141:
                # Update the value of the Spool6 Density node
                value = float(values['spoolProfileDensity6']) if values['spoolProfileDensity6'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6142:
                # Update the value of the Spool6 Diameter node
                value = float(values['spoolProfileDiameter6']) if values['spoolProfileDiameter6'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6143:
                # Update the value of the Spool6 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial6']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6144:
                # Update the value of the Spool6 Temperature Offset node
                value = float(values['spoolTempOffset6']) if values['spoolTempOffset6'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6145:
                # Update the value of the Spool7 Cost node
                value = float(values['spoolCost7']) if values['spoolCost7'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6146:
                # Update the value of the Spool7 Density node
                value = float(values['spoolProfileDensity7']) if values['spoolProfileDensity7'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6147:
                # Update the value of the Spool7 Diameter node
                value = float(values['spoolProfileDiameter7']) if values['spoolProfileDiameter7'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6148:
                # Update the value of the Spool7 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial7']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6149:
                # Update the value of the Spool7 Temperature Offset node
                value = float(values['spoolTempOffset7']) if values['spoolTempOffset7'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6150:
                # Update the value of the Spool8 Cost node
                value = float(values['spoolCost8']) if values['spoolCost8'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6151:
                # Update the value of the Spool8 Density node
                value = float(values['spoolProfileDensity8']) if values['spoolProfileDensity8'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6152:
                # Update the value of the Spool8 Diameter node
                value = float(values['spoolProfileDiameter8']) if values['spoolProfileDiameter8'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6153:
                # Update the value of the Spool8 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial8']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6154:
                # Update the value of the Spool8 Temperature Offset node
                value = float(values['spoolTempOffset8']) if values['spoolTempOffset8'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6155:
                # Update the value of the Spool9 Cost node
                value = float(values['spoolCost9']) if values['spoolCost9'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6156:
                # Update the value of the Spool9 Density node
                value = float(values['spoolProfileDensity9']) if values['spoolProfileDensity9'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6157:
                # Update the value of the Spool9 Diameter node
                value = float(values['spoolProfileDiameter9']) if values['spoolProfileDiameter9'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6158:
                # Update the value of the Spool9 Material node
                val = ua.Variant(Value=str(values['spoolProfileMaterial9']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6159:
                # Update the value of the Spool9 Temperature Offset node
                value = float(values['spoolTempOffset9']) if values['spoolTempOffset9'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6160:
                # Update the value of the Spool6 Used node
                value = float(values['spoolUsed6']) if values['spoolUsed6'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6161:
                # Update the value of the Spool6 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor6']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6162:
                # Update the value of the Spool6 Weight node
                value = float(values['spoolWeight6']) if values['spoolWeight6'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6163:
                # Update the value of the Spool7 Used node
                value = float(values['spoolUsed7']) if values['spoolUsed7'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6164:
                # Update the value of the Spool7 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor7']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6165:
                # Update the value of the Spool7 Weight node
                value = float(values['spoolWeight7']) if values['spoolWeight7'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6166:
                # Update the value of the Spool8 Used node
                value = float(values['spoolUsed8']) if values['spoolUsed8'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6167:
                # Update the value of the Spool8 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor8']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6168:
                # Update the value of the Spool8 Weight node
                value = float(values['spoolWeight8']) if values['spoolWeight8'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6169:
                # Update the value of the Spool9 Used node
                value = float(values['spoolUsed9']) if values['spoolUsed9'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6170:
                # Update the value of the Spool9 Vendor node
                val = ua.Variant(Value=str(values['spoolProfileVendor9']), VariantType=ua.VariantType.String)
                await node.write_value(val)
            elif node.nodeid.Identifier == 6171:
                # Update the value of the Spool9 Weight node
                value = float(values['spoolWeight9']) if values['spoolWeight9'] is not None else 0.0
                val = ua.Variant(Value=value, VariantType=ua.VariantType.Double)
                await node.write_value(val)
            else:
                print(f"Skipping link node {node.nodeid}")
        await asyncio.sleep(1)


# Start Server
if __name__ == "__main__":
    asyncio.run(main())
