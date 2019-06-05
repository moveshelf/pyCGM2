# -*- coding: utf-8 -*-
from setuptools import setup,find_packages
import os
import os.path
import sys
import logging
import site
import shutil

VERSION = "3.1.7"

developMode = len(sys.argv) > 1 and sys.argv[1] == "develop"
if developMode:
    logging.warning("You have selected a developer model (local install)")


for it in site.getsitepackages():
    if "site-packages" in it:
        SITE_PACKAGE_PATH = it
        break

NAME_IN_SITEPACKAGE = "pyCGM2-" + VERSION + "-py" + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + ".egg"
MAIN_PYCGM2_PATH = os.getcwd()


PYCGM2_SETTINGS_FOLDER = os.path.join(MAIN_PYCGM2_PATH, "PyCGM2", "Settings")
NEXUS_PYCGM2_VST_PATH = os.path.join(MAIN_PYCGM2_PATH, "PyCGM2", "Install", "vst")
NEXUS_PIPELINE_TEMPLATE_PATH = os.path.join(MAIN_PYCGM2_PATH, "PyCGM2", "Install", "pipelineTemplate")
PATH_TO_PYTHON_SCRIPTS = os.path.join(os.path.dirname(sys.executable), "Scripts")

# do not serve anymore since all apps are now in Scripts ( i still keep it)
if not developMode:
    PATH_IN_SITEPACKAGE = os.path.join(SITE_PACKAGE_PATH, NAME_IN_SITEPACKAGE)
else:
    PATH_IN_SITEPACKAGE = MAIN_PYCGM2_PATH


user_folder = os.getenv("PUBLIC")

if user_folder:
    NEXUS_PUBLIC_PATH = os.path.join(user_folder, "Documents", "Vicon", "Nexus2.x")
    NEXUS_PUBLIC_DOCUMENT_VST_PATH = os.path.join(NEXUS_PUBLIC_PATH, "ModelTemplates")
    NEXUS_PUBLIC_DOCUMENT_PIPELINE_PATH = os.path.join(NEXUS_PUBLIC_PATH, "Configurations", "Pipelines")
else:
    NEXUS_PUBLIC_PATH = NEXUS_PUBLIC_DOCUMENT_VST_PATH = NEXUS_PUBLIC_DOCUMENT_PIPELINE_PATH = None


def scanViconTemplatePipeline(sourcePath, desPath, pyCGM2nexusAppsPath):
    toreplace = "[TOREPLACE]"
    pyCGM2nexusAppsPath_antislash = pyCGM2nexusAppsPath.replace('\\', '/')

    for file_ in os.listdir(sourcePath):
        with open(os.path.join(sourcePath, file_), 'r') as f:
            file_contents = f.read().replace(toreplace, pyCGM2nexusAppsPath_antislash)

        if not os.path.isfile(os.path.join(desPath, file)):
            with open(os.path.join(desPath, file_), "w") as text_file:
                text_file.write(file_contents)


def gen_data_files(*src_dirs):
    results = []
    for src_dir in src_dirs:
        for root, dirs, files in os.walk(src_dir):
            results.append((root, map(lambda f: os.path.join(root, f), files)))
    return results


def gen_data_files_forScripts(*src_dirs):
    results = []
    for src_dir in src_dirs:
        for root, dirs, files in os.walk(src_dir):
            for f in files:
                if f.endswith(".py"):
                    results.append(os.path.join(root, f))
    return results


def getSubDirectories(dir):
    return [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]


