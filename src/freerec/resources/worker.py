import time
import pyautogui
import cv2
import numpy as np
from freerec.common import config
from freerec.common import util

class Worker():
    def __init__(self):
        self.codec = cv2.VideoWriter_fourcc(
            *config.video_encoding)
        self.toggle_stop = False
    
    def give_stop_signal(self):
        self.toggle_stop = True

    def record_video(self): 
        basename = config.basename
        format_  = config.video_format

        local_writer = cv2.VideoWriter(
            filename  = util.mod_fname(basename, format_), 
            fourcc    = self.codec,
            fps       = config.fps, 
            frameSize = config.resolution,
        )
        while True:
            img = pyautogui.screenshot()    
            frame = np.array(img)

            # Convert from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            local_writer.write(frame)
            if self.toggle_stop == True:
                break
            
        local_writer.release()
        self.toggle_stop = False

