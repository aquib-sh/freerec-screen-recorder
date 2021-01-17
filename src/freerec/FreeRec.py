""" Author: Shaikh Aquib
    FreeRec Screen Recorder
"""

import sys
import os
import threading
sys.path.append(os.path.abspath(
    os.path.join(os.getcwd(), os.pardir)
    ))
from freerec.resources import worker
from freerec.common import config
from freerec.resources.user_interface import Application

class Recorder:
    def __init__(self): 
        self.app = Application(config.window_size) 
        self.app.set_title(config.app_name) 
        self.app.set_icon(config.app_icon)
        self.root = self.app.get_root()
        self.audiobox = None    # for tracking value of audio checkbutton 
        self.worker = worker.Worker()

    def fill_empty_rows(self, start, end):
        """ Used to fill empty rows in order to give proper spacing
            and alignment to gird layout. """
        for i in range(start, end):
            self.app.add_label(value=" ", row_=i, column_=0)

    def fill_empty_columns(self, row_, start, end, tabs=1):
        """ Used to fill empty columns in order to give proper spacing
            and alignment to gird layout. """
        buff = "    " * tabs  
        for i in range(start, end):
            self.app.add_label(value=buff, row_=row_, column_=i)
 
    def fill_layout(self):
        """ Fill layout by arranging necassary things. """
        start_pos = (12, 6) # position of start button
        stop_pos  = (12, 1) # position of stop button

        # Add empty rows from top uptil start button row
        self.fill_empty_rows(1, start_pos[0]-1)

        # Add empty columns before button position
        self.fill_empty_columns(stop_pos[0], # row
            0,                  # start column
            stop_pos[1],        # end column
            tabs=2 
            ) 
        self.app.add_button("Stop and Save", stop_pos[0],
            stop_pos[1],
            command_ = self.send_stop_signal
            )       
 
        # Add empty columns before button position
        self.fill_empty_columns(start_pos[0], # row
            stop_pos[1]+1,      # start column
            start_pos[1]-1,     # end column
            tabs=2  
            ) 
        self.app.add_button("Start", start_pos[0], 
            start_pos[1],
            command_=self.start_recording
            ) 
        self.audio_box = self.app.add_check_box("Audio", 7,1) 
        self.app.add_label("    ", 8, 0)

        # Status will tell whether recording is on or stopped
        self.status = self.app.add_label("", 8, 1)       

        # Create canvas on top for some fancy text
        self.canvas = self.app.add_canvas(row_=0, column_=0)
        self.fancy_lbl = self.app.add_label_canvas(
            self.canvas,
            "     Now Record Your Screen With Freedom    ") 
        self.fancy_lbl.config(fg="green2", bg="Black", 
            font=("Consolas")) 

    def show_curr_val(self):
        """ Get current value of audio checkbutton. """
        print(self.audio_box.get())

    def start_recording(self):
        """ Start audio and video recording parallely using threads
            depending upon if audiobox is checked or not. """
        self.status.config(text="Started Recording",
            fg="green2", 
            bg="black",
        )
        # Start audio only if checkbutton is ticked
        if self.audio_box.get() == 1:
            global audio_recording
            audio_recording = threading.Thread(target=self.worker.record_audio)
            audio_recording.start()        
        global video_recording
        video_recording = threading.Thread(target=self.worker.record_video)
        video_recording.start() 
 
    def send_stop_signal(self):
        """ Send stop signal to audio and video recording processes. """
        t = threading.Thread(target=self.worker.give_stop_signal, args=(self.audio_box.get(),))
        t.start()
        self.status.config(text="Recording stopped and saved", 
            fg="red2",
            bg="black",
        )
        if audio_recording.is_alive():
            audio_recording.join()
        if not video_recording.is_alive() and not audio_recording.is_alive():
            merge = threading.Thread(target=self.worker.merge_audio_and_video)
            merge.start()
        
    def start(self):
        """ Start the application. """
        self.app.start()


if __name__ == "__main__":
    recorder = Recorder()
    recorder.fill_layout()
    recorder.start()
