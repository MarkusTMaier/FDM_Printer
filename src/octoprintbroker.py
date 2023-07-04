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

def get_values():
    c = make_client()
    var = opcuavar()
    print('_______________________Start collecting values in octoprintbroker.py______________________________________')
    #Commented print lines indicate all the possible functions implemented up to 03.2023 in octorest library
### VERSION INFORMATION ###
    # print("Version information: ", c.get_version())
    var.serverVersion = c.get_version()['server']
    var.apiVersion = c.get_version()['api']
    var.textVersion = c.get_version()['text']
### LOGIN ###
    #print("Current user: NOT WORKING")
### APPS - SESSION KEYS ###
    #print("Obtaining a temporary session key: DEACTIVATED since 1.4.0")
    #print("Verifying a temporary session key: DEACTIVATED since 1.4.0")
### APPS - APPLICATION KEYS PLUGIN WORKFLOW ###
    #print ("Check if the application keys plugin workflow is supported: ", c.probe_app_keys_workflow_support())
    var.probeAppKeysWorkflowSupport = c.probe_app_keys_workflow_support()
    #print("Starts the authorization process")
    #print("Check for an authorization request decision")
    #print("Run the application keys plugin workflow")
### CONNECTION HANDLING ###
    # print("Get connection settings: NOT ALL ACTIVATED: ", c.connection_info())
    var.connectionBaudrate = c.connection_info()['current']['baudrate']
    var.connectionPort = c.connection_info()['current']['port']
    var.connectionPrinterProfile = c.connection_info()['current']['printerProfile']
    var.connectionState =c.connection_info()['current']['state']
    for i in range(10): #generating 10 variables for loop
        attr_name = 'printerProfileId{}'.format(i)
        setattr(var, attr_name, None)
    for i, file_info in enumerate(c.connection_info()['options']['printerProfiles']):      #var.printerProfileId0...1...
        var_name = 'printerProfileId{}'.format(i)
        setattr(var, var_name, file_info['id'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'printerProfileName{}'.format(i)
        setattr(var, attr_name, None)
    for i, file_info in enumerate(c.connection_info()['options']['printerProfiles']):      #var.printerProfileName0...1...
        var_name = 'printerProfileName{}'.format(i)
        setattr(var, var_name, file_info['name'])
    #print("Issue a connection command: USED FOR CONNECTING OCTOPRINT TO PRINTER")
    #c.connect()        #works
    #print("Issue a connectio command: USED FOR DISCONNECTING OCTOPRINT FROM PRINTER")
    #c.disconnect()     #works
    #print("Issue a connection command: USED FOR SYMPTOM SOLVING, EMERGENCY")
    #c.fake_ack()
### FILE OPERATIONS ###
    #print("Retrieve all files: NOT ALL ACTIVATED: ", c.files())
    for i in range(10): #generating 10 variables for loop
        attr_name = 'fileName{}'.format(i)
        setattr(var, attr_name, None)
    for i, file_info in enumerate(c.files()['files']):      #var.fileName0...1...
        var_name = 'fileName{}'.format(i)
        setattr(var, var_name, file_info['name'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'fileSize{}'.format(i)
        setattr(var, attr_name, None)
    for i, file_info in enumerate(c.files()['files']):      #var.fileSize0...1...
        var_size = 'fileSize{}'.format(i)
        setattr(var, var_size, file_info['size'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'fileType{}'.format(i)
        setattr(var, attr_name, None)
    for i, file_info in enumerate(c.files()['files']):      #var.fileType0...1...
        var_type = 'fileType{}'.format(i)
        setattr(var, var_type, file_info['type'])
    #print("Retrieve a specific file's or folder's information: NEED IT? DON'T THINK SO ")
    #print("Upload file or create folder: UPLOAD FILE")
    #print("Upload file or create folder: CREATE NEW FOLDER")
    #print("Issue a file command: SELECT A FILE FOR PRINTING")
    #print("Issue a file command: SLICES AN STL FILE INTO GCODE")
    #print("Issue a file command: COPIES FILE OR FOLDER TO NEW DESTINATION")
    #print("Issue a file command: MOVE FILE OR FOLDER TO NEW DESTINATION")
    #print("Delete file")
### JOB OPERATIONS ###
    #print("Issue a job command: STARTS THE PRINT OF THE CURRENTLY SELECTED FILE")
    #print("Issue a job command: CANCELS THE CURRENT PRINT JOB")
    #print("Issue a job command: RESTARTS THE PRINT")
    #print("Issue a command: PAUSES/RESUMES CURRENT JOB") #general
    #print("Issue a command: PAUSE CURRENT JOB")  #specific
    #print("Issue a command: RESUME CURRENT JOB") #specific
    #print("Issue a command: CHANGE STATUS (PAUSED/WORKING) ") #specific
    #print("Retrieve information about the current job: ", c.job_info())
    # var.jobAveragePrintTime = c.job_info()['job']['averagePrintTime']     #seems to have disappeared
    var.jobEstimatedPrintTime = c.job_info()['job']['estimatedPrintTime']
    try:
        var.jobFilamentLength = c.job_info()['job']['filament']['length']
    except KeyError:
        var.jobFilamentLength = c.job_info()['job']['filament']['tool0']['length']
    try:
        var.jobFilamentVolume = c.job_info()['job']['filament']['volume']
    except KeyError:
        var.jobFilamentVolume = c.job_info()['job']['filament']['tool0']['volume']

    var.jobFileDate = c.job_info()['job']['file']['date']
    # var.jobFileDisplay = c.job_info()['job']['file']['display']       #ssems to have disappeared
    var.jobFileName = c.job_info()['job']['file']['name']
    var.jobFileOrigin = c.job_info()['job']['file']['origin']
    var.jobFilePath = c.job_info()['job']['file']['path']
    var.jobFileSize = c.job_info()['job']['file']['size']
    var.jobLastPrintTime = c.job_info()['job']['lastPrintTime']
    var.jobUser = c.job_info()['job']['user']
    var.progressCompletion = c.job_info()['progress']['completion']
    var.progressFilepos = c.job_info()['progress']['filepos']
    var.progressPrintTime = c.job_info()['progress']['printTime']
    var.progressPrintTimeLeft = c.job_info()['progress']['printTimeLeft']
    # var.progressPrintTimeLeftOrigin = c.job_info()['progress']['printTimeLeftOrigin']     #seems to have disappeared
    var.state = c.job_info()['state']
### LANGUAGES ###
    #print("Retrieve installed language packs (OCTOPRINT): ", c.languages())
    #print("Upload a language pack: NEW LANGUAGE PACK OCTOPRINT")
    #print("Delete a language pack: DELETE LANGUAGE PACK OCTOPRINT")
### LOG FILE MANAGEMENT ###
    #print("Retrieve a list of available log files")
    #print("Delete a specific log file")
### PRINTER OPERATIONS ###
    #print("Retrieve the current printer state: ", c.printer())
    var.sdReady = c.printer()['sd']['ready']
    var.stateError = c.printer()['state']['error']
    var.stateFlagsCancelling = c.printer()['state']['flags']['cancelling']
    var.stateFlagsClosedOrError = c.printer()['state']['flags']['closedOrError']
    var.stateFlagsError = c.printer()['state']['flags']['error']
    var.stateFlagsFinishing = c.printer()['state']['flags']['finishing']
    var.stateFlagsOperational = c.printer()['state']['flags']['operational']
    var.stateFlagsPaused = c.printer()['state']['flags']['paused']
    var.stateFlagsPausing = c.printer()['state']['flags']['pausing']
    var.stateFlagsPrinting = c.printer()['state']['flags']['printing']
    var.stateFlagsReady = c.printer()['state']['flags']['ready']
    var.stateFlagsResuming = c.printer()['state']['flags']['resuming']
    var.stateFlagsSdReady = c.printer()['state']['flags']['sdReady']
    var.stateText = c.printer()['state']['text']
    var.temperatureAActual = c.printer()['temperature']['A']['actual']
    var.temperatureAOffset = c.printer()['temperature']['A']['offset']
    var.temperatureATarget = c.printer()['temperature']['A']['target']
    var.temperaturePActual = c.printer()['temperature']['P']['actual']
    var.temperaturePOffset = c.printer()['temperature']['P']['offset']
    var.temperaturePTarget = c.printer()['temperature']['P']['target']
    var.temperatureBedActual = c.printer()['temperature']['bed']['actual']
    var.temperatureBedOffset = c.printer()['temperature']['bed']['offset']
    var.temperatureBedTarget = c.printer()['temperature']['bed']['target']
    var.temperatureTool0Actual = c.printer()['temperature']['tool0']['actual']     #what if tool0 is tool1??
    var.temperatureTool0Offset = c.printer()['temperature']['tool0']['offset']
    var.temperatureTool0Target = c.printer()['temperature']['tool0']['target']
    #print("Issue a print head command: JOGS THE PRINT HEAD BY X,Y,Z VALUE")
    #print("Issue a print head command: HOMES THE PRINT HEAD IN ALL AXES")
    #print("Issue a print head command: CHANGE FEEDRATE FACTOR 50%-200%")
    #print("Issue a tool command: SETS GIVEN TARGET TEMPERATURE OF GIVEN TOOL")
    #print("Issue a tool command: SETS GIVEN OFFSET TEMPERATURE OF GIVEN TOOL")
    #print("Issue a tool command: SELECTS THE PRINTER TOOL")
    #print("Issue a tool command: EXTRUDES FROM SELECTED TOOL")
    #print("Issue a tool command: RETRACTS FILAMENT FROM SELECTED TOOL")
    #print("Issue a tool command: CHANGES FLOW RATE OF EXTRUSION 75%-125%")
    #print("Retrieve the current tool state: ", c.tool())
    var.currentToolTemperatureActual = c.tool()['tool0']['actual']      #what if not tool0 is used??
    var.currentToolTemperatureOffset = c.tool()['tool0']['offset']
    var.currentToolTemperatureTarget = c.tool()['tool0']['target']
    #print("Issue a bed command: SETS TARGET TEMPERATURE OF BED")
    #print("Issue a bed command: SETS OFFSET TEMPERATURE OF BED")
    #print("Retrieve the current bed state: ", c.bed())
    var.currentBedTemperatureActual = c.bed()['bed']['actual']
    var.currentBedTemperatureOffset = c.bed()['bed']['offset']
    var.currentBedTemperatureTarget = c.bed()['bed']['target']
    #print("Issue a chamber command: SETS TARGET TEMPERATURE OF CHAMBER")
    #print("Issue a chamber command: SETS OFFSET TEMPERATURE OF CHAMBER")
    #print("Retrieve the current chamber state: NOT WORKING")
    #print("Issue an SD command: MAKING SD CARD READY FOR USE")
    #print("Issue an SD command: REFRESHES LIST OF FILES")
    #print("Issue an SD command: RELEASES SD CARD FROM PRINTER")
    #print("Retrieve the current SD state: ", c.sd())
    var.sdStateReady = c.sd()['ready']      #same as var.sdReady .....
    #print("Retrieves the custom controls as configured in config.yaml: ", c.custom_control_request())    #not interesting i think
    #print("Send an arbitrary command to the printer: GCODE SENDER")
### PRINTER PROFILE OPERATIONS ###
    #print("Retrieve all printer profiles: ", c.printer_profiles()) #opted for specific profile function
    profileVisualized = '_default'
    #print("Retrieve specific printer profile: ", c.printer_profile(profileVisualized))
    var.printerProfileAxeEInverted = c.printer_profile(profileVisualized)['axes']['e']['inverted']
    var.printerProfileAxeESpeed = c.printer_profile(profileVisualized)['axes']['e']['speed']
    var.printerProfileAxeXInverted = c.printer_profile(profileVisualized)['axes']['x']['inverted']
    var.printerProfileAxeXSpeed = c.printer_profile(profileVisualized)['axes']['x']['speed']
    var.printerProfileAxeYInverted = c.printer_profile(profileVisualized)['axes']['y']['inverted']
    var.printerProfileAxeYSpeed = c.printer_profile(profileVisualized)['axes']['y']['speed']
    var.printerProfileAxeZInverted = c.printer_profile(profileVisualized)['axes']['z']['inverted']
    var.printerProfileAxeZSpeed = c.printer_profile(profileVisualized)['axes']['z']['speed']
    var.printerProfileColor = c.printer_profile(profileVisualized)['color']
    var.printerProfileCurrent = c.printer_profile(profileVisualized)['current']
    var.printerProfileDefault = c.printer_profile(profileVisualized)['default']
    var.printerProfileExtruderCount = c.printer_profile(profileVisualized)['extruder']['count']
    var.printerProfileExtruderDefaultExtrusionLength = c.printer_profile(
            profileVisualized)['extruder']['defaultExtrusionLength']
    var.printerProfileExtruderNozzleDiameter = c.printer_profile(profileVisualized)['extruder']['nozzleDiameter']
    var.printerProfileExtruderOffsetX, var.printerProfileExtruderOffsetY = c.printer_profile(
        profileVisualized)['extruder']['offsets'][0]
    var.printerProfileExtruderSharedNozzle = c.printer_profile(profileVisualized)['extruder']['sharedNozzle']
    var.printerProfileHeatedBed = c.printer_profile(profileVisualized)['heatedBed']
    var.printerProfileHeatedChamber = c.printer_profile(profileVisualized)['heatedChamber']
    var.printerProfileId = c.printer_profile(profileVisualized)['id']
    var.printerProfileModel = c.printer_profile(profileVisualized)['model']
    var.printerProfileName = c.printer_profile(profileVisualized)['name']
    var.printerProfileResource = c.printer_profile(profileVisualized)['resource']
    var.printerProfileVolumeCustom_boxX_max = c.printer_profile(profileVisualized)['volume']['custom_box']['x_max']
    var.printerProfileVolumeCustom_boxX_min = c.printer_profile(profileVisualized)['volume']['custom_box']['x_min']
    var.printerProfileVolumeCustom_boxY_max = c.printer_profile(profileVisualized)['volume']['custom_box']['y_max']
    var.printerProfileVolumeCustom_boxY_min = c.printer_profile(profileVisualized)['volume']['custom_box']['y_min']
    var.printerProfileVolumeCustom_boxZ_max = c.printer_profile(profileVisualized)['volume']['custom_box']['z_max']
    var.printerProfileVolumeCustom_boxZ_min = c.printer_profile(profileVisualized)['volume']['custom_box']['z_min']
    var.printerProfileVolumeDepth = c.printer_profile(profileVisualized)['volume']['depth']
    var.printerProfileVolumeFormFactor = c.printer_profile(profileVisualized)['volume']['formFactor']
    var.printerProfileVolumeHeight = c.printer_profile(profileVisualized)['volume']['height']
    var.printerProfileVolumeOrigin = c.printer_profile(profileVisualized)['volume']['origin']
    var.printerProfileVolumeWidth = c.printer_profile(profileVisualized)['volume']['width']
    #print("Add a new printer profile")
    #print("Update an existing printer profile")
    #print("Remove an existing printer profile")
### NBSP SETTINGS ###
    #print("Retrieve current settings: ", c.settings()) #many settings from api key to camera, seems uninteresting
    #print("Regenerate the system wide API key")
    #print("Fetch template data")
### SLICING ###
    #print("Lists All slicers and Slicing Profiles: ", c.slicers)
    #print("List Slicing Profiles of a Specific Slicer: NO IDEA HOW")
    #print("Retrieve Specific Profile: NO IDEA HOW")
    #print("Add Slicing Profile")
    #print("Delete Slicing Profile")
### NBSP SYSTEM ###
    #print("List all registered commands: ", c.system_commands())        #NOT INTERESTING
    #print("List all registered system commands for a source")
    #print("Execute a registered system command")
### TIMELAPSE ###
    #print("Retrieve a list of timelapses and the current config: ", c.timelapses)       #NOT INTERESTING
    #print("Delete a timelapse")
    #print("Issue a command for an unrendered timelapse")
    #print("Delete an unrendered timelapse")
    #print("Change current timelapse config")
### USER ###
    #print("Retrieve a list of users: NOT ALL ACTIVATED: ", c.users())
    for i in range(10): #generating 10 variables for loop
        attr_name = 'userName{}'.format(i)
        setattr(var, attr_name, None)
    for i, user in enumerate(c.users()['users']):       #var.userName0...1
        attr_name = 'userName{}'.format(i)
        setattr(var, attr_name, user['name'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'userAdmin{}'.format(i)
        setattr(var, attr_name, None)
    for i, user in enumerate(c.users()['users']):       #var.userAdmin0...1
        attr_name = 'userAdmin{}'.format(i)
        setattr(var, attr_name, user['admin'])
    #print("Retrieve a user")
    #print("Add a user")
    #print("Update a user")
    #print("Delete a user")
    #print("Reset a user's password")
    #print("Retrieve a user's settings")
    #print("Update a user's settings")
    #print("Regenerate a user's personal API key")
    #print("Delete a user's personal API key")
### UTIL ###
    #print("Test paths")
    #print("Test URLs")
    #print("Test server")
### WIZARD ###
    #print("Retrieve additional data about registered wizards: NOT WORKING?")
    #print("Finish wizards")
### FILAMENT MANAGER ###   add in the return!!!!!
    # print("Retrieve informations about the selected spools: ", c.selections())
    var.selectedSpoolCost = c.selections()['selections'][0]['spool']['cost']        #all about tool0, if multitool available, extend
    var.selectedSpoolId = c.selections()['selections'][0]['spool']['id']
    var.selectedSpoolName = c.selections()['selections'][0]['spool']['name']
    var.selectedSpoolProfileDensity = c.selections()['selections'][0]['spool']['profile']['density']
    var.selectedSpoolProfileDiameter = c.selections()['selections'][0]['spool']['profile']['diameter']
    var.selectedSpoolProfileId = c.selections()['selections'][0]['spool']['profile']['id']
    var.selectedSpoolProfileMaterial = c.selections()['selections'][0]['spool']['profile']['material']
    var.selectedSpoolProfileVendor = c.selections()['selections'][0]['spool']['profile']['vendor']
    var.selectedSpoolTempOffset = c.selections()['selections'][0]['spool']['temp_offset']
    var.selectedSpoolUsed = c.selections()['selections'][0]['spool']['used']
    var.selectedSpoolWeight = c.selections()['selections'][0]['spool']['weight']
    var.selectedTool = c.selections()['selections'][0]['tool']
    # print("Retrieve informations about all available spools: ", c.spools())
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolCost{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolCost0...1
        attr_name = 'spoolCost{}'.format(i)
        setattr(var, attr_name, spool['cost'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolId{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolId0...1
        attr_name = 'spoolId{}'.format(i)
        setattr(var, attr_name, spool['id'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolName{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolName0...1
        attr_name = 'spoolName{}'.format(i)
        setattr(var, attr_name, spool['name'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolProfileDensity{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolProfileDensity0...1
        attr_name = 'spoolProfileDensity{}'.format(i)
        setattr(var, attr_name, spool['profile']['density'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolProfileDiameter{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolProfileDiameter0...1
        attr_name = 'spoolProfileDiameter{}'.format(i)
        setattr(var, attr_name, spool['profile']['diameter'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolProfileId{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolProfileId0...1
        attr_name = 'spoolProfileId{}'.format(i)
        setattr(var, attr_name, spool['profile']['id'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolProfileMaterial{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolProfileMaterial0...1
        attr_name = 'spoolProfileMaterial{}'.format(i)
        setattr(var, attr_name, spool['profile']['material'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolProfileVendor{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolProfileVendor0...1
        attr_name = 'spoolProfileVendor{}'.format(i)
        setattr(var, attr_name, spool['profile']['vendor'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolTempOffset{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolTempOffset0...1
        attr_name = 'spoolTempOffset{}'.format(i)
        setattr(var, attr_name, spool['temp_offset'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolUsed{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolUsed0...1
        attr_name = 'spoolUsed{}'.format(i)
        setattr(var, attr_name, spool['used'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'spoolWeight{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.spools()['spools']):        #var.spoolWeight0...1
        attr_name = 'spoolWeight{}'.format(i)
        setattr(var, attr_name, spool['weight'])
    # print("Retrieve information about stored filament profiles: ", c.profiles())
    for i in range(10): #generating 10 variables for loop
        attr_name = 'profileDensity{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.profiles()['profiles']):        #var.profileDensity0...1
        attr_name = 'profileDensity{}'.format(i)
        setattr(var, attr_name, spool['density'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'profileDiameter{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.profiles()['profiles']):        #var.profileDiameter0...1
        attr_name = 'profileDiameter{}'.format(i)
        setattr(var, attr_name, spool['diameter'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'profileId{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.profiles()['profiles']):        #var.profileId0...1
        attr_name = 'profileId{}'.format(i)
        setattr(var, attr_name, spool['id'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'profileMaterial{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.profiles()['profiles']):        #var.profileMaterial0...1
        attr_name = 'profileMaterial{}'.format(i)
        setattr(var, attr_name, spool['material'])
    for i in range(10): #generating 10 variables for loop
        attr_name = 'profileVendor{}'.format(i)
        setattr(var, attr_name, None)
    for i, spool in enumerate(c.profiles()['profiles']):        #var.profileVendor0..1..2..
        attr_name = 'profileVendor{}'.format(i)
        setattr(var, attr_name, spool['vendor'])
### EdoExtra ###
    #selected file number in list, if none selected 9999
    file_list = c.files()['files']
    running_file_name = c.job_info()['job']['file']['name']
    if running_file_name is None:
        var.numberInList = 9999  # If the file is None, assign 999 to the variable
    else:
        for i, file_info in enumerate(file_list):
            if file_info['name'] == running_file_name:
                var.numberInList = i
                break
    #currentState for monitoring
    if var.state == "Printing" or var.state == "Pausing" or var.state == "Resuming"\
            or var.state == "Operational / Printing from OctoPrint" or var.state == "Operational / Printing from SD"\
            or var.state == "Operational / Printing from USB" or var.state == "Cancelling":
        var.currentStateMonitoring = "Executing"
    elif var.state == "Operational" or var.state == "Paused":
        var.currentStateMonitoring = "NotExecuting"
    elif var.state == "Error" or var.state == "Closed with Error":
        var.currentStateMonitoring = "OutOfService"
    else:
        var.currentStateMonitoring = "NotAvailable"
    #currentState for production
    if c.job_info()['job']['file']['name'] == None or var.state == "Connecting":
        var.currentStateProduction = "NotAvailable"
    elif var.state == "Operational" or var.state == "Paused":
        var.currentStateProduction = "NotExecuting"
    elif var.state == "Error" or var.state == "Closed with Error":
        var.currentStateProduction = "OutOfService"
    else:
        var.currentStateProduction = "Executing"

    #print(c.gcode('M114'))     #command to read axis position, it gets executed but no result returned in python
    print("________________________End collecting values in octoprintbroker.py_______________________________________")
    return {
        'serverVersion': var.serverVersion,
        'apiVersion': var.apiVersion,
        'textVersion': var.textVersion,
        'probeAppKeysWorkflowSupport': var.probeAppKeysWorkflowSupport,
        'connectionBaudrate': var.connectionBaudrate,
        'connectionPort': var.connectionPort,
        'connectionPrinterProfile': var.connectionPrinterProfile,
        'connectionState': var.connectionState,
        'printerProfileId0': var.printerProfileId0,
        'printerProfileId1': var.printerProfileId1,
        'printerProfileId2': var.printerProfileId2,
        'printerProfileId3': var.printerProfileId3,
        'printerProfileId4': var.printerProfileId4,
        'printerProfileId5': var.printerProfileId5,
        'printerProfileId6': var.printerProfileId6,
        'printerProfileId7': var.printerProfileId7,
        'printerProfileId8': var.printerProfileId8,
        'printerProfileId9': var.printerProfileId9,
        'printerProfileName0': var.printerProfileName0,
        'printerProfileName1': var.printerProfileName1,
        'printerProfileName2': var.printerProfileName2,
        'printerProfileName3': var.printerProfileName3,
        'printerProfileName4': var.printerProfileName4,
        'printerProfileName5': var.printerProfileName5,
        'printerProfileName6': var.printerProfileName6,
        'printerProfileName7': var.printerProfileName7,
        'printerProfileName8': var.printerProfileName8,
        'printerProfileName9': var.printerProfileName9,
        'fileName0': var.fileName0,
        'fileName1': var.fileName1,
        'fileName2': var.fileName2,
        'fileName3': var.fileName3,
        'fileName4': var.fileName4,
        'fileName5': var.fileName5,
        'fileName6': var.fileName6,
        'fileName7': var.fileName7,
        'fileName8': var.fileName8,
        'fileName9': var.fileName9,
        'fileSize0': var.fileSize0,
        'fileSize1': var.fileSize1,
        'fileSize2': var.fileSize2,
        'fileSize3': var.fileSize3,
        'fileSize4': var.fileSize4,
        'fileSize5': var.fileSize5,
        'fileSize6': var.fileSize6,
        'fileSize7': var.fileSize7,
        'fileSize8': var.fileSize8,
        'fileSize9': var.fileSize9,
        'fileType0': var.fileType0,
        'fileType1': var.fileType1,
        'fileType2': var.fileType2,
        'fileType3': var.fileType3,
        'fileType4': var.fileType4,
        'fileType5': var.fileType5,
        'fileType6': var.fileType6,
        'fileType7': var.fileType7,
        'fileType8': var.fileType8,
        'fileType9': var.fileType9,
        # 'jobAveragePrintTime': var.jobAveragePrintTime,
        'jobEstimatedPrintTime': var.jobEstimatedPrintTime,
        'jobFilamentLength': var.jobFilamentLength,
        'jobFilamentVolume': var.jobFilamentVolume,
        'jobFileDate': var.jobFileDate,
        # 'jobFileDisplay': var.jobFileDisplay,
        'jobFileName': var.jobFileName,
        'jobFileOrigin': var.jobFileOrigin,
        'jobFilePath': var.jobFilePath,
        'jobFileSize': var.jobFileSize,
        'jobLastPrintTime': var.jobLastPrintTime,
        'jobUser': var.jobUser,
        'progressCompletion': var.progressCompletion,
        'progressFilepos': var.progressFilepos,
        'progressPrintTime': var.progressPrintTime,
        'progressPrintTimeLeft': var.progressPrintTimeLeft,
        # 'progressPrintTimeLeftOrigin': var.progressPrintTimeLeftOrigin,
        'state': var.state,
        'sdReady': var.sdReady,
        'stateError': var.stateError,
        'stateFlagsCancelling': var.stateFlagsCancelling,
        'stateFlagsClosedOrError': var.stateFlagsClosedOrError,
        'stateFlagsError': var.stateFlagsError,
        'stateFlagsFinishing': var.stateFlagsFinishing,
        'stateFlagsOperational': var.stateFlagsOperational,
        'stateFlagsPaused': var.stateFlagsPaused,
        'stateFlagsPausing': var.stateFlagsPausing,
        'stateFlagsPrinting': var.stateFlagsPrinting,
        'stateFlagsReady': var.stateFlagsReady,
        'stateFlagsResuming': var.stateFlagsResuming,
        'stateFlagsSdReady': var.stateFlagsReady,
        'stateText': var.stateText,
        'temperatureAActual': var.temperatureAActual,
        'temperatureAOffset': var.temperatureAOffset,
        'temperatureATarget': var.temperatureATarget,
        'temperaturePActual': var.temperaturePActual,
        'temperaturePOffset': var.temperaturePOffset,
        'temperaturePTarget': var.temperaturePTarget,
        'temperatureBedActual': var.temperatureBedActual,
        'temperatureBedOffset': var.temperatureBedOffset,
        'temperatureBedTarget': var.temperatureBedTarget,
        'temperatureTool0Actual': var.temperatureTool0Actual,
        'temperatureTool0Offset': var.temperatureTool0Offset,
        'temperatureTool0Target': var.temperatureTool0Target,
        'currentToolTemperatureActual': var.currentToolTemperatureActual,
        'currentToolTemperatureOffset': var.currentToolTemperatureOffset,
        'currentToolTemperatureTarget': var.currentToolTemperatureTarget,
        'currentBedTemperatureActual': var.currentBedTemperatureActual,
        'currentBedTemperatureOffset': var.currentBedTemperatureOffset,
        'currentBedTemperatureTarget': var.currentBedTemperatureTarget,
        'sdStateReady': var.sdStateReady,
        'printerProfileAxeEInverted': var.printerProfileAxeEInverted,
        'printerProfileAxeESpeed': var.printerProfileAxeESpeed,
        'printerProfileAxeXInverted': var.printerProfileAxeXInverted,
        'printerProfileAxeXSpeed': var.printerProfileAxeXSpeed,
        'printerProfileAxeYInverted': var.printerProfileAxeYInverted,
        'printerProfileAxeYSpeed': var.printerProfileAxeYSpeed,
        'printerProfileAxeZInverted': var.printerProfileAxeZInverted,
        'printerProfileAxeZSpeed': var.printerProfileAxeZSpeed,
        'printerProfileColor': var.printerProfileColor,
        'printerProfileCurrent': var.printerProfileCurrent,
        'printerProfileDefault': var.printerProfileDefault,
        'printerProfileExtruderCount': var.printerProfileExtruderCount,
        'printerProfileExtruderDefaultExtrusionLength': var.printerProfileExtruderDefaultExtrusionLength,
        'printerProfileExtruderNozzleDiameter': var.printerProfileExtruderNozzleDiameter,
        'printerProfileExtruderOffsetX': var.printerProfileExtruderOffsetX,
        'printerProfileExtruderOffsetY': var.printerProfileExtruderOffsetY,
        'printerProfileExtruderSharedNozzle': var.printerProfileExtruderSharedNozzle,
        'printerProfileHeatedBed': var.printerProfileHeatedBed,
        'printerProfileHeatedChamber': var.printerProfileHeatedChamber,
        'printerProfileId': var.printerProfileId,
        'printerProfileModel': var.printerProfileModel,
        'printerProfileName': var.printerProfileName,
        'printerProfileResource': var.printerProfileResource,
        'printerProfileVolumeCustom_boxX_max': var.printerProfileVolumeCustom_boxX_max,
        'printerProfileVolumeCustom_boxX_min': var.printerProfileVolumeCustom_boxX_min,
        'printerProfileVolumeCustom_boxY_max': var.printerProfileVolumeCustom_boxY_max,
        'printerProfileVolumeCustom_boxY_min': var.printerProfileVolumeCustom_boxY_min,
        'printerProfileVolumeCustom_boxZ_max': var.printerProfileVolumeCustom_boxZ_max,
        'printerProfileVolumeCustom_boxZ_min': var.printerProfileVolumeCustom_boxZ_min,
        'printerProfileVolumeDepth': var.printerProfileVolumeDepth,
        'printerProfileVolumeFormFactor': var.printerProfileVolumeFormFactor,
        'printerProfileVolumeHeight': var.printerProfileVolumeHeight,
        'printerProfileVolumeOrigin': var.printerProfileVolumeOrigin,
        'printerProfileVolumeWidth': var.printerProfileVolumeWidth,
        'userName0': var.userName0,
        'userName1': var.userName1,
        'userName2': var.userName2,
        'userName3': var.userName3,
        'userName4': var.userName4,
        'userName5': var.userName5,
        'userName6': var.userName6,
        'userName7': var.userName7,
        'userName8': var.userName8,
        'userName9': var.userName9,
        'userAdmin0': var.userAdmin0,
        'userAdmin1': var.userAdmin1,
        'userAdmin2': var.userAdmin2,
        'userAdmin3': var.userAdmin3,
        'userAdmin4': var.userAdmin4,
        'userAdmin5': var.userAdmin5,
        'userAdmin6': var.userAdmin6,
        'userAdmin7': var.userAdmin7,
        'userAdmin8': var.userAdmin8,
        'userAdmin9': var.userAdmin9,
        'selectedSpoolCost': var.selectedSpoolCost,
        'selectedSpoolId': var.selectedSpoolId,
        'selectedSpoolName': var.selectedSpoolName,
        'selectedSpoolProfileDensity': var.selectedSpoolProfileDensity,
        'selectedSpoolProfileDiameter': var.selectedSpoolProfileDiameter,
        'selectedSpoolProfileId': var.selectedSpoolProfileId,
        'selectedSpoolProfileMaterial': var.selectedSpoolProfileMaterial,
        'selectedSpoolProfileVendor': var.selectedSpoolProfileVendor,
        'selectedSpoolTempOffset': var.selectedSpoolTempOffset,
        'selectedSpoolUsed': var.selectedSpoolUsed,
        'selectedSpoolWeight': var.selectedSpoolWeight,
        'selectedTool': var.selectedTool,
        'spoolCost0': var.spoolCost0,
        'spoolCost1': var.spoolCost1,
        'spoolCost2': var.spoolCost2,
        'spoolCost3': var.spoolCost3,
        'spoolCost4': var.spoolCost4,
        'spoolCost5': var.spoolCost5,
        'spoolCost6': var.spoolCost6,
        'spoolCost7': var.spoolCost7,
        'spoolCost8': var.spoolCost8,
        'spoolCost9': var.spoolCost9,
        'spoolId0': var.spoolId0,
        'spoolId1': var.spoolId1,
        'spoolId2': var.spoolId2,
        'spoolId3': var.spoolId3,
        'spoolId4': var.spoolId4,
        'spoolId5': var.spoolId5,
        'spoolId6': var.spoolId6,
        'spoolId7': var.spoolId7,
        'spoolId8': var.spoolId8,
        'spoolId9': var.spoolId9,
        'spoolName0': var.spoolName0,
        'spoolName1': var.spoolName1,
        'spoolName2': var.spoolName2,
        'spoolName3': var.spoolName3,
        'spoolName4': var.spoolName4,
        'spoolName5': var.spoolName5,
        'spoolName6': var.spoolName6,
        'spoolName7': var.spoolName7,
        'spoolName8': var.spoolName8,
        'spoolName9': var.spoolName9,
        'spoolProfileDensity0': var.spoolProfileDensity0,
        'spoolProfileDensity1': var.spoolProfileDensity1,
        'spoolProfileDensity2': var.spoolProfileDensity2,
        'spoolProfileDensity3': var.spoolProfileDensity3,
        'spoolProfileDensity4': var.spoolProfileDensity4,
        'spoolProfileDensity5': var.spoolProfileDensity5,
        'spoolProfileDensity6': var.spoolProfileDensity6,
        'spoolProfileDensity7': var.spoolProfileDensity7,
        'spoolProfileDensity8': var.spoolProfileDensity8,
        'spoolProfileDensity9': var.spoolProfileDensity9,
        'spoolProfileDiameter0': var.spoolProfileDiameter0,
        'spoolProfileDiameter1': var.spoolProfileDiameter1,
        'spoolProfileDiameter2': var.spoolProfileDiameter2,
        'spoolProfileDiameter3': var.spoolProfileDiameter3,
        'spoolProfileDiameter4': var.spoolProfileDiameter4,
        'spoolProfileDiameter5': var.spoolProfileDiameter5,
        'spoolProfileDiameter6': var.spoolProfileDiameter6,
        'spoolProfileDiameter7': var.spoolProfileDiameter7,
        'spoolProfileDiameter8': var.spoolProfileDiameter8,
        'spoolProfileDiameter9': var.spoolProfileDiameter9,
        'spoolProfileId0': var.spoolProfileId0,
        'spoolProfileId1': var.spoolProfileId1,
        'spoolProfileId2': var.spoolProfileId2,
        'spoolProfileId3': var.spoolProfileId3,
        'spoolProfileId4': var.spoolProfileId4,
        'spoolProfileId5': var.spoolProfileId5,
        'spoolProfileId6': var.spoolProfileId6,
        'spoolProfileId7': var.spoolProfileId7,
        'spoolProfileId8': var.spoolProfileId8,
        'spoolProfileId9': var.spoolProfileId9,
        'spoolProfileMaterial0': var.spoolProfileMaterial0,
        'spoolProfileMaterial1': var.spoolProfileMaterial1,
        'spoolProfileMaterial2': var.spoolProfileMaterial2,
        'spoolProfileMaterial3': var.spoolProfileMaterial3,
        'spoolProfileMaterial4': var.spoolProfileMaterial4,
        'spoolProfileMaterial5': var.spoolProfileMaterial5,
        'spoolProfileMaterial6': var.spoolProfileMaterial6,
        'spoolProfileMaterial7': var.spoolProfileMaterial7,
        'spoolProfileMaterial8': var.spoolProfileMaterial8,
        'spoolProfileMaterial9': var.spoolProfileMaterial9,
        'spoolProfileVendor0': var.spoolProfileVendor0,
        'spoolProfileVendor1': var.spoolProfileVendor1,
        'spoolProfileVendor2': var.spoolProfileVendor2,
        'spoolProfileVendor3': var.spoolProfileVendor3,
        'spoolProfileVendor4': var.spoolProfileVendor4,
        'spoolProfileVendor5': var.spoolProfileVendor5,
        'spoolProfileVendor6': var.spoolProfileVendor6,
        'spoolProfileVendor7': var.spoolProfileVendor7,
        'spoolProfileVendor8': var.spoolProfileVendor8,
        'spoolProfileVendor9': var.spoolProfileVendor9,
        'spoolTempOffset0': var.spoolTempOffset0,
        'spoolTempOffset1': var.spoolTempOffset1,
        'spoolTempOffset2': var.spoolTempOffset2,
        'spoolTempOffset3': var.spoolTempOffset3,
        'spoolTempOffset4': var.spoolTempOffset4,
        'spoolTempOffset5': var.spoolTempOffset5,
        'spoolTempOffset6': var.spoolTempOffset6,
        'spoolTempOffset7': var.spoolTempOffset7,
        'spoolTempOffset8': var.spoolTempOffset8,
        'spoolTempOffset9': var.spoolTempOffset9,
        'spoolUsed0': var.spoolUsed0,
        'spoolUsed1': var.spoolUsed1,
        'spoolUsed2': var.spoolUsed2,
        'spoolUsed3': var.spoolUsed3,
        'spoolUsed4': var.spoolUsed4,
        'spoolUsed5': var.spoolUsed5,
        'spoolUsed6': var.spoolUsed6,
        'spoolUsed7': var.spoolUsed7,
        'spoolUsed8': var.spoolUsed8,
        'spoolUsed9': var.spoolUsed9,
        'spoolWeight0': var.spoolWeight0,
        'spoolWeight1': var.spoolWeight1,
        'spoolWeight2': var.spoolWeight2,
        'spoolWeight3': var.spoolWeight3,
        'spoolWeight4': var.spoolWeight4,
        'spoolWeight5': var.spoolWeight5,
        'spoolWeight6': var.spoolWeight6,
        'spoolWeight7': var.spoolWeight7,
        'spoolWeight8': var.spoolWeight8,
        'spoolWeight9': var.spoolWeight9,
        'profileDensity0': var.profileDensity0,
        'profileDensity1': var.profileDensity1,
        'profileDensity2': var.profileDensity2,
        'profileDensity3': var.profileDensity3,
        'profileDensity4': var.profileDensity4,
        'profileDensity5': var.profileDensity5,
        'profileDensity6': var.profileDensity6,
        'profileDensity7': var.profileDensity7,
        'profileDensity8': var.profileDensity8,
        'profileDensity9': var.profileDensity9,
        'profileDiameter0': var.profileDiameter0,
        'profileDiameter1': var.profileDiameter1,
        'profileDiameter2': var.profileDiameter2,
        'profileDiameter3': var.profileDiameter3,
        'profileDiameter4': var.profileDiameter4,
        'profileDiameter5': var.profileDiameter5,
        'profileDiameter6': var.profileDiameter6,
        'profileDiameter7': var.profileDiameter7,
        'profileDiameter8': var.profileDiameter8,
        'profileDiameter9': var.profileDiameter9,
        'profileId0': var.profileId0,
        'profileId1': var.profileId1,
        'profileId2': var.profileId2,
        'profileId3': var.profileId3,
        'profileId4': var.profileId4,
        'profileId5': var.profileId5,
        'profileId6': var.profileId6,
        'profileId7': var.profileId7,
        'profileId8': var.profileId8,
        'profileId9': var.profileId9,
        'profileMaterial0': var.profileMaterial0,
        'profileMaterial1': var.profileMaterial1,
        'profileMaterial2': var.profileMaterial2,
        'profileMaterial3': var.profileMaterial3,
        'profileMaterial4': var.profileMaterial4,
        'profileMaterial5': var.profileMaterial5,
        'profileMaterial6': var.profileMaterial6,
        'profileMaterial7': var.profileMaterial7,
        'profileMaterial8': var.profileMaterial8,
        'profileMaterial9': var.profileMaterial9,
        'profileVendor0': var.profileVendor0,
        'profileVendor1': var.profileVendor1,
        'profileVendor2': var.profileVendor2,
        'profileVendor3': var.profileVendor3,
        'profileVendor4': var.profileVendor4,
        'profileVendor5': var.profileVendor5,
        'profileVendor6': var.profileVendor6,
        'profileVendor7': var.profileVendor7,
        'profileVendor8': var.profileVendor8,
        'profileVendor9': var.profileVendor9,
        'numberInList': var.numberInList,
        'currentStateMonitoring': var.currentStateMonitoring,
        'currentStateProduction': var.currentStateProduction,
    }

if __name__ == "__main__":
    get_values()