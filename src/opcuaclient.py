import asyncio
import configparser

from asyncua import Client

async def get_values():
    config = configparser.ConfigParser()
    config.read('config.ini')
    opcUa_uri = config.get('opcUa', 'uri')
    opcUa_url = config.get('opcUa', 'url')

    #value6001 = None
    #value6002 = None
    #value6003 = None
    #value6004 = None
    #value6005 = None
    #value6006 = None
    #value6007 = None
    #value6008 = None
    #value6009 = None
    #value6010 = None
    #value6011 = None

    print(f"Connecting to {opcUa_url} ...")
    async with Client(url=opcUa_url) as client:
        # Find the namespace index
        nsindex = await client.get_namespace_index(opcUa_uri)
        print(f"Namespace Index for '{opcUa_uri}': {nsindex}")


        # Read the value of the manufacturer node
        #node = client.get_node(f"ns={nsindex};i=6001")
        #value = await node.read_value()
        #value6001 = value.Text
        #print("Value6001: ", value6001)
        ## Read the value of the productInstanceUri node
        #node = client.get_node(f"ns={nsindex};i=6002")
        #value6002 = await node.read_value()
        ## Read the value of the serialNumber node
        #node = client.get_node(f"ns={nsindex};i=6003")
        #value6003 = await node.read_value()
        ## Read the value of the operationMode node
        #node = client.get_node(f"ns={nsindex};i=6004")
        #value6004 = await node.read_value()
        ## Read the value of the name node
        #node = client.get_node(f"ns={nsindex};i=6005")
        #value6005 = await node.read_value()
        ## Read the value of the numberInList node
        #node = client.get_node(f"ns={nsindex};i=6006")
        #value6006 = await node.read_value()
        ## Read the value of the currentState node
        #node = client.get_node(f"ns={nsindex};i=6007")
        #value = await node.read_value()
        #value6007 = value.Text
        ## Read the value of the id node
        #node = client.get_node(f"ns={nsindex};i=6008")
        #value6008 = await node.read_value()
        ## Read the value of the number node
        #node = client.get_node(f"ns={nsindex};i=6009")
        #value6009 = await node.read_value()
        ## Read the value of the currentState node
        #node = client.get_node(f"ns={nsindex};i=6010")
        #value = await node.read_value()
        #value6010 = value.Text
        ## Read the value of the id node
        #node = client.get_node(f"ns={nsindex};i=6011")
        #value6011 = await node.read_value()

        node = client.get_node(f"ns={nsindex};i=6001")
        value = await node.read_value()
        value6001 = value.Text
        print("Value6001: ", value6001)
        node = client.get_node(f"ns={nsindex};i=6002")
        value = await node.read_value()
        value6002 = value
        print("Value6002: ", value6002)
        node = client.get_node(f"ns={nsindex};i=6003")
        value = await node.read_value()
        value6003 = value
        print("Value6003: ", value6003)
        node = client.get_node(f"ns={nsindex};i=6004")
        value = await node.read_value()
        value6004 = value
        print("Value6004: ", value6004)
        node = client.get_node(f"ns={nsindex};i=6005")
        value = await node.read_value()
        value6005 = value
        print("Value6005: ", value6005)
        node = client.get_node(f"ns={nsindex};i=6006")
        value = await node.read_value()
        value6006 = value
        print("Value6006: ", value6006)
        node = client.get_node(f"ns={nsindex};i=6007")
        value = await node.read_value()
        value6007 = value.Text
        print("Value6007: ", value6007)
        node = client.get_node(f"ns={nsindex};i=6008")
        value = await node.read_value()
        value6008 = value
        print("Value6008: ", value6008)
        node = client.get_node(f"ns={nsindex};i=6009")
        value = await node.read_value()
        value6009 = value
        print("Value6009: ", value6009)
        node = client.get_node(f"ns={nsindex};i=6010")
        value = await node.read_value()
        value6010 = value
        print("Value6010: ", value6010)
        node = client.get_node(f"ns={nsindex};i=6011")
        value = await node.read_value()
        value6011 = value.Text
        print("Value6011: ", value6011)
        node = client.get_node(f"ns={nsindex};i=6012")
        value = await node.read_value()
        value6012 = value
        print("Value6012: ", value6012)

        node = client.get_node(f"ns={nsindex};i=6015")
        value = await node.read_value()
        value6015 = value
        print("Value6015: ", value6015)
        node = client.get_node(f"ns={nsindex};i=6016")
        value = await node.read_value()
        value6016 = value
        print("Value6016: ", value6016)
        node = client.get_node(f"ns={nsindex};i=6017")
        value = await node.read_value()
        value6017 = value
        print("Value6017: ", value6017)
        node = client.get_node(f"ns={nsindex};i=6018")
        value = await node.read_value()
        value6018 = value
        print("Value6018: ", value6018)
        node = client.get_node(f"ns={nsindex};i=6019")
        value = await node.read_value()
        value6019 = value
        print("Value6019: ", value6019)
        node = client.get_node(f"ns={nsindex};i=6020")
        value = await node.read_value()
        value6020 = value
        print("Value6020: ", value6020)
        node = client.get_node(f"ns={nsindex};i=6021")
        value = await node.read_value()
        value6021 = value
        print("Value6021: ", value6021)
        node = client.get_node(f"ns={nsindex};i=6022")
        value = await node.read_value()
        value6022 = value
        print("Value6022: ", value6022)
        node = client.get_node(f"ns={nsindex};i=6023")
        value = await node.read_value()
        value6023 = value
        print("Value6023: ", value6023)
        node = client.get_node(f"ns={nsindex};i=6024")
        value = await node.read_value()
        value6024 = value
        print("Value6024: ", value6024)
        node = client.get_node(f"ns={nsindex};i=6025")
        value = await node.read_value()
        value6025 = value
        print("Value6025: ", value6025)
        node = client.get_node(f"ns={nsindex};i=6026")
        value = await node.read_value()
        value6026 = value
        print("Value6026: ", value6026)
        node = client.get_node(f"ns={nsindex};i=6027")
        value = await node.read_value()
        value6027 = value
        print("Value6027: ", value6027)
        node = client.get_node(f"ns={nsindex};i=6028")
        value = await node.read_value()
        value6028 = value
        print("Value6028: ", value6028)
        node = client.get_node(f"ns={nsindex};i=6029")
        value = await node.read_value()
        value6029 = value
        print("Value6029: ", value6029)
        node = client.get_node(f"ns={nsindex};i=6030")
        value = await node.read_value()
        value6030 = value
        print("Value6030: ", value6030)
        node = client.get_node(f"ns={nsindex};i=6031")
        value = await node.read_value()
        value6031 = value
        print("Value6031: ", value6031)
        node = client.get_node(f"ns={nsindex};i=6032")
        value = await node.read_value()
        value6032 = value
        print("Value6032: ", value6032)

        node = client.get_node(f"ns={nsindex};i=6034")
        value = await node.read_value()
        value6034 = value
        print("Value6034: ", value6034)
        node = client.get_node(f"ns={nsindex};i=6035")
        value = await node.read_value()
        value6035 = value
        print("Value6035: ", value6035)
        node = client.get_node(f"ns={nsindex};i=6036")
        value = await node.read_value()
        value6036 = value
        print("Value6036: ", value6036)
        node = client.get_node(f"ns={nsindex};i=6037")
        value = await node.read_value()
        value6037 = value
        print("Value6037: ", value6037)
        node = client.get_node(f"ns={nsindex};i=6038")
        value = await node.read_value()
        value6038 = value
        print("Value6038: ", value6038)
        node = client.get_node(f"ns={nsindex};i=6039")
        value = await node.read_value()
        value6039 = value
        print("Value6039: ", value6039)
        node = client.get_node(f"ns={nsindex};i=6040")
        value = await node.read_value()
        value6040 = value
        print("Value6040: ", value6040)

        node = client.get_node(f"ns={nsindex};i=6042")
        value = await node.read_value()
        value6042 = value
        print("Value6042: ", value6042)
        node = client.get_node(f"ns={nsindex};i=6043")
        value = await node.read_value()
        value6043 = value
        print("Value6043: ", value6043)
        node = client.get_node(f"ns={nsindex};i=6044")
        value = await node.read_value()
        value6044 = value
        print("Value6044: ", value6044)
        node = client.get_node(f"ns={nsindex};i=6045")
        value = await node.read_value()
        value6045 = value
        print("Value6045: ", value6045)
        node = client.get_node(f"ns={nsindex};i=6046")
        value = await node.read_value()
        value6046 = value
        print("Value6046: ", value6046)
        node = client.get_node(f"ns={nsindex};i=6047")
        value = await node.read_value()
        value6047 = value
        print("Value6047: ", value6047)
        node = client.get_node(f"ns={nsindex};i=6048")
        value = await node.read_value()
        value6048 = value
        print("Value6048: ", value6048)

        node = client.get_node(f"ns={nsindex};i=6052")
        value = await node.read_value()
        value6052 = value
        print("Value6052: ", value6052)
        node = client.get_node(f"ns={nsindex};i=6053")
        value = await node.read_value()
        value6053 = value
        print("Value6053: ", value6053)
        node = client.get_node(f"ns={nsindex};i=6054")
        value = await node.read_value()
        value6054 = value
        print("Value6054: ", value6054)
        node = client.get_node(f"ns={nsindex};i=6055")
        value = await node.read_value()
        value6055 = value
        print("Value6055: ", value6055)
        node = client.get_node(f"ns={nsindex};i=6056")
        value = await node.read_value()
        value6056 = value
        print("Value6056: ", value6056)
        node = client.get_node(f"ns={nsindex};i=6057")
        value = await node.read_value()
        value6057 = value
        print("Value6057: ", value6057)
        node = client.get_node(f"ns={nsindex};i=6058")
        value = await node.read_value()
        value6058 = value
        print("Value6058: ", value6058)
        node = client.get_node(f"ns={nsindex};i=6059")
        value = await node.read_value()
        value6059 = value
        print("Value6059: ", value6059)
        node = client.get_node(f"ns={nsindex};i=6060")
        value = await node.read_value()
        value6060 = value
        print("Value6060: ", value6060)
        node = client.get_node(f"ns={nsindex};i=6061")
        value = await node.read_value()
        value6061 = value
        print("Value6061: ", value6061)
        node = client.get_node(f"ns={nsindex};i=6062")
        value = await node.read_value()
        value6062 = value
        print("Value6062: ", value6062)
        node = client.get_node(f"ns={nsindex};i=6063")
        value = await node.read_value()
        value6063 = value
        print("Value6063: ", value6063)
        node = client.get_node(f"ns={nsindex};i=6064")
        value = await node.read_value()
        value6064 = value
        print("Value6064: ", value6064)
        node = client.get_node(f"ns={nsindex};i=6065")
        value = await node.read_value()
        value6065 = value
        print("Value6065: ", value6065)
        node = client.get_node(f"ns={nsindex};i=6066")
        value = await node.read_value()
        value6066 = value
        print("Value6066: ", value6066)
        node = client.get_node(f"ns={nsindex};i=6067")
        value = await node.read_value()
        value6067 = value
        print("Value6067: ", value6067)
        node = client.get_node(f"ns={nsindex};i=6068")
        value = await node.read_value()
        value6068 = value
        print("Value6068: ", value6068)
        node = client.get_node(f"ns={nsindex};i=6069")
        value = await node.read_value()
        value6069 = value
        print("Value6069: ", value6069)
        node = client.get_node(f"ns={nsindex};i=6070")
        value = await node.read_value()
        value6070 = value
        print("Value6070: ", value6070)
        node = client.get_node(f"ns={nsindex};i=6071")
        value = await node.read_value()
        value6071 = value
        print("Value6071: ", value6071)
        node = client.get_node(f"ns={nsindex};i=6072")
        value = await node.read_value()
        value6072 = value
        print("Value6072: ", value6072)
        node = client.get_node(f"ns={nsindex};i=6073")
        value = await node.read_value()
        value6073 = value
        print("Value6073: ", value6073)
        node = client.get_node(f"ns={nsindex};i=6074")
        value = await node.read_value()
        value6074 = value
        print("Value6074: ", value6074)
        node = client.get_node(f"ns={nsindex};i=6075")
        value = await node.read_value()
        value6075 = value
        print("Value6075: ", value6075)
        node = client.get_node(f"ns={nsindex};i=6076")
        value = await node.read_value()
        value6076 = value
        print("Value6076: ", value6076)
        node = client.get_node(f"ns={nsindex};i=6077")
        value = await node.read_value()
        value6077 = value
        print("Value6077: ", value6077)
        node = client.get_node(f"ns={nsindex};i=6078")
        value = await node.read_value()
        value6078 = value
        print("Value6078: ", value6078)
        node = client.get_node(f"ns={nsindex};i=6079")
        value = await node.read_value()
        value6079 = value
        print("Value6079: ", value6079)
        node = client.get_node(f"ns={nsindex};i=6080")
        value = await node.read_value()
        value6080 = value
        print("Value6080: ", value6080)
        node = client.get_node(f"ns={nsindex};i=6081")
        value = await node.read_value()
        value6081 = value
        print("Value6081: ", value6081)
        node = client.get_node(f"ns={nsindex};i=6082")
        value = await node.read_value()
        value6082 = value
        print("Value6082: ", value6082)
        node = client.get_node(f"ns={nsindex};i=6083")
        value = await node.read_value()
        value6083 = value
        print("Value6083: ", value6083)
        node = client.get_node(f"ns={nsindex};i=6084")
        value = await node.read_value()
        value6084 = value
        print("Value6084: ", value6084)
        node = client.get_node(f"ns={nsindex};i=6085")
        value = await node.read_value()
        value6085 = value
        print("Value6085: ", value6085)
        node = client.get_node(f"ns={nsindex};i=6086")
        value = await node.read_value()
        value6086 = value
        print("Value6086: ", value6086)
        node = client.get_node(f"ns={nsindex};i=6087")
        value = await node.read_value()
        value6087 = value
        print("Value6087: ", value6087)
        node = client.get_node(f"ns={nsindex};i=6088")
        value = await node.read_value()
        value6088 = value
        print("Value6088: ", value6088)
        node = client.get_node(f"ns={nsindex};i=6089")
        value = await node.read_value()
        value6089 = value
        print("Value6089: ", value6089)
        node = client.get_node(f"ns={nsindex};i=6090")
        value = await node.read_value()
        value6090 = value
        print("Value6090: ", value6090)
        node = client.get_node(f"ns={nsindex};i=6091")
        value = await node.read_value()
        value6091 = value
        print("Value6091: ", value6091)
        node = client.get_node(f"ns={nsindex};i=6092")
        value = await node.read_value()
        value6092 = value
        print("Value6092: ", value6092)
        node = client.get_node(f"ns={nsindex};i=6093")
        value = await node.read_value()
        value6093 = value
        print("Value6093: ", value6093)
        node = client.get_node(f"ns={nsindex};i=6094")
        value = await node.read_value()
        value6094 = value
        print("Value6094: ", value6094)
        node = client.get_node(f"ns={nsindex};i=6095")
        value = await node.read_value()
        value6095 = value
        print("Value6095: ", value6095)
        node = client.get_node(f"ns={nsindex};i=6096")
        value = await node.read_value()
        value6096 = value
        print("Value6096: ", value6096)
        node = client.get_node(f"ns={nsindex};i=6097")
        value = await node.read_value()
        value6097 = value
        print("Value6097: ", value6097)
        node = client.get_node(f"ns={nsindex};i=6098")
        value = await node.read_value()
        value6098 = value
        print("Value6098: ", value6098)
        node = client.get_node(f"ns={nsindex};i=6099")
        value = await node.read_value()
        value6099 = value
        print("Value6099: ", value6099)
        node = client.get_node(f"ns={nsindex};i=6100")
        value = await node.read_value()
        value6100 = value
        print("Value6100: ", value6100)

        node = client.get_node(f"ns={nsindex};i=6101")
        value = await node.read_value()
        value6101 = value
        print("Value6101: ", value6101)
        node = client.get_node(f"ns={nsindex};i=6102")
        value = await node.read_value()
        value6102 = value
        print("Value6102: ", value6102)
        node = client.get_node(f"ns={nsindex};i=6103")
        value = await node.read_value()
        value6103 = value
        print("Value6103: ", value6103)
        node = client.get_node(f"ns={nsindex};i=6104")
        value = await node.read_value()
        value6104 = value
        print("Value6104: ", value6104)
        node = client.get_node(f"ns={nsindex};i=6105")
        value = await node.read_value()
        value6105 = value
        print("Value6105: ", value6105)
        node = client.get_node(f"ns={nsindex};i=6106")
        value = await node.read_value()
        value6106 = value
        print("Value6106: ", value6106)
        node = client.get_node(f"ns={nsindex};i=6107")
        value = await node.read_value()
        value6107 = value
        print("Value6107: ", value6107)
        node = client.get_node(f"ns={nsindex};i=6108")
        value = await node.read_value()
        value6108 = value
        print("Value6108: ", value6108)
        node = client.get_node(f"ns={nsindex};i=6109")
        value = await node.read_value()
        value6109 = value
        print("Value6109: ", value6109)
        node = client.get_node(f"ns={nsindex};i=6110")
        value = await node.read_value()
        value6110 = value
        print("Value6110: ", value6110)
        node = client.get_node(f"ns={nsindex};i=6111")
        value = await node.read_value()
        value6111 = value
        print("Value6111: ", value6111)
        node = client.get_node(f"ns={nsindex};i=6112")
        value = await node.read_value()
        value6112 = value
        print("Value6112: ", value6112)
        node = client.get_node(f"ns={nsindex};i=6113")
        value = await node.read_value()
        value6113 = value
        print("Value6113: ", value6113)
        node = client.get_node(f"ns={nsindex};i=6114")
        value = await node.read_value()
        value6114 = value
        print("Value6114: ", value6114)
        node = client.get_node(f"ns={nsindex};i=6115")
        value = await node.read_value()
        value6115 = value
        print("Value6115: ", value6115)
        node = client.get_node(f"ns={nsindex};i=6116")
        value = await node.read_value()
        value6116 = value
        print("Value6116: ", value6116)
        node = client.get_node(f"ns={nsindex};i=6117")
        value = await node.read_value()
        value6117 = value
        print("Value6117: ", value6117)
        node = client.get_node(f"ns={nsindex};i=6118")
        value = await node.read_value()
        value6118 = value
        print("Value6118: ", value6118)
        node = client.get_node(f"ns={nsindex};i=6119")
        value = await node.read_value()
        value6119 = value
        print("Value6119: ", value6119)
        node = client.get_node(f"ns={nsindex};i=6120")
        value = await node.read_value()
        value6120 = value
        print("Value6120: ", value6120)
        node = client.get_node(f"ns={nsindex};i=6121")
        value = await node.read_value()
        value6121 = value
        print("Value6121: ", value6121)
        node = client.get_node(f"ns={nsindex};i=6122")
        value = await node.read_value()
        value6122 = value
        print("Value6122: ", value6122)
        node = client.get_node(f"ns={nsindex};i=6123")
        value = await node.read_value()
        value6123 = value
        print("Value6123: ", value6123)
        node = client.get_node(f"ns={nsindex};i=6124")
        value = await node.read_value()
        value6124 = value
        print("Value6124: ", value6124)
        node = client.get_node(f"ns={nsindex};i=6125")
        value = await node.read_value()
        value6125 = value
        print("Value6125: ", value6125)
        node = client.get_node(f"ns={nsindex};i=6126")
        value = await node.read_value()
        value6126 = value
        print("Value6126: ", value6126)
        node = client.get_node(f"ns={nsindex};i=6127")
        value = await node.read_value()
        value6127 = value
        print("Value6127: ", value6127)
        node = client.get_node(f"ns={nsindex};i=6128")
        value = await node.read_value()
        value6128 = value
        print("Value6128: ", value6128)
        node = client.get_node(f"ns={nsindex};i=6129")
        value = await node.read_value()
        value6129 = value
        print("Value6129: ", value6129)
        node = client.get_node(f"ns={nsindex};i=6130")
        value = await node.read_value()
        value6130 = value
        print("Value6130: ", value6130)
        node = client.get_node(f"ns={nsindex};i=6131")
        value = await node.read_value()
        value6131 = value
        print("Value6131: ", value6131)
        node = client.get_node(f"ns={nsindex};i=6132")
        value = await node.read_value()
        value6132 = value
        print("Value6132: ", value6132)
        node = client.get_node(f"ns={nsindex};i=6133")
        value = await node.read_value()
        value6133 = value
        print("Value6133: ", value6133)
        node = client.get_node(f"ns={nsindex};i=6134")
        value = await node.read_value()
        value6134 = value
        print("Value6134: ", value6134)
        node = client.get_node(f"ns={nsindex};i=6135")
        value = await node.read_value()
        value6135 = value
        print("Value6135: ", value6135)
        node = client.get_node(f"ns={nsindex};i=6136")
        value = await node.read_value()
        value6136 = value
        print("Value6136: ", value6136)
        node = client.get_node(f"ns={nsindex};i=6137")
        value = await node.read_value()
        value6137 = value
        print("Value6137: ", value6137)
        node = client.get_node(f"ns={nsindex};i=6138")
        value = await node.read_value()
        value6138 = value
        print("Value6138: ", value6138)
        node = client.get_node(f"ns={nsindex};i=6139")
        value = await node.read_value()
        value6139 = value
        print("Value6139: ", value6139)
        node = client.get_node(f"ns={nsindex};i=6140")
        value = await node.read_value()
        value6140 = value
        print("Value6140: ", value6140)
        node = client.get_node(f"ns={nsindex};i=6141")
        value = await node.read_value()
        value6141 = value
        print("Value6141: ", value6141)
        node = client.get_node(f"ns={nsindex};i=6142")
        value = await node.read_value()
        value6142 = value
        print("Value6142: ", value6142)
        node = client.get_node(f"ns={nsindex};i=6143")
        value = await node.read_value()
        value6143 = value
        print("Value6143: ", value6143)
        node = client.get_node(f"ns={nsindex};i=6144")
        value = await node.read_value()
        value6144 = value
        print("Value6144: ", value6144)
        node = client.get_node(f"ns={nsindex};i=6145")
        value = await node.read_value()
        value6145 = value
        print("Value6145: ", value6145)
        node = client.get_node(f"ns={nsindex};i=6146")
        value = await node.read_value()
        value6146 = value
        print("Value6146: ", value6146)
        node = client.get_node(f"ns={nsindex};i=6147")
        value = await node.read_value()
        value6147 = value
        print("Value6147: ", value6147)
        node = client.get_node(f"ns={nsindex};i=6148")
        value = await node.read_value()
        value6148 = value
        print("Value6148: ", value6148)
        node = client.get_node(f"ns={nsindex};i=6149")
        value = await node.read_value()
        value6149 = value
        print("Value6149: ", value6149)
        node = client.get_node(f"ns={nsindex};i=6150")
        value = await node.read_value()
        value6150 = value
        print("Value6150: ", value6150)
        node = client.get_node(f"ns={nsindex};i=6151")
        value = await node.read_value()
        value6151 = value
        print("Value6151: ", value6151)
        node = client.get_node(f"ns={nsindex};i=6152")
        value = await node.read_value()
        value6152 = value
        print("Value6152: ", value6152)
        node = client.get_node(f"ns={nsindex};i=6153")
        value = await node.read_value()
        value6153 = value
        print("Value6153: ", value6153)
        node = client.get_node(f"ns={nsindex};i=6154")
        value = await node.read_value()
        value6154 = value
        print("Value6154: ", value6154)
        node = client.get_node(f"ns={nsindex};i=6155")
        value = await node.read_value()
        value6155 = value
        print("Value6155: ", value6155)
        node = client.get_node(f"ns={nsindex};i=6156")
        value = await node.read_value()
        value6156 = value
        print("Value6156: ", value6156)
        node = client.get_node(f"ns={nsindex};i=6157")
        value = await node.read_value()
        value6157 = value
        print("Value6157: ", value6157)
        node = client.get_node(f"ns={nsindex};i=6158")
        value = await node.read_value()
        value6158 = value
        print("Value6158: ", value6158)
        node = client.get_node(f"ns={nsindex};i=6159")
        value = await node.read_value()
        value6159 = value
        print("Value6159: ", value6159)
        node = client.get_node(f"ns={nsindex};i=6160")
        value = await node.read_value()
        value6160 = value
        print("Value6160: ", value6160)
        node = client.get_node(f"ns={nsindex};i=6161")
        value = await node.read_value()
        value6161 = value
        print("Value6161: ", value6161)
        node = client.get_node(f"ns={nsindex};i=6162")
        value = await node.read_value()
        value6162 = value
        print("Value6162: ", value6162)
        node = client.get_node(f"ns={nsindex};i=6163")
        value = await node.read_value()
        value6163 = value
        print("Value6163: ", value6163)
        node = client.get_node(f"ns={nsindex};i=6164")
        value = await node.read_value()
        value6164 = value
        print("Value6164: ", value6164)
        node = client.get_node(f"ns={nsindex};i=6165")
        value = await node.read_value()
        value6165 = value
        print("Value6165: ", value6165)
        node = client.get_node(f"ns={nsindex};i=6166")
        value = await node.read_value()
        value6166 = value
        print("Value6166: ", value6166)
        node = client.get_node(f"ns={nsindex};i=6167")
        value = await node.read_value()
        value6167 = value
        print("Value6167: ", value6167)
        node = client.get_node(f"ns={nsindex};i=6168")
        value = await node.read_value()
        value6168 = value
        print("Value6168: ", value6168)
        node = client.get_node(f"ns={nsindex};i=6169")
        value = await node.read_value()
        value6169 = value
        print("Value6169: ", value6169)
        node = client.get_node(f"ns={nsindex};i=6170")
        value = await node.read_value()
        value6170 = value
        print("Value6170: ", value6170)
        node = client.get_node(f"ns={nsindex};i=6171")
        value = await node.read_value()
        value6171 = value
        print("Value6171: ", value6171)

        # await client.disconnect()
    return {
        #'value6001': value6001,
        #'value6002': value6002,
        #'value6003': value6003,
        #'value6004': value6004,
        #'value6005': value6005,
        #'value6006': value6006,
        #'value6007': value6007,
        #'value6008': value6008,
        #'value6009': value6009,
        #'value6010': value6010,
        #'value6011': value6011,
        'value6001': value6001,
        'value6002': value6002,
        'value6003': value6003,
        'value6004': value6004,
        'value6005': value6005,
        'value6006': value6006,
        'value6007': value6007,
        'value6008': value6008,
        'value6009': value6009,
        'value6010': value6010,
        'value6011': value6011,
        'value6012': value6012,

        'value6015': value6015,
        'value6016': value6016,
        'value6017': value6017,
        'value6018': value6018,
        'value6019': value6019,
        'value6020': value6020,
        'value6021': value6021,
        'value6022': value6022,
        'value6023': value6023,
        'value6024': value6024,
        'value6025': value6025,
        'value6026': value6026,
        'value6027': value6027,
        'value6028': value6028,
        'value6029': value6029,
        'value6030': value6030,
        'value6031': value6031,
        'value6032': value6032,

        'value6034': value6034,
        'value6035': value6035,
        'value6036': value6036,
        'value6037': value6037,
        'value6038': value6038,
        'value6039': value6039,
        'value6040': value6040,

        'value6042': value6042,
        'value6043': value6043,
        'value6044': value6044,
        'value6045': value6045,
        'value6046': value6046,
        'value6047': value6047,
        'value6048': value6048,

        'value6052': value6052,
        'value6053': value6053,
        'value6054': value6054,
        'value6055': value6055,
        'value6056': value6056,
        'value6057': value6057,
        'value6058': value6058,
        'value6059': value6059,
        'value6060': value6060,
        'value6061': value6061,
        'value6062': value6062,
        'value6063': value6063,
        'value6064': value6064,
        'value6065': value6065,
        'value6066': value6066,
        'value6067': value6067,
        'value6068': value6068,
        'value6069': value6069,
        'value6070': value6070,
        'value6071': value6071,
        'value6072': value6072,
        'value6073': value6073,
        'value6074': value6074,
        'value6075': value6075,
        'value6076': value6076,
        'value6077': value6077,
        'value6078': value6078,
        'value6079': value6079,
        'value6080': value6080,
        'value6081': value6081,
        'value6082': value6082,
        'value6083': value6083,
        'value6084': value6084,
        'value6085': value6085,
        'value6086': value6086,
        'value6087': value6087,
        'value6088': value6088,
        'value6089': value6089,
        'value6090': value6090,
        'value6091': value6091,
        'value6092': value6092,
        'value6093': value6093,
        'value6094': value6094,
        'value6095': value6095,
        'value6096': value6096,
        'value6097': value6097,
        'value6098': value6098,
        'value6099': value6099,
        'value6100': value6100,
        'value6101': value6101,
        'value6102': value6102,
        'value6103': value6103,
        'value6104': value6104,
        'value6105': value6105,
        'value6106': value6106,
        'value6107': value6107,
        'value6108': value6108,
        'value6109': value6109,
        'value6110': value6110,
        'value6111': value6111,
        'value6112': value6112,
        'value6113': value6113,
        'value6114': value6114,
        'value6115': value6115,
        'value6116': value6116,
        'value6117': value6117,
        'value6118': value6118,
        'value6119': value6119,
        'value6120': value6120,
        'value6121': value6121,
        'value6122': value6122,
        'value6123': value6123,
        'value6124': value6124,
        'value6125': value6125,
        'value6126': value6126,
        'value6127': value6127,
        'value6128': value6128,
        'value6129': value6129,
        'value6130': value6130,
        'value6131': value6131,
        'value6132': value6132,
        'value6133': value6133,
        'value6134': value6134,
        'value6135': value6135,
        'value6136': value6136,
        'value6137': value6137,
        'value6138': value6138,
        'value6139': value6139,
        'value6140': value6140,
        'value6141': value6141,
        'value6142': value6142,
        'value6143': value6143,
        'value6144': value6144,
        'value6145': value6145,
        'value6146': value6146,
        'value6147': value6147,
        'value6148': value6148,
        'value6149': value6149,
        'value6150': value6150,
        'value6151': value6151,
        'value6152': value6152,
        'value6153': value6153,
        'value6154': value6154,
        'value6155': value6155,
        'value6156': value6156,
        'value6157': value6157,
        'value6158': value6158,
        'value6159': value6159,
        'value6160': value6160,
        'value6161': value6161,
        'value6162': value6162,
        'value6163': value6163,
        'value6164': value6164,
        'value6165': value6165,
        'value6166': value6166,
        'value6167': value6167,
        'value6168': value6168,
        'value6169': value6169,
        'value6170': value6170,
        'value6171': value6171,
    }

if __name__ == "__main__":
    asyncio.run(get_values())