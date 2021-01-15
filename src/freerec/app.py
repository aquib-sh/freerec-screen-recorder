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
        self.audiobox = None 
        self.worker = worker.Worker()

    def fill_empty_rows(self, start, end):
        for i in range(start, end):
            self.app.add_label(value=" ", row_=i, column_=0)

    def fill_empty_columns(self, row_, start, end, tabs=1):
        buff = "    " * tabs  
        for i in range(start, end):
            self.app.add_label(value=buff, row_=row_, column_=i)
 
    def fill_layout(self):
        start_pos = (12, 8) # position of start button
        stop_pos  = (12, 1) # position of stop button

        # Add empty rows from top uptil start button row
        self.fill_empty_rows(0, start_pos[0]-1)

        # Add empty columns before button position
        self.fill_empty_columns(stop_pos[0], # row
            0,                  # start column
            stop_pos[1],        # end column
            tabs=3 
            ) 
        self.app.add_button("Stop", stop_pos[0],
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
            command_=self.record_video
            ) 
        self.audio_box = self.app.add_check_box("Audio", 7,1) 
        self.audio_box = self.app.add_check_box("Audio", 7,1) 

    def show_curr_val(self):
        print(self.audio_box.get())

    def record_video(self):
        t = threading.Thread(target=self.worker.record_video)
        t.start()
    
    def send_stop_signal(self):
        t = threading.Thread(target=self.worker.give_stop_signal)
        t.start()

    def end(self):
        self.app.start()



if __name__ == "__main__":
    recorder = Recorder()
    recorder.fill_layout()
    recorder.end()
