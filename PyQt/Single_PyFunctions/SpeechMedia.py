import threading
import time, os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

index = 1
audio_file_dir = r"\\172.30.2.199\\prv\\Speech\\N4"
audio_file_path_list = []
for root, dirs, files in os.walk(audio_file_dir):
    for file in files:
        absPath = root + os.sep + file
        audio_file_path_list.append(absPath)

audio = AudioSegment.from_mp3(audio_file_path_list[index])

frame_duration = 10000 
recognizer = sr.Recognizer()
def recognize_audio(start_time, duration):
    frame = audio[start_time:start_time + duration]
    frame.export("temp.wav", format="wav")

    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ja-JP")
            print(f"{text}")
            #print(f" {start_time // frame_duration + 1} Frame: {text}")
        except sr.UnknownValueError:
            pass
            #print(f"{start_time // frame_duration + 1} Frame, can not recognize")
        except sr.RequestError as e:
            pass
            #print(f"{start_time // frame_duration + 1} Frame, can not request; {e}")

def play_audio():
    play(audio)

play_thread = threading.Thread(target=play_audio)
play_thread.start()

# for i in range(0, len(audio), frame_duration):
#     recognize_audio(i, frame_duration)
#     time.sleep(6)

play_thread.join()