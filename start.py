#!/usr/bin/python
import imp
import os
import sys
import subprocess
import datetime
import time
import rtxlib
from rtxlib import info, error
from rtxlib.report import plot
from rtxlib.workflow import execute_workflow


def loadDefinition(folder):
    """ opens the given folder and searches for a definition.py file and checks if it looks valid"""
    if len(sys.argv) != 3:
        error("missing experiment folder")
        exit(1)
    try:
        wf = imp.load_source('wf', './' + folder + '/definition.py')
        wf.folder = sys.argv[2]
        testName = wf.name
        # add timestamp to execution
        ts = time.time()
        wf.timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        wf.outputFolder = wf.folder + "/" + wf.timeStamp
        os.makedirs(wf.outputFolder)
        return wf
    except IOError:
        error("Folder is not a valid experiment folder (does not contain definition.py)")
        exit(1)
    except AttributeError:
        error("Workflow did not had a name attribute")
        exit(1)
    except ImportError as e:
        error("Import failed: " + str(e))
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == "start":
        wf = loadDefinition(sys.argv[2])

        # setting global variable log_folder for logging and clear log
        rtxlib.LOG_FOLDER = wf.outputFolder
        rtxlib.clearOldLog()
        info("> Do VMTouch Prepare")
        try:
            process = subprocess.Popen("vmtouch -t ./", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            info(process.stdout.read())
        except:
            pass
        info("> Starting RTX experiment...")
        execute_workflow(wf)
        plot(wf)
        exit(0)
    if len(sys.argv) > 2 and sys.argv[1] == "report":
        wf = loadDefinition(sys.argv[2])
        info("> Starting RTX reporting...")
        plot(wf)
        exit(0)

    # Help
    info("RTX Help Page")
    info("COMMANDS:")
    info("> python rtx.py help           -> shows this page ")
    info("         rtx.py start  $folder -> runs the experiment in this folder")
    info("         rtx.py report $folder -> shows the reports for the experiment in this folder")
    info("EXAMPLE:")
    info("> python rtx.py start ./examples/http-gauss")
    exit(0)
else:
    print("Please start this file with > python rtx.py ...")
