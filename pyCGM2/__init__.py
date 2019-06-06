import sys
import glob
import re
import os
import logging
import btk


def getLastNexusVersion():
    nexusDir = "C:/Program Files (x86)/Vicon"
    dirs = os.listdir(nexusDir)
    li = []
    for it in dirs:
        if "Nexus2" in it:
            version = int(it[it.find(".")+1:])
            li.append(version)
    last = max(li)
    return "Nexus2." + str(last)


try:
    NEXUS_VERSION = getLastNexusVersion()
except OSError as e:
    logging.error("No Vicon software installed: " + str(e))
    NEXUS_VERSION = None


if NEXUS_VERSION:
    NEXUS_PATHS = ("C:/Program Files (x86)/Vicon/" + NEXUS_VERSION + "/SDK/Python",
                   "C:/Program Files (x86)/Vicon/Nexus" + NEXUS_VERSION + "/SDK/Win32")

    valid_paths = [path for path in NEXUS_PATHS if os.path.exists(path)]

    if not valid_paths:
        logging.error("Could not find the Vicon SDK in known directories: " + str(list(NEXUS_PATHS)))

    for path in valid_paths:
        if path not in sys.path:
            sys.path.append(sys.path)


# CONSTANTS
cased_path = glob.glob(re.sub(r'([^:])(?=[/\\]|$)', r'[\1]', __file__))[0]
MAIN_PYCGM2_PATH = os.path.abspath(os.path.join(os.path.dirname(cased_path), os.pardir))

#  [Optional] setting folder
PYCGM2_SETTINGS_FOLDER = os.path.join(MAIN_PYCGM2_PATH, "pyCGM2", "Settings")


#  [Optional]programData
if "PROGRAMDATA" in os.environ and os.path.isdir(os.path.join(os.environ["PROGRAMDATA"], "pyCGM2")):
    PYCGM2_APPDATA_PATH = os.path.join(os.environ["PROGRAMDATA"], "pyCGM2")
else:
    PYCGM2_APPDATA_PATH = PYCGM2_SETTINGS_FOLDER


# [Optional]: Apps path
MAIN_PYCGM2_APPS_PATH = os.path.join(MAIN_PYCGM2_PATH, "Apps")

# [Optional] path to embbbed Normative data base.
# By default, use pyCGM2-embedded normative data ( Schartz - Pinzone )
NORMATIVE_DATABASE_PATH = os.path.join(MAIN_PYCGM2_PATH, "pyCGM2", "Data", "normativeData")

# [Optional] main folder containing osim model
OPENSIM_PREBUILD_MODEL_PATH = os.path.join(PYCGM2_APPDATA_PATH, "opensim")

# [Optional] path pointing at Data Folders used for Tests
TEST_DATA_PATH = "C:\\Users\\HLS501\\Documents\\VICON DATA\\pyCGM2-Data\\"
MAIN_BENCHMARK_PATH = "C:\\Users\\HLS501\\Documents\\VICON DATA\\pyCGM2-benchmarks\\Gait patterns\\"

# [optional] path pointing pyCGM2-Nexus tools
NEXUS_PYCGM2_TOOLS_PATH = os.path.join(MAIN_PYCGM2_PATH, "pyCGM2", "Nexus")
PYCGM2_SCRIPTS_PATH = os.path.join(MAIN_PYCGM2_PATH, "Scripts")