def getFiles(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


#------------------------- UNINSTALL--------------------------------------------

# remove pyCGM2 folder or egg-link
dirSitepackage = getSubDirectories(SITE_PACKAGE_PATH)
for folder in  dirSitepackage:
    if "pyCGM2" in folder:
        shutil.rmtree(SITE_PACKAGE_PATH+folder)
        logging.info("package pyCGM2 (%s) removed" % (folder))


if "pyCGM2.egg-link" in os.listdir(SITE_PACKAGE_PATH):
    os.remove(SITE_PACKAGE_PATH+"pyCGM2.egg-link")


# remove Build/dist/egg info in the downloaded folder
localDirPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
localDirPathDirs = getSubDirectories(localDirPath)
if "build" in localDirPathDirs:
    shutil.rmtree(os.path.join(localDirPath, "build"))

if "dist" in localDirPathDirs:
    shutil.rmtree(os.path.join(localDirPath, "dist"))

if "pyCGM2.egg-info" in localDirPathDirs:
    shutil.rmtree(os.path.join(localDirPath, "pyCGM2.egg-info"))


# delete everything in programData
if os.getenv("PROGRAMDATA"):
    pd = os.getenv("PROGRAMDATA")
    pddirs = getSubDirectories(pd)
    if "pyCGM2" in pddirs:
        shutil.rmtree(os.path.join(pd, "pyCGM2"))
        logging.info("pprogramData/pyCGM2---> remove")

if NEXUS_PUBLIC_PATH and os.path.isdir(NEXUS_PUBLIC_PATH):
    # delete all previous vst and pipelines in Nexus Public Documents
    files = getFiles(NEXUS_PUBLIC_DOCUMENT_VST_PATH)
    for file in files:
        if "pyCGM2" in file[0:6]: # check 6 first letters
            os.remove(os.path.join(NEXUS_PUBLIC_DOCUMENT_VST_PATH,file))

    files = getFiles(NEXUS_PUBLIC_DOCUMENT_PIPELINE_PATH)
    for file in files:
        if "pyCGM2" in file[0:6]:
            os.remove(os.path.join(NEXUS_PUBLIC_DOCUMENT_PIPELINE_PATH,file))

#
# dirs = getSubDirectories(NEXUS_PUBLIC_DOCUMENT_PIPELINE_PATH)
# if "pyCGM2" in dirs:
#     shutil.rmtree(NEXUS_PUBLIC_DOCUMENT_PIPELINE_PATH+"pyCGM2")

# ------------------------------------------------------------------
# ------------------------- INSTALL--------------------------------------------
setup(name='pyCGM2',
      version=VERSION,
      author='Fabien Leboeuf',
      author_email='fabien.leboeuf@gmail.com',
      keywords='python CGM Vicon PluginGait',
      packages=find_packages(),
      include_package_data=True,
      license='CC-BY-SA',
      install_requires=['numpy>=1.11.0',
                        'scipy==1.2.1',
                        'matplotlib<3.0.0',
                        'pandas >=0.19.1',
                        'enum34>=1.1.2',
                        'configparser>=3.5.0',
                        'beautifulsoup4>=3.5.0',
                        'pyyaml>=3.13.0',
                        'yamlordereddictloader>=0.4.0',
                        'xlrd >=0.9.0'],
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Operating System :: Windows OS',
                   'Natural Language :: English-French',
                   'Topic :: Clinical Gait Analysis'],
      scripts=gen_data_files_forScripts("Apps", "Scripts")
)

# ------------------------------------------------------------------------------
# ------------------------- POST INSTALL---------------------------------------


# --- management of the folder ProgramData/pyCGM2----
if not developMode:
    if os.getenv("PROGRAMDATA"):
        PYCGM2_APPDATA_PATH = os.path.join(os.getenv("PROGRAMDATA"), "pyCGM2")
        shutil.copytree(PYCGM2_SETTINGS_FOLDER, PYCGM2_APPDATA_PATH)

# --- management of nexus-related files ( vst+pipelines)-----
if NEXUS_PUBLIC_PATH and os.path.isdir(NEXUS_PUBLIC_PATH):
    # vst
    content = os.listdir(NEXUS_PYCGM2_VST_PATH)
    for item in content:
        full_filename = os.path.join(NEXUS_PYCGM2_VST_PATH, item)
        shutil.copyfile(full_filename,  os.path.join(NEXUS_PUBLIC_DOCUMENT_VST_PATH,item))

    scanViconTemplatePipeline(NEXUS_PIPELINE_TEMPLATE_PATH,
                              NEXUS_PUBLIC_DOCUMENT_PIPELINE_PATH,
                              PATH_TO_PYTHON_SCRIPTS)

else:
    logging.error("[pyCGM2] - Nexus folder not detected - No generation of VST and pipelines")
