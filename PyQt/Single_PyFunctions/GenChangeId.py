import pydub
import pydub.playback
import speech_recognition as sr
import threading
import time

def play_audio(file_path):
    audio = pydub.AudioSegment.from_file(file_path)
    pydub.playback.play(audio)

def recognize_speech_from_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='ja-JP')
                print("Text:", text)
            except sr.UnknownValueError:
                print("did not recognize")
            except sr.RequestError as e:
                print(f"can not connect server; {e}")

if __name__ == "__main__":
    audio_file = "C:\\software\\26.mp3"
    threading.Thread(target=play_audio, args=(audio_file,)).start()
    time.sleep(1)
    recognize_speech_from_audio()