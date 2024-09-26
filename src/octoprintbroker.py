from octorest import OctoRest
import configparser
from myoctorest import MyOctoRest

config = configparser.ConfigParser()
config.read('config.ini')
octoprint_url = config.get('octoprint', 'url')
octoprint_apikey = config.get('octoprint', 'apikey')

def make_client():
    try:
        client = MyOctoRest(url=octoprint_url, apikey=octoprint_apikey)
        return client
    except Exception as e:
        print(e)

class opcuavar:
    def __init__(self):
        pass

def get_version_info(c):
    version = c.get_version()
    return version['server'], version['api'], version['text']
def get_connection_info(c):
    connection_info = c.connection_info()['current']
    return connection_info['baudrate'], connection_info['port'], \
           connection_info['printerProfile'], connection_info['state']
def get_printer_profile_info(c, profileVisualized):
    profile = c.printer_profile(profileVisualized)
    return profile, profile['axes'], profile['extruder'], profile['volume'], profile['volume'].get('custom_box', {})

def get_filament_info(job_info, attribute):
    try:
        return job_info['job']['filament'][attribute]
    except KeyError:
        return job_info['job']['filament']['tool0'][attribute]
    except TypeError:
        return None

def get_values():
    c = make_client()
    var = {}
    print('_______________________Start collecting values in octoprintbroker.py______________________________________')
    ### VERSION INFORMATION ###
    var['serverVersion'], var['apiVersion'], var['textVersion'] = get_version_info(c)
    var['probeAppKeysWorkflowSupport'] = c.probe_app_keys_workflow_support()
    ### CONNECTION HANDLING ###
    var['connectionBaudrate'], var['connectionPort'], \
        var['connectionPrinterProfile'], var['connectionState'] = get_connection_info(c)

    printer_profiles = c.connection_info()['options']['printerProfiles']
    for i, profile in enumerate(printer_profiles):
        var.update({
            f'printerProfileId{i}': profile['id'],
            f'printerProfileName{i}': profile['name']
        })

    ### FILE OPERATIONS ###
    files = c.files()['files']
    for i, file in enumerate(files):
        var.update({
            f'fileName{i}': file['name'],
            f'fileSize{i}': file['size'],
            f'fileType{i}': file['type']
        })


    ### JOB OPERATIONS ###
    job_info = c.job_info()
    var['jobEstimatedPrintTime'] = job_info['job']['estimatedPrintTime']
    var['jobFilamentLength'] = get_filament_info(job_info, 'length')
    var['jobFilamentVolume'] = get_filament_info(job_info, 'volume')

    file_info = job_info['job']['file']
    var['jobFileDate'] = file_info['date']
    var['jobFileName'] = file_info['name']
    var['jobFileOrigin'] = file_info['origin']
    var['jobFilePath'] = file_info['path']
    var['jobFileSize'] = file_info['size']

    var['jobLastPrintTime'] = job_info['job']['lastPrintTime']
    var['jobUser'] = job_info['job']['user']

    progress_info = job_info['progress']
    var['progressCompletion'] = progress_info['completion']
    var['progressFilepos'] = progress_info['filepos']
    var['progressPrintTime'] = progress_info['printTime']
    var['progressPrintTimeLeft'] = progress_info['printTimeLeft']

    var['state'] = job_info['state']

    ### PRINTER OPERATIONS ###
    printer_info = c.printer()
    var['sdReady'] = printer_info['sd']['ready']
    var['stateError'] = printer_info['state']['error']

    var.update({
        f'stateFlags{k.capitalize()}': v for k, v in printer_info['state']['flags'].items()
    })

    var['stateText'] = printer_info['state']['text']

    var.update({
        f'temperatureA{k.capitalize()}': v for k, v in printer_info['temperature']['A'].items()
    })
    var.update({
        f'temperatureP{k.capitalize()}': v for k, v in printer_info['temperature']['P'].items()
    })
    var.update({
        f'temperatureBed{k.capitalize()}': v for k, v in printer_info['temperature']['bed'].items()
    })
    var.update({
        f'temperatureTool0{k.capitalize()}': v for k, v in printer_info['temperature']['tool0'].items()
    })

    tool_info = c.tool()
    var.update({
        f'currentToolTemperature{k.capitalize()}': v for k, v in tool_info['tool0'].items()
    })

    bed_info = c.bed()
    var.update({
        f'currentBedTemperature{k.capitalize()}': v for k, v in bed_info['bed'].items()
    })

    var['sdStateReady'] = c.sd()['ready']

    ### PRINTER PROFILE OPERATIONS ###
    profileVisualized = '_default'
    profile, axes, extruder, volume, custom_box = get_printer_profile_info(c, profileVisualized)

    var['printerProfileAxeEInverted'] = axes['e']['inverted']
    var['printerProfileAxeESpeed'] = axes['e']['speed']
    var['printerProfileAxeXInverted'] = axes['x']['inverted']
    var['printerProfileAxeXSpeed'] = axes['x']['speed']
    var['printerProfileAxeYInverted'] = axes['y']['inverted']
    var['printerProfileAxeYSpeed'] = axes['y']['speed']
    var['printerProfileAxeZInverted'] = axes['z']['inverted']
    var['printerProfileAxeZSpeed'] = axes['z']['speed']

    var['printerProfileColor'] = profile['color']
    var['printerProfileCurrent'] = profile['current']
    var['printerProfileDefault'] = profile['default']

    var['printerProfileExtruderCount'] = extruder['count']
    var['printerProfileExtruderDefaultExtrusionLength'] = extruder['defaultExtrusionLength']
    var['printerProfileExtruderNozzleDiameter'] = extruder['nozzleDiameter']
    var['printerProfileExtruderOffsetX'], var['printerProfileExtruderOffsetY'] = extruder['offsets'][0]
    var['printerProfileExtruderSharedNozzle'] = extruder['sharedNozzle']

    var['printerProfileHeatedBed'] = profile['heatedBed']
    var['printerProfileHeatedChamber'] = profile['heatedChamber']
    var['printerProfileId'] = profile['id']
    var['printerProfileModel'] = profile['model']
    var['printerProfileName'] = profile['name']
    var['printerProfileResource'] = profile['resource']

    var['printerProfileVolumeCustom_boxX_max'] = custom_box.get('x_max')
    var['printerProfileVolumeCustom_boxX_min'] = custom_box.get('x_min')
    var['printerProfileVolumeCustom_boxY_max'] = custom_box.get('y_max')
    var['printerProfileVolumeCustom_boxY_min'] = custom_box.get('y_min')
    var['printerProfileVolumeCustom_boxZ_max'] = custom_box.get('z_max')
    var['printerProfileVolumeCustom_boxZ_min'] = custom_box.get('z_min')

    var['printerProfileVolumeDepth'] = volume['depth']
    var['printerProfileVolumeFormFactor'] = volume['formFactor']
    var['printerProfileVolumeHeight'] = volume['height']
    var['printerProfileVolumeOrigin'] = volume['origin']
    var['printerProfileVolumeWidth'] = volume['width']



    # USER
    for i in range(10):
        attr_name = 'userName{}'.format(i)
        var[attr_name] = None
    for i, user in enumerate(c.users()['users']):
        attr_name = 'userName{}'.format(i)
        var[attr_name] = user['name']
    for i in range(10):
        attr_name = 'userAdmin{}'.format(i)
        var[attr_name] = None
    for i, user in enumerate(c.users()['users']):
        attr_name = 'userAdmin{}'.format(i)
        var[attr_name] = user['admin']
