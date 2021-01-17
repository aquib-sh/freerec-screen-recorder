import audio_recog as sr
import time
import threading

r = sr.Recognizer()
r.pause_threshold=30
store = None

def record_audio():
    with sr.Microphone() as source:
        audio = r.record(source)
        global store
        store = audio
    
    temp = "speech.wav"
    with open(temp, "wb") as f:
        f.write(store.get_wav_data())
    print("saved to ", temp)
    
def get_store():
    return store

# on the stop toggle after 10 sec
def send_stop_signal():
    start = time.time()
    while True:
        curr = int(time.time() - start)
        if curr > 5:
            r.stop_toggle = True
            break
        

t1 = threading.Thread(target = record_audio)
t2 = threading.Thread(target = send_stop_signal)

t1.start()
t2.start()

"""
while True:
    curr = time.time() - start
    print(curr)
    if curr < 10:
        r.listen(source)
    else:
        break
    """

