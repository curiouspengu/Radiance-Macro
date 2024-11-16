import sys
import pathlib
sys.dont_write_bytecode = True
sys.path.append(pathlib.Path(__file__).parent.resolve())

import os
import subprocess
import json
import ctypes

import threading
from settings import *

sleep(1)
walk_sleep('1.423')
walk_send('d', 'Down')
walk_sleep('0.015')
walk_send('w', 'Down')
walk_sleep('0.172')
walk_send('space', 'Down')
walk_sleep('0.136')
walk_send('space', 'Up')
walk_sleep('0.46')
walk_send('w', 'Up')
walk_sleep('0.012')
walk_send('d', 'Up')

print("finished")
