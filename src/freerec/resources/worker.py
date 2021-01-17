""" Worker Class
    Author: Shaikh Aquib
    
    As the same suggests, this is the backbone of application.
    Worker is responsible with everything from initializing audio, video recording process,
    receiving stop signal then sending it to process, writing audio and video files then
    deleting them after merging into one by ffmpeg tool.
""" 

import time
import sys
import os
import pyautogui
import cv2
import subprocess
import numpy as np
from freerec.common import config
from freerec.common import util
from freerec.resources.speech import audio_recog as sr

class Worker():
    def __init__(self):
        self.codec = cv2.VideoWriter_fourcc(
            *config.video_encoding)
        self.toggle_stop = False
        self.r = sr.Recognizer()
        self.r.pause_threshold=30
        self.filenames = {'video':None, 'audio':None}
        
    def give_stop_signal(self, audio_status):
        self.toggle_stop = True
        if audio_status == 1:
            self.r.toggle_stop = True

    def record_video(self):
        """ Records video and saves it into a file by getting the names 
            from config file and performing the necessary changes. """
        if not os.path.exists(config.output_path):
            os.mkdir(config.output_path)
        basename = os.path.join(config.output_path, config.basename)
        format_  = config.video_format
        # If file with same name already exists then add 'n' to the end of name
        # achieved using mod_fname method inside util.py
        self.filenames['video'] = util.mod_fname(basename, format_)

        # Initialize the VideoWriter object
        local_writer = cv2.VideoWriter(
            filename = self.filenames['video'],
            fourcc    = self.codec,
            fps       = config.fps, 
            frameSize = config.resolution,
        )
        while True:
            # Here, we will take screenshots in a infinite loop and add them to array
            # It won't stop the process and break out of loop, until self.toggle_stop
            # is unabled from a seperate thread while calling.
            img = pyautogui.screenshot()    
            frame = np.array(img)

            # Convert from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            local_writer.write(frame)
            if self.toggle_stop == True:
                break
            
        local_writer.release()
        self.toggle_stop = False

    def record_audio(self):
        """ Records video and saves it into a file by getting the names 
            from config file and performing the necessary changes. """
        basename = os.path.join(config.output_path, config.basename)
        format_  = config.audio_format
       
        with sr.Microphone() as source:
            audio = self.r.record(source)
            
        self.filenames['audio'] = util.mod_fname(basename, format_) 
        with open(self.filenames['audio'], "wb") as f:
            f.write(audio.get_wav_data())
        return

    def merge_audio_and_video(self):
        """ Merges audio and video files into one and 
            then deletes the individual audio and video file. """
        # If audio file was not recorded then there
        # is no need to merge 
        if self.filenames['audio'] == None:
            pass 
        else:
            seperator = "/" # unix path seperator
            if sys.platform == 'win32':
                seperator = "\\"  # windows path seperator

            # Merge audio and video file using ffmpeg
            tool_path = os.path.join("resources", "ffmpeg")
            output_base = "F"+self.filenames['video'].split(seperator)[1]
            output_path = os.path.join(config.output_path, output_base)

            process = subprocess.run([tool_path, "-i", 
                self.filenames['video'], "-i",
                self.filenames['audio'],
                '-acodec','aac',
                '-vcodec','copy',
                '-loglevel','panic',
                '-strict','experimental',
                '-y', output_path]) 
            # Remove the individual files
            os.remove(self.filenames['video'])
            os.remove(self.filenames['audio'])
            
                        