"""
    # FILAMENT MANAGER
    var['selectedSpoolCost'] = c.selections()['selections'][0]['spool']['cost']
    var['selectedSpoolId'] = c.selections()['selections'][0]['spool']['id']
    var['selectedSpoolName'] = c.selections()['selections'][0]['spool']['name']
    var['selectedSpoolProfileDensity'] = c.selections()['selections'][0]['spool']['profile']['density']
    var['selectedSpoolProfileDiameter'] = c.selections()['selections'][0]['spool']['profile']['diameter']
    var['selectedSpoolProfileId'] = c.selections()['selections'][0]['spool']['profile']['id']
    var['selectedSpoolProfileMaterial'] = c.selections()['selections'][0]['spool']['profile']['material']
    var['selectedSpoolProfileVendor'] = c.selections()['selections'][0]['spool']['profile']['vendor']
    var['selectedSpoolTempOffset'] = c.selections()['selections'][0]['spool']['temp_offset']
    var['selectedSpoolUsed'] = c.selections()['selections'][0]['spool']['used']
    var['selectedSpoolWeight'] = c.selections()['selections'][0]['spool']['weight']
    var['selectedTool'] = c.selections()['selections'][0]['tool']
"""
    
    for i in range(10):
        var[f'spoolCost{i}'] = None
        var[f'spoolId{i}'] = None
        var[f'spoolName{i}'] = None
        var[f'spoolProfileDensity{i}'] = None
        var[f'spoolProfileDiameter{i}'] = None
        var[f'spoolProfileId{i}'] = None
        var[f'spoolProfileMaterial{i}'] = None
        var[f'spoolProfileVendor{i}'] = None
        var[f'spoolTempOffset{i}'] = None
        var[f'spoolUsed{i}'] = None
        var[f'spoolWeight{i}'] = None

    for i, spool in enumerate(c.spools()['spools']):
        var[f'spoolCost{i}'] = spool['cost']
        var[f'spoolId{i}'] = spool['id']
        var[f'spoolName{i}'] = spool['name']
        var[f'spoolProfileDensity{i}'] = spool['profile']['density']
        var[f'spoolProfileDiameter{i}'] = spool['profile']['diameter']
        var[f'spoolProfileId{i}'] = spool['profile']['id']
        var[f'spoolProfileMaterial{i}'] = spool['profile']['material']
        var[f'spoolProfileVendor{i}'] = spool['profile']['vendor']
        var[f'spoolTempOffset{i}'] = spool['temp_offset']
        var[f'spoolUsed{i}'] = spool['used']
        var[f'spoolWeight{i}'] = spool['weight']

    for i in range(10):
        var[f'profileDensity{i}'] = None
        var[f'profileDiameter{i}'] = None
        var[f'profileId{i}'] = None
        var[f'profileMaterial{i}'] = None
        var[f'profileVendor{i}'] = None

    for i, spool in enumerate(c.profiles()['profiles']):
        var[f'profileDensity{i}'] = spool['density']
        var[f'profileDiameter{i}'] = spool['diameter']
        var[f'profileId{i}'] = spool['id']
        var[f'profileMaterial{i}'] = spool['material']
        var[f'profileVendor{i}'] = spool['vendor']

    # EdoExtra
    file_list = c.files()['files']
    running_file_name = c.job_info()['job']['file']['name']
    if running_file_name is None:
        var['numberInList'] = 9999  # If the file is None, assign 999 to the variable
    else:
        for i, file_info in enumerate(file_list):
            if file_info['name'] == running_file_name:
                var['numberInList'] = i
                break

    if var['state'] in ["Printing", "Pausing", "Resuming", "Operational / Printing from OctoPrint",
                        "Operational / Printing from SD", "Operational / Printing from USB", "Cancelling"]:
        var['currentStateMonitoring'] = "Executing"
    elif var['state'] in ["Operational", "Paused"]:
        var['currentStateMonitoring'] = "NotExecuting"
    elif var['state'] in ["Error", "Closed with Error"]:
        var['currentStateMonitoring'] = "OutOfService"
    else:
        var['currentStateMonitoring'] = "NotAvailable"

    if c.job_info()['job']['file']['name'] == None or var['state'] == "Connecting":
        var['currentStateProduction'] = "NotAvailable"
    elif var['state'] in ["Printing", "Pausing", "Resuming", "Operational / Printing from OctoPrint",
                          "Operational / Printing from SD", "Operational / Printing from USB"]:
        var['currentStateProduction'] = "Running"
    elif var['state'] in ["Operational", "Paused"]:
        var['currentStateProduction'] = "Ready"
    elif var['state'] in ["Error", "Closed with Error"]:
        var['currentStateProduction'] = "OutOfService"
    else:
        var['currentStateProduction'] = "Executing"

    print(
        "________________________End collecting values in octoprintbroker.py_______________________________________")

    return var

if __name__ == "__main__":
    get_values()