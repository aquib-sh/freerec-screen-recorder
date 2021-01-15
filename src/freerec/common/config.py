""" Author: Shaikh Aquib
    Contains Default Configuration Related to Application
"""

import os
import datetime
from win32api import GetSystemMetrics
from freerec.common.util import mod_fname

resources      = os.path.join("resources", "icon")
app_icon       = os.path.join(resources, "icon_white.ico")
app_name       = "FreeRec"
window_size    = "400x300"
video_encoding = "XVID"
fps            =  30.0
basename       = "Recording{}".format(
                            datetime.datetime.now().date()
                            )
video_format   = ".avi"
audio_format   = ".wav"
video_fname    = mod_fname(basename, video_format)
audio_fname    = mod_fname(basename, audio_format)
resolution     = (GetSystemMetrics(0), GetSystemMetrics(1)) 


