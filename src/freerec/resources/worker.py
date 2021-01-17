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
        basename = os.path.join(config.output_path, config.basename)
        format_  = config.video_format
        self.filenames['video'] = util.mod_fname(basename, format_)

        local_writer = cv2.VideoWriter(
            filename = self.filenames['video'],
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

    def record_audio(self):
        """ Records audio saves saves into file. """
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
            
                        
